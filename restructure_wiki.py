import re
import os

wiki_dir = 'wiki'
files = [f for f in os.listdir(wiki_dir) if f.endswith('.html')]

for fname in files:
    path = os.path.join(wiki_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Modify .main: add margin-right and border-right
    # Handle both 260px and var(--sidebar-width) variants
    content = content.replace(
        'margin-left: 260px; flex: 1; max-width: 800px;',
        'margin-left: var(--sidebar-width); margin-right: var(--sidebar-width); flex: 1; max-width: 800px;'
    )
    # Some files already use var, only add margin-right if not present
    if 'margin-right:' not in content.split('@media')[0]:
        content = content.replace(
            'margin-left: var(--sidebar-width); flex: 1; max-width: 800px;',
            'margin-left: var(--sidebar-width); margin-right: var(--sidebar-width); flex: 1; max-width: 800px;'
        )

    # Add border-right to .main
    content = content.replace(
        'border-left: 1px solid var(--border); }',
        'border-left: 1px solid var(--border); border-right: 1px solid var(--border); }'
    )

    # 2. Add toc-sidebar CSS before @media (max-width: 900px)
    toc_css = '''        .toc-sidebar {
            width: var(--sidebar-width);
            background: var(--card);
            border-left: 1px solid var(--border);
            padding: 28px 20px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            top: 0; right: 0; z-index: 100;
        }
        .toc-sidebar h2 {
            font-size: 0.85rem;
            color: var(--primary);
            margin-bottom: 16px;
            padding-left: 10px;
            font-weight: 600;
        }
        .toc-sidebar nav ul { list-style: none; margin: 0; }
        .toc-sidebar nav li { margin: 4px 0; }
        .toc-sidebar nav a {
            display: block; color: var(--foreground); text-decoration: none;
            font-size: 0.85rem; padding: 5px 10px; border-radius: 6px;
            transition: background .15s, color .15s;
        }
        .toc-sidebar nav a:hover { background: var(--primary-8); color: var(--primary); }
        .toc-sidebar nav a.active { background: var(--primary-12); color: var(--primary); font-weight: 600; }
        .toc-sidebar .nav-group { margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--border); }
        .toc-sidebar .nav-group:first-child { margin-top: 0; padding-top: 0; border-top: none; }
        .toc-sidebar .nav-group-title {
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em;
            color: var(--muted-foreground); margin-bottom: 8px; padding-left: 10px;
        }
        @media (max-width: 1200px) {
            .toc-sidebar { display: none; }
            .main { margin-right: 0; border-right: none; }
        }
'''
    if '@media (max-width: 1200px)' not in content:
        content = content.replace(
            '        @media (max-width: 900px) {',
            toc_css + '        @media (max-width: 900px) {'
        )

    # 3. Split nav groups inside sidebar
    sidebar_start = content.find('<aside class="sidebar">')
    if sidebar_start == -1:
        print(f'Skip {fname}: no sidebar')
        continue

    sidebar_end = content.find('</aside>', sidebar_start)
    if sidebar_end == -1:
        print(f'Skip {fname}: no sidebar end')
        continue
    sidebar_end += len('</aside>')

    sidebar_html = content[sidebar_start:sidebar_end]

    # Extract nav content from sidebar
    nav_match = re.search(r'<nav>(.*?)</nav>', sidebar_html, re.DOTALL)
    if not nav_match:
        print(f'Skip {fname}: no nav in sidebar')
        continue

    nav_html = nav_match.group(1)

    # Split nav groups
    # Pattern matches: <div class="nav-group"> ... </ul> </div>
    group_pattern = r'<div class="nav-group">.*?</ul>\s*</div>'
    groups = re.findall(group_pattern, nav_html, re.DOTALL)

    wiki_nav_group = None
    article_groups = []
    for g in groups:
        if 'Wiki' in g:
            wiki_nav_group = g
        else:
            article_groups.append(g)

    if not wiki_nav_group:
        print(f'Skip {fname}: no Wiki nav group found')
        continue

    # Build new sidebar nav
    new_nav = f'<nav>\n            {wiki_nav_group}\n        </nav>'
    new_sidebar = sidebar_html.replace(nav_match.group(0), new_nav)

    # Build toc-sidebar
    article_groups_str = '\n            '.join(article_groups)
    toc_sidebar_html = f'''    <aside class="toc-sidebar">
        <h2>目录</h2>
        <nav>
            {article_groups_str}
        </nav>
    </aside>'''

    # Replace sidebar in content
    content = content[:sidebar_start] + new_sidebar + content[sidebar_end:]

    # Insert toc-sidebar right after sidebar
    # Find new sidebar end position
    new_sidebar_end = content.find('</aside>', sidebar_start) + len('</aside>')
    content = content[:new_sidebar_end] + '\n' + toc_sidebar_html + content[new_sidebar_end:]

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Done: {fname}')
    else:
        print(f'No changes: {fname}')
