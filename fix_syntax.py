with open('services/claude_service.py', encoding='utf-8') as f:
    content = f.read()

# Fix the broken regex strings
bad1 = 'text = re.sub(r"^```[a-z]*\n?", "", text, flags=re.MULTILINE)'
bad2 = 'text = re.sub(r"\n?```$", "", text, flags=re.MULTILINE)'

content = content.replace(bad1, 'text = re.sub(r"```[a-z]*", "", text)')
content = content.replace(bad2, 'text = re.sub(r"```", "", text)')

# If the above didn't work, find and fix by line
lines = content.split('\n')
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if '```[a-z]*' in line and 'sub' in line and line.count('"') < 4:
        new_lines.append('        text = re.sub(r"```[a-z]*", "", text)')
        skip_next = True
    elif skip_next and '```$' in line and 'sub' in line:
        new_lines.append('        text = re.sub(r"```", "", text)')
        skip_next = False
    elif skip_next and line.strip().startswith('text = re.sub'):
        new_lines.append('        text = re.sub(r"```", "", text)')
        skip_next = False
    else:
        new_lines.append(line)
        skip_next = False

content = '\n'.join(new_lines)

with open('services/claude_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import ast
try:
    ast.parse(content)
    print('SUCCESS: No syntax errors')
except SyntaxError as e:
    print(f'STILL HAS ERROR: line {e.lineno}: {e.msg}')