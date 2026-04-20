content = open('routers/admin.py', encoding='utf-8').read()

old = 'admin_blueprint = Blueprint(\'admin\', __name__)'
new = '''admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.get('/api/auth/my-plan')
def my_plan():
    from middleware.auth import verify_token
    from flask import request, jsonify
    token = verify_token(request)
    if not token:
        return jsonify({'error': 'unauthorized'}), 401
    user_id = token.get('sub')
    from services.credits_service import get_user_plan
    plan = get_user_plan(user_id)
    return jsonify(plan)'''

content = content.replace(old, new, 1)
open('routers/admin.py', 'w', encoding='utf-8').write(content)
print('Done - my-plan endpoint added')
