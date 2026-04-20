f = open(".env", encoding="utf-8")
content = f.read()
f.close()

if "LIGHTPANDA_TOKEN" not in content:
    content += "\nLIGHTPANDA_TOKEN=5bf6645d003e036f378fb43006e1e9af0f16f84a75c3fb4b7d33b5e3b26db22a\n"
    open(".env", "w", encoding="utf-8").write(content)
    print("OK - token added to .env")
else:
    print("Already exists")
