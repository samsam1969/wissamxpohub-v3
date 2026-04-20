content = open('admin_knowledge.html', encoding='utf-8').read()

# Fix the broken template literal in renderTable
old = '''  body.innerHTML = data.map(r =>
    <tr>
      <td><span class="badge badge-"></span></td>
      <td style="max-width:200px;font-weight:600"></td>
      <td><div class="content-preview" title=""></div></td>
      <td style="color:#fbbf24"></td>
      <td></td>
      <td class="">/10</td>'''

new = '''  body.innerHTML = data.map(r => 
    <tr>
      <td><span class="badge badge-"></span></td>
      <td style="max-width:200px;font-weight:600"></td>
      <td><div class="content-preview" title=""></div></td>
      <td style="color:#fbbf24"></td>
      <td></td>
      <td class="">/10</td>'''

content = content.replace(old, new)
open('admin_knowledge.html', 'w', encoding='utf-8').write(content)
print('Done')
