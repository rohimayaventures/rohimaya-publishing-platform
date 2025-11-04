import streamlit as st
from anthropic import Anthropic
import openai
from typing import Optional
import time

# Page configuration
st.set_page_config(
    page_title="AI Writing Assistant | Rohimaya Publishing",
    page_icon="🦚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Rohimaya branding
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
        --bronze: #B87333;
    }

    .stApp {
        background-color: var(--midnight-navy);
        color: var(--cream);
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: var(--phoenix-gold);
    }

    .stButton>button {
        background-color: var(--phoenix-orange);
        color: var(--midnight-navy);
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: var(--phoenix-gold);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 140, 66, 0.4);
    }

    .stTextArea>div>div>textarea {
        background-color: var(--deep-teal);
        color: var(--cream);
        border: 2px solid var(--peacock-teal);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }

    .stSidebar {
        background-color: var(--deep-teal);
    }

    .stSidebar .stSelectbox>div>div {
        background-color: var(--midnight-navy);
        color: var(--cream);
    }

    .output-box {
        background-color: var(--deep-teal);
        border: 2px solid var(--peacock-teal);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .header-logo {
        text-align: center;
        padding: 1rem 0;
    }

    .tagline {
        text-align: center;
        color: var(--peacock-blue-gray);
        font-style: italic;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-logo">', unsafe_allow_html=True)
st.title("🦚 AI Writing Assistant")
st.markdown('<p class="tagline">Ascend • Flourish • Enlighten</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    # API Selection
    api_provider = st.selectbox(
        "AI Provider",
        ["Claude (Anthropic)", "GPT-4 (OpenAI)"],
        help="Choose your preferred AI provider"
    )

    # Genre selection
    genre = st.selectbox(
        "Genre",
        ["General Fiction", "Fantasy", "Science Fiction", "Romance", "Thriller",
         "Mystery", "Horror", "Literary Fiction", "Young Adult", "Historical Fiction"]
    )

    # Tone slider
    tone = st.select_slider(
        "Writing Tone",
        options=["Serious", "Balanced", "Light", "Humorous"],
        value="Balanced"
    )

    # Length preference
    length = st.selectbox(
        "Output Length",
        ["Short (100-200 words)", "Medium (200-400 words)", "Long (400-600 words)"],
        index=1
    )

    st.divider()

    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.caption("**Rohimaya Publishing**")
    st.caption("Built with Claude & Streamlit")

# Helper function to get API credentials
def get_api_client(provider: str):
    """Initialize API client based on provider selection."""
    try:
        if provider == "Claude (Anthropic)":
            if "anthropic" not in st.secrets:
                st.error("⚠️ Anthropic API key not found in secrets.toml")
                return None
            return Anthropic(api_key=st.secrets["anthropic"]["api_key"])
        else:  # OpenAI
            if "openai" not in st.secrets:
                st.error("⚠️ OpenAI API key not found in secrets.toml")
                return None
            openai.api_key = st.secrets["openai"]["api_key"]
            return openai
    except Exception as e:
        st.error(f"⚠️ Error initializing API: {str(e)}")
        return None

# Helper function to call Claude API
def call_claude(prompt: str, system_context: str) -> Optional[str]:
    """Call Claude API with given prompt."""
    try:
        client = get_api_client("Claude (Anthropic)")
        if not client:
            return None

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=system_context,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"⚠️ Claude API Error: {str(e)}")
        return None

# Helper function to call OpenAI API
def call_openai(prompt: str, system_context: str) -> Optional[str]:
    """Call OpenAI API with given prompt."""
    try:
        client = get_api_client("GPT-4 (OpenAI)")
        if not client:
            return None

        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"⚠️ OpenAI API Error: {str(e)}")
        return None

# Helper function to generate AI response
def generate_response(action: str, user_text: str) -> Optional[str]:
    """Generate AI response based on action and user text."""

    # Build system context
    system_context = f"""You are a professional writing assistant for {genre} authors.
Your tone should be {tone.lower()}. Provide responses that are approximately {length.lower()}."""

    # Build prompt based on action
    prompts = {
        "Continue Writing": f"Continue this story naturally, maintaining the voice and style:\n\n{user_text}",
        "Expand Scene": f"Expand this brief scene into a detailed, vivid passage with rich description and emotion:\n\n{user_text}",
        "Polish Dialogue": f"Improve the naturalness and authenticity of this dialogue:\n\n{user_text}",
        "Show Don't Tell": f"Rewrite this passage to show rather than tell, using vivid sensory details and actions:\n\n{user_text}",
        "Fix Grammar": f"Fix any grammar, spelling, or punctuation errors in this text while maintaining the author's voice:\n\n{user_text}",
        "Improve Word Choice": f"Enhance the word choice in this passage to make it more vivid and engaging:\n\n{user_text}"
    }

    prompt = prompts.get(action, user_text)

    # Call appropriate API
    if api_provider == "Claude (Anthropic)":
        return call_claude(prompt, system_context)
    else:
        return call_openai(prompt, system_context)

# Main interface
st.write("Transform your writing with AI-powered assistance. Paste your text below and choose an action.")

# Text input
user_text = st.text_area(
    "Your Text",
    height=200,
    placeholder="Paste your writing here...",
    help="Enter the text you want to work with"
)

# Action buttons in columns
st.subheader("✨ Writing Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 Continue Writing", use_container_width=True):
        if user_text:
            with st.spinner("✍️ Continuing your story..."):
                result = generate_response("Continue Writing", user_text)
                if result:
                    st.session_state.history.append(("Continue Writing", result))
        else:
            st.warning("⚠️ Please enter some text first")

    if st.button("💬 Polish Dialogue", use_container_width=True):
        if user_text:
            with st.spinner("💬 Polishing dialogue..."):
                result = generate_response("Polish Dialogue", user_text)
                if result:
                    st.session_state.history.append(("Polish Dialogue", result))
        else:
            st.warning("⚠️ Please enter some text first")

with col2:
    if st.button("🎬 Expand Scene", use_container_width=True):
        if user_text:
            with st.spinner("🎬 Expanding scene..."):
                result = generate_response("Expand Scene", user_text)
                if result:
                    st.session_state.history.append(("Expand Scene", result))
        else:
            st.warning("⚠️ Please enter some text first")

    if st.button("👁️ Show Don't Tell", use_container_width=True):
        if user_text:
            with st.spinner("👁️ Transforming to showing..."):
                result = generate_response("Show Don't Tell", user_text)
                if result:
                    st.session_state.history.append(("Show Don't Tell", result))
        else:
            st.warning("⚠️ Please enter some text first")

with col3:
    if st.button("✅ Fix Grammar", use_container_width=True):
        if user_text:
            with st.spinner("✅ Fixing grammar..."):
                result = generate_response("Fix Grammar", user_text)
                if result:
                    st.session_state.history.append(("Fix Grammar", result))
        else:
            st.warning("⚠️ Please enter some text first")

    if st.button("🎨 Improve Word Choice", use_container_width=True):
        if user_text:
            with st.spinner("🎨 Improving word choice..."):
                result = generate_response("Improve Word Choice", user_text)
                if result:
                    st.session_state.history.append(("Improve Word Choice", result))
        else:
            st.warning("⚠️ Please enter some text first")

# Display results
if st.session_state.history:
    st.divider()
    st.subheader("📜 Results")

    # Show most recent result
    action, result = st.session_state.history[-1]
    st.markdown(f"**Action:** {action}")
    st.markdown(f'<div class="output-box">{result}</div>', unsafe_allow_html=True)

    # Copy to clipboard (using streamlit's built-in copy functionality)
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("📋 Copy to Clipboard"):
            st.code(result, language=None)
            st.success("✅ Copied! Use Ctrl+C / Cmd+C to copy the text above.")

    # Show history
    if len(st.session_state.history) > 1:
        with st.expander(f"📚 View All Results ({len(st.session_state.history)})"):
            for i, (act, res) in enumerate(reversed(st.session_state.history), 1):
                st.markdown(f"**{i}. {act}**")
                st.markdown(res)
                st.divider()

# Footer
st.divider()
st.caption("© 2025 Rohimaya Publishing | All rights reserved")
