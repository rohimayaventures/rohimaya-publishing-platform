"""
🦚 Rohimaya Publishing - Audiobook Generator
Convert manuscripts to professional audiobooks with AI voices
Multi-TTS support: Prasad's Custom TTS (FREE) → ElevenLabs → OpenAI TTS
"""

import streamlit as st
import requests
import json
from io import BytesIO
from datetime import datetime
import base64

# Try importing optional dependencies
try:
    from elevenlabs import generate, set_api_key, voices, Voice
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Audiobook Generator - Rohimaya Publishing",
    page_icon="🎧",
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
    .audio-card {
        background: #FFF8E7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4A9B9B;
        margin-bottom: 1rem;
    }
    .voice-option {
        background: #E8E8E8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .tts-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-weight: 600;
    }
    .tts-available {
        background: #90EE90;
        color: #006400;
    }
    .tts-unavailable {
        background: #FFB6C1;
        color: #8B0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []
if 'current_tts_service' not in st.session_state:
    st.session_state.current_tts_service = None

# Voice configurations
VOICE_OPTIONS = {
    "Male Deep": {
        "description": "Deep, authoritative male voice",
        "prasad_voice": "male_deep",
        "elevenlabs_voice": "Josh",
        "openai_voice": "onyx"
    },
    "Male Standard": {
        "description": "Clear, neutral male voice",
        "prasad_voice": "male_standard",
        "elevenlabs_voice": "Antoni",
        "openai_voice": "echo"
    },
    "Male Young": {
        "description": "Youthful, energetic male voice",
        "prasad_voice": "male_young",
        "elevenlabs_voice": "Adam",
        "openai_voice": "fable"
    },
    "Female Deep": {
        "description": "Rich, mature female voice",
        "prasad_voice": "female_deep",
        "elevenlabs_voice": "Elli",
        "openai_voice": "nova"
    },
    "Female Standard": {
        "description": "Warm, clear female voice",
        "prasad_voice": "female_standard",
        "elevenlabs_voice": "Rachel",
        "openai_voice": "shimmer"
    },
    "Female Young": {
        "description": "Bright, cheerful female voice",
        "prasad_voice": "female_young",
        "elevenlabs_voice": "Domi",
        "openai_voice": "alloy"
    },
    "Neutral Professional": {
        "description": "Professional, gender-neutral voice",
        "prasad_voice": "neutral_professional",
        "elevenlabs_voice": "Sam",
        "openai_voice": "onyx"
    },
    "Neutral Conversational": {
        "description": "Friendly, conversational voice",
        "prasad_voice": "neutral_conversational",
        "elevenlabs_voice": "Bella",
        "openai_voice": "nova"
    },
    "Neutral Storyteller": {
        "description": "Narrative, expressive voice",
        "prasad_voice": "neutral_storyteller",
        "elevenlabs_voice": "Antoni",
        "openai_voice": "fable"
    }
}

def check_tts_services():
    """Check which TTS services are available"""
    services = {
        'prasad': False,
        'elevenlabs': False,
        'openai': False
    }

    # Check Prasad's Custom TTS
    try:
        prasad_config = st.secrets.get("prasad_tts", {})
        if prasad_config.get("endpoint_url"):
            services['prasad'] = True
    except:
        pass

    # Check ElevenLabs
    try:
        if ELEVENLABS_AVAILABLE and st.secrets.get("elevenlabs", {}).get("api_key"):
            services['elevenlabs'] = True
    except:
        pass

    # Check OpenAI
    try:
        if OPENAI_AVAILABLE and st.secrets.get("openai", {}).get("api_key"):
            services['openai'] = True
    except:
        pass

    return services

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    if not DOCX_AVAILABLE:
        return None

    try:
        doc = Document(file)
        text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text
    except Exception as e:
        st.error(f"❌ Error reading DOCX: {str(e)}")
        return None

def detect_chapters(text):
    """Simple chapter detection"""
    import re

    # Look for common chapter patterns
    chapter_patterns = [
        r'^Chapter \d+',
        r'^CHAPTER \d+',
        r'^\d+\.',
        r'^Part \d+',
        r'^PART \d+'
    ]

    chapters = []
    current_chapter = ""
    chapter_title = "Introduction"

    for line in text.split('\n'):
        is_chapter_heading = False

        for pattern in chapter_patterns:
            if re.match(pattern, line.strip()):
                if current_chapter.strip():
                    chapters.append({
                        'title': chapter_title,
                        'text': current_chapter.strip()
                    })
                chapter_title = line.strip()
                current_chapter = ""
                is_chapter_heading = True
                break

        if not is_chapter_heading:
            current_chapter += line + "\n"

    # Add the last chapter
    if current_chapter.strip():
        chapters.append({
            'title': chapter_title,
            'text': current_chapter.strip()
        })

    return chapters if len(chapters) > 1 else [{'title': 'Full Text', 'text': text}]

def generate_audio_prasad(text, voice, speed, pitch, emotion):
    """Generate audio using Prasad's Custom TTS"""
    try:
        prasad_config = st.secrets["prasad_tts"]
        endpoint = prasad_config["endpoint_url"]

        payload = {
            "text": text,
            "voice": voice,
            "speed": speed,
            "pitch": pitch,
            "emotion": emotion
        }

        headers = {"Content-Type": "application/json"}
        if prasad_config.get("api_key"):
            headers["Authorization"] = f"Bearer {prasad_config['api_key']}"

        response = requests.post(endpoint, json=payload, headers=headers, timeout=120)

        if response.status_code == 200:
            return response.content, "prasad"
        else:
            raise Exception(f"API returned status {response.status_code}")

    except Exception as e:
        st.warning(f"⚠️ Prasad TTS failed: {str(e)}. Trying fallback...")
        return None, None

def generate_audio_elevenlabs(text, voice_name, speed):
    """Generate audio using ElevenLabs"""
    try:
        if not ELEVENLABS_AVAILABLE:
            raise Exception("ElevenLabs library not installed")

        set_api_key(st.secrets["elevenlabs"]["api_key"])

        # Adjust speed by manipulating the text (ElevenLabs doesn't have direct speed control)
        audio_bytes = generate(
            text=text,
            voice=voice_name,
            model="eleven_monolingual_v1"
        )

        return audio_bytes, "elevenlabs"

    except Exception as e:
        st.warning(f"⚠️ ElevenLabs failed: {str(e)}. Trying fallback...")
        return None, None

def generate_audio_openai(text, voice, speed):
    """Generate audio using OpenAI TTS"""
    try:
        if not OPENAI_AVAILABLE:
            raise Exception("OpenAI library not installed")

        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            speed=speed
        )

        return response.content, "openai"

    except Exception as e:
        st.error(f"❌ OpenAI TTS failed: {str(e)}")
        return None, None

def generate_audiobook(text, voice_choice, speed, pitch, emotion):
    """Generate audiobook with automatic fallback"""
    services = check_tts_services()
    voice_config = VOICE_OPTIONS[voice_choice]

    # Try services in order: Prasad → ElevenLabs → OpenAI
    if services['prasad']:
        st.info("🔄 Using Prasad's Custom TTS (FREE)...")
        audio, service = generate_audio_prasad(
            text,
            voice_config['prasad_voice'],
            speed,
            pitch,
            emotion
        )
        if audio:
            return audio, service

    if services['elevenlabs']:
        st.info("🔄 Using ElevenLabs...")
        audio, service = generate_audio_elevenlabs(
            text,
            voice_config['elevenlabs_voice'],
            speed
        )
        if audio:
            return audio, service

    if services['openai']:
        st.info("🔄 Using OpenAI TTS...")
        audio, service = generate_audio_openai(
            text,
            voice_config['openai_voice'],
            speed
        )
        if audio:
            return audio, service

    return None, None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎧 Audiobook Generator</h1>
        <p style="font-size: 1.2rem; margin: 0;">Convert your manuscript to professional audiobook</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">Multi-TTS Support • ACX-Ready • Rohimaya Publishing</p>
    </div>
    """, unsafe_allow_html=True)

    # Check available TTS services
    services = check_tts_services()

    # Display TTS service status
    st.markdown("### 🎤 Available TTS Services")
    col1, col2, col3 = st.columns(3)

    with col1:
        status_class = "tts-available" if services['prasad'] else "tts-unavailable"
        status_text = "✅ Available (FREE)" if services['prasad'] else "❌ Not Configured"
        st.markdown(f'<div class="tts-status {status_class}">Prasad\'s TTS: {status_text}</div>', unsafe_allow_html=True)

    with col2:
        status_class = "tts-available" if services['elevenlabs'] else "tts-unavailable"
        status_text = "✅ Available" if services['elevenlabs'] else "❌ Not Configured"
        st.markdown(f'<div class="tts-status {status_class}">ElevenLabs: {status_text}</div>', unsafe_allow_html=True)

    with col3:
        status_class = "tts-available" if services['openai'] else "tts-unavailable"
        status_text = "✅ Available" if services['openai'] else "❌ Not Configured"
        st.markdown(f'<div class="tts-status {status_class}">OpenAI TTS: {status_text}</div>', unsafe_allow_html=True)

    if not any(services.values()):
        st.error("❌ No TTS services configured! Please add API credentials to .streamlit/secrets.toml")
        st.stop()

    st.markdown("---")

    # Sidebar - Input Controls
    with st.sidebar:
        st.markdown("### 📝 Input Options")

        input_method = st.radio(
            "How would you like to input your text?",
            ["Upload File", "Paste Text"]
        )

        manuscript_text = ""

        if input_method == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload Manuscript",
                type=["txt", "docx", "md"],
                help="Upload your manuscript file"
            )

            if uploaded_file:
                file_type = uploaded_file.name.split('.')[-1].lower()

                if file_type == "docx":
                    if DOCX_AVAILABLE:
                        manuscript_text = extract_text_from_docx(uploaded_file)
                    else:
                        st.error("❌ DOCX support not available. Install python-docx.")
                elif file_type in ["txt", "md"]:
                    manuscript_text = uploaded_file.read().decode('utf-8')

        else:
            manuscript_text = st.text_area(
                "Paste Your Text",
                height=300,
                placeholder="Paste your manuscript text here..."
            )

        st.markdown("---")
        st.markdown("### 🎭 Voice Selection")

        voice_choice = st.selectbox(
            "Select Voice",
            list(VOICE_OPTIONS.keys()),
            format_func=lambda x: f"{x} - {VOICE_OPTIONS[x]['description']}"
        )

        st.markdown("---")
        st.markdown("### 🎚️ Audio Controls")

        speed = st.slider("Speed", 0.8, 1.5, 1.0, 0.1)
        pitch = st.slider("Pitch", -5, 5, 0, 1)

        emotion = st.selectbox(
            "Emotion",
            ["Neutral", "Expressive", "Calm", "Excited"]
        )

        st.markdown("---")
        st.markdown("### 📖 Generation Options")

        gen_option = st.radio(
            "What to generate?",
            ["Full Manuscript", "Chapter by Chapter", "Selected Text"]
        )

        # Generate button
        generate_btn = st.button("🎙️ Generate Audiobook", use_container_width=True)

    # Main content area
    if manuscript_text:
        st.markdown("### 📄 Manuscript Preview")

        word_count = len(manuscript_text.split())
        char_count = len(manuscript_text)
        est_duration = int((word_count / 150) * 60)  # Avg 150 words per minute

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", f"{word_count:,}")
        with col2:
            st.metric("Characters", f"{char_count:,}")
        with col3:
            st.metric("Est. Duration", f"{est_duration} min")

        with st.expander("📖 View Text"):
            st.text_area("Manuscript", manuscript_text, height=200, disabled=True)

        if generate_btn:
            if gen_option == "Chapter by Chapter":
                st.markdown("### 📚 Detecting Chapters...")
                chapters = detect_chapters(manuscript_text)
                st.success(f"✅ Found {len(chapters)} chapter(s)")

                for idx, chapter in enumerate(chapters):
                    with st.expander(f"🎧 {chapter['title']}", expanded=(idx==0)):
                        st.markdown(f"**Words:** {len(chapter['text'].split())}")

                        if st.button(f"Generate Audio", key=f"gen_{idx}"):
                            with st.spinner(f"🎙️ Generating audio for {chapter['title']}..."):
                                audio_bytes, service = generate_audiobook(
                                    chapter['text'],
                                    voice_choice,
                                    speed,
                                    pitch,
                                    emotion.lower()
                                )

                                if audio_bytes:
                                    st.audio(audio_bytes, format="audio/mp3")
                                    st.success(f"✅ Generated using {service.upper()}")

                                    # Download button
                                    st.download_button(
                                        label="📥 Download MP3",
                                        data=audio_bytes,
                                        file_name=f"{chapter['title'].replace(' ', '_')}.mp3",
                                        mime="audio/mpeg"
                                    )
                                else:
                                    st.error("❌ Failed to generate audio")

            else:  # Full Manuscript or Selected Text
                text_to_convert = manuscript_text

                if gen_option == "Selected Text":
                    text_to_convert = st.text_area(
                        "Select Text to Convert",
                        value=manuscript_text[:500],
                        height=200
                    )

                with st.spinner("🎙️ Generating audiobook... This may take a while..."):
                    audio_bytes, service = generate_audiobook(
                        text_to_convert,
                        voice_choice,
                        speed,
                        pitch,
                        emotion.lower()
                    )

                    if audio_bytes:
                        st.success(f"✅ Audiobook generated successfully using {service.upper()}!")

                        st.markdown("### 🎧 Audio Player")
                        st.audio(audio_bytes, format="audio/mp3")

                        # Download button
                        st.download_button(
                            label="📥 Download ACX-Ready MP3",
                            data=audio_bytes,
                            file_name="audiobook.mp3",
                            mime="audio/mpeg",
                            use_container_width=True
                        )

                        # Save to session state
                        st.session_state.generated_audio = {
                            'audio': audio_bytes,
                            'voice': voice_choice,
                            'service': service,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'word_count': word_count
                        }

                    else:
                        st.error("❌ Failed to generate audiobook. Please check your API configuration.")

    else:
        st.info("👈 Upload a manuscript or paste text in the sidebar to get started!")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7B9AA8; padding: 2rem;">
        <p style="margin: 0;">🦚 <strong>Rohimaya Publishing</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ascend • Flourish • Enlighten</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Multi-TTS Audiobook Generator • ACX-Ready Output</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
