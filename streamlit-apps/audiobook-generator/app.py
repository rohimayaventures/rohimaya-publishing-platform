"""
Audiobook Generator - Rohimaya Publishing Platform
Convert manuscripts to professional audiobooks using AI text-to-speech
"""

import streamlit as st
from openai import OpenAI
import io
import re
from datetime import datetime
from pydub import AudioSegment
import tempfile
import os

# Page configuration
st.set_page_config(
    page_title="Audiobook Generator | Rohimaya Publishing",
    page_icon="🎙️",
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

    .info-box {
        background: linear-gradient(135deg, var(--peacock-teal), var(--peacock-blue-gray));
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }

    .chapter-box {
        background: white;
        border-left: 4px solid var(--peacock-teal);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }

    .cost-estimate {
        background: linear-gradient(135deg, var(--phoenix-orange), var(--phoenix-gold));
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }

    .stSelectbox label, .stTextArea label, .stTextInput label {
        color: var(--midnight-navy);
        font-weight: 600;
    }

    .progress-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid var(--peacock-teal);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='font-size: 3rem; margin-bottom: 0.5rem;'>🎙️ Audiobook Generator</h1>
    <p style='font-size: 1.2rem; color: var(--peacock-teal);'>Transform your manuscript into professional audiobooks</p>
    <p style='color: var(--peacock-blue-gray);'>Powered by OpenAI TTS | Rohimaya Publishing Platform</p>
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

# Voice options for OpenAI TTS
OPENAI_VOICES = {
    "Alloy": {"id": "alloy", "description": "Neutral, balanced voice - great for narration"},
    "Echo": {"id": "echo", "description": "Male, clear and authoritative"},
    "Fable": {"id": "fable", "description": "British accent, expressive"},
    "Onyx": {"id": "onyx", "description": "Deep male voice, dramatic"},
    "Nova": {"id": "nova", "description": "Female, warm and friendly"},
    "Shimmer": {"id": "shimmer", "description": "Female, soft and gentle"}
}

TTS_MODELS = {
    "TTS-1": {"id": "tts-1", "quality": "Standard", "speed": "Fast", "cost_per_char": 0.000015},
    "TTS-1-HD": {"id": "tts-1-hd", "quality": "High Definition", "speed": "Slower", "cost_per_char": 0.000030}
}

AUDIO_FORMATS = {
    "MP3 (ACX-Ready)": {"format": "mp3", "bitrate": "192k"},
    "MP3 (High Quality)": {"format": "mp3", "bitrate": "320k"},
    "AAC": {"format": "aac", "bitrate": "256k"},
    "OPUS": {"format": "opus", "bitrate": "128k"}
}

def split_into_chapters(text, auto_detect=True):
    """Split text into chapters"""
    if auto_detect:
        # Look for common chapter markers
        chapter_pattern = r'(?:^|\n)(?:Chapter|CHAPTER|Ch\.|ch\.)\s*\d+|(?:^|\n)#{1,3}\s+.+|(?:^|\n)\*\*\*.+\*\*\*'
        chapters = re.split(chapter_pattern, text)
        chapters = [ch.strip() for ch in chapters if ch.strip()]

        if len(chapters) <= 1:
            # No chapters found, return whole text
            return [{"title": "Full Text", "content": text}]

        # Extract chapter titles
        chapter_titles = re.findall(chapter_pattern, text)
        result = []
        for i, content in enumerate(chapters):
            if i < len(chapter_titles):
                title = chapter_titles[i].strip()
            else:
                title = f"Chapter {i+1}"
            result.append({"title": title, "content": content})
        return result
    else:
        return [{"title": "Full Text", "content": text}]

def split_text_into_chunks(text, max_chars=4000):
    """Split text into chunks for TTS processing"""
    # OpenAI TTS has a limit, split by sentences to stay under
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def estimate_cost(text, model_key):
    """Estimate cost for TTS generation"""
    char_count = len(text)
    cost_per_char = TTS_MODELS[model_key]["cost_per_char"]
    estimated_cost = char_count * cost_per_char
    return estimated_cost, char_count

def generate_speech_openai(client, text, voice, model):
    """Generate speech using OpenAI TTS"""
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            response_format="mp3"
        )
        return response.content
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")

def combine_audio_chunks(audio_chunks):
    """Combine multiple audio chunks into single file"""
    combined = AudioSegment.empty()

    for chunk in audio_chunks:
        audio = AudioSegment.from_mp3(io.BytesIO(chunk))
        combined += audio

    return combined

def export_audio(audio_segment, format_settings):
    """Export audio with specified format"""
    output = io.BytesIO()
    audio_segment.export(
        output,
        format=format_settings["format"],
        bitrate=format_settings["bitrate"]
    )
    output.seek(0)
    return output.getvalue()

# Sidebar - Configuration
with st.sidebar:
    st.markdown("### 🎙️ Voice Settings")

    tts_provider = st.selectbox(
        "TTS Provider",
        options=["OpenAI TTS", "Inworld AI (Coming Soon)", "ElevenLabs (Coming Soon)"],
        help="Text-to-speech provider"
    )

    if tts_provider == "OpenAI TTS":
        voice_name = st.selectbox(
            "Voice",
            options=list(OPENAI_VOICES.keys()),
            help="Select the narrator voice"
        )
        st.caption(f"_{OPENAI_VOICES[voice_name]['description']}_")

        model_name = st.selectbox(
            "Model Quality",
            options=list(TTS_MODELS.keys()),
            help="TTS-1-HD provides better quality but costs 2x more"
        )
        st.caption(f"Quality: {TTS_MODELS[model_name]['quality']} | Speed: {TTS_MODELS[model_name]['speed']}")
    else:
        st.info("🚧 This provider is planned for future releases. OpenAI TTS is currently the most reliable option.")

    st.markdown("### 📄 Processing Options")

    auto_detect_chapters = st.checkbox(
        "Auto-detect Chapters",
        value=True,
        help="Automatically split text into chapters"
    )

    output_format = st.selectbox(
        "Output Format",
        options=list(AUDIO_FORMATS.keys()),
        help="Audio export format and quality"
    )

    st.markdown("### ℹ️ ACX Requirements")
    st.info("""
    **ACX-Ready Settings:**
    - Format: MP3
    - Bitrate: 192 kbps CBR
    - Sample rate: 44.1 kHz
    - Mono or Stereo
    - Peak values: -3dB to -23dB

    Use "MP3 (ACX-Ready)" format for Audible submission.
    """)

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Input Text", "🎧 Generate Audio", "💰 Cost Calculator"])

with tab1:
    st.markdown("### 📖 Enter Your Manuscript")

    col1, col2 = st.columns([2, 1])

    with col1:
        manuscript_text = st.text_area(
            "Manuscript Text",
            height=400,
            placeholder="Paste your manuscript text here...\n\nTip: Include chapter markers like 'Chapter 1' or '### Chapter Title' for automatic chapter detection.",
            help="Paste the text you want to convert to audiobook"
        )

        char_count = len(manuscript_text)
        word_count = len(manuscript_text.split())
        st.caption(f"📊 {char_count:,} characters | {word_count:,} words | ~{word_count/200:.1f} minutes estimated")

    with col2:
        st.markdown("### 📋 Quick Stats")
        if manuscript_text:
            chapters = split_into_chapters(manuscript_text, auto_detect_chapters)

            st.metric("Chapters Detected", len(chapters))
            st.metric("Total Characters", f"{char_count:,}")
            st.metric("Total Words", f"{word_count:,}")

            # Estimate duration (average speaking rate: 200 words/min)
            duration_min = word_count / 200
            st.metric("Estimated Duration", f"{duration_min:.1f} min")

            if tts_provider == "OpenAI TTS":
                cost, _ = estimate_cost(manuscript_text, model_name)
                st.markdown(f"""
                <div class='cost-estimate'>
                    💵 Estimated Cost<br/>
                    ${cost:.2f}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Enter text to see statistics")

with tab2:
    st.markdown("### 🎧 Audio Generation")

    if not manuscript_text:
        st.warning("⚠️ Please enter manuscript text in the 'Input Text' tab first")
    else:
        # Preview chapters
        st.markdown("### 📚 Detected Chapters")
        chapters = split_into_chapters(manuscript_text, auto_detect_chapters)

        for i, chapter in enumerate(chapters):
            with st.expander(f"{chapter['title']} ({len(chapter['content'])} chars)"):
                st.text(chapter['content'][:500] + "..." if len(chapter['content']) > 500 else chapter['content'])

        st.markdown("---")

        # Generate button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_button = st.button(
                "🎙️ Generate Audiobook",
                use_container_width=True,
                type="primary",
                disabled=(tts_provider != "OpenAI TTS")
            )

        if generate_button:
            if tts_provider != "OpenAI TTS":
                st.error("❌ Only OpenAI TTS is currently available")
            else:
                client = get_openai_client()

                if client is None:
                    st.error("❌ Cannot generate audio without OpenAI API key. Please configure secrets.toml")
                else:
                    # Generate audio for each chapter
                    all_audio_files = []
                    total_chapters = len(chapters)

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        for chapter_idx, chapter in enumerate(chapters):
                            status_text.markdown(f"### 🎙️ Processing: {chapter['title']}")

                            # Split chapter into chunks
                            chunks = split_text_into_chunks(chapter['content'])
                            chapter_audio_chunks = []

                            # Progress for chunks within chapter
                            chunk_progress = st.progress(0)

                            for chunk_idx, chunk in enumerate(chunks):
                                chunk_progress.progress((chunk_idx + 1) / len(chunks))

                                # Generate speech for chunk
                                audio_data = generate_speech_openai(
                                    client,
                                    chunk,
                                    OPENAI_VOICES[voice_name]["id"],
                                    TTS_MODELS[model_name]["id"]
                                )
                                chapter_audio_chunks.append(audio_data)

                            # Combine chunks for this chapter
                            if len(chapter_audio_chunks) > 1:
                                status_text.markdown(f"🔗 Combining audio chunks for {chapter['title']}...")
                                chapter_audio = combine_audio_chunks(chapter_audio_chunks)
                            else:
                                chapter_audio = AudioSegment.from_mp3(io.BytesIO(chapter_audio_chunks[0]))

                            # Export with selected format
                            chapter_audio_bytes = export_audio(chapter_audio, AUDIO_FORMATS[output_format])

                            all_audio_files.append({
                                "title": chapter['title'],
                                "audio": chapter_audio_bytes,
                                "duration": len(chapter_audio) / 1000  # seconds
                            })

                            # Update progress
                            progress_bar.progress((chapter_idx + 1) / total_chapters)

                        # Success!
                        status_text.markdown("### ✅ Audiobook Generation Complete!")
                        st.balloons()

                        # Display results
                        st.markdown("---")
                        st.markdown("### 📥 Download Your Audiobook")

                        total_duration = sum(ch["duration"] for ch in all_audio_files)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Chapters", len(all_audio_files))
                        with col2:
                            st.metric("Total Duration", f"{total_duration/60:.1f} min")
                        with col3:
                            cost, chars = estimate_cost(manuscript_text, model_name)
                            st.metric("Total Cost", f"${cost:.2f}")

                        # Download buttons for each chapter
                        st.markdown("### 📁 Individual Chapters")

                        for audio_file in all_audio_files:
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.markdown(f"""
                                <div class='chapter-box'>
                                    <strong>{audio_file['title']}</strong><br/>
                                    Duration: {audio_file['duration']:.1f} seconds
                                </div>
                                """, unsafe_allow_html=True)

                            with col2:
                                extension = AUDIO_FORMATS[output_format]["format"]
                                filename = f"{audio_file['title'].replace(' ', '_')}.{extension}"

                                st.download_button(
                                    label="📥 Download",
                                    data=audio_file["audio"],
                                    file_name=filename,
                                    mime=f"audio/{extension}",
                                    key=f"download_{audio_file['title']}"
                                )

                        # Combined audiobook download
                        if len(all_audio_files) > 1:
                            st.markdown("### 📚 Complete Audiobook")
                            st.info("Combining all chapters into a single file...")

                            # Combine all chapters
                            combined_audio = AudioSegment.empty()
                            for audio_file in all_audio_files:
                                chapter_segment = AudioSegment.from_file(
                                    io.BytesIO(audio_file["audio"]),
                                    format=AUDIO_FORMATS[output_format]["format"]
                                )
                                combined_audio += chapter_segment

                            combined_bytes = export_audio(combined_audio, AUDIO_FORMATS[output_format])

                            extension = AUDIO_FORMATS[output_format]["format"]
                            st.download_button(
                                label="📥 Download Complete Audiobook",
                                data=combined_bytes,
                                file_name=f"complete_audiobook.{extension}",
                                mime=f"audio/{extension}",
                                use_container_width=True
                            )

                    except Exception as e:
                        st.error(f"❌ Error during generation: {str(e)}")
                        st.info("💡 Try:\n- Reducing text length\n- Checking your API key\n- Using a different voice or model")

with tab3:
    st.markdown("### 💰 Cost Calculator")

    st.markdown("""
    Calculate the estimated cost for converting your manuscript to an audiobook.
    """)

    col1, col2 = st.columns(2)

    with col1:
        calc_word_count = st.number_input(
            "Word Count",
            min_value=100,
            max_value=500000,
            value=50000,
            step=1000,
            help="Total word count of your manuscript"
        )

        calc_model = st.selectbox(
            "Model",
            options=list(TTS_MODELS.keys()),
            key="calc_model"
        )

    with col2:
        # Calculate
        calc_char_count = calc_word_count * 5  # Average chars per word
        calc_cost, _ = estimate_cost("x" * calc_char_count, calc_model)
        calc_duration = calc_word_count / 200  # minutes

        st.markdown(f"""
        <div class='cost-estimate'>
            💵 Estimated Cost<br/>
            ${calc_cost:.2f}
        </div>
        """, unsafe_allow_html=True)

        st.metric("Estimated Duration", f"{calc_duration:.0f} minutes ({calc_duration/60:.1f} hours)")
        st.metric("Character Count", f"{calc_char_count:,}")

    st.markdown("### 📊 Pricing Comparison")

    st.markdown("""
    | Service | Cost per Hour | 10-Hour Book | Notes |
    |---------|---------------|--------------|-------|
    | **OpenAI TTS-1** | ~$1.80 | ~$18 | Fast, good quality |
    | **OpenAI TTS-1-HD** | ~$3.60 | ~$36 | High definition |
    | **Professional Narrator** | $200-400 | $2,000-4,000 | Human narration |
    | **ACX Per-Finished-Hour** | $50-400 | $500-4,000 | Royalty share available |
    """)

    st.success("""
    💡 **Value Proposition**: AI narration costs 50-200x less than professional narration,
    making audiobooks accessible for all authors!
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
