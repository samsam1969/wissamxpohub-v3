from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from routers.ai import ai_blueprint
from routers.admin import admin_blueprint
from routers.buyers import buyers_blueprint
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(admin_blueprint)
app.register_blueprint(ai_blueprint, url_prefix="/api/ai")
app.register_blueprint(buyers_blueprint)

@app.get("/")
def index():
    return send_from_directory(".", "WissamXpoHub_V3_Frontend_FIXED.html")

@app.get("/health")
def health():
    return {"service": "WissamXpoHub", "status": "ok", "version": "3.0.0"}


PROTECTED = ["PotentialBuyers.html", "ExportIntelligence.html"]

@app.route('/<path:filename>')
def serve_static(filename):
    base = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(base, filename)

def start_scheduler():
    import threading, time
    from datetime import datetime, timezone, timezone
    def run():
        while True:
            now = datetime.now(timezone.utc)
            if now.day == 1 and now.hour == 0:
                try:
                    from supabase import create_client
                    sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))
                    sb.rpc("reset_monthly_reports").execute()
                    print(f"Monthly reset done: {now}")
                except Exception as e:
                    print(f"Reset error: {e}")
            time.sleep(3600)
    t = threading.Thread(target=run, daemon=True)
    t.start()

if __name__ == "__main__":
    start_scheduler()
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=False)
