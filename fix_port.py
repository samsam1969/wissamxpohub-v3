import re, os

filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# استبدل app.run بنسخة تدعم Render PORT
old_patterns = [
    r"app\.run\(debug=True,\s*port=4000\)",
    r"app\.run\(port=4000,\s*debug=True\)",
    r"app\.run\(debug=True\)",
    r"app\.run\(port=4000\)",
    r"app\.run\(\)",
]

new_run = """if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port, debug=False)"""

# تحقق إن os مستورد
if "import os" not in content:
    content = "import os\n" + content

replaced = False
for pat in old_patterns:
    if re.search(pat, content):
        content = re.sub(pat, new_run.replace("if __name__ == '__main__':\n    ", ""), content)
        replaced = True
        print(f"✅ Replaced: {pat}")
        break

if not replaced:
    # نطبع آخر 20 سطر عشان نشوف الـ app.run
    lines = content.split('\n')
    print("Last 20 lines of main.py:")
    for i, line in enumerate(lines[-20:], len(lines)-20):
        print(f"{i+1}: {line}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
    print("✅ main.py saved")
