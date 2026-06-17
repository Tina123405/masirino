# ml_predictor_html.py
# صفحه پیش‌بینی پیشرفت تحصیلی با هوش مصنوعی

def render_ml_predictor_page(session_id):
    return '''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پیش‌بینی پیشرفت تحصیلی</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            min-height: 100vh;
        }
        .container { max-width: 1000px; margin: auto; }
        h1 {
            text-align: center;
            margin-bottom: 10px;
            font-size: 2rem;
            background: linear-gradient(135deg, #fff, #10b981);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .subtitle { text-align: center; margin-bottom: 30px; color: #c4c4f0; }
        .glass-card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 30px;
            margin-bottom: 25px;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .form-group label {
            font-weight: bold;
            color: #c4c4f0;
            font-size: 0.9rem;
        }
        .form-group input, .form-group select {
            padding: 12px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(0,0,0,0.3);
            color: white;
            font-size: 1rem;
            outline: none;
        }
        .form-group input:focus {
            border-color: #10b981;
        }
        .btn-predict {
            width: 100%;
            padding: 15px;
            background: linear-gradient(90deg, #10b981, #6c63ff);
            border: none;
            border-radius: 30px;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 25px;
            transition: all 0.3s;
        }
        .btn-predict:hover { transform: scale(1.02); opacity: 0.95; }
        .result-box {
            background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(108,99,255,0.15));
            border-radius: 28px;
            padding: 30px;
            text-align: center;
            display: none;
        }
        .predicted-grade {
            font-size: 4rem;
            font-weight: bold;
            background: linear-gradient(135deg, #10b981, #fff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .confidence {
            font-size: 1.1rem;
            color: #c4c4f0;
            margin: 10px 0;
        }
        .improvement {
            font-size: 1rem;
            margin: 10px 0;
        }
        .recommendations {
            text-align: right;
            margin-top: 20px;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 20px;
        }
        .recommendations li {
            margin: 10px 0;
            list-style: none;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        .back-home {
            display: block;
            text-align: center;
            margin-top: 30px;
            color: #6c63ff;
            text-decoration: none;
        }
        .info-note {
            font-size: 0.75rem;
            color: #c4c4f0;
            text-align: center;
            margin-top: 15px;
        }
        @media (max-width: 768px) {
            .form-grid { grid-template-columns: 1fr; }
            .predicted-grade { font-size: 2.5rem; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>🧠 پیش‌بینی پیشرفت تحصیلی</h1>
    <div class="subtitle">با مدل هوشمند (Random Forest از صفر)، نمره نهایی خود را پیش‌بینی کن</div>
    
    <div class="glass-card">
        <div class="form-grid">
            <div class="form-group">
                <label>📚 ساعت مطالعه روزانه (1-8)</label>
                <input type="number" id="study_hours" min="1" max="8" value="4" step="0.5">
            </div>
            <div class="form-group">
                <label>📅 روزهای مطالعه در هفته (1-7)</label>
                <input type="number" id="study_days" min="1" max="7" value="5">
            </div>
            <div class="form-group">
                <label>⭐ معدل قبلی (10-20)</label>
                <input type="number" id="prev_grade" min="10" max="20" step="0.5" value="15">
            </div>
            <div class="form-group">
                <label>😴 ساعت خواب شبانه (4-10)</label>
                <input type="number" id="sleep_hours" min="4" max="10" value="7" step="0.5">
            </div>
            <div class="form-group">
                <label>😰 سطح استرس (1-5)</label>
                <input type="number" id="stress_level" min="1" max="5" value="3">
            </div>
            <div class="form-group">
                <label>😨 اضطراب امتحان (1-5)</label>
                <input type="number" id="test_anxiety" min="1" max="5" value="3">
            </div>
            <div class="form-group">
                <label>🎯 تداوم در مطالعه (1-5)</label>
                <input type="number" id="consistency" min="1" max="5" value="3">
            </div>
            <div class="form-group">
                <label>🔄 مرور در هفته (0-10)</label>
                <input type="number" id="review_count" min="0" max="10" value="4">
            </div>
            <div class="form-group">
                <label>👨‍🏫 معلم خصوصی</label>
                <select id="tutor">
                    <option value="0">ندارم</option>
                    <option value="1">دارم</option>
                </select>
            </div>
            <div class="form-group">
                <label>📖 حضور در کلاس (1-5)</label>
                <input type="number" id="attendance" min="1" max="5" value="4">
            </div>
        </div>
        
        <button class="btn-predict" onclick="predictGrade()">🔮 پیش‌بینی نمره نهایی</button>
    </div>
    
    <div class="loading" id="loading">
        <div>⏳ در حال تحلیل با هوش مصنوعی...</div>
    </div>
    
    <div class="result-box" id="resultBox">
        <div class="predicted-grade" id="predictedGrade">--</div>
        <div class="confidence" id="confidence"></div>
        <div class="improvement" id="improvement"></div>
        <div class="recommendations" id="recommendations"></div>
    </div>
    
    <div class="info-note">
        🤖 این مدل با الگوریتم Random Forest (ساخته شده از صفر) کار میکنه و بر اساس 10 ویژگی مختلف، نمره شما رو پیش‌بینی میکنه
    </div>
    
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
const sessionId = "''' + session_id + '''";

async function predictGrade() {
    const features = {
        study_hours: parseFloat(document.getElementById('study_hours').value),
        study_days: parseFloat(document.getElementById('study_days').value),
        prev_grade: parseFloat(document.getElementById('prev_grade').value),
        sleep_hours: parseFloat(document.getElementById('sleep_hours').value),
        stress_level: parseFloat(document.getElementById('stress_level').value),
        test_anxiety: parseFloat(document.getElementById('test_anxiety').value),
        consistency: parseFloat(document.getElementById('consistency').value),
        review_count: parseFloat(document.getElementById('review_count').value),
        tutor: parseInt(document.getElementById('tutor').value),
        attendance: parseFloat(document.getElementById('attendance').value)
    };
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultBox').style.display = 'none';
    
    try {
        const res = await fetch('/api/ml-predict-pure', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, features: features })
        });
        const data = await res.json();
        
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultBox').style.display = 'block';
        
        if (data.status === 'success') {
            const grade = data.predicted_grade;
            document.getElementById('predictedGrade').innerHTML = grade;
            document.getElementById('confidence').innerHTML = '🎯 دقت پیش‌بینی: ' + data.confidence + '%';
            document.getElementById('improvement').innerHTML = '📈 فاصله تا نمره 20: ' + data.improvement_needed + ' نمره';
            
            let recHtml = '<h3>💡 توصیه‌های هوشمند:</h3><ul>';
            for (let i = 0; i < data.recommendations.length; i++) {
                recHtml += '<li>' + data.recommendations[i] + '</li>';
            }
            recHtml += '</ul>';
            document.getElementById('recommendations').innerHTML = recHtml;
        } else {
            document.getElementById('predictedGrade').innerHTML = 'خطا';
            document.getElementById('recommendations').innerHTML = '<p>❌ ' + (data.error || 'خطا در پیش‌بینی') + '</p>';
        }
    } catch(e) {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('resultBox').style.display = 'block';
        document.getElementById('predictedGrade').innerHTML = 'خطا';
        document.getElementById('recommendations').innerHTML = '<p>❌ خطا: ' + e.message + '</p>';
    }
}
</script>
</body>
</html>'''