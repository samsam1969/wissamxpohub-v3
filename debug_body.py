content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

# Find and remove wrongly placed upgrade modal
wrong_start = content.find("  <!-- Upgrade Modal -->")
real_body = content.rfind("\n</body>")

if wrong_start != -1 and wrong_start < real_body - 5000:
    # It was added in wrong place - remove it
    wrong_end = content.find("  </script>\n</body>", wrong_start)
    if wrong_end != -1:
        wrong_end = wrong_end + len("  </script>\n</body>")
        content = content[:wrong_start] + content[wrong_end:]
        print("Removed wrong modal")

# Now find the REAL last </body>
real_body = content.rfind("\n</body>")
print(f"Real </body> at position: {real_body}")
print(f"Content before it: {repr(content[real_body-100:real_body])}")
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - checking position')
