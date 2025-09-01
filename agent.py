import logging
import asyncio
import base64
import re
import requests
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RoomInputOptions,
    WorkerOptions,
    cli,
    get_job_context,
)
from livekit.agents.llm import ImageContent
from livekit.plugins import google, noise_cancellation
import requests

logger = logging.getLogger("vision-assistant")

load_dotenv()


class VisionAssistant(Agent):
    def __init__(self) -> None:
        self._tasks = []
        super().__init__(
            instructions="""You are a helpful voice assistant with vision capabilities.
If the user provides a URL to an image, fetch and analyze it.
You can also receive images directly from the user.""",
            llm=google.beta.realtime.RealtimeModel(
                voice="Puck",
                temperature=0.8,
            ),
        )

    async def on_enter(self):
        def _image_received_handler(reader, participant_identity):
            task = asyncio.create_task(
                self._image_received(reader, participant_identity)
            )
            self._tasks.append(task)
            task.add_done_callback(lambda t: self._tasks.remove(t))
            
        get_job_context().room.register_byte_stream_handler("test", _image_received_handler)

        # Handler for user input to detect URLs
        @self.session.on("user_input")
        def on_user_input(event):
            message = event.text.lower()
            if "http" in message and any(ext in message for ext in ["jpg", "png", "jpeg", "gif"]):
                # Extract URL (simple extraction)
                import re
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
                if urls:
                    url = urls[0]
                    asyncio.create_task(self.fetch_image_from_url(url))

        self.session.generate_reply(
            instructions="You are a tutor.Your task is to teach the students about their studies and also help them where they are stuck."
        )
    
    async def _image_received(self, reader, participant_identity):
        logger.info("Received image from %s: '%s'", participant_identity, reader.info.name)
        try:
            image_bytes = bytes()
            async for chunk in reader:
                image_bytes += chunk

            # Save the image to a file for viewing
            image_filename = f"received_image_{participant_identity}_{int(asyncio.get_event_loop().time())}.png"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            logger.info("Image saved to %s", image_filename)

            chat_ctx = self.chat_ctx.copy()
            chat_ctx.add_message(
                role="user",
                content=[
                    ImageContent(
                        image=f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    )
                ],
            )
            await self.update_chat_ctx(chat_ctx)
            print("Image received", self.chat_ctx.copy().to_dict(exclude_image=False))
        except Exception as e:
            logger.error("Error processing image: %s", e)

    async def fetch_image_from_url(self, url: str):
        """Fetch an image from a URL and add it to the chat context."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_bytes = response.content

            # Save the image
            image_filename = f"fetched_image_{int(asyncio.get_event_loop().time())}.png"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            logger.info("Fetched image saved to %s", image_filename)

            chat_ctx = self.chat_ctx.copy()
            chat_ctx.add_message(
                role="user",
                content=[
                    ImageContent(
                        image=f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    )
                ],
            )
            await self.update_chat_ctx(chat_ctx)
            await self.session.generate_reply("I've fetched and analyzed the image from the URL.")
        except Exception as e:
            logger.error("Error fetching image from URL: %s", e)
            await self.session.generate_reply("Sorry, I couldn't fetch the image from that URL.")


async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    session = AgentSession()
    await session.start(
        agent=VisionAssistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))