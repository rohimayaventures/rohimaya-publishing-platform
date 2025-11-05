"""
🦚 Rohimaya Publishing - Character Creator
AI-powered character development with personality profiles, backstories, and visual generation
"""

import streamlit as st
import anthropic
import openai
import json
from datetime import datetime
from io import BytesIO
import requests

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Character Creator - Rohimaya Publishing",
    page_icon="👤",
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
    .character-card {
        background: #FFF8E7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4A9B9B;
        margin-bottom: 1rem;
    }
    .archetype-badge {
        background: #FF8C42;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0.5rem 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'characters' not in st.session_state:
    st.session_state.characters = []
if 'current_character' not in st.session_state:
    st.session_state.current_character = None

# 16 Character Archetypes
ARCHETYPES = {
    "Hero": {
        "description": "The protagonist who rises to challenges and saves the day",
        "traits": "Courageous, determined, selfless",
        "motivation": "To prove their worth and protect others"
    },
    "Mentor": {
        "description": "The wise guide who trains and advises the hero",
        "traits": "Wise, patient, experienced",
        "motivation": "To pass on knowledge and see others succeed"
    },
    "Threshold Guardian": {
        "description": "Tests the hero before they can progress",
        "traits": "Challenging, protective, vigilant",
        "motivation": "To maintain order and test worthiness"
    },
    "Herald": {
        "description": "Brings news of change and calls the hero to action",
        "traits": "Observant, communicative, urgent",
        "motivation": "To deliver important messages and catalyze change"
    },
    "Shapeshifter": {
        "description": "Changes loyalties or appearance, keeping hero uncertain",
        "traits": "Mysterious, unpredictable, alluring",
        "motivation": "To serve their own interests, which may shift"
    },
    "Shadow": {
        "description": "The antagonist representing the hero's dark side",
        "traits": "Dangerous, compelling, complex",
        "motivation": "To oppose the hero and achieve their own goals"
    },
    "Ally": {
        "description": "Loyal companion who supports the hero",
        "traits": "Loyal, supportive, complementary",
        "motivation": "To help the hero succeed"
    },
    "Trickster": {
        "description": "Provides comic relief and challenges the status quo",
        "traits": "Mischievous, clever, unpredictable",
        "motivation": "To cause chaos and reveal truth through humor"
    },
    "Ruler": {
        "description": "Leader who creates order and stability",
        "traits": "Authoritative, responsible, controlling",
        "motivation": "To maintain power and create lasting prosperity"
    },
    "Creator": {
        "description": "Artist or innovator who brings new things into being",
        "traits": "Imaginative, innovative, driven",
        "motivation": "To create something of lasting value"
    },
    "Innocent": {
        "description": "Pure soul who sees the good in everything",
        "traits": "Optimistic, naive, trusting",
        "motivation": "To be happy and maintain their purity"
    },
    "Sage": {
        "description": "Seeker of truth and knowledge",
        "traits": "Thoughtful, analytical, enlightened",
        "motivation": "To understand the world through wisdom"
    },
    "Explorer": {
        "description": "Driven to discover new places and experiences",
        "traits": "Adventurous, independent, restless",
        "motivation": "To experience the world and find themselves"
    },
    "Outlaw": {
        "description": "Rebel who breaks rules to change the world",
        "traits": "Rebellious, wild, revolutionary",
        "motivation": "To overturn what isn't working"
    },
    "Magician": {
        "description": "Transforms reality through special knowledge",
        "traits": "Visionary, charismatic, transformative",
        "motivation": "To understand universal laws and make dreams real"
    },
    "Everyperson": {
        "description": "Relatable regular person who connects with everyone",
        "traits": "Grounded, relatable, empathetic",
        "motivation": "To belong and connect with others"
    }
}

def initialize_anthropic():
    """Initialize Anthropic client"""
    try:
        api_key = st.secrets.get("anthropic", {}).get("api_key", "")
        if not api_key:
            return None
        return anthropic.Anthropic(api_key=api_key)
    except:
        return None

def initialize_openai():
    """Initialize OpenAI client"""
    try:
        api_key = st.secrets.get("openai", {}).get("api_key", "")
        if not api_key:
            return None
        openai.api_key = api_key
        return True
    except:
        return None

def generate_character_profile(client, name, role, archetype, age, gender, occupation, genre):
    """Generate comprehensive character profile using Claude"""
    try:
        archetype_info = ARCHETYPES[archetype]

        prompt = f"""You are a professional character development consultant. Create a deep, compelling character profile.

Character Basics:
- Name: {name}
- Role: {role}
- Archetype: {archetype} ({archetype_info['description']})
- Age: {age}
- Gender: {gender}
- Occupation: {occupation}
- Story Genre: {genre}

Please generate a comprehensive character profile with:

1. PERSONALITY PROFILE:
   - Big Five personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
   - Temperament and general demeanor
   - Core values and beliefs
   - Moral compass

2. DETAILED BACKSTORY:
   - Childhood and family background
   - Key formative experiences
   - Important relationships
   - Traumas or challenges that shaped them

3. MOTIVATIONS & CONFLICTS:
   - Primary goal in the story
   - Internal conflicts (psychological, moral)
   - External conflicts (with people, circumstances)
   - What they fear most
   - What they desire most

4. STRENGTHS & WEAKNESSES:
   - Key strengths and skills
   - Fatal flaws or weaknesses
   - How these affect their journey

5. CHARACTER ARC:
   - Where they start emotionally/psychologically
   - How they need to change
   - What they'll learn by the end

6. PHYSICAL DESCRIPTION:
   - Appearance details
   - Distinctive features
   - Body language and mannerisms
   - Style and fashion sense

7. VOICE & DIALOGUE:
   - How they speak
   - Vocabulary level and patterns
   - Accent or dialect
   - Common phrases or speech quirks

Format your response as a JSON object with these keys:
- personality_profile
- backstory
- motivations
- internal_conflicts
- external_conflicts
- fears
- desires
- strengths
- weaknesses
- character_arc
- physical_description
- voice_and_dialogue

Make this character feel real, complex, and compelling. Include specific details that make them memorable."""

        with st.spinner("🎭 Creating character profile..."):
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

        response_text = message.content[0].text

        # Try to extract JSON
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                character_data = json.loads(json_str)
                return character_data
            else:
                return {"error": "Could not parse JSON", "raw": response_text}
        except:
            return {"error": "JSON parse error", "raw": response_text}

    except Exception as e:
        st.error(f"❌ Error generating profile: {str(e)}")
        return None

def generate_character_portrait(name, physical_description, genre, art_style):
    """Generate character portrait using DALL-E 3"""
    try:
        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

        prompt = f"Character portrait of {name}. {physical_description}. "
        prompt += f"Genre: {genre}. Art style: {art_style}. "
        prompt += "High quality character portrait, detailed face, professional book illustration style. "
        prompt += "Focus on the character's face and upper body. No text."

        with st.spinner("🎨 Generating character portrait..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

        image_url = response.data[0].url

        # Download the image
        image_response = requests.get(image_url)
        if PIL_AVAILABLE:
            image = Image.open(BytesIO(image_response.content))
            return image
        else:
            return image_response.content

    except Exception as e:
        st.error(f"❌ Error generating portrait: {str(e)}")
        return None

def export_character_to_markdown(character):
    """Export character profile to Markdown"""
    md = f"# {character['name']}\n\n"

    if character.get('portrait'):
        md += "*Portrait image saved separately*\n\n"

    md += f"**Role:** {character['role']}\n\n"
    md += f"**Archetype:** {character['archetype']}\n\n"
    md += f"**Age:** {character['age']} | **Gender:** {character['gender']} | **Occupation:** {character['occupation']}\n\n"
    md += f"**Genre:** {character['genre']}\n\n"
    md += "---\n\n"

    profile = character.get('profile', {})

    if 'personality_profile' in profile:
        md += "## Personality Profile\n\n"
        md += f"{profile['personality_profile']}\n\n"

    if 'backstory' in profile:
        md += "## Backstory\n\n"
        md += f"{profile['backstory']}\n\n"

    if 'motivations' in profile:
        md += "## Motivations\n\n"
        md += f"{profile['motivations']}\n\n"

    if 'internal_conflicts' in profile:
        md += "## Internal Conflicts\n\n"
        md += f"{profile['internal_conflicts']}\n\n"

    if 'external_conflicts' in profile:
        md += "## External Conflicts\n\n"
        md += f"{profile['external_conflicts']}\n\n"

    if 'fears' in profile:
        md += "## Fears\n\n"
        md += f"{profile['fears']}\n\n"

    if 'desires' in profile:
        md += "## Desires\n\n"
        md += f"{profile['desires']}\n\n"

    if 'strengths' in profile:
        md += "## Strengths\n\n"
        md += f"{profile['strengths']}\n\n"

    if 'weaknesses' in profile:
        md += "## Weaknesses\n\n"
        md += f"{profile['weaknesses']}\n\n"

    if 'character_arc' in profile:
        md += "## Character Arc\n\n"
        md += f"{profile['character_arc']}\n\n"

    if 'physical_description' in profile:
        md += "## Physical Description\n\n"
        md += f"{profile['physical_description']}\n\n"

    if 'voice_and_dialogue' in profile:
        md += "## Voice & Dialogue\n\n"
        md += f"{profile['voice_and_dialogue']}\n\n"

    md += "---\n\n"
    md += f"*Generated on {character.get('timestamp', 'Unknown date')}*\n"
    md += "*Created with Rohimaya Publishing Character Creator*\n"

    return md

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👤 Character Creator</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-powered character development and visual generation</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">16 Archetypes • Personality Profiles • Portrait Generation • Rohimaya Publishing</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize services
    anthropic_client = initialize_anthropic()
    openai_available = initialize_openai()

    if not anthropic_client:
        st.warning("⚠️ Anthropic API key not configured. Some features will be limited.")

    # Sidebar - Character Input
    with st.sidebar:
        st.markdown("### 👤 Character Basics")

        char_name = st.text_input("Character Name *", placeholder="Enter character name")

        role = st.selectbox(
            "Role *",
            ["Protagonist", "Antagonist", "Supporting", "Minor"]
        )

        archetype = st.selectbox(
            "Archetype *",
            list(ARCHETYPES.keys())
        )

        # Show archetype description
        st.info(f"**{archetype}**: {ARCHETYPES[archetype]['description']}")

        age = st.number_input("Age", min_value=1, max_value=200, value=25)

        gender = st.text_input("Gender", placeholder="e.g., Male, Female, Non-binary")

        occupation = st.text_input("Occupation", placeholder="e.g., Detective, Student, Wizard")

        genre = st.selectbox(
            "Story Genre",
            ["Fantasy", "Romance", "Thriller", "Mystery", "Sci-Fi", "Horror",
             "Contemporary", "Historical", "Young Adult", "Literary Fiction"]
        )

        st.markdown("---")

        # Generate profile button
        generate_profile_btn = st.button("✨ Generate Character Profile", use_container_width=True)

        st.markdown("---")

        # Visual generation
        st.markdown("### 🎨 Visual Generation")

        if st.session_state.current_character:
            art_style = st.selectbox(
                "Art Style",
                ["Photorealistic", "Digital Art", "Oil Painting", "Illustrated",
                 "Anime", "Comic Book", "Watercolor", "Sketch"]
            )

            generate_portrait_btn = st.button("🖼️ Generate Portrait", use_container_width=True)
        else:
            st.info("Generate a character profile first")
            generate_portrait_btn = False

    # Main content area
    if generate_profile_btn:
        if not char_name:
            st.error("❌ Please enter a character name")
        elif not anthropic_client:
            st.error("❌ Anthropic API key required for character generation")
        else:
            profile_data = generate_character_profile(
                anthropic_client,
                char_name,
                role,
                archetype,
                age,
                gender,
                occupation,
                genre
            )

            if profile_data:
                character = {
                    'name': char_name,
                    'role': role,
                    'archetype': archetype,
                    'age': age,
                    'gender': gender,
                    'occupation': occupation,
                    'genre': genre,
                    'profile': profile_data,
                    'portrait': None,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                st.session_state.current_character = character
                st.session_state.characters.insert(0, character)
                st.success(f"✅ Character profile created for {char_name}!")
                st.rerun()

    # Generate portrait
    if 'generate_portrait_btn' in locals() and generate_portrait_btn:
        if not openai_available:
            st.error("❌ OpenAI API key required for portrait generation")
        else:
            char = st.session_state.current_character
            portrait = generate_character_portrait(
                char['name'],
                char['profile'].get('physical_description', ''),
                char['genre'],
                art_style
            )

            if portrait:
                char['portrait'] = portrait
                st.success("✅ Portrait generated!")
                st.rerun()

    # Display current character
    if st.session_state.current_character:
        char = st.session_state.current_character

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("### 🖼️ Character Portrait")

            if char.get('portrait'):
                st.image(char['portrait'], use_container_width=True)

                # Download portrait
                if PIL_AVAILABLE and isinstance(char['portrait'], Image.Image):
                    buf = BytesIO()
                    char['portrait'].save(buf, format="PNG")
                    buf.seek(0)
                    st.download_button(
                        label="📥 Download Portrait",
                        data=buf.getvalue(),
                        file_name=f"{char['name'].replace(' ', '_')}_portrait.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                st.info("No portrait generated yet. Use the sidebar to generate one!")

            # Character basics card
            st.markdown("### 📋 Basic Info")
            st.markdown(f"**Name:** {char['name']}")
            st.markdown(f"**Role:** {char['role']}")
            st.markdown(f'<span class="archetype-badge">{char["archetype"]}</span>', unsafe_allow_html=True)
            st.markdown(f"**Age:** {char['age']}")
            st.markdown(f"**Gender:** {char['gender']}")
            st.markdown(f"**Occupation:** {char['occupation']}")
            st.markdown(f"**Genre:** {char['genre']}")

        with col2:
            st.markdown(f"### 👤 {char['name']}")

            profile = char.get('profile', {})

            # Tabbed interface for profile sections
            tabs = st.tabs([
                "Personality",
                "Backstory",
                "Motivations",
                "Conflicts",
                "Traits",
                "Arc",
                "Physical",
                "Voice"
            ])

            with tabs[0]:  # Personality
                st.markdown("#### Personality Profile")
                st.write(profile.get('personality_profile', 'N/A'))

            with tabs[1]:  # Backstory
                st.markdown("#### Backstory")
                st.write(profile.get('backstory', 'N/A'))

            with tabs[2]:  # Motivations
                st.markdown("#### Motivations")
                st.write(profile.get('motivations', 'N/A'))

                st.markdown("#### Desires")
                st.write(profile.get('desires', 'N/A'))

            with tabs[3]:  # Conflicts
                st.markdown("#### Internal Conflicts")
                st.write(profile.get('internal_conflicts', 'N/A'))

                st.markdown("#### External Conflicts")
                st.write(profile.get('external_conflicts', 'N/A'))

                st.markdown("#### Fears")
                st.write(profile.get('fears', 'N/A'))

            with tabs[4]:  # Traits
                st.markdown("#### Strengths")
                st.write(profile.get('strengths', 'N/A'))

                st.markdown("#### Weaknesses")
                st.write(profile.get('weaknesses', 'N/A'))

            with tabs[5]:  # Arc
                st.markdown("#### Character Arc")
                st.write(profile.get('character_arc', 'N/A'))

            with tabs[6]:  # Physical
                st.markdown("#### Physical Description")
                st.write(profile.get('physical_description', 'N/A'))

            with tabs[7]:  # Voice
                st.markdown("#### Voice & Dialogue")
                st.write(profile.get('voice_and_dialogue', 'N/A'))

        # Export options
        st.markdown("---")
        st.markdown("### 📥 Export Character")

        col_exp1, col_exp2, col_exp3 = st.columns(3)

        with col_exp1:
            # Markdown export
            md_content = export_character_to_markdown(char)
            st.download_button(
                label="📄 Download Markdown",
                data=md_content,
                file_name=f"{char['name'].replace(' ', '_')}_profile.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_exp2:
            # JSON export
            json_content = json.dumps(char, indent=2, default=str)
            st.download_button(
                label="💾 Download JSON",
                data=json_content,
                file_name=f"{char['name'].replace(' ', '_')}_profile.json",
                mime="application/json",
                use_container_width=True
            )

        with col_exp3:
            if st.button("🔄 New Character", use_container_width=True):
                st.session_state.current_character = None
                st.rerun()

    else:
        st.info("👈 Fill in character details in the sidebar and click 'Generate Character Profile' to begin!")

        # Show archetype reference
        st.markdown("### 🎭 Character Archetypes Reference")

        for arch_name, arch_data in ARCHETYPES.items():
            with st.expander(f"**{arch_name}**"):
                st.markdown(f"**Description:** {arch_data['description']}")
                st.markdown(f"**Traits:** {arch_data['traits']}")
                st.markdown(f"**Motivation:** {arch_data['motivation']}")

    # Character history
    if len(st.session_state.characters) > 1:
        st.markdown("---")
        st.markdown("### 📚 Character Library")

        for idx, char in enumerate(st.session_state.characters[:5]):
            with st.expander(f"👤 {char['name']} - {char['archetype']}"):
                col_a, col_b = st.columns([1, 3])

                with col_a:
                    if char.get('portrait'):
                        st.image(char['portrait'], use_container_width=True)

                with col_b:
                    st.markdown(f"**Role:** {char['role']}")
                    st.markdown(f"**Occupation:** {char['occupation']}")
                    st.markdown(f"**Genre:** {char['genre']}")

                    if st.button(f"Load Character", key=f"load_{idx}"):
                        st.session_state.current_character = char
                        st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7B9AA8; padding: 2rem;">
        <p style="margin: 0;">🦚 <strong>Rohimaya Publishing</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ascend • Flourish • Enlighten</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Character Creator powered by Claude AI & DALL-E 3</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
