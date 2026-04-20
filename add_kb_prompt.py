content = open('services/claude_service.py', encoding='utf-8').read()

old = '=== Layer 1a: ITC Trade Map Data ==='
new = '''{kb_data}

=== Layer 1a: ITC Trade Map Data ==='''

# Find the user_prompt construction and add kb_data
import re
content = re.sub(
    r'(user_prompt\s*=\s*f""")',
    r'\1\n{kb_data}\n',
    content,
    count=1
)

open('services/claude_service.py', 'w', encoding='utf-8').write(content)
print('Done - kb_data added to prompt')
