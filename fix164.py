lines = open('admin_knowledge.html', encoding='utf-8').readlines()

lines[163] = "        '<button class=\"btn btn-success btn-sm\" onclick=\"openEdit(\\'' + r.id + '\\')\">تعديل</button> '+\n"
lines[164] = "        '<button class=\"btn btn-danger btn-sm\" onclick=\"toggleActive(\\'' + r.id + '\\',' + (!r.is_active) + ')\">'+toggleText+'</button>'+\n"

open('admin_knowledge.html', 'w', encoding='utf-8').writelines(lines)
print('Done')
