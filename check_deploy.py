import os, subprocess

base = r"C:\Users\DELL\Desktop\wissamxpohub-backend"

# تحقق من الملفات الضرورية
files = ["main.py", "requirements.txt", ".env", "Procfile", "runtime.txt"]
print("=== FILE CHECK ===")
for f in files:
    path = os.path.join(base, f)
    exists = "✅" if os.path.exists(path) else "❌ MISSING"
    print(f"{exists}  {f}")

# اطبع requirements.txt لو موجود
req_path = os.path.join(base, "requirements.txt")
if os.path.exists(req_path):
    print("\n=== requirements.txt ===")
    with open(req_path) as f:
        print(f.read())
else:
    print("\n❌ requirements.txt missing — generating...")
    result = subprocess.run(
        ["pip", "freeze"], capture_output=True, text=True,
        cwd=base
    )
    print(result.stdout[:2000])
