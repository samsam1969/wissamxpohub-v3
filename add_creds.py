
f = open(".env", encoding="utf-8")

content = f.read()

f.close()

additions = """

# B2B Site Credentials

B2B_EMAIL=aegyptusxpo@gmail.com

EUROPAGES_PASSWORD=Adam12345678

KOMPASS_PASSWORD=ِAdam12345678

IMPORTYETI_PASSWORD=Adam12345678

WLW_PASSWORD=Adam12345678

"""

if "B2B_EMAIL" not in content:

    content += additions

    open(".env", "w", encoding="utf-8").write(content)

    print("OK - added to .env")

else:

    print("Already exists")

