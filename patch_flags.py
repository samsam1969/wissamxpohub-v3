import shutil
from datetime import datetime

f = open("WissamXpoHub_V3_Frontend_FIXED.html", encoding="utf-8")
html = f.read()
f.close()

shutil.copy2("WissamXpoHub_V3_Frontend_FIXED.html", f"WissamXpoHub_V3_Frontend_FIXED_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")

old = """        <!-- Animated Egypt-EU branding -->
        <div style="display:flex;align-items:center;justify-content:center;gap:20px;margin-top:18px;padding:16px;background:rgba(0,0,0,.15);border:1px solid var(--line);border-radius:14px;">
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127468;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EGYPT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
            <div style="display:flex;align-items:center;gap:6px;">
              <div style="width:20px;height:1px;background:linear-gradient(90deg,transparent,var(--line2));animation:arrowPulse 2s ease-in-out infinite;"></div>
              <div style="font-size:16px;font-weight:800;color:#60a5fa;animation:arrowPulse 2s ease-in-out infinite;">&#8594;</div>
              <div style="width:20px;height:1px;background:linear-gradient(90deg,var(--line2),transparent);animation:arrowPulse 2s ease-in-out infinite;"></div>
            </div>
            <div style="font-size:9px;color:var(--muted);font-weight:700;letter-spacing:1.5px;margin-top:2px;">EXPORT</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:center;gap:6px;animation:flagFloat 3s ease-in-out infinite;animation-delay:.5s;">
            <div style="font-size:36px;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4));">&#127466;&#127482;</div>
            <div style="font-size:10px;font-weight:700;color:var(--muted);letter-spacing:1px;">EU</div>
          </div>
        </div>"""

new = """        <!-- Flags Showcase -->
        <div id="flagsShowcase" style="margin-top:16px;padding:20px 10px 14px;background:rgba(0,0,0,.18);border:1px solid rgba(30,58,110,.6);border-radius:16px;overflow:hidden;position:relative;">
          <style>
            #flagsShowcase { perspective: 800px; }
            .fx-flag { transform-style: preserve-3d; will-change: transform; }
            .fx-eg { animation: fxEgWave 4s ease-in-out infinite; transform-origin: left center; }
            .fx-eu { animation: fxEuWave 4s ease-in-out infinite .6s; transform-origin: right center; }
            .fx-connector { animation: fxConnPulse 2.5s ease-in-out infinite; }
            @keyframes fxEgWave {
              0%,100% { transform: rotateY(12deg) rotateX(-2deg) translateY(0); }
              50%      { transform: rotateY(8deg)  rotateX(2deg)  translateY(-5px); }
            }
            @keyframes fxEuWave {
              0%,100% { transform: rotateY(-12deg) rotateX(2deg)  translateY(0); }
              50%      { transform: rotateY(-8deg)  rotateX(-2deg) translateY(-5px); }
            }
            @keyframes fxConnPulse {
              0%,100% { opacity:.25; transform:scaleX(.85); }
              50%      { opacity:.7;  transform:scaleX(1); }
            }
          </style>
          <div style="display:flex;align-items:center;justify-content:center;gap:18px;">

            <!-- Egypt Flag SVG -->
            <div class="fx-flag fx-eg" style="border-radius:6px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.4);flex-shrink:0;">
              <svg width="110" height="73" viewBox="0 0 110 73" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0"  width="110" height="24.3" fill="#CE1126"/>
                <rect x="0" y="24.3" width="110" height="24.3" fill="#FFFFFF"/>
                <rect x="0" y="48.7" width="110" height="24.3" fill="#000000"/>
                <!-- Eagle of Saladin simplified -->
                <g transform="translate(55,36.5)">
                  <ellipse cx="0" cy="0" rx="7" ry="5" fill="#C09300"/>
                  <path d="M-7,-2 Q-14,-8 -18,-4 Q-14,-1 -7,0Z" fill="#C09300"/>
                  <path d="M7,-2 Q14,-8 18,-4 Q14,-1 7,0Z" fill="#C09300"/>
                  <rect x="-4" y="2" width="8" height="5" rx="1" fill="#C09300"/>
                  <path d="M-4,7 L-5,10 L-2,10Z M4,7 L5,10 L2,10Z" fill="#C09300"/>
                  <circle cx="0" cy="-1" r="2.5" fill="#8B0000"/>
                </g>
                <!-- Subtle shine overlay -->
                <rect x="0" y="0" width="110" height="73" fill="url(#egShine)" opacity=".15"/>
                <defs>
                  <linearGradient id="egShine" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="white" stop-opacity="1"/>
                    <stop offset="60%" stop-color="white" stop-opacity="0"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>

            <!-- Connector -->
            <div class="fx-connector" style="display:flex;flex-direction:column;align-items:center;gap:4px;flex-shrink:0;">
              <svg width="36" height="16" viewBox="0 0 36 16">
                <path d="M2 8 L34 8" stroke="#2d5aa8" stroke-width="1.5" stroke-dasharray="3 2" fill="none"/>
                <path d="M26 4 L34 8 L26 12" stroke="#2d5aa8" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>

            <!-- EU Flag SVG -->
            <div class="fx-flag fx-eu" style="border-radius:6px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.55),0 2px 8px rgba(0,0,0,.4);flex-shrink:0;">
              <svg width="110" height="73" viewBox="0 0 110 73" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="110" height="73" fill="#003399"/>
                <!-- 12 stars in circle -->
                <g transform="translate(55,36.5)">
                  <g id="euStar" fill="#FFCC00">
                    <polygon points="0,-5 1.2,-1.6 4.8,-1.6 1.9,0.6 3,4 0,2 -3,4 -1.9,0.6 -4.8,-1.6 -1.2,-1.6" transform="translate(0,-18)"/>
                  </g>
                  <use href="#euStar" transform="rotate(30)"/>
                  <use href="#euStar" transform="rotate(60)"/>
                  <use href="#euStar" transform="rotate(90)"/>
                  <use href="#euStar" transform="rotate(120)"/>
                  <use href="#euStar" transform="rotate(150)"/>
                  <use href="#euStar" transform="rotate(180)"/>
                  <use href="#euStar" transform="rotate(210)"/>
                  <use href="#euStar" transform="rotate(240)"/>
                  <use href="#euStar" transform="rotate(270)"/>
                  <use href="#euStar" transform="rotate(300)"/>
                  <use href="#euStar" transform="rotate(330)"/>
                </g>
                <rect x="0" y="0" width="110" height="73" fill="url(#euShine)" opacity=".12"/>
                <defs>
                  <linearGradient id="euShine" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="white" stop-opacity="1"/>
                    <stop offset="60%" stop-color="white" stop-opacity="0"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>

          </div>
        </div>"""

if old in html:
    html = html.replace(old, new, 1)
    open("WissamXpoHub_V3_Frontend_FIXED.html", "w", encoding="utf-8").write(html)
    print("OK - premium flags added")
else:
    idx = html.find("Animated Egypt-EU branding")
    print("Not found - idx:", idx)
    if idx > 0:
        print(repr(html[idx-20:idx+100]))
