filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\main.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old = '    app.run(host="0.0.0.0", port=4000, debug=True)'
new = '    port = int(os.environ.get("PORT", 4000))\n    app.run(host="0.0.0.0", port=port, debug=False)'

if old in content:
    content = content.replace(old, new)
    print("✅ app.run fixed for Render")
else:
    print("❌ Line not found exactly — printing last 5 lines:")
    print('\n'.join(content.split('\n')[-6:]))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
    print("✅ main.py saved")
