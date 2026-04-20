import os, subprocess

base = r"C:\Users\DELL\Desktop\wissamxpohub-backend"

# 1. Procfile
with open(os.path.join(base, "Procfile"), 'w') as f:
    f.write("web: gunicorn main:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120")
print("✅ Procfile created")

# 2. runtime.txt
with open(os.path.join(base, "runtime.txt"), 'w') as f:
    f.write("python-3.12.0")
print("✅ runtime.txt created")

# 3. requirements.txt من venv
result = subprocess.run(
    [r".\venv\Scripts\python.exe", "-m", "pip", "freeze"],
    capture_output=True, text=True, cwd=base
)
reqs = result.stdout
if "gunicorn" not in reqs:
    reqs = "gunicorn==21.2.0\n" + reqs
with open(os.path.join(base, "requirements.txt"), 'w') as f:
    f.write(reqs)
print("✅ requirements.txt generated")

# 4. .gitignore
with open(os.path.join(base, ".gitignore"), 'w') as f:
    f.write("venv/\n__pycache__/\n*.pyc\n.env\n*.log\n.DS_Store\nuploads/\n")
print("✅ .gitignore created")

# Summary
print("\n=== FILES READY ===")
for f in ["Procfile","runtime.txt","requirements.txt",".gitignore","main.py"]:
    path = os.path.join(base, f)
    size = os.path.getsize(path) if os.path.exists(path) else "MISSING"
    print(f"  {f}: {size} bytes")
