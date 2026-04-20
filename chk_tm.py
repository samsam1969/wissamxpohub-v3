f = open("services/claude_service.py", encoding="utf-8")
c = f.read()
f.close()
print("trademap_service in file:", "trademap_service" in c)
print("trademap_data in file:", "trademap_data" in c)
# Show the data merge area
idx = c.find("all_data")
print(repr(c[idx:idx+400]))
