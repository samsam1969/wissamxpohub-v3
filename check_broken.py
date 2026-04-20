lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i in range(1765, 1775):
    print(f'{i+1}: {lines[i].rstrip()}')
for i in range(1932, 1942):
    print(f'{i+1}: {lines[i].rstrip()}')
