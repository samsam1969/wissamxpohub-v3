content = open('admin_knowledge.html', encoding='utf-8').read()

old = '<div class="fg"><label>المحتوى</label><textarea id="fContent"></textarea></div>'

new = '''<div class="fg"><label>المحتوى</label><textarea id="fContent"></textarea></div>
    <div class="fg">
      <label>رفع ملف (Excel/CSV/PDF/صورة) — يُحوَّل تلقائياً لنص</label>
      <input type="file" id="fFile" accept=".csv,.xlsx,.xls,.pdf,.png,.jpg,.jpeg,.txt" style="padding:8px"/>
      <div id="fileStatus" style="font-size:12px;color:#4ade80;margin-top:4px"></div>
    </div>'''

content = content.replace(old, new)

# Add file processing script before loadData()
old2 = 'document.getElementById(\'btnAdd\').onclick=openAdd;'

new2 = '''document.getElementById('fFile').onchange=function(e){
  var file=e.target.files[0];
  if(!file)return;
  var status=document.getElementById('fileStatus');
  status.textContent='جاري المعالجة...';
  var reader=new FileReader();
  
  if(file.name.endsWith('.csv')||file.name.endsWith('.txt')){
    reader.onload=function(ev){
      var text=ev.target.result;
      var lines=text.split('\\n').slice(0,50);
      document.getElementById('fContent').value=lines.join('\\n');
      status.textContent='تم تحميل '+lines.length+' سطر من '+file.name;
    };
    reader.readAsText(file,'UTF-8');
  } else if(file.name.endsWith('.xlsx')||file.name.endsWith('.xls')){
    reader.onload=function(ev){
      try{
        var data=new Uint8Array(ev.target.result);
        var wb=XLSX.read(data,{type:'array'});
        var ws=wb.Sheets[wb.SheetNames[0]];
        var csv=XLSX.utils.sheet_to_csv(ws);
        var lines=csv.split('\\n').slice(0,50);
        document.getElementById('fContent').value=lines.join('\\n');
        status.textContent='تم تحميل Excel: '+wb.SheetNames[0]+' ('+lines.length+' صف)';
      }catch(err){status.textContent='خطأ في قراءة Excel: '+err.message;}
    };
    reader.readAsArrayBuffer(file);
  } else if(file.type.startsWith('image/')){
    reader.onload=function(ev){
      var img=document.createElement('img');
      img.src=ev.target.result;
      img.onload=function(){
        document.getElementById('fContent').value+='\\n[صورة مرفقة: '+file.name+' | '+img.width+'x'+img.height+']';
        status.textContent='تم رفع الصورة: '+file.name;
      };
    };
    reader.readAsDataURL(file);
  } else if(file.name.endsWith('.pdf')){
    status.textContent='PDF: '+file.name+' — اضف المحتوى يدوياً في حقل النص';
    document.getElementById('fContent').value+='\\n[ملف PDF: '+file.name+']';
  } else {
    reader.onload=function(ev){
      document.getElementById('fContent').value=ev.target.result.substring(0,2000);
      status.textContent='تم تحميل: '+file.name;
    };
    reader.readAsText(file,'UTF-8');
  }
};

document.getElementById('btnAdd').onclick=openAdd;'''

content = content.replace(old2, new2)

# Add XLSX library
old3 = '</head>'
new3 = '<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>\n</head>'
content = content.replace(old3, new3, 1)

open('admin_knowledge.html', 'w', encoding='utf-8').write(content)
print('Done - file upload added')
