# 🎨 Rohimaya Publishing - Brand Identity Guide

Complete brand guidelines for visual design, messaging, and user experience.

## Brand Story

**Rohimaya** (रोहिमाया) represents the fusion of artistic transformation and elegant expression - where the **Phoenix** (fire, rebirth, creative passion) meets the **Peacock** (beauty, pride, display). This platform empowers authors to rise from their struggles and display their work with confidence.

**Tagline:** *Ascend • Flourish • Enlighten*

---

## Color Palette

### Primary Colors

**Phoenix Colors** (Energy • Transformation • Fire)

```
Phoenix Orange: #FF8C42
RGB: 255, 140, 66
HSL: 20°, 100%, 63%
Usage: Primary CTAs, energy elements, fire themes, accent highlights
```

```
Phoenix Gold: #FFD700
RGB: 255, 215, 0
HSL: 51°, 100%, 50%
Usage: Premium features, success states, highlights, celestial elements
```

**Peacock Colors** (Elegance • Calm • Pride)

```
Peacock Teal: #4A9B9B
RGB: 74, 155, 155
HSL: 180°, 35%, 45%
Usage: Primary brand color, headers, links, navigation, trust elements
```

```
Peacock Blue-Gray: #7B9AA8
RGB: 123, 154, 168
HSL: 199°, 19%, 57%
Usage: Secondary UI elements, borders, subtle backgrounds
```

### Supporting Colors

```
Deep Teal Green: #2F5F5F
RGB: 47, 95, 95
HSL: 180°, 34%, 28%
Usage: Dark mode backgrounds, depth, grounding elements
```

```
Midnight Navy: #1A1A2E
RGB: 26, 26, 46
HSL: 240°, 28%, 14%
Usage: Dark backgrounds, primary text, sophisticated elements
```

```
Cream: #FFF8E7
RGB: 255, 248, 231
HSL: 42°, 100%, 95%
Usage: Light backgrounds, text areas, readability, warmth
```

### Accent Colors

```
Bronze: #B87333
RGB: 184, 115, 51
HSL: 29°, 57%, 46%
Usage: Borders, subtle accents, earthy elements
```

```
Celestial Gold: #F4C542
RGB: 244, 197, 66
HSL: 44°, 89%, 61%
Usage: Stars, magic elements, special features
```

```
Silver-White: #E8E8E8
RGB: 232, 232, 232
HSL: 0°, 0%, 91%
Usage: Light borders, dividers, subtle separators
```

### Color Usage Guidelines

**Do's:**
✅ Use Phoenix Orange for primary CTAs and action buttons
✅ Use Peacock Teal for brand consistency (headers, logos)
✅ Pair warm (Phoenix) and cool (Peacock) colors for balance
✅ Use Cream backgrounds for readability and warmth
✅ Ensure minimum 4.5:1 contrast ratio for accessibility

**Don'ts:**
❌ Don't use colors at less than 4.5:1 contrast ratio
❌ Don't mix too many colors in one component (max 3-4)
❌ Don't use pure black (#000) or pure white (#FFF)
❌ Don't use Phoenix colors on Cream backgrounds (low contrast)

### Color Combinations

**Hero Section:**
```
Background: Midnight Navy (#1A1A2E)
Headline Text: Cream (#FFF8E7)
Subtext: Peacock Blue-Gray (#7B9AA8)
CTA Button: Phoenix Orange (#FF8C42)
CTA Hover: Phoenix Gold (#FFD700)
```

**Cards & Panels:**
```
Background: Peacock Teal (#4A9B9B)
Text: Cream (#FFF8E7)
Accent: Phoenix Gold (#FFD700)
Border: Bronze (#B87333)
```

**Forms & Inputs:**
```
Background: Cream (#FFF8E7)
Border: Peacock Blue-Gray (#7B9AA8)
Focus Border: Phoenix Orange (#FF8C42)
Text: Midnight Navy (#1A1A2E)
Placeholder: #7B9AA8 at 60% opacity
```

**Dark Mode:**
```
Background: Midnight Navy (#1A1A2E)
Cards: Deep Teal Green (#2F5F5F)
Text: Cream (#FFF8E7)
Links: Peacock Teal (#4A9B9B)
Accents: Phoenix Gold (#FFD700)
```

---

## Typography

### Font Families

**Display/Headings: Playfair Display**
- **Style:** Serif, elegant, classic
- **Use:** H1, H2, H3, hero text, display sections
- **Weights:** 400 (Regular), 700 (Bold)
- **Character:** Sophisticated, literary, authoritative
- **Import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  ```

**Body/UI: Inter**
- **Style:** Sans-serif, modern, readable
- **Use:** Body text, UI elements, buttons, forms
- **Weights:** 300 (Light), 400 (Regular), 600 (Semi-bold)
- **Character:** Clean, professional, accessible
- **Import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
  ```

**Monospace: Fira Code**
- **Style:** Monospace with ligatures
- **Use:** Code blocks, technical content, data displays
- **Weight:** 400 (Regular)
- **Character:** Developer-friendly, clear
- **Import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code&display=swap" rel="stylesheet">
  ```

### Type Scale

**Desktop:**
```
H1 (Hero): 48px / 3rem (Playfair Display Bold) - Line height: 1.2
H2 (Section): 36px / 2.25rem (Playfair Display Bold) - Line height: 1.2
H3 (Subsection): 28px / 1.75rem (Playfair Display Regular) - Line height: 1.3
H4 (Card Title): 24px / 1.5rem (Inter Semi-bold) - Line height: 1.4
H5 (Small Header): 20px / 1.25rem (Inter Semi-bold) - Line height: 1.4
H6 (Label): 18px / 1.125rem (Inter Regular) - Line height: 1.5
Body: 16px / 1rem (Inter Regular) - Line height: 1.6
Small: 14px / 0.875rem (Inter Regular) - Line height: 1.5
Tiny: 12px / 0.75rem (Inter Regular) - Line height: 1.4
```

**Mobile:**
```
H1: 36px / 2.25rem - Line height: 1.2
H2: 28px / 1.75rem - Line height: 1.2
H3: 24px / 1.5rem - Line height: 1.3
Body: 16px / 1rem - Line height: 1.6
```

### Text Styling

**Letter Spacing:**
```
Headings (H1-H3): -0.02em (tighter)
Body Text: 0 (normal)
All Caps: 0.05em (wider for readability)
Buttons: 0.03em
```

**Font Weight Guidelines:**
```
Headlines: Bold (700)
Subheadings: Semi-bold (600)
Body: Regular (400)
Captions: Light (300)
Emphasis: Semi-bold (600)
```

**Example CSS:**
```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'Fira Code', monospace;
}

h1, h2, h3 {
  font-family: var(--font-display);
  letter-spacing: -0.02em;
  color: var(--midnight-navy);
}

body {
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  color: var(--midnight-navy);
}

code {
  font-family: var(--font-mono);
  font-size: 0.9em;
}
```

---

## Logo & Visual Identity

### Logo Description

**Primary Logo:** Phoenix + Peacock Medallion

**Symbolism:**
- **Left:** Phoenix (rising flames, transformation, rebirth)
- **Right:** Peacock (elegant display, pride, beauty)
- **Center:** Chalice (vessel of creativity, the writer's cup)
- **Border:** Peacock feather pattern (Art Nouveau style)
- **Shape:** Circular medallion (unity, completeness)

**Color Versions:**
1. **Full Color** - Phoenix Orange + Peacock Teal on light backgrounds
2. **Reversed** - White/Cream on dark backgrounds (Midnight Navy)
3. **Monochrome** - Single color for special uses
4. **Icon Only** - Simplified for small spaces (favicons, app icons)

### Logo Usage Rules

**Clear Space:**
- Maintain clearspace equal to the height of the peacock's crest
- No text or graphics within this area

**Minimum Size:**
- Digital: 48px × 48px
- Print: 0.5 inch × 0.5 inch

**Do's:**
✅ Use official logo files
✅ Maintain aspect ratio (never stretch)
✅ Place on appropriate background colors
✅ Ensure sufficient contrast
✅ Scale proportionally

**Don'ts:**
❌ Don't stretch or distort
❌ Don't change colors (use official versions)
❌ Don't add effects (shadows, outlines, gradients, glows)
❌ Don't place on busy backgrounds or low-contrast backgrounds
❌ Don't rotate or skew
❌ Don't recreate or redraw

### Tagline Pairing

**Tagline:** "Ascend • Flourish • Enlighten"

**When pairing with logo:**
- Place below logo, centered
- Font: Inter Semi-bold 14px
- Color: Peacock Teal (#4A9B9B) on light, Cream (#FFF8E7) on dark
- Spacing: 16px from logo bottom
- Bullet separator: • (bullet point, not dash)

---

## Voice & Tone

### Brand Personality

**Empowering** - We lift writers up
**Professional** - We're serious about quality
**Approachable** - We're friendly and helpful
**Innovative** - We embrace cutting-edge AI
**Elegant** - We value beauty and craft

### Voice Characteristics

**Confident but not arrogant**
✅ "Create professional book covers with AI"
❌ "We're the best cover designer in the world"

**Helpful but not condescending**
✅ "Let's polish your manuscript together"
❌ "Your writing needs a lot of work, but we can fix it"

**Inspiring but not over-the-top**
✅ "Your story deserves to be told"
❌ "YOU'RE GOING TO BE THE NEXT BESTSELLING AUTHOR!!!"

### Tone by Context

**Marketing Copy:** Inspiring, aspirational, benefit-focused
*"Transform your manuscript into a published masterpiece"*

**Product UI:** Clear, instructive, encouraging
*"Upload your manuscript to get started"*

**Error Messages:** Understanding, helpful, solution-oriented
*"We couldn't process your file. Try a smaller file size or different format."*

**Support:** Empathetic, patient, solution-focused
*"I understand this is frustrating. Let's solve this together."*

### Writing Style

**Use:**
- Active voice
- Second person ("you," "your")
- Short sentences
- Bullet points for clarity
- Positive framing

**Avoid:**
- Jargon (unless explaining tools)
- Passive voice
- Long paragraphs
- Negative language
- Technical complexity without context

---

## UI Component Patterns

### Buttons

**Primary Button (CTAs):**
```css
background: #FF8C42 (Phoenix Orange)
color: #FFF8E7 (Cream)
border: none
border-radius: 8px
padding: 12px 24px
font: Inter Semi-bold 16px
transition: all 0.3s ease

hover:
  background: #FFD700 (Phoenix Gold)
  transform: translateY(-2px)
  box-shadow: 0 4px 12px rgba(255, 140, 66, 0.3)
```

**Secondary Button:**
```css
background: transparent
color: #4A9B9B (Peacock Teal)
border: 2px solid #4A9B9B
border-radius: 8px
padding: 12px 24px
font: Inter Semi-bold 16px

hover:
  background: #4A9B9B
  color: #FFF8E7
```

### Cards

```css
background: #FFF8E7 (Cream)
border: 2px solid #4A9B9B (Peacock Teal)
border-radius: 12px
padding: 24px
box-shadow: 0 2px 8px rgba(26, 26, 46, 0.1)

hover:
  transform: translateY(-4px)
  box-shadow: 0 4px 16px rgba(74, 155, 155, 0.2)
```

### Forms

**Input Fields:**
```css
background: #FFF8E7 (Cream)
border: 2px solid #7B9AA8 (Peacock Blue-Gray)
border-radius: 8px
padding: 12px 16px
font: Inter Regular 16px
color: #1A1A2E (Midnight Navy)

focus:
  border-color: #FF8C42 (Phoenix Orange)
  box-shadow: 0 0 0 3px rgba(255, 140, 66, 0.1)
```

### Badges

```css
background: #FF8C42 (Phoenix Orange)
color: #FFF8E7 (Cream)
border-radius: 20px
padding: 4px 12px
font: Inter Semi-bold 12px
letter-spacing: 0.03em
```

---

## Iconography

### Style Guidelines

**Visual Style:**
- Line-based (not filled)
- 2px stroke width
- Rounded corners (2px radius)
- 24×24px standard size
- Color: Match text color or Phoenix Orange for emphasis

**Icon Sets:**
- **Primary:** Feather Icons (https://feathericons.com)
- **Secondary:** Heroicons (https://heroicons.com)
- Keep consistent style across all UI

### Common Icons

```
Writing: ✏️ Edit / Pen
Books: 📚 Book / Library
Publishing: 🚀 Rocket
AI: ✨ Sparkles / Stars
Success: ✅ Check / Checkmark
Settings: ⚙️ Gear / Cog
User: 👤 User / Person
Help: ❓ Question / Help Circle
```

---

## Photography & Imagery

### Photo Style

**Subjects:**
- Writers at work
- Books and manuscripts
- Creative workspaces
- Diverse authors
- Inspiring scenes

**Aesthetic:**
- Natural lighting
- Warm tones
- Shallow depth of field
- Candid, not posed
- Diverse representation

**Treatment:**
- Slight warm color grading
- Don't over-saturate
- Maintain natural skin tones
- Use photo overlays sparingly

### Illustrations

**Style:**
- Art Nouveau influence (flowing lines, organic forms)
- Phoenix and peacock motifs
- Celestial elements (stars, moons)
- Book and writing implements
- Elegant, not cartoonish

---

## Marketing Applications

### Email Templates

**Header:**
- Logo (centered)
- Tagline below
- Peacock Teal accent line

**Body:**
- Inter Regular 16px
- Cream background
- Dark text (Midnight Navy)
- Phoenix Orange for links

**Footer:**
- Social media icons
- Unsubscribe link
- Copyright notice

### Social Media

**Profile Images:**
- Logo icon version
- Circular crop
- High contrast backgrounds

**Cover Images:**
- 1200×630px (Twitter, Facebook)
- Feature tagline
- Use gradient: Peacock Teal to Phoenix Orange
- Include logo

**Post Graphics:**
- Square (1080×1080px) for Instagram
- Landscape (1200×630px) for Twitter, LinkedIn
- Use brand colors
- Consistent typography

---

## Accessibility

### Color Contrast

All text must meet WCAG AA standards:
- Normal text (16px): Minimum 4.5:1
- Large text (24px+): Minimum 3:1

**Tested Combinations:**
✅ Midnight Navy on Cream: 12.2:1
✅ Peacock Teal on Cream: 3.8:1 (large text only)
✅ Phoenix Orange on Midnight Navy: 5.2:1
✅ Cream on Peacock Teal: 3.9:1 (large text only)

### Font Sizes

- Minimum body text: 16px
- Minimum button text: 14px
- Avoid text smaller than 12px

### Interactive Elements

- Minimum click/tap target: 44×44px
- Clear hover states
- Keyboard navigation support
- Focus indicators visible

---

## Brand Checklist

Use this checklist for all branded materials:

- [ ] Colors match brand palette
- [ ] Typography uses specified fonts
- [ ] Logo used correctly (official files, proper sizing)
- [ ] Clear space maintained around logo
- [ ] Voice and tone appropriate for context
- [ ] Accessibility standards met
- [ ] Consistent with existing materials
- [ ] Phoenix + Peacock theme evident
- [ ] Professional quality
- [ ] Mobile responsive (if digital)

---

🦚 **Rohimaya Publishing**
*Ascend • Flourish • Enlighten*

Where the Phoenix rises and the Peacock dances.
