import json
from datetime import datetime
from persian_calendar import PersianCalendar

def get_calendar_data(user_id, year, month):
    """دریافت تمام داده‌های تقویم برای یک ماه شمسی"""
    calendar = PersianCalendar()
    
    # رویدادهای ثابت
    monthly_events = calendar.get_month_events(year, month)
    
    # رویدادهای مطالعاتی
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
    
    return {
        "year": year,
        "month": month,
        "month_name": calendar.MONTHS[month - 1],
        "month_days": calendar.get_month_days(year, month),
        "first_weekday": calendar.get_first_weekday(year, month),
        "weekdays": calendar.WEEKDAYS,
        "events": all_events,
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
    """دریافت برنامه مطالعاتی کاربر برای ماه شمسی"""
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
                "description": f"مدت زمان: {row[2]} دقیقه | اولویت: {row[3]}",
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
        
        # اطمینان از وجود جدول
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
        print(f"✅ رویداد ذخیره شد: {title} - {date_str}")
        return True
    except Exception as e:
        print(f"❌ خطا در افزودن رویداد: {e}")
        return False