# 🎨 AI Cover Designer

Generate professional book covers using DALL-E 3 AI technology.

## Features

### Genre Selection (14 Options)
- Fantasy, Romance, Thriller, Mystery
- Sci-Fi, Horror, Contemporary, Historical
- Young Adult, Literary Fiction
- Non-Fiction, Business, Self-Help, Children's

### Art Styles (11 Options)
- Photorealistic, Digital Art, Oil Painting, Watercolor
- Illustrated, Minimalist, Abstract, Vintage
- Modern, Dark & Moody, Bright & Vibrant

### Customization Options
- **Book Details:** Title and author input
- **Color Palettes:** 9 predefined palettes + custom option
- **Mood & Atmosphere:** Describe the feeling you want
- **Additional Elements:** Specify objects, scenes, or themes
- **Text Overlay:** Optional title and author overlay

### Output Options
- **High-Res PNG:** 1024x1792 pixels (perfect for print)
- **Web-Res JPG:** 600x900 pixels (optimized for web)
- **Generation History:** Track and reload previous covers
- **Regeneration:** Tweak and regenerate covers

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key with DALL-E 3 access

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key:**
   ```bash
   # Create secrets file
   mkdir -p .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml

   # Edit secrets.toml and add your OpenAI API key
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## API Configuration

### OpenAI API
- **Model:** DALL-E 3
- **Size:** 1024x1792 (portrait)
- **Quality:** Standard
- **Cost:** ~$0.040 per image

Get your API key: https://platform.openai.com/api-keys

## Usage Guide

### Creating a Cover

1. **Enter Book Details:**
   - Book title (required)
   - Author name (required)

2. **Choose Design Preferences:**
   - Select genre
   - Pick art style
   - Choose color palette
   - Describe mood and atmosphere

3. **Add Optional Elements:**
   - Specify visual elements to include
   - Enable text overlay if desired

4. **Generate:**
   - Click "Generate Cover"
   - Wait for AI generation (~10-30 seconds)
   - Review and download

### Tips for Best Results

- **Be Specific:** Detailed mood descriptions produce better results
- **Genre Matching:** Choose art styles that complement your genre
- **Iterate:** Generate multiple versions and pick the best
- **Text Overlay:** Consider adding text in post-processing for more control
- **Color Palette:** "Rohimaya Brand Colors" uses our signature colors

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Add OpenAI API key to Secrets
4. Deploy!

### Local Development

```bash
streamlit run app.py
```

## Troubleshooting

### Common Issues

**"OpenAI API key not configured"**
- Ensure `.streamlit/secrets.toml` exists with valid API key

**"Error generating cover"**
- Check API key validity
- Verify OpenAI account has credits
- Check internet connection

**"Image quality is poor"**
- DALL-E 3 generates high-quality images by default
- Try adjusting your prompt description
- Consider regenerating with different parameters

## Features Roadmap

- [ ] Custom font selection for text overlay
- [ ] Batch cover generation
- [ ] Cover variations from single prompt
- [ ] Integration with Manuscript Formatter
- [ ] Direct publishing to KDP/IngramSpark
- [ ] Cover template library

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** OpenAI DALL-E 3
- **Image Processing:** Pillow (PIL)
- **API Client:** OpenAI Python SDK

## Cost Considerations

**Per Cover:**
- DALL-E 3 generation: ~$0.040
- Storage: Free (local/session)

**Optimization Tips:**
- Generate multiple variations in one session
- Use generation history to avoid duplicates
- Test prompts before final generation

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

---

🦚 **Built by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
