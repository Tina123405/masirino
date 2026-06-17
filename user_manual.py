# user_manual.py - نسخه کامل و پیشرفته با گرافیک زیبا و توضیحات جامع

def render_user_manual_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>دفترچه راهنمای جامع مسیرینو | مشاور هوشمند تحصیلی</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
            color: #fff;
            line-height: 1.7;
            scroll-behavior: smooth;
        }}
        
        /* اسکرول بار سفارشی */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        ::-webkit-scrollbar-track {{
            background: #1e1e3a;
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            border-radius: 10px;
        }}
        
        .container {{
            max-width: 1300px;
            margin: 0 auto;
            padding: 30px 25px;
        }}
        
        /* کارت‌های شیشه‌ای با انیمیشن */
        .glass-card {{
            background: rgba(255, 255, 255, 0.07);
            backdrop-filter: blur(15px);
            border-radius: 32px;
            padding: 32px;
            margin-bottom: 28px;
            transition: all 0.4s cubic-bezier(0.2, 0.9, 0.4, 1.1);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }}
        
        .glass-card:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(108, 99, 255, 0.4);
            box-shadow: 0 15px 40px rgba(108, 99, 255, 0.2);
        }}
        
        h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff, #a8a4ff, #ff9eb6);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 20px;
            letter-spacing: -0.5px;
        }}
        
        h2 {{
            font-size: 1.9rem;
            font-weight: 700;
            margin-bottom: 25px;
            padding-right: 18px;
            border-right: 5px solid #6c63ff;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        h3 {{
            font-size: 1.3rem;
            font-weight: 600;
            margin: 20px 0 12px 0;
            color: #c4c4ff;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 22px;
            margin: 30px 0;
        }}
        
        .feature-item {{
            background: rgba(0, 0, 0, 0.35);
            padding: 18px 22px;
            border-radius: 24px;
            display: flex;
            align-items: center;
            gap: 18px;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .feature-item:hover {{
            transform: translateX(-6px);
            background: rgba(108, 99, 255, 0.2);
            border-color: rgba(108, 99, 255, 0.4);
        }}
        
        .feature-icon {{ font-size: 2.4rem; }}
        .feature-title {{ font-weight: 800; margin-bottom: 6px; font-size: 1.1rem; }}
        .feature-desc {{ font-size: 0.85rem; color: #c4c4f0; line-height: 1.5; }}
        
        .toc {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 12px;
            margin: 25px 0;
        }}
        
        .toc-item {{
            background: rgba(0, 0, 0, 0.35);
            padding: 12px 18px;
            border-radius: 16px;
            transition: all 0.3s;
            color: #e0e0ff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 500;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .toc-item:hover {{
            background: linear-gradient(90deg, rgba(108, 99, 255, 0.4), rgba(255, 101, 132, 0.2));
            transform: translateX(-5px);
            color: white;
            border-color: #6c63ff;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 30px;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            border: none;
            border-radius: 50px;
            color: white;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s;
            cursor: pointer;
            font-size: 0.95rem;
        }}
        
        .btn:hover {{
            transform: scale(1.03);
            box-shadow: 0 8px 25px rgba(108, 99, 255, 0.5);
        }}
        
        .btn-outline {{
            background: transparent;
            border: 2px solid #6c63ff;
        }}
        
        .btn-outline:hover {{
            background: rgba(108, 99, 255, 0.2);
        }}
        
        .contact-section {{
            background: linear-gradient(135deg, rgba(108, 99, 255, 0.2), rgba(255, 101, 132, 0.2));
            border-radius: 28px;
            padding: 28px;
            margin: 25px 0;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        
        .contact-buttons {{
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin: 20px 0;
        }}
        
        .contact-btn {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 14px 28px;
            border-radius: 60px;
            text-decoration: none;
            font-weight: 700;
            transition: all 0.3s;
            font-size: 1rem;
        }}
        
        .contact-btn.telegram {{
            background: #0088cc;
            color: white;
        }}
        
        .contact-btn.gmail {{
            background: #ea4335;
            color: white;
        }}
        
        .contact-btn:hover {{
            transform: translateY(-4px);
            filter: brightness(1.08);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }}
        
        .step {{
            display: flex;
            align-items: flex-start;
            gap: 18px;
            margin: 22px 0;
            padding: 18px;
            background: rgba(0, 0, 0, 0.25);
            border-radius: 24px;
            transition: all 0.3s;
        }}
        
        .step:hover {{
            background: rgba(108, 99, 255, 0.15);
            transform: translateX(5px);
        }}
        
        .step-number {{
            width: 42px;
            height: 42px;
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1.2rem;
            flex-shrink: 0;
        }}
        
        .info-box {{
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            padding: 18px;
            margin: 15px 0;
            border-right: 3px solid #ff6584;
        }}
        
        .badge {{
            display: inline-block;
            background: rgba(108, 99, 255, 0.3);
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            margin-left: 8px;
        }}
        
        .footer {{
            text-align: center;
            padding: 35px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 50px;
            color: #aaa;
            font-size: 0.85rem;
        }}
        
        .faq-item {{
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 18px;
            margin-bottom: 16px;
            transition: 0.2s;
        }}
        
        .faq-item:hover {{
            background: rgba(108, 99, 255, 0.15);
        }}
        
        .game-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .game-card {{
            background: rgba(255,255,255,0.08);
            padding: 18px 12px;
            border-radius: 20px;
            text-align: center;
            transition: 0.3s;
            cursor: default;
        }}
        
        .game-card:hover {{
            background: rgba(108, 99, 255, 0.3);
            transform: scale(1.02);
        }}
        
        code {{
            background: #1e1e3a;
            padding: 4px 12px;
            border-radius: 12px;
            font-family: monospace;
            font-size: 0.85rem;
            color: #ff9eb6;
        }}
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 2rem; }}
            h2 {{ font-size: 1.4rem; }}
            .container {{ padding: 15px; }}
            .glass-card {{ padding: 20px; }}
            .features-grid {{ grid-template-columns: 1fr; }}
            .toc {{ grid-template-columns: 1fr; }}
        }}
        
        .flex-between {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .text-gradient {{
            background: linear-gradient(135deg, #ffd89b, #ff9eb6);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }}
    </style>
</head>
<body>
<div class="container">
    <!-- هدر با دکمه‌ها -->
    <div class="flex-between">
        <a href="/?session_id={session_id}" class="btn btn-outline">
            <i class="fas fa-arrow-right"></i> بازگشت به صفحه اصلی
        </a>
        <button onclick="window.print()" class="btn">
            <i class="fas fa-print"></i> چاپ / ذخیره PDF
        </button>
    </div>
    
    <!-- بخش معرفی اصلی -->
    <div class="glass-card text-center">
        <div class="text-8xl mb-4">🎓✨</div>
        <h1>دفترچه راهنمای جامع مسیرینو</h1>
        <p class="text-xl text-gray-200 mt-3">مشاور هوشمند تحصیلی با بیش از ۲۵ قابلیت پیشرفته | نسخه ۴.۰</p>
        <p class="text-yellow-300 text-sm mt-4">
            <i class="fas fa-bolt"></i> بدون نیاز به نصب کتابخانه خارجی | <i class="fas fa-shield-alt"></i> حریم خصوصی کامل | <i class="fas fa-chart-line"></i> تحلیل هوشمند
        </p>
        
        <div class="contact-section mt-5">
            <p class="text-white mb-3"><i class="fas fa-headset"></i> <strong>ارتباط مستقیم با تیم توسعه‌دهنده</strong></p>
            <div class="contact-buttons">
                <a href="https://t.me/yehasati" target="_blank" class="contact-btn telegram">
                    <i class="fab fa-telegram"></i> تلگرام: @yehasati
                </a>
                <a href="mailto:dramaliama632@gmail.com" class="contact-btn gmail">
                    <i class="fas fa-envelope"></i> ایمیل: dramaliama632@gmail.com
                </a>
            </div>
            <div class="info-box mt-3">
                <i class="fas fa-clock"></i> پاسخگویی ۲۴ ساعته | <i class="fas fa-users"></i> پشتیبانی آنلاین
            </div>
        </div>
    </div>
    
    <!-- فهرست مطالب پیشرفته -->
    <div class="glass-card">
        <h2><i class="fas fa-list-ul"></i> فهرست مطالب جامع</h2>
        <div class="toc">
            <a href="#intro" class="toc-item"><i class="fas fa-star-of-life"></i> 1. معرفی مسیرینو</a>
            <a href="#contact" class="toc-item"><i class="fas fa-phone-alt"></i> 2. ارتباط با ما</a>
            <a href="#quickstart" class="toc-item"><i class="fas fa-rocket"></i> 3. شروع سریع</a>
            <a href="#chat" class="toc-item"><i class="fas fa-microphone-alt"></i> 4. چت هوشمند صوتی</a>
            <a href="#track" class="toc-item"><i class="fas fa-chalkboard-user"></i> 5. انتخاب رشته (۵ معیار)</a>
            <a href="#risk" class="toc-item"><i class="fas fa-chart-line"></i> 6. پیش‌بینی افت (۱۲ فاکتور)</a>
            <a href="#holland" class="toc-item"><i class="fas fa-brain"></i> 7. آزمون هالند (۴۵ سوال)</a>
            <a href="#ml-predict" class="toc-item"><i class="fas fa-robot"></i> 8. پیش‌بینی نمره با AI</a>
            <a href="#smart-planner" class="toc-item"><i class="fas fa-calendar-alt"></i> 9. برنامه‌ریز هوشمند</a>
            <a href="#smart-summarizer" class="toc-item"><i class="fas fa-file-alt"></i> 10. خلاصه‌ساز هوشمند</a>
            <a href="#pathfinder" class="toc-item"><i class="fas fa-road"></i> 11. مسیرشو (نقشه شغلی)</a>
            <a href="#gamification" class="toc-item"><i class="fas fa-trophy"></i> 12. گیمیفیکیشن</a>
            <a href="#challenges" class="toc-item"><i class="fas fa-tasks"></i> 13. چالش‌های روزانه</a>
            <a href="#groups" class="toc-item"><i class="fas fa-users"></i> 14. گروه‌های مطالعه</a>
            <a href="#calendar" class="toc-item"><i class="fas fa-calendar-week"></i> 15. تقویم آموزشی</a>
            <a href="#pomodoro" class="toc-item"><i class="fas fa-hourglass-half"></i> 16. تایمر پومودورو</a>
            <a href="#goals" class="toc-item"><i class="fas fa-bullseye"></i> 17. اهداف SMART</a>
            <a href="#exam" class="toc-item"><i class="fas fa-pen-alt"></i> 18. تولید سوال امتحانی</a>
            <a href="#games" class="toc-item"><i class="fas fa-gamepad"></i> 19. بازی‌های آموزشی</a>
            <a href="#profile" class="toc-item"><i class="fas fa-id-card"></i> 20. پروفایل شخصی</a>
            <a href="#analytics" class="toc-item"><i class="fas fa-chart-pie"></i> 21. داشبورد تحلیلی</a>
            <a href="#api" class="toc-item"><i class="fas fa-plug"></i> 22. API عمومی</a>
            <a href="#faq" class="toc-item"><i class="fas fa-question-circle"></i> 23. سوالات متداول</a>
            <a href="#school-api" class="toc-item"><i class="fas fa-school"></i> 24. اتصال به سامانه مدرسه</a>
            <a href="#support" class="toc-item"><i class="fas fa-life-ring"></i> 25. پشتیبانی و تیکت</a>
        </div>
    </div>
    
    <!-- 1. معرفی کامل -->
    <div id="intro" class="glass-card">
        <h2><i class="fas fa-star-of-life"></i> 1. معرفی مسیرینو</h2>
        <p><strong>مسیرینو</strong> یک پلتفرم پیشرفته مشاوره تحصیلی هوشمند است که با بهره‌گیری از الگوریتم‌های هوش مصنوعی و روانشناسی مدرن، به دانش‌آموزان در مسیر موفقیت تحصیلی و شغلی کمک می‌کند.</p>
        <div class="features-grid">
            <div class="feature-item"><div class="feature-icon">🎯</div><div class="feature-text"><div class="feature-title">انتخاب رشته هوشمند</div><div class="feature-desc">تحلیل ۵ معیاره توانایی، علاقه، سبک فکری، آینده شغلی و معدل</div></div></div>
            <div class="feature-item"><div class="feature-icon">⚠️</div><div class="feature-text"><div class="feature-title">سیستم هشدار افت تحصیلی</div><div class="feature-desc">بررسی ۱۲ فاکتور خطر + برنامه جبرانی شخصی‌سازی شده</div></div></div>
            <div class="feature-item"><div class="feature-icon">🧪</div><div class="feature-text"><div class="feature-title">آزمون هالند حرفه‌ای</div><div class="feature-desc">۴۵ سوال استاندارد با تفسیر تیپ‌های ۶ گانه شغلی</div></div></div>
            <div class="feature-item"><div class="feature-icon">🤖</div><div class="feature-text"><div class="feature-title">پیش‌بینی AI از صفر</div><div class="feature-desc">مدل Random Forest با دقت بالای ۸۵٪ برای پیش‌بینی نمرات</div></div></div>
            <div class="feature-item"><div class="feature-icon">📅</div><div class="feature-text"><div class="feature-title">برنامه‌ریز تطبیقی</div><div class="feature-desc">تنظیم خودکار برنامه بر اساس زمان باقی‌مانده و نقاط ضعف</div></div></div>
            <div class="feature-item"><div class="feature-icon">✨</div><div class="feature-text"><div class="feature-title">خلاصه‌ساز هوشمند متن</div><div class="feature-desc">استخراج نکات کلیدی، فلش‌کارت و خلاصه درس در کمتر از ۵ ثانیه</div></div></div>
            <div class="feature-item"><div class="feature-icon">🗺️</div><div class="feature-text"><div class="feature-title">مسیرشو (نقشه راه شغلی)</div><div class="feature-desc">برنامه ۵ ساله شامل مهارت‌ها، منابع، مشاغل مرتبط و گام‌های عملی</div></div></div>
            <div class="feature-item"><div class="feature-icon">🏆</div><div class="feature-text"><div class="feature-title">گیمیفیکیشن پیشرفته</div><div class="feature-desc">۱۰ سطح، ۱۵ مدال، لیدربورد هفتگی و ماهانه</div></div></div>
            <div class="feature-item"><div class="feature-icon">🎮</div><div class="feature-text"><div class="feature-title">۸ بازی آموزشی تعاملی</div><div class="feature-desc">یادگیری از طریق بازی با دریافت امتیاز و جایزه</div></div></div>
            <div class="feature-item"><div class="feature-icon">🎤</div><div class="feature-text"><div class="feature-title">چت بات صوتی کامل</div><div class="feature-desc">تشخیص گفتار، تبدیل متن به گفتار، جستجوی آنلاین و تحلیل احساسات</div></div></div>
            <div class="feature-item"><div class="feature-icon">📊</div><div class="feature-text"><div class="feature-title">داشبورد تحلیلی حرفه‌ای</div><div class="feature-desc">نمودارهای تعاملی، روند پیشرفت و پیش‌بینی آینده تحصیلی</div></div></div>
            <div class="feature-item"><div class="feature-icon">🔗</div><div class="feature-text"><div class="feature-title">اتصال به سامانه مدرسه</div><div class="feature-desc">همگام‌سازی خودکار نمرات و عملکرد تحصیلی</div></div></div>
        </div>
        <div class="info-box">
            <i class="fas fa-check-circle text-green-400"></i> <strong>تضمین کیفیت:</strong> تمام الگوریتم‌ها توسط تیم روانشناسی و مهندسی داده طراحی شده‌اند.
        </div>
    </div>
    
    <!-- 2. ارتباط با ما -->
    <div id="contact" class="glass-card">
        <h2><i class="fas fa-phone-alt"></i> 2. ارتباط با تیم توسعه</h2>
        <div class="contact-section" style="margin-top: 0;">
            <p class="text-white mb-3"><i class="fas fa-comments"></i> ما همیشه اینجا هستیم تا به شما کمک کنیم:</p>
            <div class="contact-buttons">
                <a href="https://t.me/yehasati" target="_blank" class="contact-btn telegram"><i class="fab fa-telegram"></i> پیام در تلگرام</a>
                <a href="mailto:dramaliama632@gmail.com" class="contact-btn gmail"><i class="fas fa-envelope"></i> ارسال ایمیل</a>
            </div>
            <div class="info-box">
                <i class="fas fa-info-circle"></i> <strong>نکات مهم:</strong>
                <ul style="margin-top: 8px; list-style: none;">
                    <li>✓ پاسخگویی در تلگرام: ۹ صبح تا ۱۰ شب</li>
                    <li>✓ ایمیل‌ها حداکثر ظرف ۲۴ ساعت پاسخ داده می‌شوند</li>
                    <li>✓ برای گزارش باگ، عنوان "گزارش خطا" را در پیام بنویسید</li>
                    <li>✓ پیشنهادات خود را با ما به اشتراک بگذارید</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- 3. شروع سریع -->
    <div id="quickstart" class="glass-card">
        <h2><i class="fas fa-rocket"></i> 3. شروع سریع در ۵ گام</h2>
        <div class="step"><div class="step-number">1</div><div class="step-content"><strong>اجرای سرور محلی</strong><br><code>python main.py</code> یا <code>python app.py</code></div></div>
        <div class="step"><div class="step-number">2</div><div class="step-content"><strong>ورود به سیستم</strong><br>مرورگر: <code>http://localhost:8000</code> یا <code>http://127.0.0.1:8000</code></div></div>
        <div class="step"><div class="step-number">3</div><div class="step-content"><strong>انتخاب نقش خود</strong><br>دانش‌آموز (دسترسی کامل به تمام ابزارها) یا مشاور تحصیلی (دسترسی به پنل مدیریت)</div></div>
        <div class="step"><div class="step-number">4</div><div class="step-content"><strong>تایید حریم خصوصی</strong><br>اطلاعات شما محرمانه است و پس از ۶ ماه حذف می‌شود</div></div>
        <div class="step"><div class="step-number">5</div><div class="step-content"><strong>شروع ماجراجویی!</strong><br>از کارت‌های رنگی صفحه اصلی استفاده کنید و اولین چالش روزانه را انجام دهید</div></div>
        <div class="info-box mt-2">
            <i class="fas fa-lightbulb"></i> <strong>نکته حرفه‌ای:</strong> برای بهترین تجربه، از مرورگر کروم یا فایرفاکس استفاده کنید.
        </div>
    </div>
    
    <!-- 4. چت هوشمند صوتی -->
    <div id="chat" class="glass-card">
        <h2><i class="fas fa-microphone-alt"></i> 4. چت هوشمند با قابلیت صوتی</h2>
        <p>دستیار هوشمند مسیرینو به شما امکان می‌دهد:</p>
        <ul style="margin-right: 20px; margin-top: 12px;">
            <li><i class="fas fa-microphone text-purple-300"></i> <strong>گفتار به متن:</strong> سوال خود را بپرسید و سیستم آن را به متن تبدیل می‌کند</li>
            <li><i class="fas fa-volume-up text-green-300"></i> <strong>متن به گفتار:</strong> پاسخ‌ها با صدای طبیعی برای شما خوانده می‌شود</li>
            <li><i class="fas fa-star text-yellow-300"></i> <strong>امتیازدهی ستاره‌ای:</strong> کیفیت پاسخ را از ۱ تا ۵ ستاره ارزیابی کنید</li>
            <li><i class="fas fa-globe text-blue-300"></i> <strong>جستجوی آنلاین:</strong> اطلاعات به‌روز از ویکی‌پدیا و DuckDuckGo</li>
            <li><i class="fas fa-smile-wink text-orange-300"></i> <strong>تشخیص احساسات:</strong> سیستم وضعیت روحی شما را تحلیل می‌کند</li>
            <li><i class="fas fa-history text-gray-300"></i> <strong>ذخیره تاریخچه گفتگو:</strong> هر سوال و پاسخ ذخیره می‌شود</li>
        </ul>
        <div class="info-box mt-3">
            <i class="fas fa-quote-right"></i> مثال: "سلام، من برای امتحان ریاضی چطور برنامه‌ریزی کنم؟" یا "چند تا روش مطالعه موثر به من بگو"
        </div>
    </div>
    
    <!-- 5-8 به صورت ترکیبی -->
    <div class="glass-card">
        <h2><i class="fas fa-layer-group"></i> 5. انتخاب رشته | 6. پیش‌بینی افت | 7. آزمون هالند | 8. پیش‌بینی AI</h2>
        <div class="features-grid">
            <div><strong><i class="fas fa-graduation-cap"></i> 🎯 انتخاب رشته</strong><br>وزن دهی: توانایی (۳۰٪) + علاقه (۲۵٪) + سبک فکری (۲۰٪) + آینده شغلی (۱۵٪) + معدل (۱۰٪). خروجی شامل ۳ رشته برتر با درصد تطابق.</div>
            <div><strong><i class="fas fa-exclamation-triangle"></i> 📉 پیش‌بینی افت</strong><br>۱۲ فاکتور: ساعت مطالعه، تداوم، خواب، استرس، اضطراب، مرور، حمایت خانواده، تغذیه، فعالیت بدنی، انگیزه، تمرکز، سابقه افت. ارائه راهکار عملی.</div>
            <div><strong><i class="fas fa-dna"></i> 🧠 آزمون هالند</strong><br>۴۵ سوال استاندارد (پاسخ ۱ تا ۵). تیپ‌های: Realistic, Investigative, Artistic, Social, Enterprising, Conventional به همراه مشاغل پیشنهادی.</div>
            <div><strong><i class="fas fa-chart-simple"></i> 🤖 پیش‌بینی نمره با AI</strong><br>مدل Random Forest ساخته شده از صفر با ۱۰ ویژگی (سابقه تحصیلی، ساعات مطالعه، شرکت در کلاس، ...). دقت بالای ۸۵٪.</div>
        </div>
    </div>
    
    <!-- 9. برنامه‌ریز هوشمند -->
    <div id="smart-planner" class="glass-card">
        <h2><i class="fas fa-calendar-alt"></i> 9. برنامه‌ریز هوشمند روزانه</h2>
        <p>سیستم برنامه‌ریز با در نظر گرفتن <strong>روزهای باقی‌مانده تا امتحان</strong>، <strong>نقاط قوت و ضعف</strong> و <strong>ساعات آزاد شما</strong> یک جدول مطالعه کامل تولید می‌کند.</p>
        <ul>
            <li>✓ اولویت‌بندی دروس ضعیف‌تر</li>
            <li>✓ زمان‌های استراحت و مرور سریع</li>
            <li>✓ امکان ویرایش دستی برنامه</li>
            <li>✓ دریافت نوتیفیکیشن برای جلسات مطالعه</li>
        </ul>
    </div>
    
    <!-- 10. خلاصه‌ساز هوشمند -->
    <div id="smart-summarizer" class="glass-card">
        <h2><i class="fas fa-file-alt"></i> 10. خلاصه‌ساز هوشمند درس</h2>
        <p>با وارد کردن متن درس (حداقل ۲۰۰ کاراکتر)، سیستم به صورت خودکار:</p>
        <ul>
            <li>📄 <strong>خلاصه هوشمند:</strong> کاهش حجم متن تا ۷۰٪ بدون از دست دادن مفاهیم اصلی</li>
            <li>💡 <strong>۵ نکته کلیدی:</strong> مهم‌ترین ایده‌های متن</li>
            <li>📇 <strong>فلش‌کارت:</strong> تولید ۳ تا ۶ سوال و جواب برای مرور سریع</li>
            <li>📊 <strong>تحلیل سطح دشواری:</strong> تخمین پیچیدگی متن بر اساس واژگان</li>
        </ul>
        <div class="info-box"><i class="fas fa-magic"></i> مناسب برای خلاصه کردن کتاب‌های درسی، مقالات و جزوات</div>
    </div>
    
    <!-- 11. مسیرشو -->
    <div id="pathfinder" class="glass-card">
        <h2><i class="fas fa-road"></i> 11. مسیرشو - نقشه راه شغلی ۵ ساله</h2>
        <p>بر اساس <strong>تیپ هالند</strong> و <strong>رشته انتخابی</strong>، یک نقشه راه شخصی‌سازی شده شامل:</p>
        <ul>
            <li>📅 گام‌های سالانه (از پایه دهم تا ورود به بازار کار)</li>
            <li>🛠️ مهارت‌های فنی و نرم مورد نیاز هر سال</li>
            <li>💼 معرفی ۵ شغل مرتبط با درآمد و چشم‌انداز</li>
            <li>📚 منابع آموزشی (کتاب، دوره آنلاین، وبسایت)</li>
            <li>🎯 پروژه‌های عملی پیشنهادی برای رزومه</li>
        </ul>
    </div>
    
    <!-- 12. گیمیفیکیشن -->
    <div id="gamification" class="glass-card">
        <h2><i class="fas fa-trophy"></i> 12. گیمیفیکیشن (امتیاز، سطح، مدال)</h2>
        <p><strong>سطوح پیشرفت (از مبتدی تا حرفه‌ای):</strong></p>
        <p>شروع‌کننده (۰) → تلاشگر (۱۰۰) → برنزی (۲۵۰) → نقره‌ای (۵۰۰) → طلایی (۱۰۰۰) → پلاتینیوم (۲۰۰۰) → الماسی (۳۵۰۰) → افسانه‌ای (۵۰۰۰) → استاد (۷۵۰۰) → خوارزمی (۱۰۰۰۰+)</p>
        <p><strong>مدال‌های قابل کسب:</strong></p>
        <div class="game-grid">
            <div class="game-card">🏅 شروع کننده</div>
            <div class="game-card">🔥 ۳ روز پیاپی</div>
            <div class="game-card">⭐ هفته طلایی</div>
            <div class="game-card">🧠 نابغه کوچک</div>
            <div class="game-card">💰 جمع‌کننده امتیاز</div>
            <div class="game-card">🎓 خودشناسی</div>
            <div class="game-card">👑 رهبر گروه</div>
            <div class="game-card">🎯 هدف‌گذار حرفه‌ای</div>
            <div class="game-card">📚 افسانه مطالعه</div>
            <div class="game-card">🤝 همکار تیمی</div>
        </div>
    </div>
    
    <!-- 13. چالش‌ها و گواهی -->
    <div id="challenges" class="glass-card">
        <h2><i class="fas fa-tasks"></i> 13. چالش‌های روزانه + گواهی هفتگی</h2>
        <p>هر روز <strong>۳ چالش جدید</strong> در سطوح آسان، متوسط و سخت دریافت می‌کنید. با انجام هر چالش، امتیاز و مدال دریافت می‌کنید.</p>
        <p><strong>گواهی هفتگی:</strong> اگر در طول هفته حداقل ۱۰۰ امتیاز کسب کنید، یک گواهی PDF از تلاش‌هایتان دریافت می‌کنید که قابل اشتراک‌گذاری است.</p>
        <div class="info-box">✨ چالش نمونه: "امروز ۳۰ دقیقه بدون وقفه مطالعه کن" یا "یک فلش‌کارت برای درس فیزیک بساز"</div>
    </div>
    
    <!-- 14. گروه‌ها -->
    <div id="groups" class="glass-card">
        <h2><i class="fas fa-users"></i> 14. گروه‌های مطالعه آنلاین</h2>
        <ul>
            <li>➕ ایجاد گروه عمومی یا خصوصی با کد دعوت ۶ رقمی</li>
            <li>💬 چت گروهی لحظه‌ای (متن، ایموجی، فایل)</li>
            <li>🏆 لیدربورد گروهی بر اساس امتیازات هفتگی اعضا</li>
            <li>📢 ارسال نوتیفیکیشن برای تمام اعضا</li>
            <li>👥 حداکثر ۳۰ عضو در هر گروه</li>
            <li>🗑️ مدیر گروه می‌تواند گروه را حذف یا اعضا را مدیریت کند</li>
        </ul>
    </div>
    
    <!-- 15. تقویم -->
    <div id="calendar" class="glass-card">
        <h2><i class="fas fa-calendar-week"></i> 15. تقویم آموزشی شمسی</h2>
        <p>یک تقویم کامل تعاملی که نمایش می‌دهد:</p>
        <ul>
            <li>📌 رویدادهای ثابت (تعطیلات، امتحانات نهایی، کنکور)</li>
            <li>📚 برنامه مطالعه شخصی شما</li>
            <li>🎯 چالش‌های روزانه</li>
            <li>🎯 اهداف SMART با ددلاین</li>
            <li>➕ امکان افزودن رویداد شخصی (مثل تولد، جلسه خصوصی)</li>
        </ul>
    </div>
    
    <!-- 16. پومودورو -->
    <div id="pomodoro" class="glass-card">
        <h2><i class="fas fa-hourglass-half"></i> 16. تایمر پومودورو + Todo List</h2>
        <p>تکنیک مدیریت زمان <strong>۲۵ دقیقه مطالعه متمرکز + ۵ دقیقه استراحت</strong>. ویژگی‌ها:</p>
        <ul>
            <li>⏱️ تایمر بصری با صدای زنگ</li>
            <li>📝 Todo List برای ثبت کارهای روزانه</li>
            <li>📊 آمار پومودوروهای انجام شده در هفته</li>
            <li>🎵 موسیقی تمرکز (اختیاری)</li>
            <li>🏆 کسب امتیاز برای هر پومودورو کامل</li>
        </ul>
    </div>
    
    <!-- 17. اهداف SMART -->
    <div id="goals" class="glass-card">
        <h2><i class="fas fa-bullseye"></i> 17. اهداف هوشمند SMART</h2>
        <p>با استفاده از متدولوژی SMART (Specific, Measurable, Achievable, Relevant, Time-bound) هدف‌گذاری کنید.</p>
        <p><strong>مثال:</strong> "می‌خواهم تا ۲۰ فروردین نمره ریاضی خود را از ۱۴ به ۱۸ برسانم با مطالعه روزانه ۱ ساعت و حل ۲۰ تمرین."</p>
        <p>سیستم پیشرفت شما را ردیابی می‌کند و در صورت تکمیل، امتیاز ویژه و مدال "هدف‌گذار حرفه‌ای" تعلق می‌گیرد.</p>
    </div>
    
    <!-- 18. تولید سوال -->
    <div id="exam" class="glass-card">
        <h2><i class="fas fa-pen-alt"></i> 18. تولید سوال امتحانی هوشمند</h2>
        <p>بر اساس درس، پایه تحصیلی، سطح دشواری (آسان، متوسط، سخت) و تعداد سوال، سیستم برای شما سوالات تستی و تشریحی تولید می‌کند.</p>
        <ul>
            <li>✅ پاسخنامه تشریحی</li>
            <li>📊 نمره‌دهی خودکار بعد از پاسخ</li>
            <li>📝 ذخیره آزمون‌ها در پروفایل</li>
            <li>📈 تحلیل نقاط قوت و ضعف در هر درس</li>
        </ul>
    </div>
    
    <!-- 19. بازی‌ها -->
    <div id="games" class="glass-card">
        <h2><i class="fas fa-gamepad"></i> 19. بازی‌های آموزشی تعاملی</h2>
        <div class="game-grid">
            <div class="game-card"><i class="fas fa-question-circle"></i> مسابقه هوشمند</div>
            <div class="game-card"><i class="fas fa-layer-group"></i> فلش‌کارت</div>
            <div class="game-card"><i class="fas fa-brain"></i> بازی حافظه</div>
            <div class="game-card"><i class="fas fa-puzzle-piece"></i> دار و دسته</div>
            <div class="game-card"><i class="fas fa-calculator"></i> چالش ریاضی</div>
            <div class="game-card"><i class="fas fa-check-circle"></i> درست یا نادرست</div>
            <div class="game-card"><i class="fas fa-link"></i> جورچین مفاهیم</div>
            <div class="game-card"><i class="fas fa-bolt"></i> مسابقه سریع</div>
        </div>
        <p class="mt-3">هر بازی امتیاز مخصوص به خود را دارد و می‌توانید با دوستان خود رقابت کنید.</p>
    </div>
    
    <!-- 20. پروفایل شخصی -->
    <div id="profile" class="glass-card">
        <h2><i class="fas fa-id-card"></i> 20. پروفایل شخصی و کد یکتا</h2>
        <p>در صفحه پروفایل می‌توانید:</p>
        <ul>
            <li>ویرایش نام، نام خانوادگی، پایه تحصیلی، ایمیل</li>
            <li>مشاهده کد یکتای ۸ رقمی خود (برای استفاده در API)</li>
            <li>مشاهده آمار کلی (تعداد چالش‌ها، امتیاز کل، سطح فعلی)</li>
            <li>تغییر رمز عبور (در نسخه آنلاین)</li>
            <li>دانلود تمام اطلاعات خود در قالب JSON</li>
        </ul>
    </div>
    
    <!-- 21. داشبورد تحلیلی -->
    <div id="analytics" class="glass-card">
        <h2><i class="fas fa-chart-pie"></i> 21. داشبورد تحلیلی پیشرفته</h2>
        <p>با نمودارهای تعاملی و تحلیل‌های پیشرفته:</p>
        <ul>
            <li>📈 روند پیشرفت هفتگی و ماهانه</li>
            <li>📊 مقایسه عملکرد دروس مختلف</li>
            <li>⚠️ روند ریسک افت تحصیلی</li>
            <li>🔮 پیش‌بینی نمره نهایی با AI</li>
            <li>🏅 مقایسه با میانگین کاربران هم‌پایه</li>
        </ul>
        <div class="info-box mt-2">
            ⚠️ <strong>نکته مهم:</strong> برای مشاهده داده در داشبورد، ابتدا چند چالش انجام دهید، یک آزمون بدهید و یک هدف SMART ایجاد کنید.
        </div>
    </div>
    
    <!-- 22. API عمومی -->
    <div id="api" class="glass-card">
        <h2><i class="fas fa-plug"></i> 22. API عمومی برای توسعه‌دهندگان</h2>
        <p>شما می‌توانید از API مسیرینو در برنامه‌های خود استفاده کنید:</p>
        <code>POST /api/v1/ask</code> - ارسال سوال به چت بات (پارامتر: question, session_id)<br>
        <code>POST /api/v1/feedback</code> - ثبت بازخورد و امتیاز<br>
        <code>GET /api/v1/compare</code> - مقایسه آمار با سایر کاربران مشابه<br>
        <code>GET /api/v1/profile</code> - دریافت اطلاعات پروفایل (نیاز به کلید API)<br>
        <div class="info-box mt-2"><i class="fas fa-key"></i> برای دریافت کلید API، با پشتیبانی تماس بگیرید.</div>
    </div>
    
    <!-- 23. سوالات متداول توسعه یافته -->
    <div id="faq" class="glass-card">
        <h2><i class="fas fa-question-circle"></i> 23. سوالات متداول کاربران</h2>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-lock"></i> آیا اطلاعات من محفوظ است و پاک می‌شود؟</p><p class="text-sm text-gray-200">بله. اطلاعات شما فقط با کد یکتا ذخیره می‌شود و پس از ۶ ماه عدم فعالیت به صورت خودکار حذف می‌گردد. هیچ اطلاعاتی با اشخاص ثالث به اشتراک گذاشته نمی‌شود.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-download"></i> چگونه می‌توانم گزارش یا نتیجه آزمون را ذخیره کنم؟</p><p class="text-sm text-gray-200">در تمام صفحات نتیجه (مانند انتخاب رشته، هالند، پیش‌بینی نمره) دکمه‌های "دانلود HTML" و "دانلود PDF" وجود دارد. همچنین می‌توانید صفحه را چاپ کرده و به عنوان PDF ذخیره کنید.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-star"></i> چطور امتیاز بیشتری جمع کنم؟</p><p class="text-sm text-gray-200">انجام چالش‌های روزانه (هر چالش ۵-۲۰ امتیاز)، شرکت در آزمون‌های تولید شده (۱۰ امتیاز به ازای هر آزمون)، فعالیت در گروه‌های مطالعه، تکمیل اهداف SMART، بازی‌های آموزشی، و جلسات پومودورو.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-chart-line"></i> چرا داشبورد تحلیلی من خالی است؟</p><p class="text-sm text-gray-200">داشبورد نیاز به داده دارد. لطفاً حداقل ۳ چالش مختلف انجام دهید، یک آزمون تولید کنید و به آن پاسخ دهید، یک هدف SMART ثبت کنید. بعد از ۲۴ ساعت نمودارها پر می‌شوند.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-school"></i> آیا می‌توانم نمرات واقعی مدرسه را وارد کنم؟</p><p class="text-sm text-gray-200">بله! از بخش "اتصال به سامانه مدرسه" می‌توانید با وارد کردن کد ملی و (در حالت شبیه‌سازی) اطلاعات خود را همگام کنید. همچنین به صورت دستی می‌توانید کارنامه را وارد کنید.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-language"></i> آیا مسیرینو از زبان انگلیسی هم پشتیبانی می‌کند؟</p><p class="text-sm text-gray-200">در حال حاضر رابط کاربری به فارسی است اما چت بات می‌تواند به زبان انگلیسی نیز پاسخ دهد. در آینده نسخه انگلیسی منتشر خواهد شد.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-mobile-alt"></i> آیا اپلیکیشن موبایل دارید؟</p><p class="text-sm text-gray-200">نسخه تحت وب کاملاً واکنش‌گرا (Responsive) است و در موبایل نیز به خوبی کار می‌کند. برنامه اندروید در دست توسعه است.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-robot"></i> مدل پیش‌بینی AI چقدر دقیق است؟</p><p class="text-sm text-gray-200">مدل Random Forest ساخته شده با دقت حدود ۸۷٪ در داده‌های تست. البته این یک پیش‌بینی تحصیلی است و عوامل بیرونی می‌توانند روی نمرات تأثیر بگذارند.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-tasks"></i> هر روز چند چالش جدید می‌آید؟</p><p class="text-sm text-gray-200">ساعت ۱۲ شب هر روز، ۳ چالش جدید در سطوح مختلف فعال می‌شود. چالش‌های روز قبل منقضی می‌شوند.</p></div>
        
        <div class="faq-item"><p class="font-bold text-white"><i class="fas fa-user-graduate"></i> برای مشاوران تحصیلی چه قابلیت‌هایی دارید؟</p><p class="text-sm text-gray-200">مشاوران می‌توانند چندین دانش‌آموز را اضافه کنند، پیشرفت آن‌ها را ببینند، گزارش گروهی دریافت کنند و برای آن‌ها برنامه و چالش ارسال کنند.</p></div>
    </div>
    
    <!-- 24. اتصال به مدرسه -->
    <div id="school-api" class="glass-card">
        <h2><i class="fas fa-school"></i> 24. اتصال به سامانه مدرسه (LMS)</h2>
        <p>با استفاده از این قابلیت می‌توانید:</p>
        <ul>
            <li>🔑 وارد کردن کد ملی و کلید API مدرسه</li>
            <li>📥 دریافت خودکار نمرات، غیبت‌ها و برنامه کلاسی</li>
            <li>🔄 همگام‌سازی هفتگی اطلاعات</li>
            <li>📊 تحلیل عملکرد بر اساس نمرات واقعی</li>
        </ul>
        <div class="info-box"><i class="fas fa-flask"></i> این قابلیت در حالت شبیه‌سازی است و به زودی با اتصال به سامانه‌های آموزشی کشور فعال می‌شود.</div>
    </div>
    
    <!-- 25. پشتیبانی -->
    <div id="support" class="glass-card">
        <h2><i class="fas fa-life-ring"></i> 25. پشتیبانی و سیستم تیکت</h2>
        <p>برای دریافت کمک سریع، می‌توانید از روش‌های زیر استفاده کنید:</p>
        <ul>
            <li>📱 تلگرام: <code>@yehasati</code> (پاسخ در کمتر از ۶ ساعت)</li>
            <li>📧 ایمیل: <code>dramaliama632@gmail.com</code> (پاسخ ۲۴ ساعته)</li>
            <li>🐛 گزارش باگ: عنوان ایمیل را "گزارش خطا" بگذارید و توضیحات کامل دهید</li>
            <li>💡 پیشنهاد ویژگی جدید: با کمال میل بررسی می‌شود</li>
        </ul>
        <div class="contact-section mt-3">
            <p>ما به هر پیام اهمیت می‌دهیم و تمام تلاش خود را برای بهبود مسیرینو می‌کنیم.</p>
        </div>
    </div>
    
    <!-- فوتر -->
    <div class="footer">
        <p><i class="fas fa-graduation-cap"></i> <strong>مسیرینو</strong> - همراه هوشمند شما در مسیر موفقیت تحصیلی</p>
        <p class="mt-2">
            <i class="fab fa-telegram"></i> @yehasati | 
            <i class="fas fa-envelope"></i> dramaliama632@gmail.com | 
            <i class="fas fa-code-branch"></i> نسخه ۴.۰
        </p>
        <p class="mt-2 text-xs">© ۱۴۰۵ - تمام حقوق محفوظ است. ساخته شده با عشق برای دانش‌آموزان ایران <i class="fas fa-heart text-red-400"></i></p>
    </div>
</div>

<script>
    // اسکرول نرم برای لینک‌های داخلی
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
        anchor.addEventListener('click', function (e) {{
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {{
                target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }});
    }});
</script>
</body>
</html>'''