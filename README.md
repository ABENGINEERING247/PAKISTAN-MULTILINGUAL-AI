# Pakistan Multilingual AI Assistant 🇵🇰

A Streamlit application foundation for a professional multilingual assistant supporting Urdu, English, and Roman Urdu, with **Demo mode** and **API mode**.

## Features

- Urdu, English, Roman Urdu, and auto-detect response preference
- Demo mode works without an API key
- API mode uses the OpenAI Python SDK and a configurable model name
- Conversation context within the current Streamlit session
- Suggested prompts, clear-chat control, and responsive Streamlit layout
- API key configuration through Streamlit Secrets or environment variables
- Basic safety instructions and bounded recent conversation context

> This is an advanced starter application, not a finished enterprise SaaS. It does not yet include user accounts, persistent chat storage, official-source retrieval, billing, admin analytics, speech input/output, or a formal security audit.

## Architecture

```text
Browser
  |
  v
Streamlit UI (app.py)
  |
  v
Assistant core (assistant_core.py)
  |-- Demo response router
  `-- API mode -> OpenAI-compatible Chat Completions SDK
  |
  v
Session-only conversation history
```

For a commercial deployment, consider:
- Streamlit frontend plus a separate authenticated FastAPI backend
- PostgreSQL for users, conversations, and audit events
- Redis + worker queue for long-running jobs and rate limiting
- Official-source retrieval (RAG) with citations for Pakistan-specific government information
- User consent, privacy notice, retention/deletion controls, and access controls
- Usage metering and payment integration only after terms and compliance are reviewed

## Run locally

Requires Python 3.10 or newer.

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

The app starts in Demo mode. To use API mode, put a valid key and model name in `.env`, or use Streamlit Secrets. Never commit `.env` or real secrets.

## Configure API mode

For local use, edit `.env`:

```dotenv
OPENAI_API_KEY=your_real_key_here
OPENAI_MODEL=gpt-4o-mini
```

For Streamlit Community Cloud:
1. Push the project to a private or public GitHub repository.
2. In Streamlit Community Cloud, create an app and select `app.py` as the entry point.
3. Open the app's **Settings → Secrets**.
4. Add TOML-formatted secrets:

```toml
OPENAI_API_KEY = "your_real_key_here"
OPENAI_MODEL = "gpt-4o-mini"
```

5. Save and reboot the app.
6. Choose **API** in the sidebar.

Model availability and API pricing depend on the provider account and model access. Change the model name to one available to your account.

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository, e.g. `pakistan-multilingual-ai-assistant`.
2. Add `app.py`, `assistant_core.py`, `requirements.txt`, `README.md`, `.gitignore`, and `.streamlit/config.toml`.
3. Do **not** upload `.env` or `.streamlit/secrets.toml`.
4. Push to GitHub.
5. Create a new app in Streamlit Community Cloud and choose `app.py`.
6. Add the API key in Cloud Secrets if API mode is needed.
7. Test Demo mode, API mode, Urdu rendering, English, and Roman Urdu on desktop and mobile.

## Security checklist before commercial use

- Keep API keys in secrets/environment variables; rotate any exposed key immediately.
- Add authentication and role-based authorization before exposing private user data.
- Add per-user/IP rate limits, request size limits, and spending alerts.
- Do not log API keys, passwords, CNICs, or sensitive chat contents.
- Publish a privacy notice and define data retention/deletion procedures.
- Treat user prompts and uploaded documents as untrusted input.
- Do not let model output execute shell commands, SQL, or arbitrary code.
- Add moderation/abuse controls, exception handling, and audit trails.
- Use HTTPS and secure cookie/session settings in any custom backend.
- Add tests, monitoring, backups, and incident response procedures.
- Verify legal, tax, data-protection, consumer, and sector-specific obligations with qualified advisers before launch.

## Known limitations

- Demo answers are rule-based examples, not generated intelligence.
- API mode requires internet access and an available model/API account.
- Chat history lives in Streamlit session state and is not a permanent database.
- No live web search or official-source citations are connected.
- No speech, image, or file-upload workflow is implemented in this version.
- Streamlit is convenient for an MVP; high-concurrency commercial systems may need a separate backend and worker services.

## Project structure

```text
pakistan_multilingual_ai_assistant/
├── app.py
├── assistant_core.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

## License

Choose and add a license before publishing or commercial distribution. Review all third-party SDK terms and API-provider terms separately.
