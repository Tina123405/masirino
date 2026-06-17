# email_sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from config import DB_NAME

def send_daily_reminders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # دریافت کاربرانی که ایمیل دارند
    cursor.execute('SELECT user_id, name, email FROM users WHERE email IS NOT NULL AND email != ""')
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        user_id, name, email = user
        send_email_reminder(email, name, user_id)

def send_email_reminder(to_email, name, user_id):
    try:
        sender_email = "masirino@example.com"  # ایمیل خودت
        sender_password = "your_password"      # رمز ایمیل خودت
        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = "📚 یادآوری مطالعه - مسیرینو"
        
        body = f"""
        <html dir="rtl">
        <body style="font-family: Tahoma; direction: rtl;">
            <h2 style="color: #6c63ff;">سلام {name if name else 'کاربر گرامی'}! 🌟</h2>
            <p>این یک یادآوری دوستانه از <strong>مسیرینو</strong> است:</p>
            <ul>
                <li>✅ امروز چند تا چالش انجام دادی؟</li>
                <li>📖 برنامه مطالعه امروزت رو چک کن</li>
                <li>🎯 به اهداف SMART خودت نزدیکتر شو</li>
            </ul>
            <p>برای ورود به پنل کاربری کلیک کن:</p>
            <a href="http://localhost:8000/?session_id={user_id}" style="background:#6c63ff;color:white;padding:10px 20px;text-decoration:none;border-radius:30px;">ورود به مسیرینو</a>
            <hr>
            <small>مسیرینو - همراه تو در مسیر موفقیت تحصیلی</small>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, "html"))
        
        # اتصال به سرور ایمیل (مثال برای Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ ایمیل برای {to_email} ارسال شد")
    except Exception as e:
        print(f"❌ خطا در ارسال ایمیل به {to_email}: {e}")