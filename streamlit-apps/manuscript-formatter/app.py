import streamlit as st
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
import io
import zipfile
from ebooklib import epub
import re
from typing import Optional, Tuple

# Page configuration
st.set_page_config(
    page_title="Manuscript Formatter | Rohimaya Publishing",
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

    .stSidebar {
        background-color: var(--deep-teal);
    }

    .preview-box {
        background-color: white;
        color: black;
        border: 2px solid var(--peacock-teal);
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        font-family: 'Times New Roman', serif;
        line-height: 2;
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

    .spec-card {
        background-color: var(--deep-teal);
        border: 1px solid var(--peacock-teal);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-logo">', unsafe_allow_html=True)
st.title("🦚 Manuscript Formatter")
st.markdown('<p class="tagline">Ascend • Flourish • Enlighten</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state
if 'manuscript_content' not in st.session_state:
    st.session_state.manuscript_content = None
if 'book_title' not in st.session_state:
    st.session_state.book_title = ""
if 'author_name' not in st.session_state:
    st.session_state.author_name = ""

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Format Settings")

    # Platform selection
    platform = st.selectbox(
        "Publishing Platform",
        ["Amazon KDP", "IngramSpark", "EPUB (General)"],
        help="Choose your target publishing platform"
    )

    # Trim size selection (for print books)
    if platform in ["Amazon KDP", "IngramSpark"]:
        trim_size = st.selectbox(
            "Trim Size",
            [
                "5\" x 8\"",
                "5.5\" x 8.5\"",
                "6\" x 9\"",
                "6.14\" x 9.21\" (A5)",
                "8\" x 10\"",
                "8.5\" x 11\""
            ],
            index=2,
            help="Standard book dimensions"
        )
    else:
        trim_size = None

    # Font selection
    font_family = st.selectbox(
        "Font",
        ["Times New Roman", "Garamond", "Georgia", "Palatino", "Bookman"],
        help="Professional book fonts"
    )

    font_size = st.slider(
        "Font Size (pt)",
        min_value=10,
        max_value=14,
        value=12,
        help="Standard is 11-12pt"
    )

    # Line spacing
    line_spacing = st.selectbox(
        "Line Spacing",
        ["Single", "1.5 Lines", "Double"],
        index=1
    )

    # Chapter formatting
    chapter_starts = st.selectbox(
        "Chapter Starts",
        ["New Page", "Same Page"],
        help="Whether chapters start on a new page"
    )

    st.divider()
    st.caption("**Rohimaya Publishing**")
    st.caption("Professional manuscript formatting")

# Main interface
st.write("Upload your manuscript and format it for professional publishing.")

# Book metadata
col1, col2 = st.columns(2)
with col1:
    st.session_state.book_title = st.text_input(
        "Book Title",
        value=st.session_state.book_title,
        placeholder="Enter your book title"
    )
with col2:
    st.session_state.author_name = st.text_input(
        "Author Name",
        value=st.session_state.author_name,
        placeholder="Enter author name"
    )

# File upload
uploaded_file = st.file_uploader(
    "Upload Manuscript",
    type=['docx', 'txt'],
    help="Upload .docx or .txt file"
)

if uploaded_file:
    # Read file content
    try:
        if uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            content = []
            for para in doc.paragraphs:
                content.append(para.text)
            st.session_state.manuscript_content = '\n'.join(content)
        else:  # txt file
            st.session_state.manuscript_content = uploaded_file.read().decode('utf-8')

        st.success(f"✅ Loaded: {uploaded_file.name}")

        # Word count
        word_count = len(st.session_state.manuscript_content.split())
        st.info(f"📊 Word Count: {word_count:,} words")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {str(e)}")

# Format specifications display
if platform:
    st.subheader("📐 Format Specifications")

    specs = get_format_specs(platform, trim_size, font_family, font_size, line_spacing)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="spec-card"><strong>Margins:</strong><br>{specs["margins"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="spec-card"><strong>Font:</strong><br>{specs["font"]}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="spec-card"><strong>Spacing:</strong><br>{specs["spacing"]}</div>', unsafe_allow_html=True)

# Helper functions
def get_format_specs(platform: str, trim_size: Optional[str], font: str, size: int, spacing: str) -> dict:
    """Get format specifications based on platform."""
    specs = {
        "font": f"{font}, {size}pt",
        "spacing": spacing
    }

    if platform == "Amazon KDP":
        if trim_size == "6\" x 9\"":
            specs["margins"] = "0.75\" all sides"
        else:
            specs["margins"] = "0.5\"-1\" (varies by size)"
    elif platform == "IngramSpark":
        specs["margins"] = "0.75\" top/bottom, 0.5\" inside, 0.75\" outside"
    else:  # EPUB
        specs["margins"] = "Dynamic (device dependent)"

    return specs

def create_formatted_docx(content: str, title: str, author: str, platform: str,
                          trim_size: Optional[str], font: str, size: int,
                          spacing: str, chapter_starts: str) -> Document:
    """Create formatted Word document."""
    doc = Document()

    # Set up document margins based on trim size
    sections = doc.sections
    for section in sections:
        if trim_size == "6\" x 9\"":
            section.page_width = Inches(6)
            section.page_height = Inches(9)
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)
        elif trim_size == "5\" x 8\"":
            section.page_width = Inches(5)
            section.page_height = Inches(8)
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)
        else:  # Default 6x9
            section.page_width = Inches(6)
            section.page_height = Inches(9)
            section.top_margin = Inches(0.75)
            section.bottom_margin = Inches(0.75)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

    # Title page
    title_para = doc.add_paragraph()
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_para.add_run(title)
    title_run.font.size = Pt(size + 8)
    title_run.font.name = font
    title_run.bold = True

    # Author
    author_para = doc.add_paragraph()
    author_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author_run = author_para.add_run(f"\n\nby\n\n{author}")
    author_run.font.size = Pt(size + 2)
    author_run.font.name = font

    # Page break after title page
    doc.add_page_break()

    # Process content
    paragraphs = content.split('\n')

    for para_text in paragraphs:
        para_text = para_text.strip()

        if not para_text:
            continue

        # Check if it's a chapter heading
        is_chapter = re.match(r'^(Chapter\s+\d+|CHAPTER\s+\d+|Prologue|Epilogue)', para_text, re.IGNORECASE)

        if is_chapter and chapter_starts == "New Page":
            doc.add_page_break()

        para = doc.add_paragraph(para_text)

        # Format chapter headings
        if is_chapter:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.runs[0]
            run.font.size = Pt(size + 4)
            run.font.bold = True
            run.font.name = font
        else:
            # Regular paragraph
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            run = para.runs[0] if para.runs else para.add_run()
            run.font.size = Pt(size)
            run.font.name = font

            # Set line spacing
            if spacing == "Single":
                para.paragraph_format.line_spacing = 1.0
            elif spacing == "1.5 Lines":
                para.paragraph_format.line_spacing = 1.5
            else:  # Double
                para.paragraph_format.line_spacing = 2.0

            # First line indent (standard 0.5")
            para.paragraph_format.first_line_indent = Inches(0.5)

    return doc

def create_epub(content: str, title: str, author: str) -> epub.EpubBook:
    """Create EPUB file."""
    book = epub.EpubBook()

    # Set metadata
    book.set_identifier(f'rohimaya-{title.lower().replace(" ", "-")}')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Create chapters
    chapters = []
    chapter_texts = re.split(r'(Chapter\s+\d+|CHAPTER\s+\d+)', content)

    chapter_num = 1
    for i in range(1, len(chapter_texts), 2):
        if i + 1 < len(chapter_texts):
            chapter_title = chapter_texts[i].strip()
            chapter_content = chapter_texts[i + 1].strip()

            c = epub.EpubHtml(
                title=chapter_title,
                file_name=f'chap_{chapter_num:02d}.xhtml',
                lang='en'
            )
            c.content = f'<h1>{chapter_title}</h1>' + ''.join(
                [f'<p>{para}</p>' for para in chapter_content.split('\n') if para.strip()]
            )
            book.add_item(c)
            chapters.append(c)
            chapter_num += 1

    # Define Table of Contents
    book.toc = tuple(chapters)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body { font-family: Times New Roman, serif; line-height: 1.6; }
    h1 { text-align: center; margin-top: 2em; }
    p { text-align: justify; text-indent: 2em; margin: 0; }
    '''
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )
    book.add_item(nav_css)

    # Create spine
    book.spine = ['nav'] + chapters

    return book

# Format and download buttons
if st.session_state.manuscript_content and st.session_state.book_title and st.session_state.author_name:
    st.divider()
    st.subheader("📥 Download Formatted Manuscript")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Download as DOCX", use_container_width=True):
            with st.spinner("🔄 Formatting DOCX..."):
                try:
                    doc = create_formatted_docx(
                        st.session_state.manuscript_content,
                        st.session_state.book_title,
                        st.session_state.author_name,
                        platform,
                        trim_size,
                        font_family,
                        font_size,
                        line_spacing,
                        chapter_starts
                    )

                    # Save to bytes
                    docx_buffer = io.BytesIO()
                    doc.save(docx_buffer)
                    docx_buffer.seek(0)

                    # Download button
                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=docx_buffer,
                        file_name=f"{st.session_state.book_title.replace(' ', '_')}_formatted.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    st.success("✅ DOCX ready for download!")
                except Exception as e:
                    st.error(f"⚠️ Error creating DOCX: {str(e)}")

    with col2:
        if st.button("📕 Download as EPUB", use_container_width=True):
            with st.spinner("🔄 Creating EPUB..."):
                try:
                    book = create_epub(
                        st.session_state.manuscript_content,
                        st.session_state.book_title,
                        st.session_state.author_name
                    )

                    # Save to bytes
                    epub_buffer = io.BytesIO()
                    epub.write_epub(epub_buffer, book)
                    epub_buffer.seek(0)

                    # Download button
                    st.download_button(
                        label="⬇️ Download EPUB",
                        data=epub_buffer,
                        file_name=f"{st.session_state.book_title.replace(' ', '_')}.epub",
                        mime="application/epub+zip"
                    )
                    st.success("✅ EPUB ready for download!")
                except Exception as e:
                    st.error(f"⚠️ Error creating EPUB: {str(e)}")

    with col3:
        if st.button("📋 Preview Format", use_container_width=True):
            st.session_state.show_preview = True

    # Preview
    if 'show_preview' in st.session_state and st.session_state.show_preview:
        st.divider()
        st.subheader("👁️ Format Preview")

        # Show first few paragraphs
        preview_content = '\n\n'.join(st.session_state.manuscript_content.split('\n')[:10])

        st.markdown(
            f'<div class="preview-box" style="font-family: {font_family}; font-size: {font_size}pt; line-height: {1.0 if line_spacing == "Single" else 1.5 if line_spacing == "1.5 Lines" else 2.0};">{preview_content}</div>',
            unsafe_allow_html=True
        )

        st.info("ℹ️ This is a simplified preview. Download the formatted document for the full experience.")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    ### Step-by-Step Guide

    1. **Enter Book Details**
       - Add your book title and author name

    2. **Upload Manuscript**
       - Upload your .docx or .txt file
       - The app will display word count

    3. **Choose Format Settings**
       - Select publishing platform (Amazon KDP, IngramSpark, or EPUB)
       - Choose trim size (for print books)
       - Select font and size
       - Set line spacing and chapter formatting

    4. **Download Formatted File**
       - Click "Download as DOCX" for print books
       - Click "Download as EPUB" for ebooks
       - Click "Preview Format" to see a sample

    ### Platform-Specific Tips

    **Amazon KDP:**
    - Most popular trim size: 6" x 9"
    - Font size: 11-12pt recommended
    - Use "New Page" for chapter starts

    **IngramSpark:**
    - Professional specs with gutter margins
    - Recommended: 6" x 9" with 12pt font
    - Higher quality standards than KDP

    **EPUB:**
    - Universal ebook format
    - Works with most ereaders
    - Responsive to device settings
    """)

# Footer
st.divider()
st.caption("© 2025 Rohimaya Publishing | All rights reserved")
