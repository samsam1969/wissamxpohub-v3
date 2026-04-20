lines = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').readlines()

# Find the banner timeout and fix it to check after plan loads from API
for i, line in enumerate(lines):
    if 'if (type === "free" && isLoggedIn) showFreeTrialEndedBanner();' in line:
        print(f'Found at line {i+1}')
        # Change timeout from 2500 to 5000 to wait for API response
        lines[i-1] = '  }, 5000);\n'
        print('Fixed timeout')
        break

open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').writelines(lines)
print('Done')
