f = open("main.py", encoding="utf-8")
content = f.read()
f.close()

old = 'app.register_blueprint(ai_blueprint, url_prefix="/api/ai")'
new = 'app.register_blueprint(ai_blueprint, url_prefix="/api/ai")\napp.register_blueprint(buyers_blueprint)'

content = content.replace(old, new, 1)
open("main.py", "w", encoding="utf-8").write(content)
print("Done")
print(open("main.py", encoding="utf-8").read())
