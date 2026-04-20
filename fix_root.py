content = open('main.py', encoding='utf-8').read()

old = '@app.get("/health")'

new = '''@app.get("/")
def index():
    return send_from_directory(".", "WissamXpoHub_V3_Frontend_FIXED.html")

@app.get("/health")'''

content = content.replace(old, new, 1)
open('main.py', 'w', encoding='utf-8').write(content)
print('Done - root route added')
