"""
🦚 Rohimaya Publishing - Plot Outliner
AI-powered story structure and plot development tool
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
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Plot Outliner - Rohimaya Publishing",
    page_icon="📚",
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
    .beat-card {
        background: #FFF8E7;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #4A9B9B;
        margin-bottom: 1rem;
    }
    .structure-option {
        background: #E8E8E8;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .structure-option:hover {
        background: #4A9B9B;
        color: white;
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'plot_outline' not in st.session_state:
    st.session_state.plot_outline = None
if 'beats' not in st.session_state:
    st.session_state.beats = []

# Plot structure templates
PLOT_STRUCTURES = {
    "Three-Act Structure": {
        "description": "Classic storytelling format with setup, confrontation, and resolution",
        "beats": [
            {"name": "Act 1 - Setup", "description": "Introduce characters, world, and normal life"},
            {"name": "Inciting Incident", "description": "Event that disrupts the status quo"},
            {"name": "First Plot Point", "description": "Hero commits to the journey"},
            {"name": "Act 2 - Confrontation", "description": "Rising action, complications, obstacles"},
            {"name": "Midpoint", "description": "Major revelation or setback that changes everything"},
            {"name": "Low Point", "description": "Hero's darkest moment, all seems lost"},
            {"name": "Second Plot Point", "description": "Hero gains final piece needed for victory"},
            {"name": "Act 3 - Resolution", "description": "Climax and resolution of the conflict"},
            {"name": "Climax", "description": "Final confrontation with antagonist"},
            {"name": "Resolution", "description": "New normal, tie up loose ends"}
        ]
    },
    "Hero's Journey": {
        "description": "Joseph Campbell's monomyth - 12 stages of the hero's adventure",
        "beats": [
            {"name": "Ordinary World", "description": "Hero's normal life before the adventure"},
            {"name": "Call to Adventure", "description": "Challenge or quest is presented"},
            {"name": "Refusal of the Call", "description": "Hero hesitates or refuses initially"},
            {"name": "Meeting the Mentor", "description": "Hero gains guidance and wisdom"},
            {"name": "Crossing the Threshold", "description": "Hero commits and enters the special world"},
            {"name": "Tests, Allies, Enemies", "description": "Hero faces trials and meets companions"},
            {"name": "Approach to the Inmost Cave", "description": "Hero prepares for major challenge"},
            {"name": "Ordeal", "description": "Hero faces greatest fear or enemy"},
            {"name": "Reward", "description": "Hero gains treasure, knowledge, or reconciliation"},
            {"name": "The Road Back", "description": "Hero begins return to ordinary world"},
            {"name": "Resurrection", "description": "Final test, hero is reborn"},
            {"name": "Return with Elixir", "description": "Hero returns transformed, bringing wisdom"}
        ]
    },
    "Save the Cat": {
        "description": "Blake Snyder's 15-beat structure for screenwriting and novels",
        "beats": [
            {"name": "Opening Image", "description": "Snapshot of hero's life before change"},
            {"name": "Theme Stated", "description": "Someone hints at the story's deeper meaning"},
            {"name": "Set-Up", "description": "Introduce hero's world and what's missing"},
            {"name": "Catalyst", "description": "Life-changing event that starts the story"},
            {"name": "Debate", "description": "Hero hesitates, unsure of the path forward"},
            {"name": "Break into Two", "description": "Hero makes a choice and enters Act 2"},
            {"name": "B Story", "description": "Subplot begins, often a love story or friendship"},
            {"name": "Fun and Games", "description": "Promise of the premise is delivered"},
            {"name": "Midpoint", "description": "False victory or false defeat"},
            {"name": "Bad Guys Close In", "description": "Complications and obstacles mount"},
            {"name": "All Is Lost", "description": "Hero's lowest point"},
            {"name": "Dark Night of the Soul", "description": "Hero wallows in defeat"},
            {"name": "Break into Three", "description": "Hero finds solution to the problem"},
            {"name": "Finale", "description": "Hero executes plan and defeats antagonist"},
            {"name": "Final Image", "description": "Opposite of opening image, showing transformation"}
        ]
    },
    "Seven-Point Story Structure": {
        "description": "Dan Wells' structure focusing on character development",
        "beats": [
            {"name": "Hook", "description": "Introduction to hero in their starting state"},
            {"name": "Plot Turn 1", "description": "Event that starts the hero on their journey"},
            {"name": "Pinch Point 1", "description": "First major encounter with antagonistic force"},
            {"name": "Midpoint", "description": "Hero shifts from reaction to action"},
            {"name": "Pinch Point 2", "description": "Second encounter, stakes are raised"},
            {"name": "Plot Turn 2", "description": "Hero gains final skill/knowledge needed"},
            {"name": "Resolution", "description": "Hero confronts problem and reaches ending state"}
        ]
    },
    "Five-Act Structure": {
        "description": "Freytag's Pyramid - classical dramatic structure",
        "beats": [
            {"name": "Act 1 - Exposition", "description": "Introduction to characters, setting, conflict"},
            {"name": "Act 2 - Rising Action", "description": "Complications arise, tension builds"},
            {"name": "Act 3 - Climax", "description": "Turning point, point of highest tension"},
            {"name": "Act 4 - Falling Action", "description": "Consequences of climax unfold"},
            {"name": "Act 5 - Denouement", "description": "Resolution, loose ends tied up"}
        ]
    },
    "Romance Beat Sheet": {
        "description": "Structure specifically for romance novels",
        "beats": [
            {"name": "Meet Cute", "description": "Hero and love interest meet in memorable way"},
            {"name": "Initial Attraction", "description": "Spark of chemistry, but complications"},
            {"name": "Rejection", "description": "One or both resist the attraction"},
            {"name": "Acceptance", "description": "Characters admit feelings and get together"},
            {"name": "Honeymoon Phase", "description": "Everything is perfect between them"},
            {"name": "Conflict Arises", "description": "External or internal forces create problems"},
            {"name": "The Break", "description": "Couple breaks up or separates"},
            {"name": "Realization", "description": "Characters realize what they're losing"},
            {"name": "Grand Gesture", "description": "One character makes dramatic gesture"},
            {"name": "HEA/HFN", "description": "Happily Ever After or Happy For Now ending"}
        ]
    },
    "Mystery Structure": {
        "description": "Structure for mystery and detective stories",
        "beats": [
            {"name": "The Crime", "description": "Murder, theft, or mystery is introduced"},
            {"name": "Initial Investigation", "description": "Detective begins gathering clues"},
            {"name": "Complication", "description": "Case becomes more complex than expected"},
            {"name": "Red Herrings", "description": "False leads and misdirection"},
            {"name": "Breakthrough", "description": "Key clue or insight discovered"},
            {"name": "Second Crime", "description": "Stakes are raised with new development"},
            {"name": "Dark Moment", "description": "Detective in danger or wrong suspect caught"},
            {"name": "Final Clue", "description": "Last piece falls into place"},
            {"name": "Confrontation", "description": "Detective confronts the true culprit"},
            {"name": "Resolution", "description": "Mystery solved, motives explained"}
        ]
    },
    "Custom": {
        "description": "Build your own structure from scratch",
        "beats": []
    }
}

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

def generate_plot_outline(client, premise, genre, target_words, structure_name, structure_beats):
    """Generate plot outline using Claude"""
    try:
        beats_desc = "\n".join([f"{i+1}. {beat['name']}: {beat['description']}"
                                for i, beat in enumerate(structure_beats)])

        prompt = f"""You are a professional story consultant helping an author develop their plot outline.

Story Premise: {premise}
Genre: {genre}
Target Word Count: {target_words}
Plot Structure: {structure_name}

Structure Beats:
{beats_desc}

Please generate a detailed plot outline following this structure. For each beat, provide:
1. A specific scene or event that fits the premise
2. Character development points
3. Key plot revelations
4. Suggested word count for this section
5. Pacing recommendations

Format your response as a JSON array with objects containing:
- beat_name: Name of the beat
- scene_description: Detailed description of what happens
- character_notes: Character development in this beat
- plot_points: Key revelations or turns
- suggested_words: Recommended word count
- pacing_notes: How fast or slow this section should move

Provide creative, specific suggestions that would make this story compelling."""

        with st.spinner("🎨 Generating plot outline with AI..."):
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

        response_text = message.content[0].text

        # Try to extract JSON from the response
        try:
            # Find JSON array in response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                beats_data = json.loads(json_str)
                return beats_data
            else:
                # If no JSON found, return text response
                return response_text
        except:
            return response_text

    except Exception as e:
        st.error(f"❌ Error generating outline: {str(e)}")
        return None

def export_to_markdown(outline_data, title, author, structure_name):
    """Export outline to Markdown format"""
    md = f"# {title}\n\n"
    md += f"**Author:** {author}\n\n"
    md += f"**Structure:** {structure_name}\n\n"
    md += "---\n\n"

    if isinstance(outline_data, list):
        for i, beat in enumerate(outline_data, 1):
            md += f"## {i}. {beat.get('beat_name', f'Beat {i}')}\n\n"
            md += f"**Scene Description:**\n{beat.get('scene_description', 'N/A')}\n\n"
            md += f"**Character Notes:**\n{beat.get('character_notes', 'N/A')}\n\n"
            md += f"**Key Plot Points:**\n{beat.get('plot_points', 'N/A')}\n\n"
            md += f"**Suggested Word Count:** {beat.get('suggested_words', 'N/A')}\n\n"
            md += f"**Pacing:** {beat.get('pacing_notes', 'N/A')}\n\n"
            md += "---\n\n"
    else:
        md += str(outline_data)

    return md

def export_to_docx(outline_data, title, author, structure_name):
    """Export outline to DOCX format"""
    if not DOCX_AVAILABLE:
        return None

    try:
        doc = Document()

        # Title
        title_para = doc.add_heading(title, 0)
        title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Metadata
        doc.add_paragraph(f"Author: {author}")
        doc.add_paragraph(f"Structure: {structure_name}")
        doc.add_paragraph()

        # Beats
        if isinstance(outline_data, list):
            for i, beat in enumerate(outline_data, 1):
                # Beat heading
                doc.add_heading(f"{i}. {beat.get('beat_name', f'Beat {i}')}", 1)

                # Scene description
                doc.add_heading("Scene Description", 2)
                doc.add_paragraph(beat.get('scene_description', 'N/A'))

                # Character notes
                doc.add_heading("Character Notes", 2)
                doc.add_paragraph(beat.get('character_notes', 'N/A'))

                # Plot points
                doc.add_heading("Key Plot Points", 2)
                doc.add_paragraph(beat.get('plot_points', 'N/A'))

                # Metadata
                meta = doc.add_paragraph()
                meta.add_run(f"Suggested Word Count: ").bold = True
                meta.add_run(str(beat.get('suggested_words', 'N/A')))
                meta.add_run(" | ")
                meta.add_run("Pacing: ").bold = True
                meta.add_run(beat.get('pacing_notes', 'N/A'))

                doc.add_page_break()

        # Save to bytes
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        st.error(f"❌ Error creating DOCX: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 Plot Outliner</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-powered story structure and plot development</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">8 Professional Plot Structures • Rohimaya Publishing</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Anthropic
    client = initialize_anthropic()
    if not client:
        st.stop()

    # Sidebar - Input Form
    with st.sidebar:
        st.markdown("### 📝 Story Details")

        title = st.text_input("Story Title", placeholder="Enter your story title")
        author = st.text_input("Author Name", placeholder="Your name")

        premise = st.text_area(
            "Story Premise",
            height=150,
            placeholder="Describe your story idea in 2-3 sentences..."
        )

        genre = st.selectbox(
            "Genre",
            ["Fantasy", "Romance", "Thriller", "Mystery", "Sci-Fi", "Horror",
             "Contemporary", "Historical", "Young Adult", "Literary Fiction",
             "Non-Fiction", "Business", "Self-Help", "Children's"]
        )

        target_words = st.number_input(
            "Target Word Count",
            min_value=1000,
            max_value=500000,
            value=80000,
            step=5000
        )

        st.markdown("---")
        st.markdown("### 🎭 Plot Structure")

        structure_choice = st.selectbox(
            "Choose Structure Template",
            list(PLOT_STRUCTURES.keys())
        )

        # Display structure description
        st.info(f"**{structure_choice}**: {PLOT_STRUCTURES[structure_choice]['description']}")

        # Show number of beats
        num_beats = len(PLOT_STRUCTURES[structure_choice]['beats'])
        if num_beats > 0:
            st.markdown(f"**{num_beats} beats** in this structure")

        st.markdown("---")

        # Generate button
        generate_btn = st.button("✨ Generate Plot Outline", use_container_width=True)

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📖 Plot Outline")

        if generate_btn:
            if not premise:
                st.error("❌ Please provide a story premise")
            else:
                structure = PLOT_STRUCTURES[structure_choice]
                outline_data = generate_plot_outline(
                    client,
                    premise,
                    genre,
                    target_words,
                    structure_choice,
                    structure['beats']
                )

                if outline_data:
                    st.session_state.plot_outline = {
                        'data': outline_data,
                        'title': title or "Untitled",
                        'author': author or "Unknown",
                        'structure': structure_choice,
                        'premise': premise,
                        'genre': genre,
                        'target_words': target_words,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.success("✅ Plot outline generated!")
                    st.rerun()

        # Display current outline
        if st.session_state.plot_outline:
            outline = st.session_state.plot_outline

            st.markdown(f"### {outline['title']}")
            st.markdown(f"**By:** {outline['author']}")
            st.markdown(f"**Genre:** {outline['genre']} | **Target:** {outline['target_words']:,} words")
            st.markdown(f"**Structure:** {outline['structure']}")

            st.markdown("---")

            # Display beats
            if isinstance(outline['data'], list):
                for i, beat in enumerate(outline['data'], 1):
                    with st.expander(f"**{i}. {beat.get('beat_name', f'Beat {i}')}**", expanded=(i<=3)):
                        st.markdown("#### Scene Description")
                        st.write(beat.get('scene_description', 'N/A'))

                        st.markdown("#### Character Development")
                        st.write(beat.get('character_notes', 'N/A'))

                        st.markdown("#### Key Plot Points")
                        st.write(beat.get('plot_points', 'N/A'))

                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Suggested Words", beat.get('suggested_words', 'N/A'))
                        with col_b:
                            st.markdown(f"**Pacing:** {beat.get('pacing_notes', 'N/A')}")
            else:
                st.write(outline['data'])

            # Export options
            st.markdown("---")
            st.markdown("### 📥 Export Options")

            col_exp1, col_exp2, col_exp3 = st.columns(3)

            with col_exp1:
                # Markdown export
                md_content = export_to_markdown(
                    outline['data'],
                    outline['title'],
                    outline['author'],
                    outline['structure']
                )
                st.download_button(
                    label="📄 Download Markdown",
                    data=md_content,
                    file_name=f"{outline['title'].replace(' ', '_')}_outline.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            with col_exp2:
                # DOCX export
                if DOCX_AVAILABLE:
                    docx_bytes = export_to_docx(
                        outline['data'],
                        outline['title'],
                        outline['author'],
                        outline['structure']
                    )
                    if docx_bytes:
                        st.download_button(
                            label="📝 Download Word",
                            data=docx_bytes,
                            file_name=f"{outline['title'].replace(' ', '_')}_outline.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                else:
                    st.button("📝 Download Word", disabled=True, use_container_width=True)
                    st.caption("Install python-docx")

            with col_exp3:
                # JSON export
                json_content = json.dumps(outline, indent=2)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_content,
                    file_name=f"{outline['title'].replace(' ', '_')}_outline.json",
                    mime="application/json",
                    use_container_width=True
                )

            # Regenerate button
            if st.button("🔄 Regenerate Outline", use_container_width=True):
                st.session_state.plot_outline = None
                st.rerun()

        else:
            st.info("👈 Fill in your story details and choose a structure, then click 'Generate Plot Outline'")

    with col2:
        st.markdown("### 🎭 Structure Templates")

        for name, structure in PLOT_STRUCTURES.items():
            with st.expander(f"📖 {name}"):
                st.markdown(f"**Description:** {structure['description']}")
                st.markdown(f"**Beats:** {len(structure['beats'])}")

                if structure['beats']:
                    st.markdown("**Structure:**")
                    for i, beat in enumerate(structure['beats'], 1):
                        st.markdown(f"{i}. **{beat['name']}**")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7B9AA8; padding: 2rem;">
        <p style="margin: 0;">🦚 <strong>Rohimaya Publishing</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Ascend • Flourish • Enlighten</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Plot Outliner powered by Claude AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
