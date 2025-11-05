# 👤 Character Creator

AI-powered character development tool with personality profiles, backstories, and visual generation.

## Features

### 16 Character Archetypes

Based on Carl Jung's archetypes and Joseph Campbell's work:

1. **Hero** - The protagonist who saves the day
2. **Mentor** - The wise guide and teacher
3. **Threshold Guardian** - Tests the hero's worthiness
4. **Herald** - Brings news of change
5. **Shapeshifter** - Mysterious and unpredictable
6. **Shadow** - The antagonist and dark reflection
7. **Ally** - Loyal companion and supporter
8. **Trickster** - Comic relief and chaos agent
9. **Ruler** - Leader who creates order
10. **Creator** - Artist and innovator
11. **Innocent** - Pure soul with optimism
12. **Sage** - Seeker of truth and wisdom
13. **Explorer** - Adventurer and discoverer
14. **Outlaw** - Rebel and revolutionary
15. **Magician** - Transformer of reality
16. **Everyperson** - Relatable regular person

### Comprehensive Character Profiles

The AI generates:

**Personality Profile:**
- Big Five personality traits
- Myers-Briggs type (optional)
- Temperament
- Core values and beliefs

**Detailed Backstory:**
- Childhood and family
- Formative experiences
- Key relationships
- Trauma and challenges

**Character Elements:**
- Motivations and goals
- Internal conflicts
- External conflicts
- Fears and weaknesses
- Strengths and skills
- Character arc suggestions

**Physical Description:**
- Appearance details
- Distinctive features
- Body language
- Style and fashion

**Voice & Dialogue:**
- Speech patterns
- Vocabulary level
- Catchphrases
- Accent/dialect

### Visual Generation

- **DALL-E 3 Portraits** - High-quality character portraits
- **Multiple Art Styles** - Photorealistic, illustrated, anime, etc.
- **Download Options** - Save portraits as PNG
- **Character Gallery** - Track all created characters

### Export Options

- **Markdown** - Clean text format
- **JSON** - For importing/backing up
- **PDF** - Professional character sheet (coming soon)
- **HTML** - Character bible (coming soon)

## Installation

### Prerequisites
- Python 3.8+
- Anthropic API key (Claude)
- OpenAI API key (optional, for portraits)

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

### Anthropic Claude API
- **Model:** Claude 3.5 Sonnet
- **Purpose:** Generate character profiles
- **Cost:** ~$0.01 per character

Get your API key: https://console.anthropic.com/

### OpenAI API (Optional)
- **Model:** DALL-E 3
- **Purpose:** Generate character portraits
- **Cost:** ~$0.040 per image

Get your API key: https://platform.openai.com/api-keys

## Usage Guide

### Creating a Character

1. **Enter Basic Info:**
   - Character name (required)
   - Role (protagonist, antagonist, etc.)
   - Choose archetype (16 options)
   - Age, gender, occupation
   - Story genre

2. **Generate Profile:**
   - Click "Generate Character Profile"
   - AI creates comprehensive profile
   - Review personality, backstory, conflicts

3. **Generate Portrait (Optional):**
   - Choose art style
   - Click "Generate Portrait"
   - Wait for DALL-E 3 generation
   - Download if desired

4. **Export:**
   - Download as Markdown or JSON
   - Save for reference
   - Use in your writing

### Tips for Best Results

**Archetype Selection:**
- Choose archetype that fits character's role
- Don't feel bound by archetype - use as starting point
- Mix archetypes for complex characters

**Input Details:**
- More specific occupation = better results
- Include genre for appropriate tone
- Age affects voice and perspective

**Portrait Generation:**
- Physical description from profile used automatically
- Try different art styles for variety
- Photorealistic works best for contemporary
- Illustrated works best for fantasy

**Using Profiles:**
- Reference during writing for consistency
- Track character arcs
- Ensure character actions match motivations
- Use dialogue notes for authentic voice

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

**"Anthropic API key not configured"**
- Ensure `.streamlit/secrets.toml` exists with valid API key
- Check key format: `sk-ant-xxxxx`

**"Error generating profile"**
- Check API key validity
- Verify Claude API access
- Check internet connection

**"Portrait generation failed"**
- Verify OpenAI API key is configured
- Check OpenAI account has credits
- Physical description may be too vague - try regenerating profile

**"Export not working"**
- Markdown always works (no dependencies)
- JSON always works (no dependencies)
- PDF requires reportlab: `pip install reportlab`

## Features Roadmap

- [ ] Relationship mapper (visual web)
- [ ] Character comparison tool
- [ ] Dialogue generator
- [ ] Character interview mode
- [ ] Integration with Plot Outliner
- [ ] Character evolution tracker
- [ ] Voice consistency checker
- [ ] Character bible generator

## Tech Stack

- **Frontend:** Streamlit
- **AI Models:**
  - Anthropic Claude 3.5 Sonnet (profiles)
  - OpenAI DALL-E 3 (portraits)
- **Image Processing:** Pillow (PIL)
- **Export:** ReportLab (PDF - optional)

## Cost Considerations

**Per Character:**
- Profile generation: ~$0.01 (Claude)
- Portrait generation: ~$0.04 (DALL-E 3)
- Storage: Free (local/session)

**Optimization Tips:**
- Generate profile first, review before portrait
- Save characters as JSON for backup
- Portraits are optional - use when needed

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

---

🦚 **Built by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
