lines = open('services/claude_service.py', encoding='utf-8').readlines()

# Fix line 471 (index 470)
lines[470] = '            if ts["url"] not in [s if isinstance(s, str) else s.get("url","") for s in source_urls]:\n'

# Fix line 472 - use get with fallback
lines[471] = '                source_urls.append({"name": ts.get("name",""), "url": ts.get("url",""), "type": "tavily"})\n'

open('services/claude_service.py', 'w', encoding='utf-8').writelines(lines)
print('Done - source_urls type fixed')
