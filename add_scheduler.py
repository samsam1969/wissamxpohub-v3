content = open('main.py', encoding='utf-8').read()

old = 'if __name__ == "__main__":'

new = '''def start_scheduler():
    import threading, time
    from datetime import datetime
    def run():
        while True:
            now = datetime.utcnow()
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

if __name__ == "__main__":'''

content = content.replace(old, new, 1)

# Also call start_scheduler before app.run
old2 = 'app.run('
new2 = 'start_scheduler()\n    app.run('
content = content.replace(old2, new2, 1)

open('main.py', 'w', encoding='utf-8').write(content)
print('Done - scheduler added')
