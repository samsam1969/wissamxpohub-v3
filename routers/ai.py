from flask import Blueprint, request, jsonify
from middleware.auth import verify_token
from services import claude_service, credits_service
import asyncio

ai_blueprint = Blueprint("ai", __name__)

def run(coro):
    return asyncio.run(coro)

@ai_blueprint.post("/export-advisor")
def export_advisor():
    token_payload = verify_token(request)
    if not token_payload:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = token_payload.get("sub", "")
    email = token_payload.get("email", "")
    body = request.get_json()
    run(credits_service.ensure_user_profile(user_id, email))
    try:
        remaining = run(credits_service.deduct_credit(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 402
    try:
        result = run(claude_service.get_export_advice(
            body.get("product"), body.get("hs_code"),
            body.get("target_market"), body.get("company_info", ""),
            body.get("sources_mode", "auto")
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # Save to history
    try:
        from services.credits_service import save_report_history
        save_report_history(user_id, email,
            body.get("product",""), body.get("hs_code",""),
            body.get("target_market",""),
            result["advisor"][:500] if result.get("advisor") else "")
    except Exception as e:
        pass
    return jsonify({"advisor": result["advisor"], "plan": result["plan"], "remaining": remaining, "sourcesUsed": result["sourcesUsed"], "sourceUrls": result["sourceUrls"]})

@ai_blueprint.post("/buyer-message")
def buyer_message():
    token_payload = verify_token(request)
    if not token_payload:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = token_payload.get("sub", "")
    email = token_payload.get("email", "")
    body = request.get_json()
    run(credits_service.ensure_user_profile(user_id, email))
    try:
        remaining = run(credits_service.deduct_credit(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 402
    try:
        result = run(claude_service.get_buyer_message(
            body.get("product"), body.get("hs_code"),
            body.get("target_market"), body.get("company_info", ""),
            body.get("tone", "professional")
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"advisor": result["advisor"], "plan": result["plan"], "remaining": remaining, "sourcesUsed": result["sourcesUsed"], "sourceUrls": result["sourceUrls"]})

@ai_blueprint.post("/opportunity-scanner")
def opportunity_scanner():
    token_payload = verify_token(request)
    if not token_payload:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = token_payload.get("sub", "")
    email = token_payload.get("email", "")
    body = request.get_json()
    run(credits_service.ensure_user_profile(user_id, email))
    try:
        remaining = run(credits_service.deduct_credit(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 402
    try:
        result = run(claude_service.get_opportunity_scan(
            body.get("product"), body.get("hs_code", "auto")
        ))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"product_analyzed": result.get("product_analyzed", ""), "hs_code": result.get("hs_code", ""), "analysis_year": result.get("analysis_year", "2024"), "markets": result.get("markets", []), "summary": result.get("summary", ""), "sourcesUsed": result.get("sourcesUsed", []), "remaining": remaining})