content = open('services/claude_service.py', encoding='utf-8').read()

old = '    # ── Layer 1: Comtrade data'

new = '''    # ── Layer 0: Knowledge Base (Internal - Highest Priority)
    kb_data = ""
    try:
        from services.knowledge_service import search_knowledge_base
        kb_data = search_knowledge_base(
            hs_code=hs_code[:6] if hs_code else None,
            market=target_market,
        )
    except Exception as e:
        kb_data = ""

    # ── Layer 1: Comtrade data'''

content = content.replace(old, new, 1)
open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done - Layer 0 KB added')
