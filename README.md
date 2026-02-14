# runpod-serverless-template

Minimal template for deploying a small Text‑to‑Speech API to Runpod (and for local testing).

Overview
--------

This repository is a lightweight template that exposes a FastAPI-based TTS endpoint (`/v1/audio/speech`) and a healthcheck (`/ping`). The example `app/api.py` shows how a backend model can be wired into the API — replace or modify `app/api.py` to integrate your own model or backend logic.

Prerequisites
-------------

- Python 3.8+ (project uses `pyproject.toml`) and a virtual environment
- Docker (optional, used for building and running containers locally and for pushing images to Runpod)

Local testing
-------------

1. Create and activate a virtual environment, then install dependencies (project uses `pyproject.toml`):

	 - Windows (PowerShell):

		 ```powershell
		 .venv\Scripts\Activate.ps1
		 pip install -e .
		 ```

	 - or install from `requirements.txt` if you prefer:

		 ```powershell
		 pip install -r requirements.txt
		 ```

2. Start the local server. This template includes a convenience command used in this workspace: `uv sync`.

	 - Run the workspace helper (if available):

		 ```powershell
		 uv sync
		 ```

	 - Or run Uvicorn directly (the ASGI app is `app.api:app`):

		 ```powershell
		 python -m uvicorn app.api:app --host 0.0.0.0 --port 8000
		 ```

3. Test the API with the example client or curl. Example using the included sample request:

	 ```powershell
	 python utils\sample_request.py
	 ```

	 Or use curl to create a WAV file:

	 ```bash
	 curl -X POST http://localhost:8000/v1/audio/speech \
		 -H "Content-Type: application/json" \
		 -d '{"text":"Hello from Runpod template","voice":"af_heart"}' \
		 --output out.wav
	 ```

Runpod deployment
-----------------

You can deploy this template to Runpod using a container image. The container should expose a HTTP server and provide a `/ping` health endpoint (this repo already includes it).

1. Build and tag a container image locally:

	 ```bash
	 docker build -t yourrepo/runpod-template:latest .
	 ```

2. Push the image to a registry Runpod can access (Docker Hub, GHCR, etc.):

	 ```bash
	 docker push yourrepo/runpod-template:latest
	 ```

3. In the Runpod dashboard create a new worker using a Custom Container and provide the image name. Configure the container port to the port your app listens on (the example uses `PORT` with a default of `80` when run via `python app/api.py`, but when running with Uvicorn you can choose `8000` — set the Runpod port accordingly).

4. Add any required environment variables (API keys, model paths, etc.) in the Runpod UI and start the worker. Use the `/ping` endpoint to verify health.

Docker: build and run locally
----------------------------

Build the image:

```bash
docker build -t runpod-serverless-template:latest .
```

Run the container mapping host port 8000 to the container's default port (this project listens on the `PORT` env var; by default the included `__main__` runs Uvicorn on port 80):

```bash
docker run --rm -p 8000:80 runpod-serverless-template:latest
```

If you prefer the container to listen on `8000` inside the container, set `PORT` accordingly and map ports the same:

```bash
docker run --rm -e PORT=8000 -p 8000:8000 runpod-serverless-template:latest
```

Notes
-----

- This repository is a template. Update `app/api.py` to integrate your model or backend logic — the FastAPI `app` instance is defined there and the server entrypoint is present for local runs.
- The health route `/ping` is required by Runpod to monitor instance health.
- See `utils/standalone_inference.py` and `utils/gradio_web_ui.py` for example helper scripts and UI wiring.

Questions or next steps
-----------------------

If you'd like, I can:

- run the app locally and test the endpoints
- add a GitHub Actions workflow to build and push images automatically
- convert the project to include a `requirements.txt` or a Docker multi-stage build optimized for size
