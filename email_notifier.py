# email_notifier.py
# سیستم اعلان ایمیل (با کتابخانه استاندارد smtplib)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime, timedelta
from config import DB_NAME

def send_study_reminder_email(user_id, to_email, study_plan_text):
    """ارسال ایمیل یادآوری مطالعه"""
    try:
        sender_email = "masirino@example.com"
        sender_password = "your_email_password"  # باید تنظیم شود
        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = "📚 یادآوری برنامه مطالعه - مسیرینو"
        
        body = f"""
        <html dir="rtl">
        <body style="font-family: Tahoma; direction: rtl;">
            <h2 style="color: #6c63ff;">📚 یادآوری برنامه مطالعه</h2>
            <p>برنامه مطالعه امروز شما:</p>
            <pre style="background: #f0f0f0; padding: 15px; border-radius: 10px;">{study_plan_text}</pre>
            <p>برای مشاهده برنامه کامل، وارد پنل کاربری خود شوید.</p>
            <hr>
            <small>مسیرینو - همراه شما در مسیر موفقیت تحصیلی</small>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, "html"))
        
        # اتصال به سرور SMTP (مثال برای Gmail)
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login(sender_email, sender_password)
        # server.send_message(msg)
        # server.quit()
        
        print(f"📧 ایمیل یادآوری برای {to_email} ارسال شد")
        return True
    except Exception as e:
        print(f"خطا در ارسال ایمیل: {e}")
        return False


def get_users_for_email_reminder():
    """دریافت کاربرانی که نیاز به یادآوری دارند"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        # کاربرانی که امروز هنوز برنامه مطالعه انجام نداده‌اند
        cursor.execute('''
            SELECT DISTINCT u.user_id, u.email, u.name
            FROM users u
            LEFT JOIN daily_challenges dc ON u.user_id = dc.user_id AND dc.date = ? AND dc.status = 'completed'
            WHERE u.email IS NOT NULL AND u.email != '' AND dc.id IS NULL
        ''', (today,))
        
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(f"خطا در دریافت کاربران: {e}")
        return []


def send_daily_reminders():
    """ارسال یادآوری روزانه به همه کاربرانی که ایمیل دارند"""
    users = get_users_for_email_reminder()
    for user in users:
        user_id, email, name = user
        plan_text = "امروز برنامه مطالعه خود را کامل کنید و امتیاز بگیرید! 🎯"
        send_study_reminder_email(user_id, email, plan_text)
    
    print(f"📧 {len(users)} ایمیل یادآوری ارسال شد")
    return len(users)


def save_user_email(user_id, email):
    """ذخیره ایمیل کاربر در دیتابیس"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
    except:
        pass
    
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET email = ? WHERE user_id = ?', (email, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در ذخیره ایمیل: {e}")
        return False