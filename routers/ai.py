from flask import Blueprint, request, jsonify
from middleware.auth import verify_token
from services import claude_service, credits_service
import asyncio

ai_blueprint = Blueprint("ai", __name__)

# ═══ Registered HS Codes - Egyptian Export Products ═══
REGISTERED_HS_CODES = {
    # Fresh Fruits
    "080510","080521","080529","080540","080550","080410","080420","080430",
    "080440","080450","080610","080711","080719","080810","080910","080930",
    "080940","081010","081020","081030","081090",
    # Frozen Fruits
    "081110","081120","081190",
    # Dried Fruits
    "081310","081320","081340","081350",
    # Fresh Vegetables
    "070200","070310","070320","070390","070410","070490","070511","070519",
    "070610","070690","070700","070810","070820","070910","070920","070930",
    "070940","070951","070960","070970","070993","071090",
    # Frozen Vegetables
    "071010","071021","071022","071040","071080",
    # Other Egyptian exports
    "100630","100610","090111","030617","020130","040221","170111","160414",
    "520811","620520","630211","190190","200410","200899"
}



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
    hs_code_check = (body or {}).get("hs_code", "").strip()

    # ═══ Security: Validate HS Code ═══
    if not hs_code_check:
        return jsonify({"error": "HS Code is required"}), 400
    if hs_code_check not in REGISTERED_HS_CODES:
        return jsonify({
            "error": f"HS Code '{hs_code_check}' is not registered.",
            "message": "Only registered Egyptian export products are supported.",
        }), 422
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