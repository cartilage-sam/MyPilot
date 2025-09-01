# Vision Assistant Agent

This project implements a voice-based AI assistant with vision capabilities using the LiveKit Agents framework. The agent can participate in a LiveKit room, respond to voice commands, and analyze images provided either through a direct data stream or by fetching from a URL.

## Features

- **Voice Interaction**: Utilizes Google's real-time text-to-speech (TTS) and speech-to-text (STT) for natural voice conversations.
- **Vision Capabilities**: Can receive and process images.
  - **Direct Image Upload**: Handles images sent via LiveKit's data channels.
  - **URL Fetching**: Automatically detects image URLs in chat, fetches them, and adds them to the conversation context.
- **Noise Cancellation**: Integrates noise cancellation to improve audio quality.
- **Asynchronous**: Built with Python's `asyncio` for non-blocking operations.

## How It Works

### `VisionAssistant` Class

This is the core of the agent. It inherits from `livekit.agents.Agent` and is initialized with:
- **Instructions**: A prompt that defines its persona and capabilities.
- **LLM**: `google.beta.realtime.RealtimeModel` is used for language understanding and generation, configured with a specific voice ("Puck").

#### Key Methods:

- **`on_enter()`**: This async method is called when the agent joins a room. It sets up handlers for:
  - **Image Reception**: `register_byte_stream_handler` listens for incoming image data on the "test" topic.
  - **User Input**: A `user_input` event listener checks for image URLs in text messages using regex. If a URL is found, it triggers `fetch_image_from_url`.

- **`_image_received()`**:
  - Triggered by the byte stream handler.
  - Asynchronously reads image data chunks.
  - Saves the received image to a local file (e.g., `received_image_participant_1693651200.png`).
  - Encodes the image in base64 and adds it to the chat context using `ImageContent`.

- **`fetch_image_from_url()`**:
  - Triggered by the URL detector in `on_enter`.
  - Uses the `requests` library to download the image from the provided URL.
  - Saves the fetched image locally (e.g., `fetched_image_1693651200.png`).
  - Adds the image to the chat context for the LLM to "see".
  - Generates a confirmation message to the user.

### `entrypoint` Function

This is the main entry point for the LiveKit worker.
- It establishes a connection to the LiveKit room.
- It creates an `AgentSession` and starts it with an instance of our `VisionAssistant`.
- It configures the room to accept video and enable noise cancellation.

## How to Run

1.  **Set up your environment**:
    - Create a `.env` file with your `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`.
    - Install the required dependencies:
      ```bash
      pip install -r requirements.txt
      ```

2.  **Run the agent**:
    ```bash
    python agent.py dev 
    ```
    The agent will connect to the LiveKit server and wait in a room.

3.  **Interact with the agent**:
    - Join the same LiveKit room as a participant.
    - **To send an image directly**: Use a client application that can send data via LiveKit's byte stream on the "test" topic.
    - **To have the agent fetch an image**: Send a text message containing a URL to a JPG, PNG, or GIF image. For example: "Can you tell me what's in this image? https://example.com/my_photo.png"

The agent will save any processed images locally in the project directory.
