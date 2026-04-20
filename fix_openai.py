f = open("services/deepsearch_service.py", encoding="utf-8")
content = f.read()
f.close()

# Fix: use correct OpenAI chat completions endpoint with web search
old_payload = '''        payload = json.dumps({
            "model": "gpt-4o-mini",
            "tools": [{"type": "web_search_preview"}],
            "input": query,
            "max_output_tokens": 1500
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/responses",'''

new_payload = '''        payload = json.dumps({
            "model": "gpt-4o-mini-search-preview",
            "messages": [{"role":"user","content": query}],
            "max_tokens": 800
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",'''

if old_payload in content:
    content = content.replace(old_payload, new_payload, 1)
    print("OK: endpoint fixed to chat/completions")
else:
    print("FAIL - manual fix needed")

# Fix response parsing for chat completions
old_parse = '''            output = data.get("output", [])
            texts = []
            for item in output:
                if item.get("type") == "message":
                    for c in item.get("content", []):
                        if c.get("type") == "output_text":
                            texts.append(c.get("text",""))
            return "\\n".join(texts) if texts else "[No results]"'''

new_parse = '''            choices = data.get("choices", [])
            texts = [c.get("message",{}).get("content","") for c in choices]
            return "\\n".join(t for t in texts if t) or "[No results]"'''

if old_parse in content:
    content = content.replace(old_parse, new_parse, 1)
    print("OK: response parsing fixed")

open("services/deepsearch_service.py", "w", encoding="utf-8").write(content)
print("Done")
