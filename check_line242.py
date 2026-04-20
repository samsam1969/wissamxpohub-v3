lines = open('admin_knowledge.html', encoding='utf-8').readlines()
for i in range(238, 248):
    print(f'{i+1}: {lines[i].rstrip()}')
