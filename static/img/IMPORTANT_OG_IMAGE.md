# OG Image Note

The site now references `og-default.png` instead of `og-default.svg` for better Google search results display.

## Required Action

You need to create a PNG image file at:
`static/img/og-default.png`

### Specifications:

- **Size**: 1200 x 630 pixels
- **Format**: PNG or JPG
- **Content**: Should include:
  - NSA logo/branding
  - Text: "NUST Society of Artificial Intelligence"
  - Tagline: "Learn. Build. Evolve."
  - Modern gradient background (cyan/purple/green tones)

### Quick Fix Option:

You can temporarily copy an existing image or create one using:

- Canva (use "Open Graph" preset)
- Figma
- Any image editor

### Alternative:

If you want to keep using SVG, you can revert `templates/layout.html` line 29 back to:

```
{% set og_image = base_url ~ url_for('static', filename='img/og-default.svg') %}
```

But note that SVG images may not display properly in Google search previews.
