content = open('main.py', encoding='utf-8').read()
content = content.replace(
    'from datetime import datetime',
    'from datetime import datetime, timezone'
).replace(
    'now = datetime.utcnow()',
    'now = datetime.now(timezone.utc)'
)
open('main.py', 'w', encoding='utf-8').write(content)
print('Done - datetime fixed')
