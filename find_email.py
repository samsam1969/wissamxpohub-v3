lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'wx_user_email' in line or 'userEmail' in line or 'statEmail' in line:
        print(f'{i+1}: {line.rstrip()[:100]}')
