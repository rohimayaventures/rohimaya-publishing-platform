"""
🦚 Rohimaya Publishing - AI Cover Designer
Generate professional book covers using DALL-E 3 AI
"""

import streamlit as st
import openai
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Cover Designer - Rohimaya Publishing",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rohimaya brand colors
BRAND_COLORS = {
    "Phoenix Orange": "#FF8C42",
    "Phoenix Gold": "#FFD700",
    "Peacock Teal": "#4A9B9B",
    "Peacock Blue-Gray": "#7B9AA8",
    "Deep Teal Green": "#2F5F5F",
    "Midnight Navy": "#1A1A2E",
    "Cream": "#FFF8E7",
    "Bronze": "#B87333",
    "Celestial Gold": "#F4C542",
    "Silver-White": "#E8E8E8"
}

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
    .cover-card {
        background: #FFF8E7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4A9B9B;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #1A1A2E;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'current_cover' not in st.session_state:
    st.session_state.current_cover = None

def initialize_openai():
    """Initialize OpenAI client"""
    try:
        api_key = st.secrets.get("openai", {}).get("api_key", "")
        if not api_key:
            st.warning("⚠️ OpenAI API key not configured. Please add it to .streamlit/secrets.toml")
            return None
        openai.api_key = api_key
        return True
    except Exception as e:
        st.error(f"❌ Error initializing OpenAI: {str(e)}")
        return None

def generate_cover_prompt(title, author, genre, art_style, color_palette, mood, additional_elements):
    """Generate detailed DALL-E prompt from user inputs"""

    prompt = f"Book cover design for '{title}' by {author}. "
    prompt += f"Genre: {genre}. "
    prompt += f"Art style: {art_style}. "

    if mood:
        prompt += f"Mood and atmosphere: {mood}. "

    if color_palette != "Custom":
        prompt += f"Color palette: {color_palette} dominant colors. "

    if additional_elements:
        prompt += f"Include these elements: {additional_elements}. "

    prompt += "Professional book cover design, high quality, detailed, eye-catching, suitable for publishing. "
    prompt += "No text or typography on the cover - pure visual imagery only."

    return prompt

def generate_cover_image(prompt):
    """Generate cover using DALL-E 3"""
    try:
        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

        with st.spinner("🎨 Creating your book cover with AI magic..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",  # Portrait orientation for book covers
                quality="standard",
                n=1
            )

        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Download the image
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        return image, revised_prompt

    except Exception as e:
        st.error(f"❌ Error generating cover: {str(e)}")
        return None, None

def add_text_overlay(image, title, author, title_font_size=80, author_font_size=40):
    """Add title and author text to cover image"""
    try:
        # Create a copy to avoid modifying original
        img_with_text = image.copy()
        draw = ImageDraw.Draw(img_with_text)

        # Calculate positions (centered at top and bottom)
        img_width, img_height = img_with_text.size

        # Note: Using default font since custom fonts may not be available
        # In production, you'd load custom fonts

        # Add title at top (white text with black shadow for readability)
        title_y = 100
        # Shadow
        draw.text((img_width//2 + 2, title_y + 2), title, fill="black", anchor="mm")
        # Main text
        draw.text((img_width//2, title_y), title, fill="white", anchor="mm")

        # Add author at bottom
        author_y = img_height - 150
        # Shadow
        draw.text((img_width//2 + 2, author_y + 2), f"by {author}", fill="black", anchor="mm")
        # Main text
        draw.text((img_width//2, author_y), f"by {author}", fill="white", anchor="mm")

        return img_with_text

    except Exception as e:
        st.error(f"❌ Error adding text overlay: {str(e)}")
        return image

def image_to_bytes(image, format="PNG"):
    """Convert PIL Image to bytes"""
    buf = BytesIO()
    image.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎨 AI Cover Designer</h1>
        <p style="font-size: 1.2rem; margin: 0;">Create stunning book covers with AI-powered design</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Powered by DALL-E 3 • Rohimaya Publishing</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize OpenAI
    if not initialize_openai():
        st.stop()

    # Sidebar - Input Form
    with st.sidebar:
        st.markdown("### 📝 Book Details")

        title = st.text_input("Book Title *", placeholder="Enter your book title")
        author = st.text_input("Author Name *", placeholder="Enter author name")

        st.markdown("---")
        st.markdown("### 🎭 Design Preferences")

        # Genre selection (14 options)
        genre = st.selectbox(
            "Genre *",
            [
                "Fantasy",
                "Romance",
                "Thriller",
                "Mystery",
                "Sci-Fi",
                "Horror",
                "Contemporary",
                "Historical",
                "Young Adult",
                "Literary Fiction",
                "Non-Fiction",
                "Business",
                "Self-Help",
                "Children's"
            ]
        )

        # Art style selection (11 options)
        art_style = st.selectbox(
            "Art Style *",
            [
                "Photorealistic",
                "Digital Art",
                "Oil Painting",
                "Watercolor",
                "Illustrated",
                "Minimalist",
                "Abstract",
                "Vintage",
                "Modern",
                "Dark & Moody",
                "Bright & Vibrant"
            ]
        )

        # Color palette
        color_palette = st.selectbox(
            "Color Palette",
            ["Custom", "Warm Tones", "Cool Tones", "Monochrome",
             "Vibrant", "Pastel", "Dark", "Light", "Rohimaya Brand Colors"]
        )

        mood = st.text_area(
            "Mood & Atmosphere",
            placeholder="Describe the mood (e.g., mysterious, hopeful, intense)",
            height=100
        )

        additional_elements = st.text_area(
            "Additional Elements (Optional)",
            placeholder="Specific elements to include (e.g., dragon, cityscape, forest)",
            height=100
        )

        st.markdown("---")
        st.markdown("### 🎨 Text Overlay")

        add_overlay = st.checkbox("Add title and author overlay", value=False)

        st.markdown("---")

        # Generate button
        generate_btn = st.button("✨ Generate Cover", use_container_width=True)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🖼️ Generated Cover")

        if generate_btn:
            if not title or not author:
                st.error("❌ Please fill in both Book Title and Author Name")
            else:
                # Generate the cover
                prompt = generate_cover_prompt(
                    title, author, genre, art_style,
                    color_palette, mood, additional_elements
                )

                with st.expander("🔍 View AI Prompt"):
                    st.code(prompt, language=None)

                image, revised_prompt = generate_cover_image(prompt)

                if image:
                    # Add text overlay if requested
                    if add_overlay:
                        image = add_text_overlay(image, title, author)

                    # Save to session state
                    st.session_state.current_cover = {
                        'image': image,
                        'title': title,
                        'author': author,
                        'genre': genre,
                        'art_style': art_style,
                        'prompt': prompt,
                        'revised_prompt': revised_prompt,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Add to history
                    st.session_state.generation_history.insert(0, st.session_state.current_cover)

                    st.success("✅ Cover generated successfully!")

        # Display current cover
        if st.session_state.current_cover:
            cover_data = st.session_state.current_cover

            st.image(cover_data['image'], use_container_width=True)

            st.markdown("#### 📥 Download Options")

            col_dl1, col_dl2 = st.columns(2)

            with col_dl1:
                # High-res PNG download
                png_bytes = image_to_bytes(cover_data['image'], "PNG")
                st.download_button(
                    label="📥 High-Res PNG",
                    data=png_bytes,
                    file_name=f"{cover_data['title'].replace(' ', '_')}_cover.png",
                    mime="image/png",
                    use_container_width=True
                )

            with col_dl2:
                # Web-res JPG download (resized to 600x900)
                web_image = cover_data['image'].copy()
                web_image.thumbnail((600, 900), Image.Resampling.LANCZOS)
                jpg_bytes = image_to_bytes(web_image, "JPEG")
                st.download_button(
                    label="📥 Web-Res JPG",
                    data=jpg_bytes,
                    file_name=f"{cover_data['title'].replace(' ', '_')}_cover_web.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )

            # Regenerate button
            if st.button("🔄 Regenerate with Same Settings", use_container_width=True):
                st.rerun()

        else:
            st.info("👈 Fill in the details in the sidebar and click 'Generate Cover' to create your book cover!")

    with col2:
        st.markdown("### 📚 Generation History")

        if st.session_state.generation_history:
            for idx, cover in enumerate(st.session_state.generation_history[:5]):  # Show last 5
                with st.expander(f"📖 {cover['title']} - {cover['timestamp']}"):
                    st.image(cover['image'], use_container_width=True)
                    st.markdown(f"**Author:** {cover['author']}")
                    st.markdown(f"**Genre:** {cover['genre']}")
                    st.markdown(f"**Art Style:** {cover['art_style']}")

                    if st.button(f"Load This Cover", key=f"load_{idx}"):
                        st.session_state.current_cover = cover
                        st.rerun()
        else:
            st.info("No generation history yet. Create your first cover to see it here!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7B9AA8; padding: 2rem;">
        <p style="margin: 0;">🦚 <strong>Rohimaya Publishing</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ascend • Flourish • Enlighten</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">AI Cover Designer powered by DALL-E 3</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
