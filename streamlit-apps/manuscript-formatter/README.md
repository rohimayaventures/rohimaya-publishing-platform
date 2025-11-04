# 🦚 Manuscript Formatter - Rohimaya Publishing

**Professional manuscript formatting for Amazon KDP, IngramSpark, and EPUB**

## Features

- **Multiple Platform Support** - Format for Amazon KDP, IngramSpark, and EPUB
- **Standard Trim Sizes** - 5"x8", 5.5"x8.5", 6"x9", A5, 8"x10", 8.5"x11"
- **Professional Fonts** - Times New Roman, Garamond, Georgia, Palatino, Bookman
- **Customizable Spacing** - Single, 1.5, or double line spacing
- **Chapter Formatting** - Automatic chapter detection and formatting
- **Live Preview** - See how your manuscript will look
- **Export Formats** - DOCX for print, EPUB for ebooks
- **Word Count** - Automatic word count calculation

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run app.py
```

### 3. Deploy to Streamlit Cloud
1. Push this directory to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Select `streamlit-apps/manuscript-formatter/app.py` as the main file
5. Deploy!

## Usage

### Step 1: Enter Book Details
- Book title
- Author name

### Step 2: Upload Manuscript
- Supported formats: .docx, .txt
- App will display word count

### Step 3: Configure Format Settings
- **Platform:** Amazon KDP, IngramSpark, or EPUB
- **Trim Size:** Choose standard book dimensions (print only)
- **Font:** Select professional book font
- **Font Size:** 10-14pt (11-12pt recommended)
- **Line Spacing:** Single, 1.5 Lines, or Double
- **Chapter Starts:** New Page or Same Page

### Step 4: Download
- **DOCX:** For print publishing (KDP, IngramSpark)
- **EPUB:** For ebook distribution
- **Preview:** See formatted sample before downloading

## Platform Specifications

### Amazon KDP
- **Trim Sizes:** Multiple options (6"x9" most popular)
- **Margins:** 0.5"-1" depending on page count
- **Font Size:** 11-12pt recommended
- **Quality:** Standard self-publishing requirements

### IngramSpark
- **Trim Sizes:** Professional standards
- **Margins:** Includes gutter margins for perfect binding
- **Font Size:** 12pt recommended
- **Quality:** Higher standards for bookstore distribution

### EPUB
- **Format:** Universal ebook standard
- **Compatibility:** Works with Kindle, Apple Books, Kobo, etc.
- **Responsive:** Adapts to device settings
- **CSS Styling:** Professional typography built-in

## File Format Support

### Input Formats
- **.docx** - Microsoft Word documents
- **.txt** - Plain text files

### Output Formats
- **.docx** - Formatted Word document for print publishing
- **.epub** - Ebook format for digital distribution

## Best Practices

### For Print Books (KDP/IngramSpark)
- Use 6"x9" trim size (most popular)
- Font: Times New Roman or Garamond
- Size: 11-12pt
- Spacing: 1.5 lines for readability
- Chapter starts: New page
- Include proper title page

### For Ebooks (EPUB)
- Font choice matters less (readers customize)
- Focus on clean chapter structure
- Use proper heading hierarchy
- Include table of contents
- Test on multiple devices

## Technical Details

**Formatting Features:**
- Automatic margins based on trim size
- First-line paragraph indentation (0.5")
- Chapter detection (regex-based)
- Centered chapter headings
- Justified body text
- Professional title page
- Page breaks between chapters

**EPUB Features:**
- Proper metadata (title, author, language)
- Chapter-based navigation
- Embedded CSS for typography
- Table of contents generation
- Compatible with EPUB 3 standard

## Tech Stack

- **Framework:** Streamlit
- **Document Processing:** python-docx
- **EPUB Creation:** ebooklib
- **Python:** 3.9+

## Troubleshooting

**Issue:** Chapters not detected
- **Solution:** Ensure chapters start with "Chapter 1", "CHAPTER 1", "Prologue", or "Epilogue"

**Issue:** Font not displaying correctly
- **Solution:** Download the formatted file - preview is simplified

**Issue:** EPUB not opening on device
- **Solution:** Ensure device supports EPUB 3 format

## Roadmap

- [ ] PDF export for print-ready files
- [ ] More trim size options
- [ ] Custom margin settings
- [ ] Advanced styling options
- [ ] Batch processing

## Support

For issues or questions, contact Rohimaya Publishing support.

---

**Rohimaya Publishing** | Ascend • Flourish • Enlighten
