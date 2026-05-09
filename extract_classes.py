import os
import re
import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(r"C:\Users\frida\Documents\seo-skill-main\docs\html-css-js\tailwind-html")
OUTPUT_DIR = Path(r"C:\Users\frida\Documents\seo-skill-main\docs\html-css-js\css")

def extract_classes_from_html(filepath):
    """从HTML文件中提取所有class属性中的类名"""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []
    
    # 匹配 class="..." 和 class='...'
    classes = []
    for match in re.finditer(r'class=["\']([^"\']+)["\']', content):
        class_str = match.group(1)
        # 处理多个空格分隔的类名
        class_list = [c.strip() for c in class_str.split() if c.strip()]
        classes.extend(class_list)
    return classes

def main():
    all_classes = Counter()
    module_classes = {}
    
    for html_file in BASE_DIR.rglob("*.html"):
        rel_path = html_file.relative_to(BASE_DIR)
        module = rel_path.parts[0] if rel_path.parts else "root"
        
        classes = extract_classes_from_html(html_file)
        all_classes.update(classes)
        
        if module not in module_classes:
            module_classes[module] = Counter()
        module_classes[module].update(classes)
    
    print(f"Total HTML files scanned: {sum(1 for _ in BASE_DIR.rglob('*.html'))}")
    print(f"Total class occurrences: {sum(all_classes.values())}")
    print(f"Unique classes: {len(all_classes)}")
    print(f"\nTop 20 most common classes:")
    for cls, count in all_classes.most_common(20):
        print(f"  {cls}: {count}")
    
    # 保存完整类名列表
    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / "all-classes.json", "w", encoding="utf-8") as f:
        json.dump({
            "total_unique": len(all_classes),
            "total_occurrences": sum(all_classes.values()),
            "classes": dict(all_classes.most_common())
        }, f, indent=2, ensure_ascii=False)
    
    # 保存各模块类名
    with open(OUTPUT_DIR / "module-classes.json", "w", encoding="utf-8") as f:
        module_data = {}
        for mod, counter in module_classes.items():
            module_data[mod] = {
                "unique": len(counter),
                "classes": dict(counter.most_common())
            }
        json.dump(module_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to {OUTPUT_DIR}/all-classes.json and module-classes.json")

if __name__ == "__main__":
    main()
