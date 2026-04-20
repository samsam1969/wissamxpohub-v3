f = open("services/claude_service.py", encoding="utf-8")
content = f.read()
f.close()

old = """---

## القسم الخامس: قائمة المشترين المحتملين التفصيلية

- جدول 15 شركة حقيقية مع: الاسم | الدولة | النشاط | المدينة | الموقع | حجم المشتريات المتوقع | الأولوية
- تحليل مفصل لكل شركة
- كيفية التواصل مع كل مجموعة
- نصائح التفاوض الخاصة بكل سوق
- استراتيجية بناء العلاقات التجارية

تعليمات: عربية فقط. أضف [المصدر، السنة] لكل رقم. اكتب بشكل مفصل جداً."""

new = """تعليمات: عربية فقط. أضف [المصدر، السنة] لكل رقم. اكتب بشكل مفصل جداً."""

if old in content:
    content = content.replace(old, new, 1)
    print("OK - Section 5 removed from Part 2")
else:
    print("Not found")

open("services/claude_service.py", "w", encoding="utf-8").write(content)
print("Done")
