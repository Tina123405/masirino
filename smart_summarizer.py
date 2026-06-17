# smart_summarizer.py
# تولید خودکار خلاصه درس با الگوریتم ساده (بدون AI خارجی)

import re
from collections import Counter

class SmartSummarizer:
    @staticmethod
    def summarize(text, num_sentences=5):
        """
        خلاصه‌سازی ساده با روش امتیازدهی به جملات
        بدون نیاز به هیچ کتابخانه AI
        """
        if not text or len(text) < 100:
            return text or "متن برای خلاصه‌سازی کافی نیست"
        
        # تقسیم به جملات
        sentences = re.split(r'[.!؟]+\s*', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if len(sentences) <= num_sentences:
            return text
        
        # استخراج کلمات کلیدی
        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(words)
        
        # حذف کلمات پرتکرار بی‌معنی
        stopwords = {'و', 'به', 'از', 'برای', 'که', 'این', 'آن', 'است', 'با', 'را', 'در', 'یک', 'های', 'باشد', 'شود'}
        for sw in stopwords:
            if sw in word_freq:
                del word_freq[sw]
        
        # امتیازدهی به جملات
        sentence_scores = []
        for i, sent in enumerate(sentences):
            sent_words = re.findall(r'\w+', sent.lower())
            score = sum(word_freq.get(w, 0) for w in sent_words if w not in stopwords)
            # جملات اول و آخر امتیاز بیشتری می‌گیرند
            if i == 0 or i == len(sentences) - 1:
                score *= 1.5
            sentence_scores.append((i, sent, score))
        
        # انتخاب بهترین جملات
        sentence_scores.sort(key=lambda x: x[2], reverse=True)
        best_indices = sorted([idx for idx, _, _ in sentence_scores[:num_sentences]])
        
        # ساخت خلاصه
        summary = ". ".join([sentences[idx] for idx in best_indices])
        if not summary.endswith('.'):
            summary += "."
        
        return summary
    
    @staticmethod
    def extract_key_points(text, num_points=5):
        """استخراج نکات کلیدی از متن"""
        sentences = re.split(r'[.!؟]+\s*', text)
        
        # جملات کوتاه (احتمالاً نکات کلیدی)
        key_points = [s.strip() for s in sentences if 20 < len(s) < 120]
        
        # اگر نکته کافی نبود، جملات اول را بردار
        if len(key_points) < num_points:
            key_points = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        return key_points[:num_points]
    
    @staticmethod
    def generate_flashcards(text, num_cards=5):
        """تولید فلش‌کارت از متن"""
        sentences = re.split(r'[.!؟]+\s*', text)
        flashcards = []
        
        for sent in sentences[:num_cards*2]:
            if len(sent) > 80:
                # جمله بلند را به سوال و جواب تبدیل کن
                if 'است' in sent or 'می‌باشد' in sent:
                    q = sent.replace('است', 'چیست؟').replace('می‌باشد', 'چیست؟')
                    flashcards.append({"question": q[:70], "answer": sent[:100]})
                    if len(flashcards) >= num_cards:
                        break
        
        return flashcards[:num_cards]


# ========== صفحه HTML برای نمایش ==========
def render_summarizer_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <title>خلاصه‌ساز هوشمند - مسیرینو</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
        }}
        .container {{ max-width: 900px; margin: auto; }}
        .glass-card {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); border-radius: 28px; padding: 25px; margin-bottom: 20px; }}
        textarea {{ width: 100%; padding: 15px; border-radius: 20px; background: rgba(0,0,0,0.3); color: white; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px; }}
        button {{ width: 100%; padding: 14px; background: linear-gradient(90deg, #6c63ff, #ff6584); border: none; border-radius: 30px; color: white; font-weight: bold; cursor: pointer; }}
        .summary-box {{ background: rgba(0,0,0,0.3); padding: 20px; border-radius: 20px; margin-top: 15px; }}
        .flashcard {{ background: rgba(108,99,255,0.2); padding: 15px; border-radius: 16px; margin: 10px 0; cursor: pointer; transition: all 0.3s; }}
        .flashcard:hover {{ transform: scale(1.02); background: rgba(108,99,255,0.4); }}
        .back-home {{ display: block; text-align: center; margin-top: 20px; color: #6c63ff; }}
        hr {{ margin: 15px 0; border-color: rgba(255,255,255,0.1); }}
    </style>
</head>
<body>
<div class="container">
    <h1 style="text-align:center; margin-bottom:20px">✨ خلاصه‌ساز هوشمند درس</h1>
    <div class="glass-card">
        <textarea id="inputText" rows="8" placeholder="متن درس خود را اینجا وارد کنید...&#10;(مثلاً 2-3 صفحه از کتاب درسی)"></textarea>
        <button onclick="summarize()">🤖 تولید خلاصه هوشمند</button>
    </div>
    <div id="result"></div>
    <a href="/" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<script>
const sessionId = "{session_id}";

async function summarize() {{
    const text = document.getElementById('inputText').value;
    if (!text.trim() || text.length < 100) {{
        alert('لطفاً حداقل ۱۰۰ کاراکتر متن وارد کنید');
        return;
    }}
    
    const res = await fetch('/api/smart-summarize', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ session_id: sessionId, text: text }})
    }});
    const data = await res.json();
    
    let html = `<div class="glass-card">
        <h3>📝 خلاصه هوشمند</h3>
        <div class="summary-box">${{data.summary.replace(/\\n/g, '<br>')}}</div>
        <hr>
        <h3>💡 نکات کلیدی</h3>
        <ul>`;
    
    for (let i = 0; i < data.key_points.length; i++) {{
        html += `<li style="margin:8px 0">✨ ${{data.key_points[i]}}</li>`;
    }}
    
    html += `</ul><hr><h3>📇 فلش‌کارت‌های پیشنهادی</h3>`;
    
    for (let i = 0; i < data.flashcards.length; i++) {{
        const fc = data.flashcards[i];
        html += `<div class="flashcard" onclick="this.querySelector('.answer').style.display='block'">
            <strong>❓ ${{fc.question}}</strong>
            <div class="answer" style="display:none; margin-top:10px; color:#f59e0b">✅ ${{fc.answer}}</div>
            <small style="color:#c4c4f0">(برای دیدن پاسخ کلیک کنید)</small>
        </div>`;
    }}
    
    html += `<button onclick="window.print()" style="margin-top:15px">🖨️ چاپ</button></div>`;
    document.getElementById('result').innerHTML = html;
}}
</script>
</body>
</html>'''