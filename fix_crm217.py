lines = open('admin_crm.html', encoding='utf-8').readlines()

# Fix lines 217-219 - replace complex wa link with simple version
lines[215] = "      '<td>'+\n"
lines[216] = "        '<button class=\"btn btn-warning btn-sm\" onclick=\"openEdit(\\'' + u.user_id + '\\')\">تعديل</button> '+\n"
lines[217] = "        '<a href=\"https://wa.me/' + (u.phone||'').replace(/[^0-9]/g,'') + '\" target=\"_blank\" class=\"btn btn-success btn-sm\" style=\"text-decoration:none\">واتساب</a>'+\n"

open('admin_crm.html', 'w', encoding='utf-8').writelines(lines)
print('Done - CRM JS fixed')
