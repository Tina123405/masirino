# dynamic_planner.py
# برنامه‌ریز هوشمند روزانه - فقط بر اساس تعداد روز

from datetime import datetime, timedelta

class DynamicStudyPlanner:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def generate_plan(self, days_input, subject, weak_chapters, strong_chapters):
        """
        تولید برنامه هوشمند بر اساس تعداد روزهای باقی‌مانده
        days_input: تعداد روز (مثلاً "2" یا "30")
        """
        
        # تبدیل به عدد صحیح
        try:
            days_available = int(days_input)
        except:
            return {
                "error": "❌ فقط تعداد روز را به صورت عدد وارد کنید (مثال: 5)"
            }
        
        if days_available <= 0:
            return {
                "error": f"❌ تعداد روز ({days_available}) نامعتبر است. عدد مثبت وارد کن."
            }
        
        # محدودیت حداکثر 30 روز
        days_available = min(days_available, 30)
        
        plan = []
        
        # استراتژی بر اساس زمان باقی‌مانده
        if days_available <= 2:
            strategy = "emergency"
            strategy_desc = "⚠️ فوری - فقط ۲ روز مونده!"
        elif days_available <= 5:
            strategy = "intensive"
            strategy_desc = "🔥 فشرده - زمان محدود"
        elif days_available <= 10:
            strategy = "normal"
            strategy_desc = "📚 استاندارد - زمان مناسب"
        else:
            strategy = "relaxed"
            strategy_desc = "🌿 متعادل - زمان کافی"
        
        weak_count = len(weak_chapters)
        strong_count = len(strong_chapters)
        
        if weak_count == 0 and strong_count == 0:
            return {"error": "لطفاً حداقل یک درس ضعیف یا قوی وارد کنید"}
        
        # توزیع روزها
        if strategy == "emergency":
            weak_days = days_available
            strong_days = 0
        elif strategy == "intensive":
            weak_days = min(weak_count, days_available)
            strong_days = days_available - weak_days
        elif strategy == "normal":
            weak_days = min(weak_count + 1, days_available)
            strong_days = days_available - weak_days
        else:
            weak_days = min(weak_count, max(1, days_available // 2))
            strong_days = days_available - weak_days
        
        if weak_days == 0 and weak_count > 0:
            weak_days = min(weak_count, days_available)
            strong_days = days_available - weak_days
        
        # ساخت برنامه
        weak_index = 0
        strong_index = 0
        
        for day in range(1, days_available + 1):
            daily_task = {
                "day": day,
                "date": self._get_future_date(day),
                "tasks": []
            }
            
            remaining = days_available - day + 1
            
            # درس‌های ضعیف
            if weak_index < weak_count and day <= weak_days:
                chapter = weak_chapters[weak_index]
                
                daily_task["tasks"].append({
                    "type": "weak_study",
                    "title": f"📖 مطالعه عمیق {chapter}",
                    "description": f"خواندن دقیق {chapter} + علامت‌گذاری + خلاصه‌نویسی",
                    "duration": 50 if strategy == "emergency" else 45,
                    "priority": "بسیار مهم",
                    "method": "مطالعه فعال - هر پاراگراف را توضیح بده"
                })
                
                if strategy != "emergency":
                    daily_task["tasks"].append({
                        "type": "weak_practice",
                        "title": f"✏️ تمرین {chapter}",
                        "description": f"حل ۱۵ تست {chapter} + تحلیل اشتباهات",
                        "duration": 35,
                        "priority": "مهم",
                        "method": "تست‌زنی با تایمر"
                    })
                
                weak_index += 1
            
            # درس‌های قوی
            elif strong_index < strong_count and day > weak_days:
                chapter = strong_chapters[strong_index]
                daily_task["tasks"].append({
                    "type": "strong_review",
                    "title": f"🔄 مرور {chapter}",
                    "description": f"مرور ۱۰ دقیقه‌ای نکات کلیدی {chapter}",
                    "duration": 15,
                    "priority": "کم",
                    "method": "مرور سریع با فلش‌کارت"
                })
                strong_index += 1
            
            # جمع‌بندی روزانه
            daily_task["tasks"].append({
                "type": "daily_review",
                "title": "🎯 جمع‌بندی روزانه",
                "description": "مرور درس‌های امروز + برنامه‌ریزی فردا",
                "duration": 10,
                "priority": "متوسط" if remaining > 3 else "مهم",
                "method": "تکنیک فاینمن - به کسی یاد بده"
            })
            
            total_minutes = sum(t.get("duration", 0) for t in daily_task["tasks"])
            daily_task["total_hours"] = round(total_minutes / 60, 1)
            plan.append(daily_task)
        
        # روز آخر: جمع‌بندی ویژه (فقط اگر زمان کم باشد)
        if plan and days_available <= 7:
            plan[-1]["tasks"].insert(0, {
                "type": "final_review",
                "title": "🎓 شب امتحان - جمع‌بندی نهایی",
                "description": "مرور نکات طلایی ۳۰ دقیقه، سپس استراحت و خواب کافی",
                "duration": 30,
                "priority": "بسیار مهم",
                "method": "فقط مرور - درس جدید نخوان!"
            })
        
        total_hours = sum(day.get("total_hours", 0) for day in plan)
        
        return {
            "subject": subject,
            "days_remaining": days_available,
            "weak_chapters": weak_chapters,
            "strong_chapters": strong_chapters,
            "strategy": strategy_desc,
            "daily_plan": plan,
            "total_study_hours": round(total_hours, 1),
            "recommendation": self._get_recommendation(days_available, weak_count, strategy)
        }
    
    def _get_future_date(self, day_offset):
        """تاریخ شمسی برای روز X ام (فقط برای نمایش)"""
        today = datetime.now()
        future_date = today + timedelta(days=day_offset - 1)
        
        year = future_date.year
        month = future_date.month
        day = future_date.day
        
        # تبدیل میلادی به شمسی (ساده)
        if month > 3 or (month == 3 and day >= 21):
            shamsi_year = year - 621
            shamsi_month = month - 3
            shamsi_day = day
            if shamsi_month <= 0:
                shamsi_month += 12
                shamsi_year -= 1
        else:
            shamsi_year = year - 622
            shamsi_month = month + 9
            shamsi_day = day
        
        if shamsi_month > 12:
            shamsi_month -= 12
            shamsi_year += 1
        
        month_names = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", 
                       "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
        
        return f"{shamsi_year}/{shamsi_month:02d}/{shamsi_day:02d} ({month_names[shamsi_month-1]})"
    
    def _get_recommendation(self, days, weak_count, strategy):
        if strategy == "emergency":
            return "⚠️ فقط ۲ روز مونده! فقط روی مهم‌ترین مباحث تمرکز کن. شب امتحان زود بخواب."
        elif strategy == "intensive":
            return "🔥 زمان محدود! هر روز برنامه رو دقیق اجرا کن. اشتباهات رو یادداشت کن."
        elif strategy == "normal":
            return "📚 برنامه متعادل. به آن پایبند باش و هر شب مرور روزانه رو انجام بده."
        else:
            return "🌿 زمان خوبی داری. برنامه رو دنبال کن و از منابع جانبی هم استفاده کن."


# ========== صفحه HTML ==========
def render_planner_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>برنامه‌ریز هوشمند - مسیرینو</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1000px; margin: auto; }}
        .glass-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 30px;
            margin-bottom: 20px;
        }}
        h1 {{ text-align: center; margin-bottom: 10px; }}
        h1 small {{ font-size: 0.8rem; color: #c4c4f0; display: block; margin-top: 5px; }}
        input, textarea {{
            width: 100%;
            padding: 12px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(0,0,0,0.3);
            color: white;
            margin-bottom: 15px;
            font-size: 1rem;
        }}
        button {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            border: none;
            border-radius: 30px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            font-size: 1.1rem;
        }}
        button:hover {{ opacity: 0.9; }}
        .plan-day {{
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
            padding: 15px;
            margin-bottom: 12px;
        }}
        .task-item {{
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 12px;
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}
        .priority-high {{ border-right: 4px solid #ef4444; }}
        .priority-medium {{ border-right: 4px solid #f59e0b; }}
        .priority-low {{ border-right: 4px solid #10b981; }}
        .strategy-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        .task-method {{ font-size: 0.7rem; color: #a0a0ff; margin-top: 5px; }}
        .back-home {{ display: block; text-align: center; margin-top: 20px; color: #6c63ff; text-decoration: none; }}
        hr {{ margin: 15px 0; border-color: rgba(255,255,255,0.1); }}
        .info-text {{
            font-size: 0.9rem;
            color: #ffd700;
            margin-bottom: 15px;
            text-align: center;
            background: rgba(0,0,0,0.3);
            padding: 10px;
            border-radius: 16px;
        }}
        .stats {{
            background: rgba(0,0,0,0.2);
            border-radius: 16px;
            padding: 12px;
            margin-bottom: 15px;
        }}
        .stats p {{ margin: 5px 0; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📅 برنامه‌ریز هوشمند روزانه<br><small>بر اساس نقاط قوت و ضعف شما</small></h1>
    
    <div class="glass-card">
        <div class="info-text">
            💡 <strong>روش کار:</strong><br>
            فقط تعداد روز باقی‌مانده تا امتحان را وارد کن.<br>
            مثال: <strong>2</strong> (یعنی ۲ روز دیگه امتحان داری)<br>
            مثال: <strong>30</strong> (یعنی ۳۰ روز دیگه امتحان داری)
        </div>
        <input type="number" id="daysLeft" placeholder="تعداد روز باقی‌مانده تا امتحان" value="5" min="1" max="90">
        <input type="text" id="subject" placeholder="نام درس" value="ریاضی">
        <textarea id="weakChapters" rows="2" placeholder="درس‌های ضعیف (با کاما جدا کنید)&#10;مثال: فصل 3, فصل 5"></textarea>
        <textarea id="strongChapters" rows="2" placeholder="درس‌های قوی (با کاما جدا کنید)&#10;مثال: فصل 1, فصل 2"></textarea>
        <button onclick="generatePlan()">🎯 ساخت برنامه هوشمند</button>
    </div>
    
    <div id="result"></div>
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
const sessionId = "{session_id}";

async function generatePlan() {{
    const daysLeft = document.getElementById('daysLeft').value;
    const subject = document.getElementById('subject').value;
    const weakText = document.getElementById('weakChapters').value;
    const strongText = document.getElementById('strongChapters').value;
    
    const weakChapters = weakText.split(',').map(s => s.trim()).filter(s => s);
    const strongChapters = strongText.split(',').map(s => s.trim()).filter(s => s);
    
    if (!daysLeft || daysLeft <= 0) {{
        alert('لطفاً تعداد روز باقی‌مانده را وارد کن');
        return;
    }}
    
    if (!subject) {{
        alert('لطفاً نام درس را وارد کن');
        return;
    }}
    
    if (weakChapters.length === 0 && strongChapters.length === 0) {{
        alert('لطفاً حداقل یک درس ضعیف یا قوی وارد کن');
        return;
    }}
    
    document.getElementById('result').innerHTML = '<div class="glass-card" style="text-align:center">⏳ در حال ساخت برنامه...</div>';
    
    try {{
        const res = await fetch('/api/dynamic-planner', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{
                session_id: sessionId,
                days_input: daysLeft,
                subject: subject,
                weak_chapters: weakChapters,
                strong_chapters: strongChapters
            }})
        }});
        const data = await res.json();
        
        if (data.error) {{
            document.getElementById('result').innerHTML = `<div class="glass-card" style="border:1px solid #ef4444">
                <h3 style="color:#ef4444">❌ خطا</h3>
                <p>${{data.error}}</p>
            </div>`;
            return;
        }}
        
        let strategyColor = '#f59e0b';
        if (data.strategy.includes('فوری')) strategyColor = '#ef4444';
        else if (data.strategy.includes('کافی')) strategyColor = '#10b981';
        
        let html = `<div class="glass-card">
            <h3>📚 برنامه مطالعه ${{data.subject}}</h3>
            <div class="stats">
                <p>⏰ روزهای باقی‌مانده: <strong style="color:#ffd700; font-size:1.3rem">${{data.days_remaining}}</strong> روز</p>
                <p>📊 مجموع ساعات مطالعه: <strong>${{data.total_study_hours}}</strong> ساعت</p>
                <p>📋 استراتژی: <span class="strategy-badge" style="background:${{strategyColor}}">${{data.strategy}}</span></p>
                <p>📖 درس‌های ضعیف: ${{data.weak_chapters.join('، ') || 'ندارد'}}</p>
                <p>✅ درس‌های قوی: ${{data.strong_chapters.join('، ') || 'ندارد'}}</p>
                <p>💡 توصیه: ${{data.recommendation}}</p>
            </div>
            <hr>`;
        
        for (let i = 0; i < data.daily_plan.length; i++) {{
            const day = data.daily_plan[i];
            html += `<div class="plan-day">
                <h4>📅 روز ${{day.day}} - ${{day.date}} <span style="font-size:0.7rem">(⏱️ ${{day.total_hours}} ساعت)</span></h4>`;
            
            for (let j = 0; j < day.tasks.length; j++) {{
                const task = day.tasks[j];
                let priorityClass = '';
                if (task.priority === 'بسیار مهم') priorityClass = 'priority-high';
                else if (task.priority === 'مهم') priorityClass = 'priority-medium';
                else priorityClass = 'priority-low';
                
                let typeIcon = '';
                if (task.type === 'weak_study') typeIcon = '📖';
                else if (task.type === 'weak_practice') typeIcon = '✏️';
                else if (task.type === 'strong_review') typeIcon = '🔄';
                else if (task.type === 'daily_review') typeIcon = '🎯';
                else if (task.type === 'final_review') typeIcon = '🎓';
                else typeIcon = '📌';
                
                html += `<div class="task-item ${{priorityClass}}">
                    <div style="flex:1">
                        <strong>${{typeIcon}} ${{task.title}}</strong><br>
                        <small>${{task.description}}</small>
                        <div class="task-method">🎯 روش: ${{task.method || 'مطالعه استاندارد'}}</div>
                    </div>
                    <div style="min-width:80px; text-align:left">⏱️ ${{task.duration}} دقیقه</div>
                </div>`;
            }}
            html += `</div>`;
        }}
        
        html += `<button onclick="window.print()" style="margin-top:15px">🖨️ چاپ برنامه</button></div>`;
        document.getElementById('result').innerHTML = html;
    }} catch(e) {{
        document.getElementById('result').innerHTML = `<div class="glass-card" style="border:1px solid #ef4444">
            <h3 style="color:#ef4444">❌ خطا</h3>
            <p>خطا در ارتباط با سرور: ${{e.message}}</p>
        </div>`;
    }}
}}
</script>
</body>
</html>'''