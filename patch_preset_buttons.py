"""
WissamXpoHub — Patch: Remove Preset Buttons from AI Research Settings
يحذف أزرار الـ Preset من قسمي Selected Sources و Requested Information
"""

import os
import shutil
from datetime import datetime

# ── المسار — عدّله لو الملف في مكان مختلف
FILE_PATH = r"C:\Users\DELL\Desktop\wissamxpohub-backend\WissamXpoHub_V3_Frontend_FIXED.html"

# ── نسخة احتياطية قبل التعديل
def backup(path):
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    bk_path = path.replace(".html", f"_BACKUP_{ts}.html")
    shutil.copy2(path, bk_path)
    print(f"✓ نسخة احتياطية: {bk_path}")
    return bk_path

# ── الأزرار المراد حذفها (Selected Sources)
SRC_BLOCK = """          <div class="btns" style="margin-top:0;">
            <button type="button" class="secondary" onclick="presetSources('auto')">Auto</button>
            <button type="button" class="secondary" onclick="presetSources('official')">Official</button>
            <button type="button" class="secondary" onclick="presetSources('buyers')">Buyers</button>
            <button type="button" class="secondary" onclick="presetSources('stats')">Stats</button>
            <button type="button" class="ghost"     onclick="clearSources()">Clear</button>
          </div>"""

# ── الأزرار المراد حذفها (Requested Information)
INFO_BLOCK = """          <div class="btns" style="margin-top:0;">
            <button type="button" class="secondary" onclick="presetInfo('brief')">Full Brief</button>
            <button type="button" class="secondary" onclick="presetInfo('buyers')">Buyer Focus</button>
            <button type="button" class="secondary" onclick="presetInfo('rules')">Rules Focus</button>
            <button type="button" class="secondary" onclick="presetInfo('stats')">Stats Focus</button>
            <button type="button" class="ghost"     onclick="clearRequestedInfo()">Clear</button>
          </div>"""

def patch():
    if not os.path.exists(FILE_PATH):
        print(f"✗ الملف غير موجود: {FILE_PATH}")
        print("  تأكد من المسار وأعد التشغيل.")
        return

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    original_len = len(html)
    removed = 0

    # حذف أزرار Sources
    if SRC_BLOCK in html:
        html = html.replace(SRC_BLOCK, "", 1)
        removed += 1
        print("✓ تم حذف أزرار Selected Sources (Auto/Official/Buyers/Stats/Clear)")
    else:
        print("⚠ لم يُعثر على أزرار Selected Sources — ربما تم حذفها مسبقاً")

    # حذف أزرار Info
    if INFO_BLOCK in html:
        html = html.replace(INFO_BLOCK, "", 1)
        removed += 1
        print("✓ تم حذف أزرار Requested Information (Full Brief/Buyer Focus/Rules Focus/Stats Focus/Clear)")
    else:
        print("⚠ لم يُعثر على أزرار Requested Information — ربما تم حذفها مسبقاً")

    if removed == 0:
        print("\n✗ لم يُطبَّق أي تعديل — تأكد إن الملف لم يتغير.")
        return

    # نسخة احتياطية ثم الحفظ
    backup(FILE_PATH)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    saved_bytes = original_len - len(html)
    print(f"\n✅ تم الحفظ — حُذف {saved_bytes} حرف ({removed}/2 بلوك)")
    print(f"   الملف: {FILE_PATH}")
    print("\nالخطوة التالية: أعد تحميل الصفحة في المتصفح (Ctrl+Shift+R)")

if __name__ == "__main__":
    patch()
