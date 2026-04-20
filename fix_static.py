content = open("main.py", encoding="utf-8").read()
if "send_from_directory" not in content:
    old = "from flask import Flask"
    new = "from flask import Flask, send_from_directory\nimport os"
    content = content.replace(old, new, 1)

    # Add static file route
    route = """
@app.route('/<path:filename>')
def serve_static(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base, filename)

"""
    # Insert before first @app.route or before if __name__
    if "if __name__" in content:
        content = content.replace("if __name__", route + "if __name__", 1)

    open("main.py", "w", encoding="utf-8").write(content)
    print("main.py updated - static file serving added")
else:
    print("Already has send_from_directory")
