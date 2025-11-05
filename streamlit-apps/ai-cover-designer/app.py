"""
AI Cover Designer - Rohimaya Publishing Platform
Professional book cover generation using DALL-E 3
"""

import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
from PIL import Image
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Cover Designer | Rohimaya Publishing",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rohimaya Branding CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    :root {
        --phoenix-orange: #FF8C42;
        --phoenix-gold: #FFD700;
        --peacock-teal: #4A9B9B;
        --peacock-blue-gray: #7B9AA8;
        --deep-teal: #2F5F5F;
        --midnight-navy: #1A1A2E;
        --cream: #FFF8E7;
    }

    .main {
        background-color: var(--cream);
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: var(--midnight-navy);
    }

    p, label, .stMarkdown {
        font-family: 'Inter', sans-serif;
    }

    .stButton > button {
        background-color: var(--phoenix-orange);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #FF6B1A;
        box-shadow: 0 4px 12px rgba(255, 140, 66, 0.3);
    }

    .cover-preview {
        border: 4px solid var(--peacock-teal);
        border-radius: 12px;
        padding: 1rem;
        background: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }

    .info-box {
        background: linear-gradient(135deg, var(--peacock-teal), var(--peacock-blue-gray));
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }

    .stSelectbox label, .stTextArea label, .stTextInput label {
        color: var(--midnight-navy);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🎨 AI Cover Designer</h1>
    <p style='font-size: 1.2rem; color: var(--peacock-teal);'>Create stunning book covers with AI-powered design</p>
    <p style='color: var(--peacock-blue-gray);'>Powered by DALL-E 3 | Rohimaya Publishing Platform</p>
</div>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    """Initialize and cache OpenAI client"""
    try:
        api_key = st.secrets["openai"]["api_key"]
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"⚠️ Error loading OpenAI API key: {str(e)}")
        st.info("Please configure your OpenAI API key in `.streamlit/secrets.toml`")
        return None

# Genre and style options
GENRES = [
    "Fiction",
    "Non-Fiction",
    "Mystery/Thriller",
    "Romance",
    "Fantasy",
    "Science Fiction",
    "Horror",
    "Historical Fiction",
    "Biography/Memoir",
    "Self-Help",
    "Business",
    "Children's",
    "Young Adult",
    "Poetry"
]

ART_STYLES = [
    "Realistic",
    "Oil Painting",
    "Watercolor",
    "Minimalist",
    "Typography-focused",
    "Illustrated",
    "Photographic",
    "Abstract",
    "Vintage",
    "Modern/Contemporary",
    "Hand-drawn"
]

IMAGE_SIZES = {
    "Standard (1024x1024)": "1024x1024",
    "Portrait (1024x1792)": "1024x1792",
    "Landscape (1792x1024)": "1792x1024"
}

def generate_cover_prompt(title, author, genre, style, mood, additional_details):
    """Generate optimized DALL-E 3 prompt for book cover"""
    prompt = f"Professional book cover design for '{title}' by {author}. "
    prompt += f"Genre: {genre}. "
    prompt += f"Art style: {style}. "

    if mood:
        prompt += f"Mood/atmosphere: {mood}. "

    if additional_details:
        prompt += f"Additional elements: {additional_details}. "

    # Add quality guidelines
    prompt += "The design should be eye-catching, professional, and suitable for commercial publishing. "
    prompt += "Include clear space for title and author name. "
    prompt += "High quality, detailed artwork with strong visual impact."

    return prompt

def generate_cover_image(client, prompt, size, quality="hd"):
    """Generate cover image using DALL-E 3"""
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        image_url = response.data[0].url
        return image_url, response.data[0].revised_prompt
    except Exception as e:
        raise Exception(f"Error generating image: {str(e)}")

def download_image(url):
    """Download image from URL and return PIL Image"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        raise Exception(f"Error downloading image: {str(e)}")

def image_to_bytes(img, format='PNG'):
    """Convert PIL Image to bytes"""
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

# Sidebar - Input Form
with st.sidebar:
    st.markdown("### 📝 Book Details")

    book_title = st.text_input(
        "Book Title *",
        placeholder="Enter your book title",
        help="The title of your book"
    )

    author_name = st.text_input(
        "Author Name *",
        placeholder="Enter author name",
        help="Author's name for the cover"
    )

    st.markdown("### 🎭 Design Preferences")

    genre = st.selectbox(
        "Genre *",
        options=GENRES,
        help="Select the primary genre of your book"
    )

    art_style = st.selectbox(
        "Art Style *",
        options=ART_STYLES,
        help="Choose the artistic style for your cover"
    )

    mood = st.text_input(
        "Mood/Atmosphere",
        placeholder="e.g., mysterious, uplifting, dark",
        help="Optional: Describe the mood you want to convey"
    )

    additional_details = st.text_area(
        "Additional Details",
        placeholder="Specific elements, colors, symbols, or themes...",
        help="Optional: Any specific details you want in the design",
        height=100
    )

    st.markdown("### 🖼️ Image Settings")

    image_size_label = st.selectbox(
        "Image Size",
        options=list(IMAGE_SIZES.keys()),
        index=1,  # Default to Portrait
        help="Choose the aspect ratio for your cover"
    )
    image_size = IMAGE_SIZES[image_size_label]

    quality = st.radio(
        "Quality",
        options=["HD", "Standard"],
        index=0,
        help="HD provides better quality but takes longer"
    )

    st.markdown("---")

    generate_button = st.button(
        "🎨 Generate Cover",
        use_container_width=True,
        type="primary"
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    <div class='info-box'>
        <h4 style='color: white; margin-top: 0;'>Create Your Perfect Cover in 3 Steps:</h4>
        <ol style='color: white;'>
            <li><strong>Enter Details:</strong> Fill in your book title, author, and genre</li>
            <li><strong>Customize Design:</strong> Choose art style, mood, and specific elements</li>
            <li><strong>Generate & Download:</strong> AI creates your cover in seconds</li>
        </ol>
        <p style='margin-bottom: 0;'><strong>💡 Pro Tip:</strong> Be specific with your mood and additional details for best results!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💰 Pricing")
    st.info("""
    **DALL-E 3 Pricing:**
    - Standard Quality: ~$0.04 per image
    - HD Quality: ~$0.08 per image

    Generate multiple variations to find your perfect cover!
    """)

with col2:
    st.markdown("### 🎨 Your Generated Cover")

    # Initialize session state
    if 'generated_image_url' not in st.session_state:
        st.session_state.generated_image_url = None
    if 'revised_prompt' not in st.session_state:
        st.session_state.revised_prompt = None
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None

# Handle generation
if generate_button:
    # Validation
    if not book_title or not author_name:
        st.error("⚠️ Please fill in both Book Title and Author Name")
    else:
        client = get_openai_client()

        if client is None:
            st.error("❌ Cannot generate cover without OpenAI API key. Please configure secrets.toml")
        else:
            with st.spinner("🎨 Creating your cover design... This may take 10-30 seconds..."):
                try:
                    # Generate prompt
                    prompt = generate_cover_prompt(
                        book_title, author_name, genre, art_style, mood, additional_details
                    )

                    # Generate image
                    quality_setting = "hd" if quality == "HD" else "standard"
                    image_url, revised_prompt = generate_cover_image(
                        client, prompt, image_size, quality_setting
                    )

                    # Download image
                    img = download_image(image_url)

                    # Store in session state
                    st.session_state.generated_image_url = image_url
                    st.session_state.revised_prompt = revised_prompt
                    st.session_state.generated_image = img

                    st.success("✅ Cover generated successfully!")
                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Try simplifying your prompt or checking your API key")

# Display generated cover
if st.session_state.generated_image is not None:
    with col2:
        st.markdown("<div class='cover-preview'>", unsafe_allow_html=True)
        st.image(st.session_state.generated_image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download buttons
        st.markdown("### 💾 Download Options")

        col_dl1, col_dl2 = st.columns(2)

        with col_dl1:
            # PNG download
            png_bytes = image_to_bytes(st.session_state.generated_image, 'PNG')
            st.download_button(
                label="📥 Download PNG",
                data=png_bytes,
                file_name=f"{book_title.replace(' ', '_')}_cover.png",
                mime="image/png",
                use_container_width=True
            )

        with col_dl2:
            # JPEG download
            jpeg_bytes = image_to_bytes(st.session_state.generated_image, 'JPEG')
            st.download_button(
                label="📥 Download JPEG",
                data=jpeg_bytes,
                file_name=f"{book_title.replace(' ', '_')}_cover.jpg",
                mime="image/jpeg",
                use_container_width=True
            )

        # Show revised prompt
        with st.expander("🔍 View AI-Enhanced Prompt"):
            st.markdown("**Original Request:**")
            original_prompt = generate_cover_prompt(
                book_title, author_name, genre, art_style, mood, additional_details
            )
            st.text(original_prompt)

            st.markdown("**AI-Enhanced Prompt:**")
            st.text(st.session_state.revised_prompt)
            st.caption("DALL-E 3 optimizes prompts for better results")

        # Metadata
        with st.expander("📊 Image Details"):
            st.markdown(f"""
            - **Size:** {image_size}
            - **Quality:** {quality}
            - **Genre:** {genre}
            - **Style:** {art_style}
            - **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: var(--peacock-blue-gray);'>
    <p><strong>Rohimaya Publishing Platform</strong></p>
    <p>Where creativity meets innovation | AI-powered publishing tools</p>
    <p style='font-size: 0.9rem;'>🦚 Rise from the ashes, soar with grace</p>
</div>
""", unsafe_allow_html=True)
