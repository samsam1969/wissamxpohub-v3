import os
from supabase import create_client
from functools import wraps
from flask import request, jsonify

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_KEY'))

PLANS = {
    'starter': {'limit': 5,   'price': 299},
    'pro':     {'limit': 25,  'price': 599},
    'agency':  {'limit': 100, 'price': 1490},
}

def get_user_plan(user_id):
    res = supabase.table('user_plans').select('*').eq('user_id', user_id).single().execute()
    if not res.data:
        supabase.table('user_plans').insert({'user_id': user_id, 'plan_type': 'starter', 'reports_limit': 5, 'price_egp': 299}).execute()
        return {'plan_type': 'starter', 'reports_used': 0, 'reports_limit': 5}
    return res.data

def check_and_increment(user_id):
    plan = get_user_plan(user_id)
    if plan['reports_used'] >= plan['reports_limit']:
        return False, plan
    supabase.table('user_plans').update({'reports_used': plan['reports_used'] + 1}).eq('user_id', user_id).execute()
    plan['reports_used'] += 1
    return True, plan

def require_credits(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = request.headers.get('X-User-Id')
        if not user_id:
            return jsonify({'error': 'unauthorized'}), 401
        allowed, plan = check_and_increment(user_id)
        if not allowed:
            return jsonify({
                'error': 'limit_reached',
                'message': f'وصلت للحد الأقصى ({plan[\"reports_limit\"]}) تقارير لباقة {plan[\"plan_type\"]}',
                'plan': plan,
                'upgrade_url': '/upgrade'
            }), 403
        return f(*args, **kwargs)
    return decorated
