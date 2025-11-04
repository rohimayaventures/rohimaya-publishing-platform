# 🦚 AI Writing Assistant - Rohimaya Publishing

**Professional AI-powered writing assistance for authors**

## Features

- **Continue Writing** - AI continues your story naturally based on context
- **Expand Scene** - Turn brief scenes into detailed, vivid passages
- **Polish Dialogue** - Improve conversation naturalness and authenticity
- **Show Don't Tell** - Transform telling into showing with sensory details
- **Fix Grammar** - Clean up grammar, spelling, and punctuation errors
- **Improve Word Choice** - Enhance vocabulary for more vivid writing

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create `.streamlit/secrets.toml` with your API keys:

```toml
[anthropic]
api_key = "sk-ant-xxxxx"

[openai]
api_key = "sk-xxxxx"
```

### 3. Run Locally
```bash
streamlit run app.py
```

### 4. Deploy to Streamlit Cloud
1. Push this directory to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select `streamlit-apps/ai-writing-assistant/app.py` as the main file
5. Add secrets in Streamlit Cloud dashboard (Settings → Secrets)

## Usage

1. Paste your writing into the text area
2. Select your preferred genre, tone, and length in the sidebar
3. Choose an action button based on what you need
4. Review the AI-generated result
5. Copy to clipboard or save to your manuscript

## Customization

**Supported Genres:**
- General Fiction, Fantasy, Science Fiction, Romance, Thriller, Mystery, Horror, Literary Fiction, Young Adult, Historical Fiction

**Writing Tones:**
- Serious, Balanced, Light, Humorous

**Output Lengths:**
- Short (100-200 words)
- Medium (200-400 words)
- Long (400-600 words)

## API Providers

This app supports two AI providers:
- **Claude (Anthropic)** - Recommended for creative writing
- **GPT-4 (OpenAI)** - Alternative option

You only need one API key to use the app, though having both provides flexibility.

## Tech Stack

- **Framework:** Streamlit
- **AI Providers:** Claude 3.5 Sonnet, GPT-4 Turbo
- **Python:** 3.9+

## Support

For issues or questions, contact Rohimaya Publishing support.

---

**Rohimaya Publishing** | Ascend • Flourish • Enlighten
