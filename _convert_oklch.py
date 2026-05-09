import re
import numpy as np

# Correct Oklab -> XYZ matrices (W3C CSS Color Module Level 4)
M_oklab_to_lms_c = np.array([
    [1.0,  0.3963377774,  0.2158037573],
    [1.0, -0.1055613458, -0.0638541728],
    [1.0, -0.0894841775, -1.2914855480]
])
M_lms_to_xyz = np.array([
    [ 1.2270138511035211, -0.5577992887910691,  0.2812561489664677],
    [-0.0405801784237345,  1.1122568696168821, -0.0716766786656241],
    [-0.0763812845057069, -0.4214813234181464,  1.5861632204405947]
])
M_xyz_to_srgb = np.array([
    [ 3.240969941904522, -1.537383177570093, -0.498610760293056],
    [-0.969243636280880,  1.875967501507721,  0.041555057407176],
    [ 0.055630079696993, -0.203976958888976,  1.056971514242878]
])

def oklab_to_xyz(L, a, b):
    lms_c = M_oklab_to_lms_c @ np.array([L, a, b])
    lms = lms_c ** 3
    xyz = M_lms_to_xyz @ lms
    return xyz

def xyz_to_srgb(x, y, z):
    rgb_lin = M_xyz_to_srgb @ np.array([x, y, z])
    rgb = []
    for v in rgb_lin:
        if v <= 0.0031308:
            rgb.append(v * 12.92)
        else:
            rgb.append(1.055 * (v ** (1/2.4)) - 0.055)
    return rgb

def oklch_to_hex(L, C, h):
    h_rad = np.deg2rad(h)
    a = C * np.cos(h_rad)
    b = C * np.sin(h_rad)
    xyz = oklab_to_xyz(L, a, b)
    rgb = xyz_to_srgb(*xyz)
    rgb = [max(0, min(1, c)) for c in rgb]
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255+0.5), int(rgb[1]*255+0.5), int(rgb[2]*255+0.5))

def repl_oklch(m):
    L = float(m.group(1))
    C = float(m.group(2))
    h = float(m.group(3))
    alpha = m.group(4)
    hex_color = oklch_to_hex(L, C, h)
    if alpha:
        a = int(float(alpha) * 255 + 0.5)
        return hex_color + '{:02x}'.format(a)
    return hex_color

# Read source themes.css
with open(r'C:\Users\frida\Documents\caifangwen.github.io\assets\css\themes.css', 'r', encoding='utf-8') as f:
    src = f.read()

# Convert all oklch -> hex
pattern = r'oklch\(\s*([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)(?:\s*/\s*([0-9.]+))?\s*\)'
src_hex = re.sub(pattern, repl_oklch, src)

# Extract all CSS rule blocks (selector -> body)
blocks = re.findall(r'((?::root|\.dark|\[data-theme="[^"]+"\](?:\.dark)?))\s*\{([^}]*)\}', src_hex)

# Build theme_map preserving order
theme_map = {}
for sel, body in blocks:
    theme_map[sel.strip()] = body.strip()

# Helpers to build output
alias_light = '''  --primary: var(--color-primary);
  --primary-foreground: var(--color-primary-foreground);
  --secondary: var(--color-secondary);
  --secondary-foreground: var(--color-secondary-foreground);
  --accent: var(--color-accent);
  --accent-foreground: var(--color-accent-foreground);
  --background: var(--color-background);
  --foreground: var(--color-foreground);
  --muted: var(--color-muted);
  --muted-foreground: var(--color-muted-foreground);
  --border: var(--color-border);
  --card: var(--color-card);
  --card-foreground: var(--color-card-foreground);
  --popover: var(--color-popover);
  --popover-foreground: var(--color-popover-foreground);
  --destructive: #ef4444;
  --destructive-foreground: #ffffff;
  --input: var(--color-border);
  --ring: var(--color-primary);
  --success: var(--color-tip);
  --warning: var(--color-warning);
  --danger: var(--color-caution);
  --info: var(--color-note);
  --important: var(--color-important);
  --code-bg: #18181b;
  --code-text: #f4f4f5;
  --primary-5: rgba(24,24,27,0.05);
  --primary-8: rgba(24,24,27,0.08);
  --primary-10: rgba(24,24,27,0.10);
  --primary-12: rgba(24,24,27,0.12);
  --primary-15: rgba(24,24,27,0.15);
  --primary-20: rgba(24,24,27,0.20);
  --primary-30: rgba(24,24,27,0.30);
  --success-5: rgba(16,185,129,0.05);
  --success-15: rgba(16,185,129,0.15);
  --warning-5: rgba(245,158,11,0.05);
  --warning-15: rgba(245,158,11,0.15);
  --danger-5: rgba(239,68,68,0.05);
  --danger-15: rgba(239,68,68,0.15);
  --shadow: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px -1px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.08);'''

alias_dark = '''  --primary: var(--color-primary);
  --primary-foreground: var(--color-primary-foreground);
  --secondary: var(--color-secondary);
  --secondary-foreground: var(--color-secondary-foreground);
  --accent: var(--color-accent);
  --accent-foreground: var(--color-accent-foreground);
  --background: var(--color-background);
  --foreground: var(--color-foreground);
  --muted: var(--color-muted);
  --muted-foreground: var(--color-muted-foreground);
  --border: var(--color-border);
  --card: var(--color-card);
  --card-foreground: var(--color-card-foreground);
  --popover: var(--color-popover);
  --popover-foreground: var(--color-popover-foreground);
  --destructive: #f87171;
  --destructive-foreground: #18181b;
  --input: var(--color-border);
  --ring: var(--color-primary);
  --success: var(--color-tip);
  --warning: var(--color-warning);
  --danger: var(--color-caution);
  --info: var(--color-note);
  --important: var(--color-important);
  --code-bg: #09090b;
  --code-text: #f4f4f5;
  --primary-5: rgba(250,250,250,0.05);
  --primary-8: rgba(250,250,250,0.08);
  --primary-10: rgba(250,250,250,0.10);
  --primary-12: rgba(250,250,250,0.12);
  --primary-15: rgba(250,250,250,0.15);
  --primary-20: rgba(250,250,250,0.20);
  --primary-30: rgba(250,250,250,0.30);
  --success-5: rgba(52,211,153,0.05);
  --success-15: rgba(52,211,153,0.15);
  --warning-5: rgba(251,191,36,0.05);
  --warning-15: rgba(251,191,36,0.15);
  --danger-5: rgba(248,113,113,0.05);
  --danger-15: rgba(248,113,113,0.15);
  --shadow: 0 1px 3px 0 rgba(0,0,0,0.2), 0 1px 2px -1px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -1px rgba(0,0,0,0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.4), 0 4px 6px -2px rgba(0,0,0,0.4);'''

out = '''/* ==========================================================================
   FR Theme System — Multi-theme palette ported from caifangwen.github.io
   All oklch values converted to hex for maximum browser compatibility
   ========================================================================== */

/* --------------------------------------------------------------------------
   §1  Default Light (no data-theme)
   -------------------------------------------------------------------------- */
:root {
''' + theme_map.get(':root', '') + '\n' + alias_light + '''
}

/* --------------------------------------------------------------------------
   §2  Default Dark
   -------------------------------------------------------------------------- */
[data-theme="dark"] {
''' + theme_map.get('.dark', '') + '\n' + alias_dark + '''
}

/* --------------------------------------------------------------------------
   §3  Named Light Themes
   -------------------------------------------------------------------------- */
'''

named = ['claude', 'bumblebee', 'emerald', 'nord', 'sunset', 'abyss', 'dracula', 'amethyst', 'slate', 'twitter']
for name in named:
    sel = f'[data-theme="{name}"]'
    if sel in theme_map:
        out += f'{sel} {{\n' + theme_map[sel] + '\n}\n\n'

out += '''/* --------------------------------------------------------------------------
   §4  Named Dark Themes
   -------------------------------------------------------------------------- */
'''
for name in named:
    sel = f'[data-theme="{name}"].dark'
    if sel in theme_map:
        # Map to data-theme="name-dark" for consistency with our JS
        out += f'[data-theme="{name}-dark"] {{\n' + theme_map[sel] + '\n}\n\n'

# Add alias propagation for named light themes
out += '''/* --------------------------------------------------------------------------
   §5  Alias propagation for named light themes
   -------------------------------------------------------------------------- */
[data-theme="claude"],
[data-theme="bumblebee"],
[data-theme="emerald"],
[data-theme="nord"],
[data-theme="sunset"],
[data-theme="abyss"],
[data-theme="dracula"],
[data-theme="amethyst"],
[data-theme="slate"],
[data-theme="twitter"] {
''' + alias_light + '''
}

/* --------------------------------------------------------------------------
   §6  Alias propagation for named dark themes
   -------------------------------------------------------------------------- */
[data-theme="claude-dark"],
[data-theme="bumblebee-dark"],
[data-theme="emerald-dark"],
[data-theme="nord-dark"],
[data-theme="sunset-dark"],
[data-theme="abyss-dark"],
[data-theme="dracula-dark"],
[data-theme="amethyst-dark"],
[data-theme="slate-dark"],
[data-theme="twitter-dark"] {
''' + alias_dark + '''
}
'''

with open(r'C:\Users\frida\Documents\seo-skill-main\docs\html-css-js\fr-themes.css', 'w', encoding='utf-8') as f:
    f.write(out)

print("Done. Rebuilt fr-themes.css correctly.")
