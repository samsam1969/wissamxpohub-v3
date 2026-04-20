content = open('routers/admin.py', encoding='utf-8').read()

old = "@admin_blueprint.get('/api/auth/check-feature/<feature>')"

new = """@admin_blueprint.get('/admin/crm')
def crm_page():
    return send_from_directory('.', 'admin_crm.html')

@admin_blueprint.get('/api/admin/crm/users')
def get_crm_users():
    from middleware.auth import verify_token
    from flask import request, jsonify
    token = verify_token(request)
    if not token or token.get('email') != 'wissamxpo@outlook.com':
        return jsonify({'error': 'Unauthorized'}), 401
    from services.knowledge_service import supabase
    profiles = supabase.table('user_profiles').select('*').execute().data or []
    plans    = supabase.table('user_plans').select('*').execute().data or []
    plans_map = {p['user_id']: p for p in plans}
    result = []
    for p in profiles:
        uid = p.get('user_id')
        plan = plans_map.get(uid, {})
        result.append({
            'user_id':       uid,
            'email':         p.get('email',''),
            'full_name':     p.get('full_name',''),
            'phone':         p.get('phone',''),
            'company':       p.get('company',''),
            'plan_type':     plan.get('plan_type', p.get('plan_type','free')),
            'reports_used':  plan.get('reports_used',0),
            'reports_limit': plan.get('reports_limit',1),
            'price_egp':     plan.get('price_egp',0),
            'sub_end':       plan.get('sub_end'),
            'total_reports': p.get('total_reports',0),
            'last_login':    p.get('last_login'),
            'notes':         p.get('notes',''),
        })
    result.sort(key=lambda x: x.get('plan_type','free'))
    return jsonify(result)

@admin_blueprint.post('/api/admin/crm/update-user')
def update_crm_user():
    from middleware.auth import verify_token
    from flask import request, jsonify
    token = verify_token(request)
    if not token or token.get('email') != 'wissamxpo@outlook.com':
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()
    uid  = data.get('user_id')
    from services.knowledge_service import supabase
    supabase.table('user_plans').update({
        'plan_type':     data.get('plan_type'),
        'reports_limit': data.get('reports_limit'),
        'price_egp':     data.get('price_egp'),
        'sub_end':       data.get('sub_end'),
    }).eq('user_id', uid).execute()
    if data.get('notes') is not None:
        supabase.table('user_profiles').update({
            'notes': data.get('notes')
        }).eq('user_id', uid).execute()
    return jsonify({'ok': True})

@admin_blueprint.get('/api/auth/check-feature/<feature>')"""

content = content.replace(old, new, 1)
open('routers/admin.py', 'w', encoding='utf-8').write(content)
print('Done - CRM endpoints added')
