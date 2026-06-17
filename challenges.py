import random
from datetime import datetime, date

CHALLENGES_BANK = {
    "آسان": [
        {"id": "easy_1", "title": "📖 ۲۰ دقیقه مطالعه", "desc": "۲۰ دقیقه بدون وقفه درس بخون", "points": 10, "time": 20, "icon": "📖"},
        {"id": "easy_2", "title": "✍️ ۵ کلمه جدید انگلیسی", "desc": "۵ کلمه جدید انگلیسی یاد بگیر و معنی‌ش رو بنویس", "points": 10, "time": 10, "icon": "📝"},
        {"id": "easy_3", "title": "🧘 ۵ دقیقه تمرکز", "desc": "۵ دقیقه مدیتیشن یا تنفس عمیق برای افزایش تمرکز", "points": 10, "time": 5, "icon": "🧘"},
        {"id": "easy_4", "title": "📝 ۵ تست ریاضی", "desc": "۵ تست ریاضی حل کن", "points": 10, "time": 15, "icon": "🔢"},
        {"id": "easy_5", "title": "📚 مرور درس دیروز", "desc": "مطالب دیروز رو ۱۰ دقیقه مرور کن", "points": 10, "time": 10, "icon": "🔄"},
    ],
    "متوسط": [
        {"id": "medium_1", "title": "📖 ۴۵ دقیقه مطالعه", "desc": "۴۵ دقیقه بدون وقفه درس بخون", "points": 20, "time": 45, "icon": "📚"},
        {"id": "medium_2", "title": "🎯 ۱۵ تست زبان", "desc": "۱۵ تست زبان انگلیسی بزن", "points": 20, "time": 25, "icon": "🎯"},
        {"id": "medium_3", "title": "📝 خلاصه‌نویسی", "desc": "از یک درس ۱۰ خط خلاصه مفید بنویس", "points": 20, "time": 20, "icon": "✍️"},
        {"id": "medium_4", "title": "💪 ۲۰ دقیقه ورزش", "desc": "۲۰ دقیقه ورزش سبک برای افزایش انرژی", "points": 20, "time": 20, "icon": "🏃"},
        {"id": "medium_5", "title": "📊 تحلیل آزمون", "desc": "آزمون قبلی رو تحلیل کن و اشتباهاتت رو یادداشت کن", "points": 20, "time": 30, "icon": "📊"},
    ],
    "سخت": [
        {"id": "hard_1", "title": "📖 ۹۰ دقیقه مطالعه", "desc": "۹۰ دقیقه مطالعه عمیق و متمرکز", "points": 34, "time": 90, "icon": "🏆"},
        {"id": "hard_2", "title": "🎯 ۳۰ تست ترکیبی", "desc": "۳۰ تست از دروس مختلف بزن", "points": 33, "time": 50, "icon": "🎯"},
        {"id": "hard_3", "title": "📝 حل مسائل چالش‌برانگیز", "desc": "۵ مسئله سخت ریاضی یا فیزیک حل کن", "points": 33, "time": 45, "icon": "🧠"},
        {"id": "hard_4", "title": "🎓 شبیه‌سازی آزمون", "desc": "یک آزمون ۶۰ سوالی در شرایط واقعی بده", "points": 0, "time": 90, "icon": "📝"},  # غیرفعال
        {"id": "hard_5", "title": "📚 تدریس به دیگران", "desc": "یک مبحث رو به یکی از دوستانت آموزش بده", "points": 0, "time": 30, "icon": "🎓"},  # غیرفعال
    ]
}

# اضافه کردن import در ابتدای فایل
import sqlite3
from config import DB_NAME
from gamification import add_points_to_user, update_challenge_completed


def get_daily_challenges(user_id, level="آسان"):
    """دریافت ۳ چالش تصادفی از سطح مشخص شده"""
    random.seed(datetime.now().date().isoformat() + user_id[:8])
    
    challenges = CHALLENGES_BANK.get(level, CHALLENGES_BANK["آسان"])
    selected = random.sample(challenges, min(3, len(challenges)))
    
    today = datetime.now().date().isoformat()
    
    result = []
    for ch in selected:
        result.append({
            "challenge_id": ch["id"] + "_" + today,
            "title": ch["title"],
            "description": ch["desc"],
            "points": ch["points"],
            "time_estimate": ch["time"],
            "icon": ch["icon"],
            "category": "عمومی",
            "status": "pending",
            "is_new": True,
            "level": level
        })
    
    return result


def complete_user_challenge(user_id, challenge_id, level):
    """تکمیل چالش و افزودن امتیاز + گیمیفیکیشن"""
    import sqlite3
    from config import DB_NAME
    from datetime import datetime
    
    # پیدا کردن امتیاز چالش بر اساس level و challenge_id
    points = 0
    challenge_title = ""
    
    # پیدا کردن چالش در بانک
    if level == "آسان":
        for ch in CHALLENGES_BANK["آسان"]:
            if ch["id"] in challenge_id:
                points = ch["points"]
                challenge_title = ch["title"]
                break
    elif level == "متوسط":
        for ch in CHALLENGES_BANK["متوسط"]:
            if ch["id"] in challenge_id:
                points = ch["points"]
                challenge_title = ch["title"]
                break
    elif level == "سخت":
        for ch in CHALLENGES_BANK["سخت"]:
            if ch["id"] in challenge_id:
                points = ch["points"]
                challenge_title = ch["title"]
                break
    
    # اگر امتیاز پیدا نشد، مقدار پیش‌فرض
    if points == 0:
        points = 10
        challenge_title = challenge_id
    
    print(f"🎯 چالش {challenge_title} با {points} امتیاز تکمیل شد")
    
    # بروزرسانی جدول user_points
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # ایجاد جدول اگر وجود ندارد
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                user_id TEXT PRIMARY KEY,
                total_points INTEGER DEFAULT 0,
                weekly_points INTEGER DEFAULT 0,
                last_updated TIMESTAMP
            )
        ''')
        
        # بررسی وجود کاربر
        cursor.execute('SELECT total_points, weekly_points FROM user_points WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        today = datetime.now().date().isoformat()
        
        if row:
            total = row[0] + points
            weekly = row[1] + points
            cursor.execute('''
                UPDATE user_points 
                SET total_points = ?, weekly_points = ?, last_updated = ?
                WHERE user_id = ?
            ''', (total, weekly, datetime.now().isoformat(), user_id))
        else:
            cursor.execute('''
                INSERT INTO user_points (user_id, total_points, weekly_points, last_updated)
                VALUES (?, ?, ?, ?)
            ''', (user_id, points, points, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ امتیاز {points} به کاربر {user_id[:8]} اضافه شد")
        
        # تلاش برای استفاده از سیستم گیمیفیکیشن (اختیاری)
        try:
            from gamification import add_points_to_user
            add_points_to_user(user_id, points, f"تکمیل چالش: {challenge_title}")
        except ImportError:
            print("⚠️ ماژول gamification یافت نشد، فقط امتیاز در دیتابیس ثبت شد")
        except Exception as e:
            print(f"⚠️ خطا در گیمیفیکیشن: {e}")
        
        return {"success": True, "points": points}
        
    except Exception as e:
        print(f"❌ خطا در ثبت امتیاز: {e}")
        return {"success": False, "message": str(e)}

def get_user_points(user_id):
    """دریافت امتیازات کاربر"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('SELECT total_points, weekly_points FROM user_points WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        total_points = row[0] if row else 0
        weekly_points = row[1] if row else 0
        
        # تعداد چالش‌های انجام شده امروز
        today = datetime.now().date().isoformat()
        cursor.execute('SELECT COUNT(*) FROM daily_challenges WHERE user_id = ? AND date = ? AND status = "completed"', (user_id, today))
        completed_today = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total": total_points,
            "weekly": weekly_points,
            "completed": completed_today,
            "streak": 0
        }
    except Exception as e:
        print(f"خطا در دریافت امتیازات: {e}")
        return {"total": 0, "weekly": 0, "completed": 0, "streak": 0}

def get_weekly_certificate(user_id):
    """تولید و ذخیره گواهی هفتگی با طراحی حرفه‌ای"""
    from datetime import datetime
    import sqlite3
    import os
    from config import DB_NAME

    try:
        print(f"🔍 شروع تولید گواهی برای کاربر: {user_id}")
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # بررسی امتیاز هفتگی
        cursor.execute('SELECT weekly_points FROM user_points WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        weekly_points = row[0] if row else 0
        print(f"📊 امتیاز هفتگی: {weekly_points}")

        if weekly_points < 100:
            return {"success": False, "message": f"امتیاز هفتگی شما {weekly_points} است. برای دریافت گواهی به حداقل 100 امتیاز نیاز دارید."}

        # دریافت نام کاربر
        cursor.execute('SELECT name, lastname, user_code FROM users WHERE user_id = ?', (user_id,))
        user_row = cursor.fetchone()
        
        if user_row and user_row[0]:
            user_full_name = f"{user_row[0]} {user_row[1] if user_row[1] else ''}".strip()
        else:
            user_full_name = user_row[1] if user_row and user_row[1] else user_id[:8]
        
        user_code = user_row[2] if user_row else user_id[:8]

        # دریافت تعداد چالش‌های انجام شده
        cursor.execute('SELECT COUNT(*) FROM daily_challenges WHERE user_id = ? AND status = "completed"', (user_id,))
        challenges_count = cursor.fetchone()[0] or 0

        # دریافت سطح کاربر
        cursor.execute('SELECT current_level FROM gamification WHERE user_id = ?', (user_id,))
        level_row = cursor.fetchone()
        user_level = level_row[0] if level_row else 1

        # تاریخ امروز به شمسی (تقریبی)
        today = datetime.now()
        persian_date = f"{today.year} - {today.month} - {today.day}"

        # ساخت HTML گواهی با طراحی حرفه‌ای
        certificate_html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>گواهی تلاش هفتگی - مسیرینو</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
                @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Vazirmatn', 'Poppins', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 40px;
                }}
                
                .certificate-wrapper {{
                    max-width: 900px;
                    width: 100%;
                    animation: fadeInUp 0.8s ease-out;
                }}
                
                @keyframes fadeInUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(30px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                
                .certificate {{
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
                    border-radius: 32px;
                    padding: 50px;
                    position: relative;
                    overflow: hidden;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }}
                
                /* تزئینات پس‌زمینه */
                .certificate::before {{
                    content: '';
                    position: absolute;
                    top: -50%;
                    right: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(108,99,255,0.05) 0%, transparent 70%);
                    pointer-events: none;
                }}
                
                .certificate::after {{
                    content: '🎓';
                    position: absolute;
                    bottom: 20px;
                    left: 20px;
                    font-size: 100px;
                    opacity: 0.05;
                    pointer-events: none;
                }}
                
                /* هدر گواهی */
                .certificate-header {{
                    text-align: center;
                    margin-bottom: 30px;
                    position: relative;
                }}
                
                .logo {{
                    font-size: 4rem;
                    margin-bottom: 15px;
                    animation: float 3s ease-in-out infinite;
                }}
                
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                
                .title {{
                    font-size: 2.5rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #6c63ff, #ff6584);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    margin-bottom: 10px;
                }}
                
                .subtitle {{
                    color: #666;
                    font-size: 0.9rem;
                    letter-spacing: 2px;
                }}
                
                /* بدنه گواهی */
                .certificate-body {{
                    text-align: center;
                    margin: 40px 0;
                    position: relative;
                }}
                
                .award-text {{
                    color: #888;
                    font-size: 1.1rem;
                    margin-bottom: 20px;
                }}
                
                .recipient-name {{
                    font-size: 2.2rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #333, #6c63ff);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    margin: 20px 0;
                    padding: 10px 20px;
                    display: inline-block;
                    border-bottom: 3px solid #6c63ff;
                    border-top: 3px solid #ff6584;
                }}
                
                .stats-container {{
                    display: flex;
                    justify-content: center;
                    gap: 30px;
                    margin: 35px 0;
                    flex-wrap: wrap;
                }}
                
                .stat-box {{
                    background: linear-gradient(135deg, #f5f7fa, #fff);
                    border-radius: 20px;
                    padding: 20px 30px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
                    border: 1px solid rgba(108,99,255,0.2);
                    min-width: 140px;
                }}
                
                .stat-icon {{
                    font-size: 2rem;
                    margin-bottom: 10px;
                }}
                
                .stat-value {{
                    font-size: 2rem;
                    font-weight: 800;
                    color: #6c63ff;
                }}
                
                .stat-label {{
                    color: #888;
                    font-size: 0.8rem;
                    margin-top: 5px;
                }}
                
                .message {{
                    background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(255,101,132,0.08));
                    border-radius: 20px;
                    padding: 20px;
                    margin: 25px 0;
                    font-size: 1rem;
                    color: #555;
                    line-height: 1.8;
                    border-right: 4px solid #6c63ff;
                }}
                
                /* فوتر گواهی */
                .certificate-footer {{
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-end;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px dashed #ddd;
                    flex-wrap: wrap;
                    gap: 20px;
                }}
                
                .signature {{
                    text-align: center;
                }}
                
                .signature-line {{
                    width: 150px;
                    height: 2px;
                    background: linear-gradient(90deg, #6c63ff, #ff6584);
                    margin: 10px 0;
                }}
                
                .signature-text {{
                    color: #888;
                    font-size: 0.8rem;
                }}
                
                .certificate-id {{
                    text-align: left;
                    color: #aaa;
                    font-size: 0.7rem;
                }}
                
                .date {{
                    text-align: right;
                    color: #aaa;
                    font-size: 0.8rem;
                }}
                
                .stamp {{
                    position: absolute;
                    bottom: 50px;
                    right: 50px;
                    width: 100px;
                    height: 100px;
                    border: 3px solid #ff6584;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.8rem;
                    font-weight: bold;
                    color: #ff6584;
                    transform: rotate(-15deg);
                    background: rgba(255,101,132,0.05);
                    pointer-events: none;
                }}
                
                .stamp span {{
                    transform: rotate(15deg);
                    display: inline-block;
                }}
                
                /* مدال‌ها */
                .medal-badge {{
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                    background: linear-gradient(135deg, #ffd700, #ffed4e);
                    padding: 5px 15px;
                    border-radius: 50px;
                    font-size: 0.8rem;
                    font-weight: bold;
                    color: #8B6914;
                    margin-top: 15px;
                }}
                
                @media (max-width: 600px) {{
                    .certificate {{ padding: 25px; }}
                    .title {{ font-size: 1.8rem; }}
                    .recipient-name {{ font-size: 1.5rem; }}
                    .stats-container {{ gap: 15px; }}
                    .stat-box {{ padding: 12px 20px; min-width: 100px; }}
                    .stat-value {{ font-size: 1.5rem; }}
                    .stamp {{ width: 70px; height: 70px; bottom: 30px; right: 30px; font-size: 0.6rem; }}
                }}
                
                @media print {{
                    body {{
                        background: white;
                        padding: 0;
                    }}
                    .certificate {{
                        box-shadow: none;
                        padding: 30px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="certificate-wrapper">
                <div class="certificate">
                    <div class="certificate-header">
                        <div class="logo">🎓</div>
                        <h1 class="title">گواهی تلاش هفتگی</h1>
                        <p class="subtitle">CERTIFICATE OF ACHIEVEMENT</p>
                    </div>
                    
                    <div class="certificate-body">
                        <p class="award-text">این گواهی به پاس تلاش و پشتکار در هفته گذشته به</p>
                        <div class="recipient-name">{user_full_name}</div>
                        
                        <div class="stats-container">
                            <div class="stat-box">
                                <div class="stat-icon">⭐</div>
                                <div class="stat-value">{weekly_points}</div>
                                <div class="stat-label">امتیاز کسب شده</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-icon">✅</div>
                                <div class="stat-value">{challenges_count}</div>
                                <div class="stat-label">چالش انجام شده</div>
                            </div>
                            <div class="stat-box">
                                <div class="stat-icon">🏆</div>
                                <div class="stat-value">{user_level}</div>
                                <div class="stat-label">سطح کاربری</div>
                            </div>
                        </div>
                        
                        <div class="message">
                            🌟 تو ثابت کردی که با پشتکار و انضباط می‌توان به هر هدفی رسید.<br>
                            این گواهی نمادی از تعهد تو به پیشرفت و یادگیری است. به خودت افتخار کن!
                        </div>
                        
                        <div class="medal-badge">
                            🏅 مدال تلاشگر هفته
                        </div>
                    </div>
                    
                    <div class="certificate-footer">
                        <div class="signature">
                            <div class="signature-line"></div>
                            <div class="signature-text">مدیر مسیرینو</div>
                        </div>
                        <div class="date">
                            📅 تاریخ: {persian_date}
                        </div>
                        <div class="certificate-id">
                            🆔 کد: {user_code[:8]}
                        </div>
                    </div>
                    
                    <div class="stamp">
                        <span>تأیید شد ✓</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # ذخیره فایل در پوشه static
        static_dir = "static"
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        filename = f"cert_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        file_path = os.path.join(static_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(certificate_html)
        
        print(f"✅ فایل گواهی ذخیره شد: {file_path}")
        
        # مسیر نسبی برای استفاده در URL
        url_path = f"/static/{filename}"

        # ثبت در دیتابیس
        cursor.execute('''
            INSERT INTO certificates (user_id, certificate_type, earned_at, file_path)
            VALUES (?, 'weekly_effort', ?, ?)
        ''', (user_id, datetime.now().isoformat(), file_path))

        conn.commit()
        conn.close()

        return {"success": True, "message": "گواهی شما صادر شد!", "url": url_path}

    except Exception as e:
        print(f"❌ خطا در صدور گواهی: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "message": f"خطای داخلی: {str(e)}"}