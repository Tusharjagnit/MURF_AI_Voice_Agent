# 30 Days of AI Voice Agents Challenge 🎙️

This repository documents my journey through the #30DaysOfVoiceAgents challenge by Murf AI. It showcases the daily progress of building a sophisticated, conversational AI voice agent from the ground up. The project is a work in progress, with the goal of creating a feature-rich, production-ready voice agent by Day 30.

---

## 🖼️ Current Progress (Day 12)

![Final UI Screenshot](day12_task/screenshot.png) 
*(You can replace `screenshot.png` with an actual screenshot of your final UI)*

---

## 🚀 Project Overview

This project evolved from a simple "Hello World" API into a full-fledged voice-to-voice conversational agent. The final version, located in the `day12_task` folder, features a modern chat interface where a user can record their voice, have it transcribed, processed by a Large Language Model (LLM), and receive a spoken response synthesized by a high-quality Text-to-Speech (TTS) service.

The application is built with a Python FastAPI backend and a vanilla JavaScript frontend, demonstrating a full-stack approach to building AI-powered voice applications.

---

## 🗺️ The Journey: Daily Breakdown

The project was built incrementally, with each day's folder representing a new stage of development.

- **Day 1: Project Setup (`day1_project_setup`)**
  - Initialized a basic FastAPI server to serve a simple HTML page.

- **Day 2 & 3: Text-to-Speech Integration (`day2_rest_tts` & `day3_advanced_tts`)**
  - Integrated the Murf AI TTS API to convert text into speech.
  - Explored advanced TTS features like changing voice, style, and tone.

- **Day 4: Building an Echo Bot (`day4_echo_bot`)**
  - Added the AssemblyAI API for Speech-to-Text (STT) transcription.
  - Created an "echo bot" that would listen to the user, transcribe their speech, and speak it back to them.

- **Day 11: Robust Error Handling (`day11_task`)**
  - Made the application resilient to API failures.
  - Implemented `try-except` blocks for all external API calls.
  - Created a system to play pre-generated fallback audio files for specific errors, providing a better user experience.
  - Configured the development server to auto-reload on `.env` file changes for easier debugging.

- **Day 12: The Complete Conversational Agent (`day12_task`)**
  - **LLM Integration:** Added Google's Gemini LLM to generate intelligent, human-like responses, turning the echo bot into a true conversational agent.
  - **UI Overhaul:** Completely revamped the frontend to a modern, minimalist chat interface with a single stateful record button and CSS animations.
  - **Backend Cleanup:** Refactored the FastAPI backend to support the new UI and removed obsolete endpoints.
  - **Markdown Support:** Integrated `marked.js` to render the LLM's Markdown responses correctly in the chat history.
  - **Barge-In Functionality:** Implemented the ability for users to interrupt the AI's speech at any time by clicking the microphone, creating a more fluid conversation.

---

## 🏗️ Current Architecture

The final application uses a client-server architecture:

1.  **Client (Browser):** The JavaScript frontend captures audio using the `MediaRecorder` API.
2.  **API Request:** The audio is sent as a blob to the FastAPI backend.
3.  **Backend Pipeline:**
    - **STT:** The backend sends the audio to **AssemblyAI** for transcription.
    - **LLM:** The transcribed text is sent to the **Google Gemini** API, along with the chat history, to generate a response.
    - **TTS:** The LLM's text response is sent to the **Murf AI** API to synthesize the voice.
4.  **API Response:** The backend streams the generated audio back to the client.
5.  **Playback:** The client plays the received audio automatically.

---

## ✨ Features

-   **End-to-End Voice Interaction:** Seamlessly talk to an AI and hear it respond.
-   **Stateful Conversation:** Remembers chat history for contextual responses.
-   **Modern & Responsive UI:** A clean, single-button chat interface with animations.
-   **Robust Error Handling:** Gracefully handles API failures with user-friendly audio feedback.
-   **Developer-Friendly:** The development server supports live reloading for both code and environment variable changes.

---

## 🛠️ Tech Stack

-   **Backend:** Python, FastAPI
-   **Frontend:** Vanilla JavaScript, HTML5, CSS3
-   **Speech-to-Text (STT):** AssemblyAI
-   **Large Language Model (LLM):** Google Gemini
-   **Text-to-Speech (TTS):** Murf AI
-   **Web Server:** Uvicorn with Watchfiles
-   **Dependencies:** `python-dotenv`, `httpx`

---

## ⚙️ How to Run the Project

The most up-to-date version of the project is in the `day12_task` folder. As the project progresses, you may need to check the latest daily folder for the most recent code.

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd MURF_AI_Voice_Agent
    ```

2.  **Create and Activate a Python Virtual Environment**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Navigate to the final project folder and install the required packages.
    ```bash
    cd day12_task
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    -   In the `day12_task` folder, rename `env_example.txt` to `.env`.
    -   Open the `.env` file and add your API keys.

5.  **Start the Server**
    While inside the `day12_task` folder, run the start script.
    ```bash
    # For Windows
    start.bat

    # For macOS/Linux (you may need to create a start.sh)
    # uvicorn main:app --reload --reload-include .env --host 0.0.0.0
    ```

6.  **Open in Browser**
    Navigate to `http://127.0.0.1:8000` in your web browser.

---

## 🔑 Required Environment Variables

Create a `.env` file in the `day12_task` directory with the following keys:

```
ASSEMBLYAI_API_KEY="YOUR_ASSEMBLYAI_API_KEY"
MURF_API_KEY="YOUR_MURF_API_KEY"
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```

---
#BuildwithMurf #30DaysofVoiceAgents #VoiceTech #AI #MurfAIChallenge
