content = open('main.py', encoding='utf-8').read()

if 'admin_blueprint' not in content:
    content = content.replace(
        'from routers.ai import ai_blueprint',
        'from routers.ai import ai_blueprint\nfrom routers.admin import admin_blueprint'
    )
    content = content.replace(
        'app.register_blueprint(ai_blueprint',
        'app.register_blueprint(admin_blueprint)\napp.register_blueprint(ai_blueprint'
    )
    open('main.py', 'w', encoding='utf-8').write(content)
    print('Done - admin registered')
else:
    print('Already registered')
