lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Show context around line 1905
for i in range(1900, 1915):
    print(f'{i+1}: {lines[i].rstrip()}')
