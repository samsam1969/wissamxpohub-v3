f = open("main.py", encoding="utf-8")
content = f.read()
f.close()

old_import = "from routers.ai import ai_blueprint"
new_import = "from routers.ai import ai_blueprint\nfrom routers.buyers import buyers_blueprint"

old_register = "app.register_blueprint(ai_blueprint)"
new_register = "app.register_blueprint(ai_blueprint)\napp.register_blueprint(buyers_blueprint)"

changed = 0
if "buyers_blueprint" not in content:
    content = content.replace(old_import, new_import, 1)
    content = content.replace(old_register, new_register, 1)
    changed = 1

open("main.py", "w", encoding="utf-8").write(content)
print("Done" if changed else "Already registered")
