filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# نطبع الكود حول السطر 3178 - 3210 لنشوف الـ full context
print("=== CONTEXT (lines 3175-3215) ===")
for i, line in enumerate(lines[3174:3215], start=3175):
    print(f"{i}: {line}", end='')
