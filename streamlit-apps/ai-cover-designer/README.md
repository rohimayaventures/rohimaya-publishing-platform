# 🎨 AI Cover Designer

Professional book cover generation powered by DALL-E 3 for the Rohimaya Publishing Platform.

## ✨ Features

- **DALL-E 3 Integration**: Leverages OpenAI's most advanced image generation model
- **14 Genre Options**: From Fiction to Poetry, covering all major publishing categories
- **11 Art Styles**: Choose from Realistic, Oil Painting, Watercolor, Minimalist, and more
- **Flexible Sizing**: Portrait, Landscape, or Square formats
- **HD Quality Options**: Standard or High-Definition output
- **Multiple Download Formats**: PNG and JPEG support
- **Instant Preview**: See your cover design immediately
- **Professional Branding**: Beautiful Rohimaya-themed interface
- **Prompt Transparency**: View both original and AI-enhanced prompts
- **Mobile Responsive**: Works on all devices

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key with DALL-E 3 access
- pip package manager

### Setup Steps

1. **Navigate to the app directory:**
   ```bash
   cd streamlit-apps/ai-cover-designer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   - Copy the example secrets file:
     ```bash
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

1. **Enter Book Details:**
   - Book Title (required)
   - Author Name (required)
   - Select Genre from dropdown

2. **Customize Design:**
   - Choose Art Style (11 options)
   - Specify Mood/Atmosphere (optional)
   - Add Additional Details for specific elements

3. **Configure Settings:**
   - Select Image Size (Portrait recommended for books)
   - Choose Quality (HD for professional use)

4. **Generate & Download:**
   - Click "Generate Cover"
   - Wait 10-30 seconds for AI generation
   - Preview your cover
   - Download in PNG or JPEG format

### Tips for Best Results

**Be Specific:**
```
Good: "A lone astronaut standing on a red planet with two moons in a purple sky"
Better: "A lone astronaut in a white suit standing on a rocky red Martian surface,
        with two moons visible in a purple-orange dusk sky, mysterious atmosphere"
```

**Genre-Specific Suggestions:**

- **Mystery/Thriller**: Use "dark", "mysterious", "shadows", "urban" keywords
- **Romance**: Include "warm", "intimate", "emotional", "soft lighting"
- **Fantasy**: Specify "magical elements", "mythical creatures", "epic landscapes"
- **Business**: Request "professional", "modern", "clean", "bold typography"
- **Children's**: Ask for "colorful", "friendly", "playful", "illustrated"

**Artistic Styles:**

- **Typography-focused**: Best for non-fiction and business books
- **Illustrated**: Perfect for children's books and young adult
- **Photographic**: Ideal for memoirs and biographies
- **Minimalist**: Great for literary fiction and self-help
- **Oil Painting**: Excellent for historical fiction

## 🖼️ Image Size Guide

| Size | Dimensions | Best For |
|------|------------|----------|
| Portrait | 1024x1792 | Standard book covers (recommended) |
| Square | 1024x1024 | Social media, thumbnails |
| Landscape | 1792x1024 | E-book banners, promotional graphics |

## 💰 Cost Estimates

**DALL-E 3 Pricing** (as of 2024):

- **Standard Quality**: ~$0.04 per image
- **HD Quality**: ~$0.08 per image

**Recommended Approach:**
- Generate 3-5 variations: $0.20-$0.40
- Select and refine best option: $0.04-$0.08
- Total estimated cost per cover: **$0.24-$0.48**

Compare to hiring a professional designer ($100-$500+), this is extremely cost-effective!

## 📋 API Key Configuration

### Getting Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key (you won't see it again!)

### Setting Up Secrets

Create `.streamlit/secrets.toml` in the app directory:

```toml
[openai]
api_key = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
```

**Security Note:** Never commit `secrets.toml` to version control!

## 🌐 Deployment

### Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add AI Cover Designer"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `streamlit-apps/ai-cover-designer/app.py`
   - Add secrets in the dashboard:
     - Go to App Settings > Secrets
     - Paste your secrets.toml content

3. **Your app will be live at:**
   ```
   https://[your-app-name].streamlit.app
   ```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-cover-designer .
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-xxx ai-cover-designer
```

## 🔧 Troubleshooting

### Common Issues

**Issue: "Error loading OpenAI API key"**
- **Solution**: Check that `.streamlit/secrets.toml` exists and contains valid API key
- Verify format: `[openai]` section header, then `api_key = "sk-..."`

**Issue: "Rate limit exceeded"**
- **Solution**: DALL-E 3 has usage limits. Wait a few minutes or check your OpenAI dashboard
- Consider upgrading your OpenAI plan for higher limits

**Issue: "Image generation timeout"**
- **Solution**: HD images take longer (20-30 seconds). Try Standard quality first
- Check your internet connection

**Issue: "Content policy violation"**
- **Solution**: DALL-E 3 has content restrictions. Avoid:
  - Violence, gore, or disturbing imagery
  - Copyrighted characters or celebrities
  - Explicit content
- Rephrase your prompt to be more abstract

**Issue: App won't start**
- **Solution**: Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt --upgrade
  ```

**Issue: Poor quality results**
- **Solution**:
  - Use HD quality setting
  - Be more specific in your prompt
  - Try different art styles
  - Generate multiple variations

### Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `401 Unauthorized` | Invalid API key | Check your OpenAI API key |
| `429 Too Many Requests` | Rate limit hit | Wait and retry |
| `500 Server Error` | OpenAI service issue | Retry in a few minutes |
| `timeout` | Request took too long | Check internet, try standard quality |

## 📚 Examples

### Mystery Novel Cover
```
Title: The Last Witness
Author: Sarah Mitchell
Genre: Mystery/Thriller
Style: Photographic
Mood: Dark, suspenseful, noir
Details: Foggy city street at night, single streetlight, shadows
```

### Fantasy Epic Cover
```
Title: Crown of Dragons
Author: Alex Storm
Genre: Fantasy
Style: Oil Painting
Mood: Epic, magical, adventurous
Details: Dragon silhouette, ancient castle, golden crown, purple sky
```

### Business Book Cover
```
Title: Strategic Innovation
Author: Dr. James Chen
Genre: Business
Style: Minimalist
Mood: Professional, modern, bold
Details: Abstract geometric shapes, corporate colors, clean typography space
```

## 🎓 Best Practices

1. **Generate Multiple Versions**: Create 3-5 variations with slight prompt changes
2. **Test Different Styles**: Same book can look amazing in different artistic styles
3. **Consider Your Audience**: Genre conventions help readers identify your book
4. **Leave Space for Text**: Ensure design has clear areas for title/author
5. **Check at Thumbnail Size**: Covers should be recognizable when small
6. **Save Your Prompts**: Keep successful prompts for future reference
7. **Iterate**: Refine based on initial results

## 🆘 Support

For issues or questions:

- **GitHub Issues**: [rohimaya-publishing-platform/issues](https://github.com/rohimayaventures/rohimaya-publishing-platform/issues)
- **Email**: support@rohimaya.com
- **Documentation**: See main project README

## 📄 License

Part of the Rohimaya Publishing Platform - All rights reserved

---

**Rohimaya Publishing Platform**
🦚 Where creativity meets innovation | Rise from the ashes, soar with grace
