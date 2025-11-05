"""
🦚 Rohimaya Publishing - Marketing Copy Generator
AI-powered marketing content for books: blurbs, social posts, emails, ads, and press materials
"""

import streamlit as st
import anthropic
import json
from datetime import datetime
from io import BytesIO

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Marketing Copy Generator - Rohimaya Publishing",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4A9B9B 0%, #FF8C42 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #FF8C42;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FFD700;
        color: #1A1A2E;
        transform: translateY(-2px);
    }
    .copy-card {
        background: #FFF8E7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4A9B9B;
        margin-bottom: 1rem;
    }
    .copy-header {
        background: #4A9B9B;
        color: white;
        padding: 0.75rem;
        border-radius: 5px;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_copy' not in st.session_state:
    st.session_state.generated_copy = {}

def initialize_anthropic():
    """Initialize Anthropic client"""
    try:
        api_key = st.secrets.get("anthropic", {}).get("api_key", "")
        if not api_key:
            st.warning("⚠️ Anthropic API key not configured. Please add it to .streamlit/secrets.toml")
            return None
        return anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing Anthropic: {str(e)}")
        return None

def generate_copy(client, content_type, book_info, tone="professional"):
    """Generate marketing copy using Claude"""

    prompts = {
        # Book Blurbs
        "blurb_25": f"""Write a 25-word book blurb for Twitter/X.

Book Title: {book_info['title']}
Author: {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create a compelling 25-word hook. Focus on intrigue and the core conflict. Make readers want to know more.""",

        "blurb_50": f"""Write a 50-word book blurb for social media.

Book Title: {book_info['title']}
Author: {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create an engaging 50-word description. Include the protagonist, the conflict, and what's at stake.""",

        "blurb_150": f"""Write a 150-word back cover blurb.

Book Title: {book_info['title']}
Author: {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}
Target Audience: {book_info.get('audience', 'General readers')}

Create a compelling back cover description that hooks readers and makes them want to buy. Include character intro, conflict, stakes, and a cliffhanger ending.""",

        "blurb_300": f"""Write a 300-word Amazon book description.

Book Title: {book_info['title']}
Author: {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}
Target Audience: {book_info.get('audience', 'General readers')}
Key Themes: {book_info.get('themes', 'N/A')}

Create a detailed Amazon description with:
- Attention-grabbing opening
- Character introduction
- Plot setup and conflict
- Stakes and tension
- Call-to-action ending
- Use formatting (bold, italics) where appropriate""",

        # Social Media Posts
        "twitter": f"""Write 3 variations of Twitter/X posts (280 characters max) for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create engaging tweets with:
- Hook in first line
- Relevant hashtags
- Call-to-action
- Variety in approach (different angles)

Tone: {tone}""",

        "instagram": f"""Write 3 Instagram caption variations for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

For each caption include:
- Compelling story hook
- Emoji usage (relevant to genre)
- 10-15 relevant hashtags
- Call-to-action (link in bio)
- Engaging question to boost comments

Tone: {tone}""",

        "facebook": f"""Write 3 Facebook post variations for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create longer-form posts (300-400 words) with:
- Personal storytelling angle
- Book highlights
- Reader benefits
- Call-to-action
- Engagement prompts

Tone: {tone}""",

        "linkedin": f"""Write 3 professional LinkedIn post variations for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create professional posts highlighting:
- Professional insights or lessons
- Author expertise
- Target professional audience
- Industry relevance
- Professional call-to-action

Tone: Professional and insightful""",

        "tiktok": f"""Write 3 TikTok video script variations for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

For each script include:
- Hook (first 3 seconds)
- Key plot points or themes
- Trending sounds/effects suggestions
- Visual suggestions
- Call-to-action
- Hashtags

Keep it under 60 seconds. Make it engaging and trendy.

Tone: {tone}""",

        # Email Campaigns
        "launch_email": f"""Write a book launch announcement email.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Include:
- Attention-grabbing subject line (3 variations)
- Personal greeting
- Excitement about launch
- Book description
- Where to buy (links placeholder)
- Launch bonuses (if any)
- Call-to-action
- Author signature

Tone: {tone}""",

        "arc_request": f"""Write an ARC (Advance Review Copy) request email.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Include:
- Subject line (professional, not spammy)
- Polite introduction
- Book details
- Why their review matters
- What you're offering (free ARC)
- Review instructions
- Timeline
- Thank you

Tone: Professional and respectful""",

        "review_request": f"""Write a review request email for readers who purchased the book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}

Include:
- Friendly subject line
- Thank you for reading
- Request for honest review
- How to leave review (Amazon, Goodreads)
- Why reviews matter
- Optional: incentive mention
- Warm closing

Tone: Grateful and friendly""",

        # Ad Copy
        "amazon_ads": f"""Write Amazon Ads copy for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create 3 variations with:
- Headline (50 characters max)
- Body copy (150 characters max)
- Call-to-action

Focus on clicking through to book page.

Tone: {tone}""",

        "facebook_ads": f"""Write Facebook Ads copy for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}
Target Audience: {book_info.get('audience', 'General readers')}

Create 3 ad variations with:
- Primary text (125 characters)
- Headline (40 characters)
- Description (30 characters)
- Call-to-action

Focus on stopping scroll and generating interest.

Tone: {tone}""",

        "bookbub": f"""Write BookBub Featured Deal copy for this book.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}

Create compelling copy (200 words) that:
- Hooks readers immediately
- Highlights unique selling points
- Creates urgency for the deal
- Ends with clear CTA

Tone: {tone}""",

        # Press Materials
        "press_release": f"""Write a press release for this book launch.

Book: {book_info['title']} by {book_info['author']}
Genre: {book_info['genre']}
Description: {book_info['description']}
Comparable Titles: {book_info.get('comps', 'N/A')}

Include:
- Press release headline
- Dateline
- Lead paragraph (who, what, when, where, why)
- Book details and description
- Author bio
- Availability information
- Contact information (placeholder)
- Boilerplate about publisher

Professional press release format.

Tone: Professional and newsworthy""",

        "author_bio_short": f"""Write a short author bio (50 words) for {book_info['author']}.

Context: Promoting {book_info['title']}
Genre: {book_info['genre']}

Include:
- Name and credentials
- Writing focus or expertise
- Notable achievements (placeholder if unknown)
- Current location or status

Tone: Professional yet personable""",

        "author_bio_medium": f"""Write a medium author bio (150 words) for {book_info['author']}.

Context: Promoting {book_info['title']}
Genre: {book_info['genre']}

Include:
- Background and credentials
- Writing journey or expertise
- Previous works (placeholder if first book)
- Awards or recognition (placeholder)
- Personal touch (interests, location)
- Website/social media mention

Tone: Professional and engaging""",

        "author_bio_long": f"""Write a long author bio (300 words) for {book_info['author']}.

Context: Promoting {book_info['title']}
Genre: {book_info['genre']}

Include:
- Detailed background
- Writing journey and inspiration
- Career highlights
- This book's genesis
- Personal life (appropriate details)
- Writing philosophy or approach
- Future projects mention
- Contact/website info

Tone: Professional, personal, and compelling"""
    }

    if content_type not in prompts:
        return None

    try:
        with st.spinner(f"✨ Generating {content_type.replace('_', ' ')}..."):
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompts[content_type]
                }]
            )

        return message.content[0].text

    except Exception as e:
        st.error(f"❌ Error generating copy: {str(e)}")
        return None

def export_all_to_pdf(book_info, generated_copy):
    """Export all generated copy to PDF"""
    if not REPORTLAB_AVAILABLE:
        return None

    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#4A9B9B',
            alignment=TA_CENTER
        )

        story.append(Paragraph(f"Marketing Copy: {book_info['title']}", title_style))
        story.append(Spacer(1, 0.3*inch))

        # Book info
        story.append(Paragraph(f"<b>Author:</b> {book_info['author']}", styles['Normal']))
        story.append(Paragraph(f"<b>Genre:</b> {book_info['genre']}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Generated copy sections
        for section_name, content in generated_copy.items():
            if content:
                story.append(PageBreak())
                story.append(Paragraph(section_name.replace('_', ' ').title(), styles['Heading2']))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(content.replace('\n', '<br/>'), styles['Normal']))
                story.append(Spacer(1, 0.2*inch))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        st.error(f"❌ Error creating PDF: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📢 Marketing Copy Generator</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-powered marketing content for your book</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Blurbs • Social Posts • Emails • Ads • Press Materials • Rohimaya Publishing</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Anthropic
    client = initialize_anthropic()
    if not client:
        st.stop()

    # Sidebar - Book Info
    with st.sidebar:
        st.markdown("### 📚 Book Information")

        title = st.text_input("Book Title *", placeholder="Enter book title")
        author = st.text_input("Author Name *", placeholder="Your name")
        genre = st.selectbox(
            "Genre *",
            ["Fantasy", "Romance", "Thriller", "Mystery", "Sci-Fi", "Horror",
             "Contemporary", "Historical", "Young Adult", "Literary Fiction",
             "Non-Fiction", "Business", "Self-Help", "Children's"]
        )

        description = st.text_area(
            "Book Description *",
            height=150,
            placeholder="Brief summary of your book (2-3 paragraphs)"
        )

        audience = st.text_input(
            "Target Audience",
            placeholder="e.g., Women 25-45, YA readers, Business professionals"
        )

        themes = st.text_input(
            "Key Themes",
            placeholder="e.g., Redemption, Family, Survival"
        )

        comps = st.text_input(
            "Comparable Titles",
            placeholder="e.g., Harry Potter, Hunger Games"
        )

        st.markdown("---")

        tone = st.selectbox(
            "Overall Tone",
            ["Professional", "Casual", "Dramatic", "Humorous", "Inspirational"]
        )

        st.markdown("---")

        if st.button("🗑️ Clear All Generated Copy", use_container_width=True):
            st.session_state.generated_copy = {}
            st.rerun()

    # Main content
    if not title or not author or not description:
        st.info("👈 Please fill in the required book information in the sidebar to begin generating marketing copy.")
        st.stop()

    book_info = {
        'title': title,
        'author': author,
        'genre': genre,
        'description': description,
        'audience': audience,
        'themes': themes,
        'comps': comps
    }

    # Content type selection
    st.markdown("### 📝 Select Content Type to Generate")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Book Blurbs",
        "📱 Social Media",
        "📧 Email Campaigns",
        "📊 Ad Copy",
        "📰 Press Materials"
    ])

    with tab1:  # Book Blurbs
        st.markdown("#### Book Blurbs (4 Lengths)")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate 25-Word Blurb", use_container_width=True):
                copy = generate_copy(client, "blurb_25", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["25-Word Blurb"] = copy
                    st.rerun()

            if st.button("Generate 150-Word Blurb", use_container_width=True):
                copy = generate_copy(client, "blurb_150", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["150-Word Blurb (Back Cover)"] = copy
                    st.rerun()

        with col2:
            if st.button("Generate 50-Word Blurb", use_container_width=True):
                copy = generate_copy(client, "blurb_50", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["50-Word Blurb"] = copy
                    st.rerun()

            if st.button("Generate 300-Word Blurb", use_container_width=True):
                copy = generate_copy(client, "blurb_300", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["300-Word Blurb (Amazon)"] = copy
                    st.rerun()

    with tab2:  # Social Media
        st.markdown("#### Social Media Posts (8 Platforms)")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Twitter/X Posts", use_container_width=True):
                copy = generate_copy(client, "twitter", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Twitter/X Posts"] = copy
                    st.rerun()

            if st.button("Facebook Posts", use_container_width=True):
                copy = generate_copy(client, "facebook", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Facebook Posts"] = copy
                    st.rerun()

            if st.button("TikTok Scripts", use_container_width=True):
                copy = generate_copy(client, "tiktok", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["TikTok Scripts"] = copy
                    st.rerun()

            if st.button("Threads Posts", use_container_width=True):
                st.info("Similar to Twitter - use Twitter/X posts for Threads")

        with col2:
            if st.button("Instagram Captions", use_container_width=True):
                copy = generate_copy(client, "instagram", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Instagram Captions"] = copy
                    st.rerun()

            if st.button("LinkedIn Posts", use_container_width=True):
                copy = generate_copy(client, "linkedin", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["LinkedIn Posts"] = copy
                    st.rerun()

            if st.button("Pinterest Descriptions", use_container_width=True):
                st.info("Similar to Instagram - use Instagram captions for Pinterest")

            if st.button("Bluesky Posts", use_container_width=True):
                st.info("Similar to Twitter - use Twitter/X posts for Bluesky")

    with tab3:  # Email Campaigns
        st.markdown("#### Email Campaigns (9 Types)")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Launch Announcement", use_container_width=True):
                copy = generate_copy(client, "launch_email", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Launch Announcement Email"] = copy
                    st.rerun()

            if st.button("ARC Request Email", use_container_width=True):
                copy = generate_copy(client, "arc_request", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["ARC Request Email"] = copy
                    st.rerun()

            if st.button("Review Request", use_container_width=True):
                copy = generate_copy(client, "review_request", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Review Request Email"] = copy
                    st.rerun()

            if st.button("Newsletter Feature", use_container_width=True):
                st.info("Use Launch Announcement as template for newsletter")

            if st.button("Behind-the-Scenes", use_container_width=True):
                st.info("Customize Launch Email with personal writing stories")

        with col2:
            if st.button("Sale Announcement", use_container_width=True):
                st.info("Adapt Launch Email with sale pricing and urgency")

            if st.button("Series Announcement", use_container_width=True):
                st.info("Adapt Launch Email for series announcement")

            if st.button("Reader Engagement", use_container_width=True):
                st.info("Use Review Request template with engagement focus")

            if st.button("New Release Teaser", use_container_width=True):
                st.info("Adapt Launch Email for pre-launch teaser")

    with tab4:  # Ad Copy
        st.markdown("#### Ad Copy (7 Platforms)")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Amazon Ads", use_container_width=True):
                copy = generate_copy(client, "amazon_ads", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Amazon Ads"] = copy
                    st.rerun()

            if st.button("Facebook Ads", use_container_width=True):
                copy = generate_copy(client, "facebook_ads", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Facebook Ads"] = copy
                    st.rerun()

            if st.button("Google Ads", use_container_width=True):
                st.info("Similar to Amazon Ads - use Amazon format for Google")

            if st.button("Goodreads Giveaway", use_container_width=True):
                st.info("Use 150-word blurb for Goodreads giveaway")

        with col2:
            if st.button("BookBub Featured Deal", use_container_width=True):
                copy = generate_copy(client, "bookbub", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["BookBub Featured Deal"] = copy
                    st.rerun()

            if st.button("Instagram Ads", use_container_width=True):
                st.info("Use Facebook Ads format for Instagram")

            if st.button("TikTok Ads", use_container_width=True):
                st.info("Use TikTok Scripts from Social Media tab")

    with tab5:  # Press Materials
        st.markdown("#### Press Materials")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Press Release", use_container_width=True):
                copy = generate_copy(client, "press_release", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Press Release"] = copy
                    st.rerun()

            if st.button("Short Author Bio (50 words)", use_container_width=True):
                copy = generate_copy(client, "author_bio_short", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Author Bio - Short"] = copy
                    st.rerun()

        with col2:
            if st.button("Medium Author Bio (150 words)", use_container_width=True):
                copy = generate_copy(client, "author_bio_medium", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Author Bio - Medium"] = copy
                    st.rerun()

            if st.button("Long Author Bio (300 words)", use_container_width=True):
                copy = generate_copy(client, "author_bio_long", book_info, tone.lower())
                if copy:
                    st.session_state.generated_copy["Author Bio - Long"] = copy
                    st.rerun()

    # Display generated copy
    if st.session_state.generated_copy:
        st.markdown("---")
        st.markdown("### ✨ Generated Marketing Copy")

        for section_name, content in st.session_state.generated_copy.items():
            with st.expander(f"📄 {section_name}", expanded=True):
                st.text_area(
                    "Copy",
                    value=content,
                    height=200,
                    key=f"display_{section_name}",
                    label_visibility="collapsed"
                )

                col_copy1, col_copy2, col_copy3 = st.columns(3)

                with col_copy1:
                    st.button(
                        "📋 Copy to Clipboard",
                        key=f"copy_{section_name}",
                        use_container_width=True,
                        on_click=lambda x=content: st.write(f"Copied! (Use Ctrl+C)")
                    )

                with col_copy2:
                    st.download_button(
                        label="💾 Download TXT",
                        data=content,
                        file_name=f"{section_name.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key=f"dl_{section_name}"
                    )

                with col_copy3:
                    if st.button("🔄 Regenerate", key=f"regen_{section_name}", use_container_width=True):
                        # Find the content type key for regeneration
                        # This is simplified - in production you'd store the type
                        st.info("Click the generate button again to create a new version")

        # Export all
        st.markdown("---")
        st.markdown("### 📥 Export All")

        col_export1, col_export2 = st.columns(2)

        with col_export1:
            if REPORTLAB_AVAILABLE:
                pdf_bytes = export_all_to_pdf(book_info, st.session_state.generated_copy)
                if pdf_bytes:
                    st.download_button(
                        label="📄 Download All as PDF",
                        data=pdf_bytes,
                        file_name=f"{title.replace(' ', '_')}_marketing_copy.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.button("📄 Download All as PDF", disabled=True, use_container_width=True)
                st.caption("Install reportlab for PDF export")

        with col_export2:
            # JSON export
            json_export = {
                'book_info': book_info,
                'generated_copy': st.session_state.generated_copy,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.download_button(
                label="💾 Download All as JSON",
                data=json.dumps(json_export, indent=2),
                file_name=f"{title.replace(' ', '_')}_marketing_copy.json",
                mime="application/json",
                use_container_width=True
            )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7B9AA8; padding: 2rem;">
        <p style="margin: 0;">🦚 <strong>Rohimaya Publishing</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ascend • Flourish • Enlighten</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Marketing Copy Generator powered by Claude AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
