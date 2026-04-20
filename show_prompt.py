lines = open('services/claude_service.py', encoding='utf-8').readlines()
for i in range(455, 475):
    print(f'{i+1}: {lines[i].rstrip()}')
