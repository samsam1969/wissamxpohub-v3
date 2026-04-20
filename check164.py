lines = open('admin_knowledge.html', encoding='utf-8').readlines()
for i in range(160, 170):
    print(f'{i+1}: {lines[i].rstrip()}')
