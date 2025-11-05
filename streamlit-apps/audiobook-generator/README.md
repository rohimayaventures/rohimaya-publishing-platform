# 🎧 Audiobook Generator

Convert manuscripts to professional audiobooks with AI-powered text-to-speech.

## Features

### Multi-TTS Support (Automatic Fallback)
1. **Prasad's Custom TTS** (FREE) - Priority 1
2. **ElevenLabs** (High Quality) - Priority 2
3. **OpenAI TTS** (Reliable) - Priority 3

The system automatically tries services in order and falls back if one fails.

### Voice Selection (9 AI Voices)

**Male Voices:**
- Male Deep - Deep, authoritative
- Male Standard - Clear, neutral
- Male Young - Youthful, energetic

**Female Voices:**
- Female Deep - Rich, mature
- Female Standard - Warm, clear
- Female Young - Bright, cheerful

**Neutral Voices:**
- Neutral Professional - Professional tone
- Neutral Conversational - Friendly, casual
- Neutral Storyteller - Narrative, expressive

### Audio Controls
- **Speed:** 0.8x to 1.5x (0.1x increments)
- **Pitch:** -5 to +5 (1 increment)
- **Emotion:** Neutral, Expressive, Calm, Excited

### Input Options
- Upload manuscript (.txt, .docx, .md)
- Paste text directly
- Automatic chapter detection

### Generation Modes
- **Full Manuscript** - Convert entire book
- **Chapter by Chapter** - Generate individual chapters
- **Selected Text** - Convert specific passages

### Output
- ACX-ready MP3 (44.1kHz, 192kbps)
- Audio player preview
- Individual chapter files
- Progress tracking

## Installation

### Prerequisites
- Python 3.8+
- At least one TTS API key (Prasad's TTS, ElevenLabs, or OpenAI)

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   ```bash
   # Create secrets file
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml

   # Edit secrets.toml and add your API keys
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## API Configuration

### Prasad's Custom TTS (Recommended - FREE)
- **Endpoint:** Configure your custom endpoint
- **API Key:** Optional (if authentication required)
- **Cost:** FREE
- **Quality:** Excellent for most use cases

### ElevenLabs
- **API:** https://elevenlabs.io/
- **Cost:** ~$0.30 per 1000 characters
- **Quality:** Highest quality, very natural
- **Voices:** Professional voice library

Get your API key: https://elevenlabs.io/app/settings/api-keys

### OpenAI TTS
- **Model:** tts-1
- **Cost:** $0.015 per 1,000 characters
- **Quality:** Good, reliable
- **Voices:** 6 built-in voices

Get your API key: https://platform.openai.com/api-keys

## Usage Guide

### Basic Workflow

1. **Input Your Text:**
   - Upload a file (TXT, DOCX, MD)
   - Or paste text directly

2. **Select Voice:**
   - Choose from 9 voice options
   - Preview voice descriptions

3. **Adjust Settings:**
   - Set speed (0.8x - 1.5x)
   - Adjust pitch (-5 to +5)
   - Select emotion

4. **Choose Generation Mode:**
   - Full manuscript
   - Chapter by chapter
   - Selected text only

5. **Generate:**
   - Click "Generate Audiobook"
   - Wait for processing
   - Preview and download

### Chapter Detection

The app automatically detects chapters using common patterns:
- "Chapter 1", "Chapter 2", etc.
- "CHAPTER 1", "CHAPTER 2", etc.
- "Part 1", "Part 2", etc.
- Numbered sections (1., 2., etc.)

### ACX Requirements

Output meets ACX (Audiobook Creation Exchange) standards:
- Sample rate: 44.1kHz
- Bit rate: 192kbps
- Format: MP3
- Mono or stereo

## Tips for Best Results

### Voice Selection
- **Fiction:** Use storyteller or expressive voices
- **Non-Fiction:** Use professional or standard voices
- **Children's Books:** Use young, energetic voices
- **Business:** Use professional, authoritative voices

### Speed Settings
- **Standard:** 1.0x (normal reading pace)
- **Slower:** 0.8-0.9x (educational content)
- **Faster:** 1.1-1.2x (dynamic content)

### Chapter Management
- Generate chapter by chapter for long manuscripts
- Allows for breaks and consistency checks
- Easier to fix individual chapters if needed

### Cost Optimization
- Use Prasad's Custom TTS when available (FREE)
- Test with short samples first
- Generate chapters incrementally

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Add API keys to Secrets
4. Deploy!

### Local Development

```bash
streamlit run app.py
```

## Troubleshooting

### Common Issues

**"No TTS services configured"**
- Add at least one API key to secrets.toml
- Verify API key format is correct

**"Failed to generate audio"**
- Check API key validity
- Verify account has credits
- Try a different TTS service

**"DOCX support not available"**
- Install python-docx: `pip install python-docx`

**"Audio quality is poor"**
- Try ElevenLabs for highest quality
- Adjust speed to 1.0x for natural pace
- Use "Expressive" emotion for better intonation

**"Generation is slow"**
- Long texts take time (expected)
- Use chapter-by-chapter mode
- Consider splitting very long manuscripts

## Cost Estimates

### Per 50,000 word novel:

**Prasad's Custom TTS:**
- Cost: $0 (FREE)
- Time: Varies by endpoint

**ElevenLabs:**
- Characters: ~300,000
- Cost: ~$90
- Time: ~15-30 minutes

**OpenAI TTS:**
- Characters: ~300,000
- Cost: ~$4.50
- Time: ~10-20 minutes

## Features Roadmap

- [ ] Background music integration
- [ ] Multiple voice support (dialogue)
- [ ] Sound effects library
- [ ] Professional voice casting
- [ ] Direct ACX upload
- [ ] Batch processing
- [ ] Voice cloning (custom voices)
- [ ] Pronunciation dictionary
- [ ] Chapter markers export

## Tech Stack

- **Frontend:** Streamlit
- **TTS Engines:** Custom API, ElevenLabs, OpenAI
- **Audio Processing:** pydub
- **Document Parsing:** python-docx

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

## Credits

Built by Prasad (Peacock) with 🦚 for Rohimaya Publishing.

---

🦚 **Built by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
