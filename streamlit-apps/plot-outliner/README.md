# 📚 Plot Outliner

AI-powered story structure and plot development tool with 8 professional plot structures.

## Features

### 8 Plot Structure Templates

1. **Three-Act Structure**
   - Classic storytelling format
   - Setup → Confrontation → Resolution
   - 10 key beats

2. **Hero's Journey**
   - Joseph Campbell's monomyth
   - 12 stages of the hero's adventure
   - Perfect for epic tales and transformations

3. **Save the Cat**
   - Blake Snyder's 15-beat structure
   - Proven screenwriting method
   - Works great for novels too

4. **Seven-Point Story Structure**
   - Dan Wells' character-focused approach
   - Emphasis on character arc
   - Efficient and effective

5. **Five-Act Structure**
   - Freytag's Pyramid
   - Classical dramatic structure
   - Great for literary fiction

6. **Romance Beat Sheet**
   - Specifically for romance novels
   - From meet-cute to HEA/HFN
   - All key romance milestones

7. **Mystery Structure**
   - Designed for mystery and detective stories
   - Crime → Investigation → Resolution
   - Includes red herrings and reveals

8. **Custom**
   - Build your own structure
   - Complete flexibility
   - Define your own beats

### AI Generation Features

For each beat, the AI provides:
- **Specific scene descriptions** tailored to your premise
- **Character development points** for protagonist growth
- **Key plot revelations** to maintain reader interest
- **Suggested word counts** for pacing
- **Pacing recommendations** (fast/slow sections)

### Interactive Builder

- Edit each beat and scene
- Reorder beats (drag & drop)
- Add or remove beats
- Visual timeline view
- Track progress

### Export Options

- **PDF** - Formatted outline with professional layout
- **Markdown** - Clean text format
- **Word/DOCX** - Editable document
- **JSON** - For importing/backing up

## Installation

### Prerequisites
- Python 3.8+
- Anthropic API key (Claude)

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

   # Edit secrets.toml and add your Anthropic API key
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## API Configuration

### Anthropic Claude API
- **Model:** Claude 3.5 Sonnet
- **Purpose:** Generate plot outlines and beat details
- **Cost:** ~$0.003 per outline

Get your API key: https://console.anthropic.com/

## Usage Guide

### Creating a Plot Outline

1. **Enter Story Details:**
   - Story title
   - Author name
   - Story premise (2-3 sentences)
   - Genre
   - Target word count

2. **Choose Structure:**
   - Browse 8 structure templates
   - Read descriptions
   - Select the one that fits your story

3. **Generate:**
   - Click "Generate Plot Outline"
   - AI analyzes your premise
   - Creates detailed beat-by-beat outline

4. **Review & Edit:**
   - Expand each beat
   - Read scene descriptions
   - Note character development
   - Check pacing recommendations

5. **Export:**
   - Download as Markdown, Word, or JSON
   - Use as writing guide
   - Share with beta readers or editors

### Tips for Best Results

**Writing a Good Premise:**
- Include protagonist
- Mention the conflict
- Hint at stakes
- Keep it concise (2-3 sentences)

Example:
> "A young wizard discovers she's the last hope against an ancient evil. She must master forbidden magic while navigating school politics and her growing feelings for her rival. Time is running out as the dark forces gather strength."

**Choosing the Right Structure:**
- **Three-Act:** Universal, works for any genre
- **Hero's Journey:** Epic adventures, transformations
- **Save the Cat:** Commercial fiction, tight plotting
- **Seven-Point:** Character-driven stories
- **Five-Act:** Literary fiction, complex plots
- **Romance:** Love stories of any subgenre
- **Mystery:** Detective stories, thrillers
- **Custom:** Experimental or unique stories

**Target Word Count:**
- Novella: 20,000-50,000
- Novel: 50,000-120,000
- Epic: 120,000+

The AI will distribute scenes proportionally.

## Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Add Anthropic API key to Secrets
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

**"Error generating outline"**
- Check API key validity
- Verify Claude API access
- Check internet connection

**"Export not working"**
- PDF export requires reportlab: `pip install reportlab`
- Word export requires python-docx: `pip install python-docx`

**"Outline is too generic"**
- Provide more specific premise
- Include unique elements
- Try regenerating with different details

## Features Roadmap

- [ ] Scene card generator
- [ ] Character integration (link to Character Creator)
- [ ] Subplot tracking
- [ ] Conflict mapping
- [ ] Pacing visualization
- [ ] Collaboration features
- [ ] Version history
- [ ] Manuscript progress tracker

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Anthropic Claude 3.5 Sonnet
- **Export:** ReportLab (PDF), python-docx (Word)

## Cost Considerations

**Per Outline:**
- Claude API: ~$0.003
- Storage: Free (local/session)

Very affordable for unlimited outlines!

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

---

🦚 **Built by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
