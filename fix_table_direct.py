lines = open('admin_knowledge.html', encoding='utf-8').readlines()

# Replace lines 241-258 (index 240-257) with correct template literal
new_render = '''  body.innerHTML = data.map(r => 
    <tr>
      <td><span class="badge badge-"></span></td>
      <td style="max-width:200px;font-weight:600"></td>
      <td><div class="content-preview" title=""></div></td>
      <td style="color:#fbbf24"></td>
      <td></td>
      <td class="">/10</td>
      <td class=""></td>
      <td style="font-size:11px;color:#6b7280;max-width:150px"></td>
      <td>
        <button class="btn btn-success btn-sm" onclick='openEdit()'>تعديل</button>
        <button class="btn btn-danger btn-sm" onclick="toggleActive('', )" style="margin-top:4px"></button>
      </td>
    </tr>
  ).join("");
}
'''

lines[240:258] = [new_render]
open('admin_knowledge.html', 'w', encoding='utf-8').writelines(lines)
print('Done - table fixed')
