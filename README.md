# AI Orchestration App

This is a FastAPI application integrating **LangChain** and **LangGraph** to orchestrate an AI Animation Workflow.

The system is composed of three main agents that work sequentially to produce video content from a simple text prompt.

## Setup

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and set your keys:
    ```bash
    OPENAI_API_KEY=sk-...
    GOOGLE_API_KEY=...
    # RUNWAY_API_KEY=... (Optional)
    ```

2.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```

3.  **Access API**:
    Open `http://localhost:8000/docs` to interact with the endpoints.

## Animation Workflow Guide

The workflow consists of three distinct steps. You can trigger them independently via the API.

### Step 1: Generate Scenario (Scripting)
**Endpoint**: `POST /scenarios/generate`

The **Scenario Agent** uses an LLM (OpenAI/Gemini) to write a detailed video script, splitting it into scenes with visual descriptions and voiceovers.

**Example Payload**:
```json
{
  "topic": "Cyberpunk Detective",
  "style": "Noir Anime",
  "target_audience": "Adults",
  "duration": 60,
  "llm_provider": "openai"
}
```

**Output**: A JSON object containing the `Scenario` with a list of `Scenes`.

---

### Step 2: Generate Visual Layout (Image Generation)
**Endpoint**: `POST /assets/generate_from_scenario`

The **Image Agent** takes the generated `Scenario` output. It creates a "Storyboard" by planning 10-15 keyframes and then uses **DALL-E 3** to generate consistent images.

**Input**: Pass the full `Scenario` JSON object you got from Step 1.
**Output**: A list of `ImageAsset` objects, including local paths to the generated images (stored in `static/images/`).

---

### Step 3: Generate Video Clips
**Endpoint**: `POST /video/generate`

The **Video Agent** takes the images and the scenario info to generate video clips. It supports pluggable providers (default is `mock`, designed for Runway/Luma integration).

**Input**: Pass the list of `ImageAsset` objects from Step 2.
**Output**: A list of `VideoAsset` objects with paths to the generated videos.

**Note**: The Voiceover generation step is currently disabled/skipped in this workflow.

## Verification Scripts

You can run the provided shell scripts to verify each stage:

- `./verify_scenarios.sh` - Tests the Scripting Agent.
- `./verify_assets.sh` - Tests the Image planning and DALL-E generation.
- `./verify_video.sh` - Tests the Video generation (Mock provider).
