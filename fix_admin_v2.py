filepath = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''        if(tok2){
          var pay2 = JSON.parse(atob(tok2.split(".")[1]));
          if(pay2.email === "wissamxpo@outlook.com"){
            var al2 = document.getElementById("adminLinks");
            if(al2) al2.style.display = "inline-flex";
          }
        }'''

new_block = '''        // Method 1: via JWT token
        if(tok2){
          try {
            var pay2 = JSON.parse(atob(tok2.split(".")[1]));
            if(pay2.email === "wissamxpo@outlook.com"){
              var al2 = document.getElementById("adminLinks");
              if(al2) al2.style.setProperty("display","inline-flex","important");
              console.log("[Admin] ✅ Shown via JWT");
            }
          } catch(je){ console.log("[Admin] JWT decode failed:", je); }
        }
        // Method 2: direct wx_user_email (simpler & reliable)
        var directEmail = localStorage.getItem("wx_user_email") || "";
        if(directEmail.trim().toLowerCase() === "wissamxpo@outlook.com"){
          var al3 = document.getElementById("adminLinks");
          if(al3) al3.style.setProperty("display","inline-flex","important");
          console.log("[Admin] ✅ Shown via wx_user_email");
        }'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print("✅ Block replaced successfully")
else:
    print("❌ Block not found exactly — check whitespace/tabs")
    # نطبع الـ chars حول السطر 3190 للتشخيص
    idx = content.find('pay2.email')
    if idx != -1:
        print("Found pay2.email at char:", idx)
        print(repr(content[idx-200:idx+200]))

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
    print("✅ File saved!")
