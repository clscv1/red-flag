# flag check 🚩💚

Red flag → green flag detector powered by **Jev** via OpenRouter.

## Setup

1. Add your OpenRouter API key to `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-...
   ```

2. Install and run:
   ```bash
   uv sync
   uv run red-flag
   ```

3. Open **http://127.0.0.1:8765**

Paste a situation, hit **run the check**, and Jev scores it on a red-to-green scale.
