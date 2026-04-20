import re

filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# نبحث عن كل المحتوى المتعلق بـ adminLinks
patterns = [
    r'adminLinks',
    r'DOMContentLoaded',
    r'wissamxpo',
    r'checkAdmin',
    r'isAdmin',
    r'user_email',
    r'userEmail',
]

lines = content.split('\n')
for i, line in enumerate(lines):
    for p in patterns:
        if p.lower() in line.lower():
            print(f"Line {i+1}: {line.strip()}")
            break
