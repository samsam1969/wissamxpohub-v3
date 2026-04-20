content = open('services/claude_service.py', encoding='utf-8').read()

old = '''    return {
        "advisor": advisor_text,
        "plan": _extract_plan_steps(advisor_text),
        "sourcesUsed": sources_used,
        "sourceUrls": source_urls,
        "tokensUsed": message.usage.input_tokens + message.usage.output_tokens
    }'''

new = '''    # Merge Tavily sources with existing sources
    if tavily_sources:
        for ts in tavily_sources:
            if ts["url"] not in [s.get("url","") for s in source_urls]:
                source_urls.append({"name": ts["title"], "url": ts["url"], "type": "tavily"})
        sources_used.append("Tavily Web Intelligence 2024-2026")

    return {
        "advisor": advisor_text,
        "plan": _extract_plan_steps(advisor_text),
        "sourcesUsed": sources_used,
        "sourceUrls": source_urls,
        "tokensUsed": message.usage.input_tokens + message.usage.output_tokens
    }'''

content = content.replace(old, new)
open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done - Tavily sources added to response')
