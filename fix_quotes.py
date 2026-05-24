import glob
import os

path = r'd:\laragon\www\api_mejorada\citas\templates\citas\*.html'
for filepath in glob.glob(path):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "\\'" in content:
        content = content.replace("\\'", "'")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed quotes in {os.path.basename(filepath)}")
