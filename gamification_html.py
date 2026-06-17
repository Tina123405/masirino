# gamification_html.py
# صفحه نمایش پروفایل کاربر با گیمیفیکیشن

def render_gamification_profile_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پروفایل و افتخارات - مسیرینو</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: auto; }}
        h1 {{ text-align: center; margin-bottom: 30px; }}
        
        .profile-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 30px;
            margin-bottom: 25px;
            text-align: center;
        }}
        .level-icon {{
            font-size: 4rem;
            margin-bottom: 10px;
        }}
        .level-name {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .points {{
            font-size: 2rem;
            font-weight: bold;
            color: #ffd700;
            margin: 15px 0;
        }}
        .streak {{
            background: rgba(255,107,107,0.2);
            border-radius: 30px;
            padding: 10px 20px;
            display: inline-block;
            margin: 10px 0;
        }}
        .progress-bar {{
            height: 12px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            margin: 20px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ffd700, #ff6584);
            border-radius: 10px;
            transition: width 0.5s;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
            padding: 15px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #6c63ff;
        }}
        .stat-label {{
            font-size: 0.8rem;
            color: #c4c4f0;
            margin-top: 5px;
        }}
        
        .achievements-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .achievement-card {{
            background: rgba(0,0,0,0.3);
            border-radius: 16px;
            padding: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s;
        }}
        .achievement-card.locked {{
            opacity: 0.5;
            filter: grayscale(0.5);
        }}
        .achievement-icon {{
            font-size: 2rem;
        }}
        .achievement-info {{
            flex: 1;
        }}
        .achievement-name {{
            font-weight: bold;
        }}
        .achievement-desc {{
            font-size: 0.7rem;
            color: #c4c4f0;
        }}
        
        .leaderboard-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .leaderboard-table th, .leaderboard-table td {{
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .leaderboard-table th {{
            color: #6c63ff;
        }}
        .rank-1 {{ color: #ffd700; font-weight: bold; }}
        .rank-2 {{ color: #c0c0c0; font-weight: bold; }}
        .rank-3 {{ color: #cd7f32; font-weight: bold; }}
        
        .btn {{
            padding: 10px 25px;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            font-weight: bold;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            color: white;
            text-decoration: none;
            display: inline-block;
        }}
        .back-home {{
            display: block;
            text-align: center;
            margin-top: 30px;
            color: #6c63ff;
            text-decoration: none;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🏆 پروفایل و افتخارات من</h1>
    
    <div id="profileContent">
        <div style="text-align:center; padding:50px">⏳ در حال بارگذاری...</div>
    </div>
    
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
const sessionId = "{session_id}";

async function loadGamification() {{
    try {{
        const res = await fetch('/api/gamification/status?session_id=' + sessionId);
        const data = await res.json();
        
        if (data.status === 'ok') {{
            let achievementsHtml = '';
            for (let ach of data.achievements) {{
                achievementsHtml += `
                    <div class="achievement-card">
                        <div class="achievement-icon">${{ach.icon}}</div>
                        <div class="achievement-info">
                            <div class="achievement-name">${{ach.name}}</div>
                            <div class="achievement-desc">${{ach.description}}</div>
                        </div>
                    </div>
                `;
            }}
            
            // نمایش مدال‌های قفل شده
            const totalAchievements = data.total_achievements || 30;
            const earnedCount = data.achievements_count || 0;
            for (let i = earnedCount; i < Math.min(earnedCount + 5, totalAchievements); i++) {{
                achievementsHtml += `
                    <div class="achievement-card locked">
                        <div class="achievement-icon">❓</div>
                        <div class="achievement-info">
                            <div class="achievement-name">مدال مخفی</div>
                            <div class="achievement-desc">با ادامه فعالیت باز می‌شود</div>
                        </div>
                    </div>
                `;
            }}
            
            const stats = data.stats || {{}};
            
            document.getElementById('profileContent').innerHTML = `
                <div class="profile-card">
                    <div class="level-icon" style="color: ${{data.level_color}}">${{data.level_icon}}</div>
                    <div class="level-name" style="color: ${{data.level_color}}">${{data.level_name}}</div>
                    <div class="points">⭐ ${{data.total_points}} امتیاز</div>
                    <div class="streak">🔥 استریک: ${{data.streak_days}} روز متوالی</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${{(data.total_points / (data.total_points + data.points_to_next_level)) * 100}}%"></div>
                    </div>
                    <div>تا سطح بعدی: ${{data.points_to_next_level}} امتیاز</div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card"><div class="stat-value">${{stats.challenges_completed || 0}}</div><div class="stat-label">چالش انجام شده</div></div>
                    <div class="stat-card"><div class="stat-value">${{stats.exams_taken || 0}}</div><div class="stat-label">آزمون داده</div></div>
                    <div class="stat-card"><div class="stat-value">${{stats.avg_exam_score || 0}}%</div><div class="stat-label">میانگین نمره</div></div>
                    <div class="stat-card"><div class="stat-value">${{stats.messages_sent || 0}}</div><div class="stat-label">پیام در گروه‌ها</div></div>
                </div>
                
                <div class="profile-card">
                    <h3>🏅 مدال‌های کسب شده (${{data.achievements_count}}/${{data.total_achievements}})</h3>
                    <div class="achievements-grid">
                        ${{achievementsHtml || '<p>هنوز مدالی کسب نکردی. ادامه بده!</p>'}}
                    </div>
                </div>
                
                <div class="profile-card" id="leaderboardSection">
                    <h3>🏆 لیدربرد برترین‌ها</h3>
                    <div id="leaderboardContent">⏳ در حال بارگذاری...</div>
                </div>
            `;
            
            loadLeaderboard();
        }} else {{
            document.getElementById('profileContent').innerHTML = '<div class="profile-card"><p>❌ خطا در بارگذاری داده‌ها</p></div>';
        }}
    }} catch(e) {{
        document.getElementById('profileContent').innerHTML = '<div class="profile-card"><p>❌ خطا: ' + e.message + '</p></div>';
    }}
}}

async function loadLeaderboard() {{
    try {{
        const res = await fetch('/api/gamification/leaderboard');
        const data = await res.json();
        
        if (data.status === 'ok' && data.leaderboard) {{
            let html = '<table class="leaderboard-table"><thead><tr><th>رتبه</th><th>کاربر</th><th>امتیاز</th><th>سطح</th></tr></thead><tbody>';
            for (let u of data.leaderboard) {{
                let rankClass = '';
                if (u.rank === 1) rankClass = 'rank-1';
                else if (u.rank === 2) rankClass = 'rank-2';
                else if (u.rank === 3) rankClass = 'rank-3';
                
                let medal = u.rank === 1 ? '🥇' : (u.rank === 2 ? '🥈' : (u.rank === 3 ? '🥉' : u.rank));
                html += `<tr>
                    <td class="${{rankClass}}">${{medal}}</td>
                    <td>${{u.name}}</td>
                    <td>⭐ ${{u.points}}</td>
                    <td>سطح ${{u.level}}</td>
                </tr>`;
            }}
            html += '</tbody></table>';
            document.getElementById('leaderboardContent').innerHTML = html;
        }}
    }} catch(e) {{
        document.getElementById('leaderboardContent').innerHTML = '<p>خطا در بارگذاری لیدربرد</p>';
    }}
}}

loadGamification();
</script>
</body>
</html>'''