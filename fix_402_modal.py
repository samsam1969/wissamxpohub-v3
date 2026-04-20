content = open('WissamXpoHub_V3_Frontend_FIXED.html', encoding='utf-8').read()

old = '''      if (data.error === "limit_reached") {
      showUpgradeModal();
    }'''

new = '''      if (data.error === "limit_reached") {
      showUpgradeModal("وصلت للحد الأقصى — اختر باقة للاستمرار");
    }'''

content = content.replace(old, new, 1)

# Also handle 402 error from fetch
old2 = '''    } catch (err) {
      if(box) box.textContent = "خطأ في الاتصال: " + err.message;'''

new2 = '''    } catch (err) {
      if(err.message && err.message.includes("402")) {
        showUpgradeModal("وصلت للحد الأقصى — اختر باقة للاستمرار");
        return;
      }
      if(box) box.textContent = "خطأ في الاتصال: " + err.message;'''

content = content.replace(old2, new2, 1)

# Handle 402 in fetch response
old3 = '''      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || HTTP );
      }'''

new3 = '''      if (response.status === 402) {
        const errData = await response.json().catch(() => ({}));
        showUpgradeModal(errData.message || "وصلت للحد الأقصى — اختر باقة للاستمرار");
        return;
      }
      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.error || HTTP );
      }'''

content = content.replace(old3, new3, 1)
open('WissamXpoHub_V3_Frontend_FIXED.html', 'w', encoding='utf-8').write(content)
print('Done - 402 shows upgrade modal')
