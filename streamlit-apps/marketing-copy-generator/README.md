# 📢 Marketing Copy Generator

AI-powered marketing content generator for books - create blurbs, social posts, emails, ads, and press materials.

## Features

### Book Blurbs (4 Lengths)

1. **25-Word Blurb** - Perfect for Twitter/X
2. **50-Word Blurb** - Social media friendly
3. **150-Word Blurb** - Back cover description
4. **300-Word Blurb** - Amazon description

### Social Media Posts (8 Platforms)

- **Twitter/X** - 280 character posts with hashtags
- **Instagram** - Captions with emojis and hashtags
- **Facebook** - Longer-form engaging posts
- **LinkedIn** - Professional content
- **TikTok** - Video scripts with hooks and trends
- **Pinterest** - Pin descriptions
- **Threads** - Conversational posts
- **Bluesky** - Casual social posts

### Email Campaigns (9 Types)

1. **Launch Announcement** - Book release email
2. **Newsletter Feature** - Feature in newsletter
3. **Sale Announcement** - Promotional pricing
4. **ARC Request** - Request advance reviews
5. **Review Request** - Ask readers for reviews
6. **Series Announcement** - New series info
7. **Behind-the-Scenes** - Author insights
8. **Reader Engagement** - Build community
9. **New Release Teaser** - Pre-launch hype

### Ad Copy (7 Platforms)

- **Amazon Ads** - Headline + body copy
- **Facebook Ads** - Primary text, headline, description
- **Google Ads** - Responsive ad copy
- **BookBub** - Featured deal description
- **Goodreads** - Giveaway copy
- **Instagram Ads** - Story and feed ads
- **TikTok Ads** - Video ad scripts

### Press Materials

- **Press Release** - Professional announcement
- **Author Bio (Short)** - 50 words
- **Author Bio (Medium)** - 150 words
- **Author Bio (Long)** - 300 words
- **Media Kit Summary** - Press materials
- **Interview Talking Points** - Media prep

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
- **Purpose:** Generate marketing copy
- **Cost:** ~$0.003 per generation

Get your API key: https://console.anthropic.com/

## Usage Guide

### Getting Started

1. **Enter Book Information:**
   - Book title (required)
   - Author name (required)
   - Genre (required)
   - Book description (required)
   - Target audience (optional)
   - Key themes (optional)
   - Comparable titles (optional)

2. **Select Tone:**
   - Professional
   - Casual
   - Dramatic
   - Humorous
   - Inspirational

3. **Generate Copy:**
   - Navigate to relevant tab
   - Click generate button
   - Review generated content
   - Copy or download

4. **Export:**
   - Individual TXT files
   - All copy as PDF
   - All copy as JSON

### Tips for Best Results

**Book Description:**
- Provide 2-3 detailed paragraphs
- Include main characters
- Mention core conflict
- Highlight what makes it unique

**Target Audience:**
- Be specific (e.g., "Women 25-45 who love romance")
- Include reading preferences
- Mention comparable book fans

**Themes:**
- List 3-5 key themes
- Include emotional elements
- Mention what readers will feel

**Comparable Titles:**
- List 2-3 similar books
- Include popular, recognizable titles
- Match genre and tone

**Tone Selection:**
- **Professional:** Business, non-fiction, serious fiction
- **Casual:** Contemporary, romance, YA
- **Dramatic:** Thriller, literary fiction, epic fantasy
- **Humorous:** Comedy, satire, light romance
- **Inspirational:** Self-help, memoir, uplifting fiction

### Content Type Strategies

**Blurbs:**
- 25-word: Hook and intrigue
- 50-word: Hook + conflict
- 150-word: Full plot tease
- 300-word: Detailed Amazon description

**Social Media:**
- Generate 3 variations
- Test different approaches
- Use platform-specific features
- Engage with questions

**Emails:**
- Personalize subject lines
- A/B test different versions
- Include clear CTAs
- Time launches strategically

**Ads:**
- Test multiple variations
- Focus on benefits, not features
- Create urgency when appropriate
- Use power words

**Press Materials:**
- Keep factual and professional
- Include all relevant details
- Proofread carefully
- Update regularly

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

**"Error generating copy"**
- Check API key validity
- Verify Claude API access
- Check internet connection
- Verify sufficient API credits

**"Copy is too generic"**
- Provide more detailed book description
- Add specific themes and audience
- Include comparable titles
- Try regenerating with different tone

**"PDF export not working"**
- Install reportlab: `pip install reportlab`
- Or use individual TXT downloads

### Quality Tips

**If generated copy is off-target:**
1. Refine book description
2. Be more specific about audience
3. Try different tone setting
4. Regenerate for variations

**If length is wrong:**
- AI tries to match requested length
- Some variation is normal
- Edit as needed for exact requirements

**If style doesn't match:**
- Adjust tone setting
- Modify book description focus
- Try regenerating multiple times

## Features Roadmap

- [ ] A/B testing suggestions
- [ ] SEO keyword integration
- [ ] Hashtag research
- [ ] Trending topic integration
- [ ] Competitor analysis
- [ ] Performance tracking
- [ ] Content calendar
- [ ] Multi-book campaign support

## Tech Stack

- **Frontend:** Streamlit
- **AI Model:** Anthropic Claude 3.5 Sonnet
- **Export:** ReportLab (PDF - optional)

## Cost Considerations

**Per Generation:**
- Single content piece: ~$0.003
- Full campaign (20+ pieces): ~$0.06
- Very affordable for comprehensive marketing

**Optimization:**
- Generate what you need
- Save JSON for backup
- Regenerate as needed
- No storage costs (local/session)

## Marketing Strategy

### Launch Strategy

1. **Pre-Launch (4 weeks before):**
   - Generate ARC request emails
   - Create social media teasers
   - Prepare press release

2. **Launch Week:**
   - Send launch announcement email
   - Post to all social platforms
   - Run launch week ads
   - Distribute press release

3. **Post-Launch (Ongoing):**
   - Request reviews via email
   - Continue social media posts
   - Run targeted ads
   - Engage with readers

### Content Calendar

- **Daily:** Social media posts
- **Weekly:** Newsletter/blog content
- **Monthly:** Email campaign
- **As needed:** Ad copy, press materials

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

---

🦚 **Built by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
