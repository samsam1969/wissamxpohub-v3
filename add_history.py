content = open('routers/ai.py', encoding='utf-8').read()

old = '    return jsonify({"advisor": result["advisor"], "plan": result["plan"], "remaining": remaining, "sourcesUsed": result["sourcesUsed"], "sourceUrls": result["sourceUrls"]})'

new = '''    # Save to history
    try:
        from services.credits_service import save_report_history
        save_report_history(user_id, email,
            body.get("product",""), body.get("hs_code",""),
            body.get("target_market",""),
            result["advisor"][:500] if result.get("advisor") else "")
    except Exception as e:
        pass
    return jsonify({"advisor": result["advisor"], "plan": result["plan"], "remaining": remaining, "sourcesUsed": result["sourcesUsed"], "sourceUrls": result["sourceUrls"]})'''

content = content.replace(old, new, 1)
open('routers/ai.py', 'w', encoding='utf-8').write(content)
print('Done - history saving added')
