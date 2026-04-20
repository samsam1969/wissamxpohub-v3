content = open('Blog.html', encoding='utf-8').read()

old = '''  }).catch(function(){
    // Fallback to localStorage
    var planType = localStorage.getItem("wx_plan_type") || "free";
    var allowed = ["starter","pro","agency"];
    if(allowed.indexOf(planType) === -1) showLock(true);
  });'''

new = '''  }).catch(function(){
    // If backend unreachable, deny access for security
    showLock(true);
  });'''

content = content.replace(old, new, 1)
open('Blog.html', 'w', encoding='utf-8').write(content)
print('Done - Blog lock secured')
