content = open('PotentialBuyers.html', encoding='utf-8').read()
# Check if lock script exists
if 'check-feature' in content:
    print('Lock EXISTS in PotentialBuyers')
    # Show the lock script
    start = content.find('<script>\n(function(){')
    print(content[start:start+200])
else:
    print('Lock MISSING in PotentialBuyers')
