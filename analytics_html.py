# analytics_html.py
# صفحه آنالیتیکس پیشرفته - با پشتیبانی از داده‌های دمو

def render_analytics_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد تحلیلی - مسیرینو</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
        body, button, input, select, textarea, div, span, p, h1, h2, h3, h4, a {{
            font-family: 'Inter', 'Vazirmatn', 'Vazir', 'Shabnam', 'IRANSans', 'Tahoma', 'Segoe UI', system-ui, sans-serif !important;
        }}
        :root{{--bg:linear-gradient(135deg,#0f0c29,#302b63,#24243e);--card:rgba(255,255,255,0.08);--text:#fff;--muted:#c4c4f0}}
        [data-theme="light"]{{--bg:linear-gradient(135deg,#f5f7fa,#e4e8f0);--card:rgba(255,255,255,0.9);--text:#1a1a2e;--muted:#666}}
        body{{background:var(--bg);color:var(--text);padding:30px;min-height:100vh}}
        .container{{max-width:1400px;margin:auto}}
        .glass-card{{background:var(--card);backdrop-filter:blur(20px);border-radius:28px;padding:25px;margin-bottom:20px}}
        h2{{margin-bottom:20px;font-size:1.5rem;border-right:4px solid #6c63ff;padding-right:15px}}
        h3{{margin:15px 0;font-size:1.2rem;color:var(--muted)}}
        
        .charts-grid{{
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(450px,1fr));
            gap:25px;
            margin-bottom:25px;
        }}
        .chart-box{{
            background:rgba(0,0,0,0.2);
            border-radius:20px;
            padding:20px;
        }}
        .chart-title{{
            font-weight:bold;
            margin-bottom:15px;
            text-align:center;
        }}
        canvas{{
            width:100%;
            height:300px;
            background:rgba(255,255,255,0.02);
            border-radius:16px;
        }}
        
        .stats-row{{
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
            gap:15px;
            margin-bottom:25px;
        }}
        .stat-card{{
            background:rgba(0,0,0,0.3);
            border-radius:20px;
            padding:20px;
            text-align:center;
        }}
        .stat-value{{
            font-size:2rem;
            font-weight:bold;
            color:#ffd700;
        }}
        .stat-label{{
            font-size:0.8rem;
            color:var(--muted);
            margin-top:5px;
        }}
        .trend-up{{color:#10b981}}
        .trend-down{{color:#ef4444}}
        .trend-stable{{color:#f59e0b}}
        
        .demo-alert{{
            background:rgba(255,193,7,0.15);
            border-right:4px solid #ffc107;
            padding:15px 20px;
            border-radius:16px;
            margin-bottom:20px;
        }}
        .demo-alert p{{
            color:#ffc107;
            margin:0;
            font-size:0.9rem;
        }}
        .demo-alert strong{{
            color:#ffd700;
        }}
        
        .subjects-table{{
            width:100%;
            border-collapse:collapse;
        }}
        .subjects-table th,.subjects-table td{{
            padding:12px;
            text-align:right;
            border-bottom:1px solid rgba(255,255,255,0.1);
        }}
        .subjects-table th{{
            color:#6c63ff;
        }}
        .subject-good{{color:#10b981}}
        .subject-medium{{color:#f59e0b}}
        .subject-weak{{color:#ef4444}}
        
        .progress-bar{{
            height:8px;
            background:rgba(255,255,255,0.1);
            border-radius:10px;
            overflow:hidden;
            width:100px;
            display:inline-block;
            margin-right:10px;
        }}
        .progress-fill{{
            height:100%;
            border-radius:10px;
        }}
        
        .back-home{{
            display:inline-block;
            margin-top:20px;
            color:#6c63ff;
            text-decoration:none;
        }}
        .refresh-btn{{
            background:linear-gradient(90deg,#6c63ff,#ff6584);
            border:none;
            padding:8px 20px;
            border-radius:30px;
            color:white;
            cursor:pointer;
            margin-bottom:15px;
        }}
        .forecast-badge{{
            background:rgba(108,99,255,0.3);
            padding:5px 12px;
            border-radius:20px;
            font-size:0.7rem;
            display:inline-block;
            margin-top:10px;
        }}
        @media(max-width:768px){{
            .charts-grid{{grid-template-columns:1fr}}
            .stats-row{{grid-template-columns:repeat(2,1fr)}}
        }}
    </style>
</head>
<body>
<div class="container">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px">
        <h1 style="font-size:1.8rem">📊 داشبورد تحلیلی پیشرفته</h1>
        <button class="refresh-btn" onclick="loadAnalytics()">🔄 به‌روزرسانی لحظه‌ای</button>
    </div>
    
    <div id="analyticsContent">
        <div style="text-align:center;padding:50px">⏳ در حال بارگذاری داده‌های تحلیلی...</div>
    </div>
    
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
var sessionId = "{session_id}";

function loadAnalytics() {{
    fetch('/api/analytics/data?session_id=' + sessionId)
        .then(function(res) {{ return res.json(); }})
        .then(function(data) {{
            if(data.status === 'ok') {{
                renderAnalytics(data);
            }} else {{
                document.getElementById('analyticsContent').innerHTML = '<div class="glass-card" style="text-align:center"><p>❌ خطا در بارگذاری داده‌ها</p></div>';
            }}
        }})
        .catch(function(err) {{
            console.error(err);
            document.getElementById('analyticsContent').innerHTML = '<div class="glass-card" style="text-align:center"><p>❌ خطا: ' + err.message + '</p></div>';
        }});
}}

function renderAnalytics(data) {{
    var html = '';
    
    // ========== اعلان داده دمو (اگر داده شبیه‌سازی شده باشد) ==========
    if(data.is_demo_data === true) {{
        html += '<div class="demo-alert">';
        html += '<p>📊 <strong>داده‌های نمایش داده شده شبیه‌سازی شده هستند.</strong> برای دیدن داده‌های واقعی خود:</p>';
        html += '<ul style="margin-top:8px; margin-right:20px; color:#ffc107cc">';
        html += '<li>✅ چالش‌های روزانه را انجام دهید (هر چالش امتیاز می‌دهد)</li>';
        html += '<li>📝 در آزمون‌های آموزشی شرکت کنید</li>';
        html += '<li>🎯 اهداف SMART ایجاد کنید و پیشرفت آنها را ثبت کنید</li>';
        html += '<li>🗺️ از مسیرشو بازدید کنید و شغل‌های مورد علاقه خود را ذخیره کنید</li>';
        html += '</ul>';
        html += '<p style="margin-top:8px">✨ پس از انجام این فعالیت‌ها، نمودارها به‌طور خودکار با داده‌های واقعی شما به‌روز می‌شوند.</p>';
        html += '</div>';
    }}
    
    // ========== کارت‌های آمار سریع ==========
    var timeline = data.timeline || [];
    var lastWeek = timeline.length > 0 ? timeline[timeline.length - 1] : {{ points: 0, challenges: 0, avg_exam_score: 0 }};
    var prevWeek = timeline.length > 1 ? timeline[timeline.length - 2] : {{ points: 0, challenges: 0, avg_exam_score: 0 }};
    
    var pointsChange = lastWeek.points - prevWeek.points;
    var challengesChange = lastWeek.challenges - prevWeek.challenges;
    var pointsTrendClass = (pointsChange >= 0) ? 'trend-up' : 'trend-down';
    var pointsTrendSymbol = (pointsChange >= 0) ? '▲' : '▼';
    var challengesTrendClass = (challengesChange >= 0) ? 'trend-up' : 'trend-down';
    var challengesTrendSymbol = (challengesChange >= 0) ? '▲' : '▼';
    
    html += '<div class="stats-row">';
    html += '<div class="stat-card"><div class="stat-value">' + lastWeek.points + '</div><div class="stat-label">⭐ امتیاز این هفته</div><div class="' + pointsTrendClass + '">' + pointsTrendSymbol + ' ' + Math.abs(pointsChange) + ' نسبت به هفته قبل</div></div>';
    html += '<div class="stat-card"><div class="stat-value">' + lastWeek.challenges + '</div><div class="stat-label">✅ چالش‌های این هفته</div><div class="' + challengesTrendClass + '">' + challengesTrendSymbol + ' ' + Math.abs(challengesChange) + '</div></div>';
    
    var accuracy = data.prediction_accuracy || {{ accuracy: 0, samples: 0 }};
    html += '<div class="stat-card"><div class="stat-value">' + (accuracy.accuracy || 0) + '%</div><div class="stat-label">🎯 دقت پیش‌بینی AI</div><div>بر اساس ' + (accuracy.samples || 0) + ' نمونه</div></div>';
    
    var comparison = data.comparison || {{}};
    var totalPoints = 0;
    for(var i = 0; i < timeline.length; i++) {{
        totalPoints += timeline[i].points;
    }}
    var yourAvgPoints = timeline.length > 0 ? Math.round(totalPoints / timeline.length) : 0;
    html += '<div class="stat-card"><div class="stat-value">' + yourAvgPoints + '</div><div class="stat-label">📊 میانگین امتیاز شما</div><div>مشابه‌ها: ' + (comparison.avg_points_similar || 0) + '</div></div>';
    html += '</div>';
    
    // ========== نمودارها ==========
    html += '<div class="charts-grid">';
    
    // نمودار 1: روند امتیازات
    html += '<div class="chart-box"><div class="chart-title">📈 روند امتیازات هفتگی</div><canvas id="pointsChart" width="400" height="250"></canvas>';
    var pointsTrend = data.points_trend || {{}};
    if(pointsTrend.forecast && pointsTrend.forecast.length > 0) {{
        html += '<div class="forecast-badge">🔮 پیش‌بینی هفته آینده: +' + pointsTrend.forecast[0] + ' امتیاز</div>';
    }}
    html += '</div>';
    
    // نمودار 2: روند نمرات آزمون
    html += '<div class="chart-box"><div class="chart-title">📝 روند نمرات آزمون‌ها</div><canvas id="examChart" width="400" height="250"></canvas></div>';
    
    // نمودار 3: روند ریسک افت
    html += '<div class="chart-box"><div class="chart-title">⚠️ روند ریسک افت تحصیلی</div><canvas id="riskChart" width="400" height="250"></canvas></div>';
    
    // نمودار 4: پیش‌بینی آینده
    html += '<div class="chart-box"><div class="chart-title">🔮 پیش‌بینی پیشرفت (4 هفته آینده)</div><canvas id="forecastChart" width="400" height="250"></canvas></div>';
    
    html += '</div>';
    
    // ========== جدول عملکرد دروس ==========
    var subjects = data.subjects || [];
    if(subjects.length > 0) {{
        html += '<div class="glass-card"><h3>📚 عملکرد دروس</h3><table class="subjects-table"><thead><tr><th>درس</th><th>میانگین نمره</th><th>تعداد آزمون</th><th>وضعیت</th></tr></thead><tbody>';
        for(var sIdx = 0; sIdx < subjects.length; sIdx++) {{
            var s = subjects[sIdx];
            var statusClass = (s.level === 'good') ? 'subject-good' : ((s.level === 'medium') ? 'subject-medium' : 'subject-weak');
            var statusText = (s.level === 'good') ? '✅ قوی' : ((s.level === 'medium') ? '⚠️ قابل قبول' : '❌ نیاز به تلاش');
            var barColor = (s.level === 'good') ? '#10b981' : ((s.level === 'medium') ? '#f59e0b' : '#ef4444');
            var escapedSubject = escapeHtml(s.subject);
            html += '<tr>' +
                '<td>' + escapedSubject + '</td>' +
                '<td><div class="progress-bar" style="width:100px"><div class="progress-fill" style="width:' + s.avg_score + '%;background:' + barColor + '"></div></div> ' + s.avg_score + '%</td>' +
                '<td>' + (s.exam_count || 0) + '</td>' +
                '<td class="' + statusClass + '">' + statusText + '</td>' +
                '</tr>';
        }}
        html += '</tbody></table></div>';
    }}
    
    // ========== تحلیل روند و توصیه ==========
    html += '<div class="glass-card"><h3>💡 تحلیل هوشمند پیشرفت شما</h3>';
    
    var pointsTrendDir = pointsTrend.direction || 'stable';
    var examTrend = data.exam_trend || {{}};
    var examTrendDir = examTrend.direction || 'stable';
    
    if(pointsTrendDir === 'up') {{
        html += '<p>📈 ✅ روند امتیازات شما <strong class="trend-up">صعودی</strong> است! عالی کار می‌کنی، همینطور ادامه بده.</p>';
    }} else if(pointsTrendDir === 'down') {{
        html += '<p>📉 ⚠️ روند امتیازات شما <strong class="trend-down">نزولی</strong> است. بهتر است برنامه مطالعه خود را مرور کنید.</p>';
    }} else {{
        html += '<p>📊 روند امتیازات شما پایدار است. برای پیشرفت بیشتر، چالش‌های سطح بالاتر را امتحان کن.</p>';
    }}
    
    if(examTrendDir === 'up') {{
        html += '<p>🎯 نمرات آزمون‌های شما رو به بهبود است! مهارت‌های تست‌زنی شما در حال ارتقاست.</p>';
    }} else if(examTrendDir === 'down') {{
        html += '<p>📝 نمرات آزمون‌های شما کاهش داشته. پیشنهاد می‌کنم روی دروس ضعیف تمرکز بیشتر کنی.</p>';
    }}
    
    var similarPoints = comparison.avg_points_similar || 0;
    if(similarPoints > 0 && yourAvgPoints < similarPoints) {{
        html += '<p>👥 میانگین امتیاز کاربران مشابه شما ' + similarPoints + ' است. می‌توانی با انجام روزانه چالش‌ها به آنها برسی.</p>';
    }}
    
    // اضافه کردن توصیه برای کاربران جدید (داده دمو)
    if(data.is_demo_data === true) {{
        html += '<div style="margin-top:15px; padding:12px; background:rgba(108,99,255,0.15); border-radius:16px;">';
        html += '<p style="color:#6c63ff">✨ <strong>نکته:</strong> برای مشاهده آمار واقعی خود، همین الان یکی از چالش‌های روزانه را انجام بده! هر چالش 10-20 امتیاز دارد و نمودارها را پر می‌کند.</p>';
        html += '</div>';
    }}
    
    html += '</div>';
    
    document.getElementById('analyticsContent').innerHTML = html;
    
    // رسم نمودارها بعد از اینکه DOM آماده شد
    drawCharts(data);
}}

function drawCharts(data) {{
    var timeline = data.timeline || [];
    var weekLabels = [];
    var pointsData = [];
    var examData = [];
    
    for(var i = 0; i < timeline.length; i++) {{
        weekLabels.push(timeline[i].week_label);
        pointsData.push(timeline[i].points);
        examData.push(timeline[i].avg_exam_score);
    }}
    
    // نمودار 1: امتیازات
    var pointsCanvas = document.getElementById('pointsChart');
    if(pointsCanvas) {{
        var trendLine = (data.points_trend && data.points_trend.trend_line) ? data.points_trend.trend_line : null;
        drawLineChart(pointsCanvas, weekLabels, pointsData, 'امتیاز', '#6c63ff', trendLine);
    }}
    
    // نمودار 2: نمرات آزمون
    var examCanvas = document.getElementById('examChart');
    if(examCanvas) {{
        var examTrendLine = (data.exam_trend && data.exam_trend.trend_line) ? data.exam_trend.trend_line : null;
        drawLineChart(examCanvas, weekLabels, examData, 'نمره (%)', '#10b981', examTrendLine);
    }}
    
    // نمودار 3: روند ریسک
    var riskTrend = data.risk_trend || [];
    var riskLabels = [];
    var riskData = [];
    for(var r = 0; r < riskTrend.length; r++) {{
        var d = riskTrend[r].date || '';
        riskLabels.push(d.length > 5 ? d.slice(5) : d);
        riskData.push(riskTrend[r].risk);
    }}
    var riskCanvas = document.getElementById('riskChart');
    if(riskCanvas && riskData.length > 0) {{
        drawLineChart(riskCanvas, riskLabels, riskData, 'ریسک (%)', '#ef4444', null);
    }}
    
    // نمودار 4: پیش‌بینی
    var forecastCanvas = document.getElementById('forecastChart');
    if(forecastCanvas) {{
        var historical = pointsData.slice(-4);
        var forecast = (data.points_trend && data.points_trend.forecast) ? data.points_trend.forecast : [];
        var allLabels = [];
        var weekSlice = weekLabels.slice(-4);
        for(var w = 0; w < weekSlice.length; w++) {{
            allLabels.push(weekSlice[w]);
        }}
        allLabels.push('هفته 9', 'هفته 10', 'هفته 11', 'هفته 12');
        var allData = [];
        for(var h = 0; h < historical.length; h++) {{
            allData.push(historical[h]);
        }}
        for(var f = 0; f < forecast.length; f++) {{
            allData.push(forecast[f]);
        }}
        drawLineChart(forecastCanvas, allLabels, allData, 'پیش‌بینی امتیاز', '#f59e0b', null);
    }}
}}

function drawLineChart(canvas, labels, dataPoints, label, color, trendLine) {{
    var ctx = canvas.getContext('2d');
    var container = canvas.parentElement;
    var width = (container ? container.clientWidth : 400) - 40;
    var height = 250;
    canvas.width = width;
    canvas.height = height;
    
    ctx.clearRect(0, 0, width, height);
    
    if(dataPoints.length === 0) {{
        ctx.fillStyle = '#888';
        ctx.font = '14px Vazirmatn';
        ctx.textAlign = 'center';
        ctx.fillText('داده‌ای برای نمایش وجود ندارد', width/2, height/2);
        return;
    }}
    
    var maxVal = Math.max.apply(null, dataPoints.concat([100]));
    var minVal = Math.min.apply(null, dataPoints.concat([0]));
    var range = maxVal - minVal;
    if(range === 0) range = 1;
    
    var padding = {{ top: 20, right: 30, bottom: 30, left: 40 }};
    var graphWidth = width - padding.left - padding.right;
    var graphHeight = height - padding.top - padding.bottom;
    
    var xStep = dataPoints.length > 1 ? graphWidth / (dataPoints.length - 1) : graphWidth;
    
    // رسم محورها
    ctx.strokeStyle = 'rgba(255,255,255,0.2)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, height - padding.bottom);
    ctx.lineTo(width - padding.right, height - padding.bottom);
    ctx.stroke();
    
    // رسم خط داده اصلی
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    var firstPoint = true;
    for(var i = 0; i < dataPoints.length; i++) {{
        var x = padding.left + i * xStep;
        var y = padding.top + graphHeight - ((dataPoints[i] - minVal) / range) * graphHeight;
        if(firstPoint) {{
            ctx.moveTo(x, y);
            firstPoint = false;
        }} else {{
            ctx.lineTo(x, y);
        }}
    }}
    ctx.stroke();
    
    // رسم نقاط داده
    ctx.fillStyle = color;
    for(var i = 0; i < dataPoints.length; i++) {{
        var x = padding.left + i * xStep;
        var y = padding.top + graphHeight - ((dataPoints[i] - minVal) / range) * graphHeight;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    }}
    
    // رسم خط روند (اگر وجود داشته باشد)
    if(trendLine && trendLine.length === dataPoints.length) {{
        ctx.beginPath();
        ctx.strokeStyle = '#ffd700';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        var first = true;
        for(var i = 0; i < trendLine.length; i++) {{
            var x = padding.left + i * xStep;
            var val = trendLine[i];
            val = Math.min(maxVal, Math.max(minVal, val));
            var y = padding.top + graphHeight - ((val - minVal) / range) * graphHeight;
            if(first) {{
                ctx.moveTo(x, y);
                first = false;
            }} else {{
                ctx.lineTo(x, y);
            }}
        }}
        ctx.stroke();
        ctx.setLineDash([]);
    }}
    
    // برچسب‌های محور X
    ctx.fillStyle = '#c4c4f0';
    ctx.font = '10px Vazirmatn';
    ctx.textAlign = 'center';
    for(var i = 0; i < labels.length; i++) {{
        var x = padding.left + i * xStep;
        ctx.fillText(labels[i], x, height - padding.bottom + 15);
    }}
    
    // برچسب‌های محور Y
    ctx.textAlign = 'right';
    for(var i = 0; i <= 4; i++) {{
        var val = minVal + (range * i / 4);
        var y = padding.top + graphHeight - (i / 4) * graphHeight;
        ctx.fillText(Math.round(val), padding.left - 5, y);
    }}
    
    // عنوان نمودار
    ctx.fillStyle = '#ffd700';
    ctx.font = 'bold 12px Vazirmatn';
    ctx.textAlign = 'center';
    ctx.fillText(label, width/2, padding.top - 5);
}}

function escapeHtml(text) {{
    if(!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}}

// بارگذاری اولیه
loadAnalytics();
setInterval(loadAnalytics, 30000);
</script>
</body>
</html>'''
    
    return html_content