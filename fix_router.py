content = """from flask import Blueprint, request, jsonify
from middleware.auth import verify_token
from services.buyers_service import search_buyers, get_product_name
import os
import logging

logger = logging.getLogger(__name__)
buyers_blueprint = Blueprint("buyers", __name__)

def get_api_key():
    return os.getenv("ANTHROPIC_API_KEY", "")

@buyers_blueprint.route("/api/buyers/search", methods=["POST"])
def search_buyers_endpoint():
    user = verify_token(request)
    if not user:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    try:
        data = request.get_json(force=True, silent=True) or {}
        hs_code = str(data.get("hs_code", "")).strip()
        country = str(data.get("country", "")).strip()
        if not hs_code or len(hs_code) < 4:
            return jsonify({"ok": False, "error": "hs_code required (min 4 digits)"}), 400
        if not country:
            return jsonify({"ok": False, "error": "country required"}), 400
        hs_code = hs_code.replace(".", "")[:10]
        country = country[:100]
        api_key = get_api_key()
        if not api_key:
            return jsonify({"ok": False, "error": "ANTHROPIC_API_KEY not configured"}), 500
        logger.info(f"Buyer search: hs={hs_code} country={country}")
        result = search_buyers(hs_code=hs_code, country=country, anthropic_api_key=api_key)
        if result.get("error"):
            return jsonify({"ok": False, "error": result["error"]}), 500
        buyers = result.get("buyers", [])
        return jsonify({"ok": True, "buyers": buyers, "product_name": result.get("product_name", ""), "hs_code": hs_code, "country": country, "count": len(buyers), "cached": result.get("cached", False)})
    except Exception as e:
        logger.error(f"buyers endpoint error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@buyers_blueprint.route("/api/buyers/product-name", methods=["GET"])
def get_product_name_endpoint():
    hs_code = request.args.get("hs_code", "").strip()
    if not hs_code:
        return jsonify({"ok": False, "error": "hs_code required"}), 400
    name = get_product_name(hs_code)
    return jsonify({"ok": True, "hs_code": hs_code, "product_name": name})
"""
with open("routers/buyers.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done - buyers.py fixed")
