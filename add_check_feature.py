content = open('routers/admin.py', encoding='utf-8').read()

old = "@admin_blueprint.get('/api/auth/my-plan')"

new = '''@admin_blueprint.get('/api/auth/check-feature/<feature>')
def check_feature(feature):
    from middleware.auth import verify_token
    from flask import request, jsonify
    token = verify_token(request)
    if not token:
        return jsonify({'allowed': False, 'reason': 'not_logged_in'}), 401
    user_id = token.get('sub')
    from services.credits_service import has_feature, get_user_plan
    allowed = has_feature(user_id, feature)
    plan = get_user_plan(user_id)
    return jsonify({
        'allowed': allowed,
        'plan_type': plan.get('plan_type', 'free'),
        'reports_used': plan.get('reports_used', 0),
        'reports_limit': plan.get('reports_limit', 1)
    })

@admin_blueprint.get('/api/auth/my-plan')'''

content = content.replace(old, new, 1)
open('routers/admin.py', 'w', encoding='utf-8').write(content)
print('Done - check-feature endpoint added')
