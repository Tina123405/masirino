from datetime import datetime

class PersianCalendar:
    """کلاس مدیریت تقویم شمسی"""
    
    # نام ماه‌های شمسی
    MONTHS = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    
    # نام روزهای هفته (شنبه = 0, جمعه = 6)
    WEEKDAYS = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]
    
    @staticmethod
    def is_leap_year(year):
        """تشخیص سال کبیسه شمسی"""
        return ((year + 38) % 2820 == 0) or ((year + 38) % 2820 == 4) or \
               ((year + 38) % 2820 == 8) or ((year + 38) % 2820 == 12) or \
               ((year + 38) % 2820 == 16) or ((year + 38) % 2820 == 20) or \
               ((year + 38) % 2820 == 24) or ((year + 38) % 2820 == 28) or \
               ((year + 38) % 2820 == 32) or ((year + 38) % 2820 == 36)
    
    @staticmethod
    def get_month_days(year, month):
        """تعداد روزهای ماه شمسی"""
        if 1 <= month <= 6:
            return 31
        elif 7 <= month <= 11:
            return 30
        else:  # month == 12
            return 29 if PersianCalendar.is_leap_year(year) else 28
    
    @staticmethod
    def get_first_weekday(year, month):
        """
        محاسبه اولین روز هفته ماه شمسی
        بازگشت: 0=شنبه, 1=یکشنبه, ..., 6=جمعه
        """
        # تاریخ مبنا: 1 فروردین 1400 = 22 مارس 2021 = روز دوشنبه
        # دوشنبه در سیستم ما = 2 (شنبه=0, یکشنبه=1, دوشنبه=2)
        base_year = 1400
        base_month = 1
        base_day = 1
        base_weekday = 2  # دوشنبه
        
        # محاسبه اختلاف روزها
        days_diff = 0
        
        # اختلاف سال‌ها
        for y in range(base_year, year):
            days_diff += 365 + (1 if PersianCalendar.is_leap_year(y) else 0)
        
        # اختلاف ماه‌ها در سال جاری
        for m in range(base_month, month):
            days_diff += PersianCalendar.get_month_days(year, m)
        
        # محاسبه روز هفته (شنبه = 0)
        return (base_weekday + days_diff) % 7
    
    @staticmethod
    def get_current_date():
        """دریافت تاریخ شمسی امروز (بدون نیاز به jdatetime)"""
        now = datetime.now()
        
        # تبدیل تقریبی میلادی به شمسی
        # روز مبنا: 1 فروردین 1400 = 22 مارس 2021 (روز 81 سال میلادی)
        miladi_year = now.year
        miladi_day_of_year = now.timetuple().tm_yday
        
        # محاسبه سال شمسی
        if miladi_day_of_year >= 80:  # بعد از 21 مارس
            persian_year = miladi_year - 621
            persian_day = miladi_day_of_year - 79
        else:
            persian_year = miladi_year - 622
            persian_day = miladi_day_of_year + 286
        
        # محاسبه ماه و روز شمسی
        persian_month = 1
        for m in range(1, 13):
            month_days = PersianCalendar.get_month_days(persian_year, m)
            if persian_day <= month_days:
                persian_month = m
                break
            persian_day -= month_days
        
        return {
            "year": persian_year,
            "month": persian_month,
            "day": persian_day,
            "weekday": datetime.now().weekday(),
            "weekday_name": PersianCalendar.WEEKDAYS[datetime.now().weekday()],
            "month_name": PersianCalendar.MONTHS[persian_month - 1]
        }
    
    @staticmethod
    def get_month_events(year, month):
        """رویدادهای ثابت شمسی"""
        events = {
            (1, 1): {"title": "🎊 نوروز - سال نو مبارک", "type": "holiday", "description": "آغاز سال نو"},
            (1, 13): {"title": "🏞️ سیزده بدر - روز طبیعت", "type": "holiday", "description": "روز طبیعت"},
            (2, 14): {"title": "🎂 روز پدر", "type": "religious", "description": "ولادت حضرت علی (ع)"},
            (3, 20): {"title": "📅 پایان سال تحصیلی", "type": "school", "description": "پایان امتحانات"},
            (6, 1): {"title": "📅 شروع مدارس", "type": "school_start", "description": "بازگشایی مدارس"},
            (9, 16): {"title": "🎓 روز دانشجو", "type": "event", "description": "۱۶ آذر"},
            (9, 30): {"title": "🌙 شب یلدا", "type": "event", "description": "شب چله"},
            (10, 11): {"title": "🎂 روز زن", "type": "religious", "description": "ولادت حضرت زهرا (س)"},
            (11, 22): {"title": "🎊 ۲۲ بهمن", "type": "holiday", "description": "پیروزی انقلاب"},
            (12, 29): {"title": "🎊 عید نوروز", "type": "holiday", "description": "آغاز سال جدید"},
        }
        
        month_events = []
        for (m, d), event in events.items():
            if m == month:
                month_events.append({
                    "id": f"{year}_{m}_{d}",
                    "date": f"{year}-{m:02d}-{d:02d}",
                    "title": event["title"],
                    "type": event["type"],
                    "description": event["description"],
                    "is_fixed": True
                })
        
        # رویدادهای امتحانات فصلی
        if month == 3:
            month_events.append({
                "id": "exam_june",
                "date": f"{year}-03-15",
                "title": "📝 امتحانات خرداد",
                "type": "exam",
                "description": "شروع امتحانات پایان سال"
            })
        elif month == 9:
            month_events.append({
                "id": "exam_azar",
                "date": f"{year}-09-15",
                "title": "📝 امتحانات آذر",
                "type": "exam",
                "description": "امتحانات میان ترم"
            })
        elif month == 10:
            month_events.append({
                "id": "exam_day",
                "date": f"{year}-10-15",
                "title": "📝 امتحانات دی",
                "type": "exam",
                "description": "امتحانات پایان ترم اول"
            })
        
        return month_events


def get_calendar_data(user_id, year, month):
    """دریافت تمام داده‌های تقویم برای یک ماه شمسی"""
    cal = PersianCalendar()
    
    # اطلاعات پایه ماه
    month_days = cal.get_month_days(year, month)
    first_weekday = cal.get_first_weekday(year, month)
    
    # رویدادهای ثابت
    monthly_events = cal.get_month_events(year, month)
    
    # رویدادهای مطالعاتی (از دیتابیس)
    study_plans = get_study_plan_events(user_id, year, month)
    
    # رویدادهای چالش‌ها
    challenges = get_challenge_events(user_id, year, month)
    
    # ضرب‌الاجل‌های اهداف
    goal_deadlines = get_goal_deadlines(user_id, year, month)
    
    # رویدادهای شخصی کاربر
    user_events = get_user_events(user_id, year, month)
    
    all_events = monthly_events + study_plans + challenges + goal_deadlines + user_events
    
    # حذف رویدادهای تکراری
    unique_events = {}
    for event in all_events:
        if event["id"] not in unique_events:
            unique_events[event["id"]] = event
    all_events = list(unique_events.values())
    
    all_events.sort(key=lambda x: x.get("date", ""))
    
    current_date = cal.get_current_date()
    
    return {
        "year": year,
        "month": month,
        "month_name": cal.MONTHS[month - 1],
        "month_days": month_days,
        "first_weekday": first_weekday,
        "weekdays": cal.WEEKDAYS,
        "events": all_events,
        "current": {
            "year": current_date["year"],
            "month": current_date["month"],
            "day": current_date["day"]
        },
        "summary": {
            "total_events": len(all_events),
            "exam_count": len([e for e in all_events if e.get("type") == "exam"]),
            "holiday_count": len([e for e in all_events if e.get("type") == "holiday"]),
            "study_count": len([e for e in all_events if e.get("type") == "study_task"]),
            "challenge_count": len([e for e in all_events if e.get("type") == "challenge"]),
            "goal_count": len([e for e in all_events if e.get("type") == "goal_deadline"])
        }
    }


def get_study_plan_events(user_id, year, month):
    """دریافت برنامه مطالعاتی کاربر"""
    events = []
    import sqlite3
    from config import DB_NAME
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        month_str = f"{year}-{month:02d}"
        cursor.execute('''
            SELECT subject, planned_date, duration, priority
            FROM study_plans 
            WHERE user_id = ? AND planned_date LIKE ?
            ORDER BY planned_date
        ''', (user_id, f"{month_str}%"))
        
        results = cursor.fetchall()
        for row in results:
            events.append({
                "id": f"study_{row[1]}",
                "date": row[1],
                "title": f"📖 مطالعه {row[0]}",
                "type": "study_task",
                "description": f"مدت: {row[2]} دقیقه | اولویت: {row[3]}",
                "duration": row[2],
                "priority": row[3]
            })
        conn.close()
    except Exception as e:
        print(f"خطا در دریافت برنامه مطالعاتی: {e}")
    
    return events


def get_challenge_events(user_id, year, month):
    """دریافت چالش‌های تکمیل شده"""
    events = []
    import sqlite3
    from config import DB_NAME
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        month_str = f"{year}-{month:02d}"
        cursor.execute('''
            SELECT title, date, points
            FROM daily_challenges 
            WHERE user_id = ? AND status = 'completed' AND date LIKE ?
            ORDER BY date
        ''', (user_id, f"{month_str}%"))
        
        results = cursor.fetchall()
        for row in results:
            events.append({
                "id": f"challenge_{row[1]}",
                "date": row[1],
                "title": f"🏆 {row[0]}",
                "type": "challenge",
                "description": f"+{row[2]} امتیاز",
                "points": row[2]
            })
        conn.close()
    except Exception as e:
        print(f"خطا در دریافت چالش‌ها: {e}")
    
    return events


def get_goal_deadlines(user_id, year, month):
    """دریافت ضرب‌الاجل‌های اهداف SMART"""
    events = []
    import sqlite3
    from config import DB_NAME
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        month_str = f"{year}-{month:02d}"
        cursor.execute('''
            SELECT title, deadline, priority, progress
            FROM smart_goals 
            WHERE user_id = ? AND deadline IS NOT NULL AND deadline LIKE ?
            ORDER BY deadline
        ''', (user_id, f"{month_str}%"))
        
        results = cursor.fetchall()
        for row in results:
            status = "⚠️" if row[3] < 50 else "✅"
            events.append({
                "id": f"goal_{row[1]}",
                "date": row[1],
                "title": f"{status} {row[0]}",
                "type": "goal_deadline",
                "description": f"اولویت: {row[2]} | پیشرفت: {row[3]}%",
                "progress": row[3]
            })
        conn.close()
    except Exception as e:
        print(f"خطا در دریافت اهداف: {e}")
    
    return events


def get_user_events(user_id, year, month):
    """دریافت رویدادهای شخصی کاربر"""
    events = []
    import sqlite3
    from config import DB_NAME
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        month_str = f"{year}-{month:02d}"
        cursor.execute('''
            SELECT title, date, description, event_type, id
            FROM user_calendar_events 
            WHERE user_id = ? AND date LIKE ?
            ORDER BY date
        ''', (user_id, f"{month_str}%"))
        
        results = cursor.fetchall()
        for row in results:
            events.append({
                "id": row[4],
                "date": row[1],
                "title": f"📌 {row[0]}",
                "type": row[3] if row[3] else "custom",
                "description": row[2] if row[2] else "",
                "is_custom": True
            })
        conn.close()
    except Exception as e:
        print(f"خطا در دریافت رویدادهای شخصی: {e}")
    
    return events


def add_user_event(user_id, title, date_str, description):
    """افزودن رویداد شخصی کاربر"""
    import sqlite3
    from config import DB_NAME
    from datetime import datetime
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                date TEXT,
                description TEXT,
                event_type TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT INTO user_calendar_events (user_id, title, date, description, event_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, title, date_str, description, "custom", datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در افزودن رویداد: {e}")
        return False