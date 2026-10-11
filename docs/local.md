# Local setup

RxRevive-agent runs as a local Python application. Its database, conversations, uploaded files, indexes, and results are stored in the `persistence/` directory. Calls to configured model or scientific data providers use your network connection and credentials.

## Requirements

- Python 3.11, 3.12, or 3.13
- An API key for the language model provider configured by this installation
- Java is required when running the included CPSign models

## Install and start

From the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your provider key to `.env`, then launch the application:

```powershell
python main.py
```

Open [http://localhost:7860](http://localhost:7860). Set `LOCAL_CONSTRAINED_MODE=true` in `.env` to use the reduced-resource profile documented in [Constrained mode](../CONSTRAINED_MODE.md).

To run with Docker, configure `.env` and use `docker compose up --build`. Stop the container with `docker compose down`; persistent files remain under `persistence/`.
