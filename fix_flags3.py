import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()
shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old_marker = "        <!-- Flags Showcase -->"
end_marker = "        </div>\n        </div>"

si = html.find(old_marker)
ei = html.find(end_marker, si) + len(end_marker)

new_flags = """        <!-- Flags Showcase -->
        <div style="margin-top:16px;padding:22px 10px 18px;background:rgba(4,10,24,.55);border:1px solid rgba(30,58,110,.5);border-radius:16px;overflow:hidden;">
          <style>
            .wxflag-eg{animation:wxEg 5s ease-in-out infinite;transform-origin:center center;transform-box:fill-box;}
            .wxflag-eu{animation:wxEu 5s ease-in-out infinite .8s;transform-origin:center center;transform-box:fill-box;}
            .wxconn{animation:wxConn 2.5s ease-in-out infinite;}
            @keyframes wxEg{0%,100%{transform:rotateY(14deg) translateY(0px);}50%{transform:rotateY(8deg) translateY(-6px);}}
            @keyframes wxEu{0%,100%{transform:rotateY(-14deg) translateY(0px);}50%{transform:rotateY(-8deg) translateY(-6px);}}
            @keyframes wxConn{0%,100%{opacity:.2;}50%{opacity:.8;}}
          </style>
          <div style="display:flex;align-items:center;justify-content:center;gap:16px;perspective:900px;">

            <!-- Egypt Flag -->
            <div class="wxflag-eg" style="border-radius:5px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.7),0 3px 10px rgba(0,0,0,.5);flex-shrink:0;width:120px;height:80px;">
              <svg width="120" height="80" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0"    width="120" height="26.6" fill="#CE1126"/>
                <rect x="0" y="26.6" width="120" height="26.8" fill="#FFFFFF"/>
                <rect x="0" y="53.4" width="120" height="26.6" fill="#000000"/>
                <g transform="translate(60,40)">
                  <rect x="-3.5" y="-7" width="7" height="9" fill="#C8992A"/>
                  <path d="M-3.5,-7 Q0,-11 3.5,-7" fill="#C8992A"/>
                  <path d="M-14,-5 Q-10,-10 -3.5,-7 L-3.5,2 Q-10,-1 -14,2Z" fill="#C8992A"/>
                  <path d="M14,-5 Q10,-10 3.5,-7 L3.5,2 Q10,-1 14,2Z" fill="#C8992A"/>
                  <rect x="-5" y="2" width="10" height="6" rx="1" fill="#C8992A"/>
                  <path d="M-5,8 L-6,12 M-2,8 L-2,12 M2,8 L2,12 M5,8 L6,12" stroke="#C8992A" stroke-width="1.2" fill="none"/>
                </g>
                <defs><linearGradient id="egS" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0%" stop-color="white" stop-opacity="0.18"/><stop offset="100%" stop-color="white" stop-opacity="0"/></linearGradient></defs>
                <rect x="0" y="0" width="120" height="80" fill="url(#egS)"/>
              </svg>
            </div>

            <!-- Connector -->
            <div class="wxconn" style="flex-shrink:0;">
              <svg width="40" height="20" viewBox="0 0 40 20" xmlns="http://www.w3.org/2000/svg">
                <line x1="2" y1="10" x2="38" y2="10" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,3"/>
                <polyline points="30,4 38,10 30,16" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>

            <!-- EU Flag -->
            <div class="wxflag-eu" style="border-radius:5px;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.7),0 3px 10px rgba(0,0,0,.5);flex-shrink:0;width:120px;height:80px;">
              <svg width="120" height="80" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="120" height="80" fill="#003399"/>
                <g transform="translate(60,40)" fill="#FFCC00">
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(30) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(60) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(90) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(120) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(150) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(180) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(210) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(240) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(270) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(300) translate(0,-19)"/>
                  <polygon points="0,-5.5 1.3,-1.8 5.2,-1.8 2.1,0.7 3.2,4.5 0,2.2 -3.2,4.5 -2.1,0.7 -5.2,-1.8 -1.3,-1.8" transform="rotate(330) translate(0,-19)"/>
                </g>
                <defs><linearGradient id="euS" x1="0" y1="0" x2="0.6" y2="1"><stop offset="0%" stop-color="white" stop-opacity="0.15"/><stop offset="100%" stop-color="white" stop-opacity="0"/></linearGradient></defs>
                <rect x="0" y="0" width="120" height="80" fill="url(#euS)"/>
              </svg>
            </div>

          </div>
        </div>"""

if si != -1 and ei > si:
    html = html[:si] + new_flags + html[ei:]
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - flags updated, size:", len(html))
else:
    print("FAIL - si:", si, "ei:", ei)
