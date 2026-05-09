# Huahao Blog Component Library

## File Structure

```
huahao-blog/
├── index.html                 # Component demo / documentation page
├── hh-variables.css           # Design tokens (colors, fonts, spacing)
├── hh-base.css                # Article base styles (.hh-post)
├── hh-components.css          # 46 content components
└── hh-wordpress-bundle.css    # Concatenated file for WP Additional CSS
```

## WordPress Usage

1. Open `hh-wordpress-bundle.css`
2. Copy the entire contents
3. Paste into: **Appearance → Customize → Additional CSS**
4. Click Publish

## Component Demo

Open `index.html` in a browser to see all 46 components rendered.

## Design Tokens

Edit `hh-variables.css` to customize brand colors:
- `--hh-ink`: Primary text
- `--hh-text`: Body text
- `--hh-border`: Borders
- `--hh-font-head`: Heading font (Georgia)
- `--hh-font-body`: Body font (Roboto)
