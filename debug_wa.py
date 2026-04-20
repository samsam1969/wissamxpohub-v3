content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Remove the incorrectly added WhatsApp button (added before wrong </body>)
import re

# Find and remove the wa button that was added in wrong place
wa_block = content.find('<!-- WhatsApp Upgrade Float Button -->')
body_tag = content.rfind('</body>')  # Last </body> = correct one

if wa_block != -1 and wa_block < body_tag:
    # Check if it was added in wrong place (inside a string)
    # Find the REAL last </body>
    real_end = content.rfind('\n</body>')
    print(f'WA button at: {wa_block}')
    print(f'Last </body> at: {real_end}')
    print(f'Content around WA: {repr(content[wa_block-50:wa_block+100])}')
