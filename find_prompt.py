lines = open('services/claude_service.py', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'prompt' in line.lower() and ('f"""' in line or '= f' in line):
        print(f'{i+1}: {line.rstrip()}')
