lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'showFreeTrialEndedBanner' in line or 'freeTrialBanner' in line:
        print(f'{i+1}: {line.rstrip()[:80]}')
