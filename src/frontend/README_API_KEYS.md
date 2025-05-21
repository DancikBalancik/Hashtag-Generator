# API Key Storage for Hashtag Generator

API keys for LLM providers (OpenAI, Anthropic, Azure, etc.) are stored **only in your browser's localStorage** for privacy and security. They are never written to disk or sent to the backend server.

- **Location:** Browser localStorage (per browser, per device)
- **How to clear:** Use the API Keys tab in the app, or clear your browser's site data for this app.
- **Not stored in any file:** No API key files are created on disk, so nothing sensitive is committed to git.

If you package this app as a desktop app (Electron), keys will be stored in the local storage of the Electron browser context.
