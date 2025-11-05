# 🎙️ Audiobook Generator

Convert manuscripts into professional audiobooks using AI text-to-speech technology for the Rohimaya Publishing Platform.

## ✨ Features

### Core Functionality
- **OpenAI TTS Integration**: Primary TTS provider (most reliable)
- **Multiple AI Voices**: 6 distinct voices (Alloy, Echo, Fable, Onyx, Nova, Shimmer)
- **Quality Options**: Standard (TTS-1) and HD (TTS-1-HD) models
- **Automatic Chapter Detection**: Intelligently splits manuscripts into chapters
- **Multi-Chapter Support**: Process and download chapters individually
- **Progress Tracking**: Real-time progress bars and status updates
- **Cost Estimation**: Calculate costs before generation
- **Multiple Export Formats**: MP3 (ACX-ready), AAC, OPUS

### ACX-Ready Output
- **Format**: MP3, 192 kbps CBR
- **Sample Rate**: 44.1 kHz
- **Ready for Audible submission**

### Professional Features
- **Batch Processing**: Handle long manuscripts by splitting into chunks
- **Combined Output**: Merge all chapters into single audiobook file
- **Rohimaya Branding**: Beautiful, professional interface
- **Mobile Responsive**: Works on all devices
- **Error Handling**: Comprehensive error messages and recovery

### Future Enhancements (Planned)
- Inworld AI integration
- ElevenLabs integration
- Voice cloning capabilities
- Emotion and pacing controls

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key with TTS access
- ffmpeg (required for audio processing)
- pip package manager

### System Dependencies

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
Download ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### Setup Steps

1. **Navigate to the app directory:**
   ```bash
   cd streamlit-apps/audiobook-generator
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   - Copy the example secrets file:
     ```bash
     mkdir -p .streamlit
     cp .streamlit/secrets.toml.example .streamlit/secrets.toml
     ```
   - Edit `.streamlit/secrets.toml` and add your OpenAI API key:
     ```toml
     [openai]
     api_key = "sk-your-actual-api-key-here"
     ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 🎯 Usage Guide

### Basic Workflow

1. **Prepare Your Manuscript:**
   - Format with clear chapter markers (e.g., "Chapter 1", "### Chapter Title")
   - Remove unnecessary formatting
   - Proofread for TTS-friendly text

2. **Configure Settings (Sidebar):**
   - Select voice (preview descriptions)
   - Choose model quality (Standard or HD)
   - Enable/disable auto-chapter detection
   - Select output format

3. **Input Text:**
   - Go to "Input Text" tab
   - Paste your manuscript
   - Review detected chapters and statistics

4. **Generate Audio:**
   - Switch to "Generate Audio" tab
   - Preview detected chapters
   - Click "Generate Audiobook"
   - Monitor progress

5. **Download:**
   - Download individual chapters
   - Or download complete merged audiobook
   - Files are ready for distribution or ACX submission

### Voice Selection Guide

| Voice | Gender | Characteristics | Best For |
|-------|--------|-----------------|----------|
| **Alloy** | Neutral | Balanced, clear | General narration, non-fiction |
| **Echo** | Male | Authoritative, clear | Business, technical books |
| **Fable** | Male | British accent, expressive | Fantasy, historical fiction |
| **Onyx** | Male | Deep, dramatic | Thrillers, mysteries |
| **Nova** | Female | Warm, friendly | Romance, self-help |
| **Shimmer** | Female | Soft, gentle | Children's books, poetry |

### Model Quality Comparison

| Model | Quality | Speed | Cost per 1M chars | Best For |
|-------|---------|-------|-------------------|----------|
| **TTS-1** | Standard | Fast | $15 | Drafts, previews, quick tests |
| **TTS-1-HD** | High-Def | Slower | $30 | Final production, publishing |

### Chapter Detection

The app automatically detects chapters using these patterns:

- `Chapter 1`, `Chapter One`, etc.
- `CHAPTER 1`, `CHAPTER ONE`
- `Ch. 1`, `ch. 1`
- Markdown headers: `# Chapter Title`, `## Chapter Title`
- Triple asterisks: `*** Chapter Title ***`

**Pro Tip:** Use consistent formatting for best results!

### Text Formatting Tips

**Good Practices:**
```
Chapter 1: The Beginning

It was a dark and stormy night. The wind howled through the trees,
and rain pelted against the windows.

"We must leave now," Sarah whispered urgently.
```

**Things to Fix:**
- Remove special characters that TTS struggles with: `@#$%^&*`
- Spell out abbreviations: "Dr. Smith" → "Doctor Smith"
- Write numbers as words: "123" → "one hundred twenty-three"
- Expand acronyms first time: "NASA (National Aeronautics and Space Administration)"
- Use proper punctuation for natural pauses

## 💰 Cost Estimates

### Pricing (OpenAI TTS)

**Per Character:**
- TTS-1: $0.000015
- TTS-1-HD: $0.000030

**Example Costs:**

| Book Length | Words | Characters* | TTS-1 Cost | TTS-1-HD Cost |
|-------------|-------|-------------|------------|---------------|
| Short story | 5,000 | 25,000 | $0.38 | $0.75 |
| Novella | 20,000 | 100,000 | $1.50 | $3.00 |
| Novel | 80,000 | 400,000 | $6.00 | $12.00 |
| Epic novel | 150,000 | 750,000 | $11.25 | $22.50 |

*Estimated at 5 characters per word

### Cost Comparison

| Option | 80,000-word novel | Notes |
|--------|-------------------|-------|
| **AI TTS (Standard)** | $6 | This app |
| **AI TTS (HD)** | $12 | This app |
| **Professional narrator** | $2,000-$4,000 | Per-finished-hour rate |
| **ACX narration** | $500-$4,000 | Varies by narrator |

**Savings: 99%+ compared to professional narration!**

### Duration Estimates

Average speaking rate: **150-200 words per minute**

| Word Count | Duration (200 wpm) | Duration (150 wpm) |
|------------|--------------------|--------------------|
| 50,000 | 4.2 hours | 5.6 hours |
| 80,000 | 6.7 hours | 8.9 hours |
| 100,000 | 8.3 hours | 11.1 hours |
| 150,000 | 12.5 hours | 16.7 hours |

## 📋 API Key Configuration

### Getting Your OpenAI API Key

1. **Sign up/Login:**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Create account or sign in

2. **Create API Key:**
   - Navigate to API Keys section
   - Click "Create new secret key"
   - Name it (e.g., "Audiobook Generator")
   - Copy the key immediately (you won't see it again!)

3. **Add to Secrets:**
   - Edit `.streamlit/secrets.toml`
   - Paste your key:
     ```toml
     [openai]
     api_key = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
     ```

4. **Set Usage Limits (Recommended):**
   - In OpenAI dashboard, set monthly spending limits
   - Start with $10-20 for testing
   - Monitor usage regularly

### Security Best Practices

- ✅ Never commit `secrets.toml` to version control
- ✅ Use environment variables in production
- ✅ Set spending limits on OpenAI account
- ✅ Rotate API keys periodically
- ✅ Monitor usage in OpenAI dashboard
- ❌ Never share your API key
- ❌ Never hardcode keys in source code

## 🌐 Deployment

### Streamlit Cloud

1. **Prepare Repository:**
   ```bash
   git add .
   git commit -m "Add Audiobook Generator"
   git push origin main
   ```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repository
   - Select `streamlit-apps/audiobook-generator/app.py`
   - Add secrets in dashboard:
     - App Settings > Secrets
     - Paste contents of `secrets.toml`

3. **Important Notes:**
   - Streamlit Cloud may have file size limits
   - For large audiobooks, consider local deployment
   - Processing time may be limited

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
docker build -t audiobook-generator .
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-xxx \
  audiobook-generator
```

### Local Production Setup

For processing large manuscripts locally:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with custom port
streamlit run app.py --server.port=8502
```

## 🔧 Troubleshooting

### Common Issues

**Issue: "Error loading OpenAI API key"**
- **Cause**: Missing or incorrect `secrets.toml` configuration
- **Solution**:
  1. Ensure `.streamlit/secrets.toml` exists
  2. Verify format: `[openai]` section header
  3. Check API key starts with `sk-`
  4. No quotes or extra spaces

**Issue: "ffmpeg not found"**
- **Cause**: Audio processing requires ffmpeg
- **Solution**:
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt-get install ffmpeg`
  - Windows: Download from ffmpeg.org and add to PATH
  - Verify: `ffmpeg -version`

**Issue: "Rate limit exceeded"**
- **Cause**: Too many requests to OpenAI API
- **Solution**:
  - Wait 1-2 minutes between large requests
  - Upgrade OpenAI plan for higher limits
  - Process smaller chunks

**Issue: "Memory error with large files"**
- **Cause**: Processing very long manuscripts
- **Solution**:
  - Process chapters individually instead of all at once
  - Use TTS-1 (standard) instead of HD
  - Split manuscript into smaller sections
  - Increase system RAM or use cloud processing

**Issue: "Audio sounds robotic"**
- **Cause**: Using Standard (TTS-1) model
- **Solution**:
  - Switch to TTS-1-HD for better quality
  - Try different voices
  - Improve text formatting (punctuation, spacing)

**Issue: "Chapter detection not working"**
- **Cause**: Non-standard chapter formatting
- **Solution**:
  - Use clear chapter markers: "Chapter 1", "Chapter 2"
  - Or disable auto-detection and process as single file
  - Manually add chapter markers before processing

**Issue: "Generation stops mid-process"**
- **Cause**: Network timeout or API error
- **Solution**:
  - Check internet connection
  - Verify OpenAI API status
  - Process in smaller batches
  - Check API key has available credits

### Error Messages

| Error Code | Meaning | Solution |
|------------|---------|----------|
| `401` | Invalid API key | Verify API key in secrets.toml |
| `429` | Rate limit | Wait and retry, or upgrade plan |
| `500` | OpenAI server error | Retry in a few minutes |
| `timeout` | Request too long | Reduce chunk size |

### Performance Optimization

**For Large Manuscripts:**

1. **Process in Batches:**
   - Generate 5-10 chapters at a time
   - Download and save each batch
   - Combine manually if needed

2. **Use Standard Quality First:**
   - Test with TTS-1 (cheaper, faster)
   - Once satisfied, regenerate in HD

3. **Optimize Text:**
   - Remove unnecessary whitespace
   - Clean up formatting
   - Spell out abbreviations

## 📚 ACX Submission Guide

### Preparing for Audible (ACX)

1. **Use ACX-Ready Settings:**
   - Output Format: "MP3 (ACX-Ready)"
   - This ensures 192 kbps, 44.1 kHz

2. **Audio Requirements:**
   - Between 192-320 kbps
   - 44.1 kHz or 48 kHz sample rate
   - Mono or stereo
   - Consistent volume levels

3. **File Naming:**
   - Opening credits: `BookTitle_Open.mp3`
   - Chapters: `BookTitle_Ch01.mp3`, `BookTitle_Ch02.mp3`
   - Closing credits: `BookTitle_Close.mp3`

4. **Additional Requirements:**
   - Opening/closing credits (create separately)
   - Room tone (1-5 seconds of silence)
   - No long pauses or music

5. **Quality Check:**
   - Peak values: -3dB to -23dB
   - RMS: -18dB to -23dB
   - Max noise floor: -60dB
   - Use ACX Audio Lab tool for verification

### Post-Processing (Optional)

For even better quality, use audio editing software:

- **Audacity** (free): Normalize, compress, EQ
- **Adobe Audition**: Professional mastering
- **iZotope RX**: Noise reduction, enhancement

## 📖 Examples

### Fiction Novel

**Settings:**
- Voice: Nova or Fable
- Model: TTS-1-HD
- Format: MP3 (ACX-Ready)
- Auto-detect chapters: Yes

**Text format:**
```
Chapter 1: A New Beginning

The sun rose over the mountains, casting golden light across the valley.
Sarah stood at the window, watching the world awaken.

"Today is the day," she whispered to herself.
```

### Non-Fiction Book

**Settings:**
- Voice: Alloy or Echo
- Model: TTS-1-HD
- Format: MP3 (ACX-Ready)
- Auto-detect chapters: Yes

**Text format:**
```
Chapter 1: Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that enables
computers to learn from data without being explicitly programmed.

In this chapter, we'll explore three key concepts:
1. Supervised learning
2. Unsupervised learning
3. Reinforcement learning
```

### Children's Book

**Settings:**
- Voice: Shimmer or Nova
- Model: TTS-1-HD
- Format: MP3 (High Quality)
- Auto-detect chapters: No

**Text format:**
```
Once upon a time, in a magical forest, there lived a friendly dragon
named Spark. Spark loved to help all the animals in the forest.

One sunny morning, Spark heard a tiny voice calling, "Help! Help!"
```

## 💡 Best Practices

### Text Preparation

1. **Proofread Carefully:**
   - Fix typos and spelling errors
   - Check punctuation
   - Remove special characters

2. **Format for Audio:**
   - Use consistent chapter markers
   - Break long paragraphs
   - Add pauses with punctuation

3. **Consider Pacing:**
   - Use commas for natural pauses
   - Periods for longer pauses
   - Ellipsis (...) for dramatic pauses

### Voice Selection

1. **Match to Genre:**
   - Mystery: Onyx (deep, dramatic)
   - Romance: Nova (warm, friendly)
   - Business: Echo (authoritative)

2. **Test Multiple Voices:**
   - Generate first chapter with different voices
   - Compare and choose best fit

3. **Consistency:**
   - Use same voice throughout book
   - Maintain same settings

### Cost Management

1. **Start Small:**
   - Test with one chapter
   - Verify quality before full generation

2. **Use Standard for Testing:**
   - TTS-1 for drafts and tests
   - TTS-1-HD only for final production

3. **Set Budget Limits:**
   - Configure OpenAI spending limits
   - Monitor costs regularly

## 🆘 Support

For issues or questions:

- **GitHub Issues**: [rohimaya-publishing-platform/issues](https://github.com/rohimayaventures/rohimaya-publishing-platform/issues)
- **Email**: support@rohimaya.com
- **Documentation**: See main project README
- **OpenAI Support**: [help.openai.com](https://help.openai.com)

## 📄 License

Part of the Rohimaya Publishing Platform - All rights reserved

---

**Rohimaya Publishing Platform**
🦚 Where creativity meets innovation | Rise from the ashes, soar with grace
