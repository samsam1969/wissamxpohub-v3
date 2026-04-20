lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i in range(1480, 1510):
    print(f'{i+1}: {lines[i].rstrip()}')
