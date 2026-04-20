f = open("main.py", encoding="utf-8")
content = f.read()
f.close()

old = """@app.route('/<path:filename>')
def serve_static(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base, filename)"""

new = """PROTECTED = ["PotentialBuyers.html", "ExportIntelligence.html"]

@app.route('/<path:filename>')
def serve_static(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base, filename)"""

content = content.replace(old, new, 1)
open("main.py", "w", encoding="utf-8").write(content)
print("OK: main.py updated")
