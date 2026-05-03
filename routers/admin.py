import os, sys
from flask import Blueprint, request, jsonify, send_from_directory
from middleware.auth import verify_token

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.get('/admin/crm')
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

@admin_blueprint.get('/api/auth/check-feature/<feature>')
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
    return jsonify(plan)

ADMIN_EMAIL = 'wissamxpo@outlook.com'

def require_admin(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = verify_token(request)
        if not token or token.get('email') != ADMIN_EMAIL:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@admin_blueprint.get('/admin/knowledge')
def admin_page():
    return send_from_directory('.', 'admin_knowledge.html')

@admin_blueprint.get('/api/admin/knowledge')
@require_admin
def list_knowledge():
    from services.knowledge_service import supabase
    res = supabase.table('knowledge_base').select('*').order('priority', desc=True).execute()
    return jsonify(res.data)

@admin_blueprint.post('/api/admin/knowledge')
@require_admin
def add_knowledge():
    from services.knowledge_service import supabase
    data = request.get_json()
    res = supabase.table('knowledge_base').insert({
        'category':    data.get('category'),
        'subcategory': data.get('subcategory'),
        'hs_code':     data.get('hs_code') or None,
        'market':      data.get('market') or None,
        'title':       data.get('title'),
        'content':     data.get('content'),
        'source':      data.get('source'),
        'priority':    int(data.get('priority', 5)),
        'is_active':   True
    }).execute()
    return jsonify({'ok': True})

@admin_blueprint.put('/api/admin/knowledge/<id>')
@require_admin
def update_knowledge(id):
    from services.knowledge_service import supabase
    data = request.get_json()
    supabase.table('knowledge_base').update({
        'category':  data.get('category'),
        'hs_code':   data.get('hs_code') or None,
        'market':    data.get('market') or None,
        'title':     data.get('title'),
        'content':   data.get('content'),
        'source':    data.get('source'),
        'priority':  int(data.get('priority', 5)),
        'is_active': data.get('is_active', True)
    }).eq('id', id).execute()
    return jsonify({'ok': True})

@admin_blueprint.delete('/api/admin/knowledge/<id>')
@require_admin
def delete_knowledge(id):
    from services.knowledge_service import supabase
    supabase.table('knowledge_base').update({'is_active': False}).eq('id', id).execute()
    return jsonify({'ok': True})
