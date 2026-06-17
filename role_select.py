# role_select.py
def render_role_select_page(session_id):
    return f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>انتخاب نقش - مسیرینو</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .role-card {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(20px);
            border-radius: 32px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.4s;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .role-card:hover {{
            transform: translateY(-10px) scale(1.02);
            background: rgba(108,99,255,0.2);
        }}
        .role-icon {{ font-size: 5rem; margin-bottom: 20px; }}
        .role-title {{ font-size: 1.8rem; font-weight: bold; margin-bottom: 10px; }}
        .role-desc {{ color: #c4c4f0; font-size: 0.9rem; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #fff, #6c63ff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎓 به مسیرینو خوش آمدی</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="role-card" onclick="selectRole('student')">
            <div class="role-icon">📚</div>
            <div class="role-title">دانش‌آموز / دانشجو</div>
            <div class="role-desc">مشاوره تحصیلی، برنامه ریزی، آزمون‌ها و بازی‌های آموزشی</div>
        </div>
        <div class="role-card" onclick="selectRole('counselor')">
            <div class="role-icon">👨‍🏫</div>
            <div class="role-title">مشاور تحصیلی</div>
            <div class="role-desc">مشاهده وضعیت دانش‌آموزان، آمار و گزارش‌های پیشرفت</div>
        </div>
    </div>
</div>
<script>
const sessionId = "{session_id}";
function selectRole(role) {{
    fetch('/save-role', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ session_id: sessionId, role: role }})
    }})
    .then(res => res.json())
    .then(data => {{
        if (data.status === 'ok') window.location.href = '/consent-page?session_id=' + sessionId;
        else alert('خطا: ' + (data.message || 'مشکل در ثبت نقش'));
    }})
    .catch(err => alert('خطا در ارتباط با سرور'));
}}
</script>
</body>
</html>'''