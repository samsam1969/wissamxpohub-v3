with open('services/claude_service.py', encoding='utf-8') as f:
    content = f.read()

# Reduce tokens to reasonable limits
content = content.replace('MAX_TOKENS_ADVISOR = 16000', 'MAX_TOKENS_ADVISOR = 6000')

with open('services/claude_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done:', 'MAX_TOKENS_ADVISOR = 6000' in content)