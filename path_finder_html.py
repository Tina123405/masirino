# path_finder_html.py - نسخه کامل بدون خطا با سیستم پیشنهاددهنده

def render_path_finder_page(session_id):
    return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مسیرشو - نقشه راه آینده</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            min-height: 100vh;
        }}
        .container {{ max-width: 1200px; margin: auto; }}
        h1 {{
            text-align: center;
            margin-bottom: 40px;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #fff, #6c63ff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }}
        .roadmap-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .roadmap-card:hover {{ transform: translateY(-5px); background: rgba(255,255,255,0.15); }}
        .roadmap-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; }}
        .roadmap-title {{ font-size: 1.5rem; font-weight: bold; }}
        .match-badge {{ background: #10b981; padding: 5px 15px; border-radius: 30px; font-size: 0.9rem; }}
        .roadmap-meta {{ display: flex; gap: 20px; margin: 15px 0; color: #c4c4f0; flex-wrap: wrap; }}
        .steps-preview {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 15px 0; }}
        .step-preview {{ background: rgba(108,99,255,0.3); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; }}
        .btn {{
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            border: none;
            padding: 10px 25px;
            border-radius: 30px;
            color: white;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s;
        }}
        .btn-outline {{
            background: rgba(108, 99, 255, 0.2) !important;
            border: 1px solid #6c63ff !important;
        }}
        .btn-outline:hover {{
            background: rgba(108, 99, 255, 0.4) !important;
            transform: scale(1.02);
        }}
        .btn:hover {{ transform: scale(1.02); opacity: 0.9; }}
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}
        .modal-content {{
            background: linear-gradient(135deg, #1a1a3e, #2d2b55);
            border-radius: 28px;
            padding: 30px;
            max-width: 700px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }}
        .close {{
            float: right;
            font-size: 1.8rem;
            cursor: pointer;
            color: #ff6584;
        }}
        .step {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 15px;
            margin: 10px 0;
            border-right: 3px solid #6c63ff;
        }}
        .step-year {{ color: #6c63ff; font-weight: bold; }}
        .step-title {{ font-size: 1.1rem; font-weight: bold; margin: 5px 0; }}
        .loading {{ text-align: center; padding: 50px; font-size: 1.2rem; }}
        .back-home {{ display: block; text-align: center; margin-top: 30px; color: #6c63ff; text-decoration: none; }}
        .no-data {{ text-align: center; padding: 50px; background: rgba(255,255,255,0.1); border-radius: 28px; }}
        .no-data h3 {{ margin-bottom: 20px; color: #ff6584; }}
        .no-data a {{
            display: inline-block;
            background: #6c63ff;
            padding: 10px 25px;
            border-radius: 30px;
            color: white;
            text-decoration: none;
            margin: 10px;
        }}
        .flex-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎯 مسیرشو - نقشه راه آینده تو</h1>
    <div id="content" class="loading">⏳ در حال بارگذاری...</div>
    <a href="/?session_id={session_id}" class="back-home">← بازگشت به صفحه اصلی</a>
</div>

<div id="detailModal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <div id="modalBody"></div>
    </div>
</div>

<script>
    const sessionId = "{session_id}";
    
    async function loadData() {{
        try {{
            const res = await fetch(`/api/path-finder?session_id=${{sessionId}}`);
            const data = await res.json();
            
            if (data.recommended_roadmaps && data.recommended_roadmaps.length > 0) {{
                let html = '';
                for (let i = 0; i < data.recommended_roadmaps.length; i++) {{
                    const rm = data.recommended_roadmaps[i];
                    
                    let stepsHtml = '';
                    const previewSteps = rm.steps.slice(0, 3);
                    for (let j = 0; j < previewSteps.length; j++) {{
                        stepsHtml += '<span class="step-preview">' + this.escapeHtml(previewSteps[j].title) + '</span>';
                    }}
                    if (rm.steps.length > 3) {{
                        stepsHtml += '<span class="step-preview">+ بیشتر</span>';
                    }}
                    
                    html += `
                        <div class="roadmap-card">
                            <div class="roadmap-header">
                                <span class="roadmap-title">${{this.escapeHtml(rm.title)}}</span>
                                <span class="match-badge">🎯 ${{rm.match_percent || 85}}% تطابق</span>
                            </div>
                            <div class="roadmap-meta">
                                <span>📅 ${{rm.duration_years}} سال</span>
                                <span>💰 ${{rm.income_range}}</span>
                                <span>📈 ${{rm.job_growth}}</span>
                            </div>
                            <div class="steps-preview">
                                ${{stepsHtml}}
                            </div>
                            <div class="flex-buttons">
                                <button class="btn" onclick="showDetail('${{rm.type}}')" style="flex: 2;">مشاهده مسیر کامل 🔍</button>
                                <button class="btn btn-outline" onclick="saveCareer('${{rm.type}}')" style="flex: 1;">❤️ ذخیره</button>
                            </div>
                        </div>
                    `;
                }}
                document.getElementById('content').innerHTML = html;
            }} else {{
                document.getElementById('content').innerHTML = `
                    <div class="no-data">
                        <h3>😊 برای دیدن مسیر شخصی‌سازی شده، ابتدا این کارها رو انجام بده:</h3>
                        <div>
                            <a href="/holland-test?session_id=${{sessionId}}">🧠 آزمون هالند</a>
                            <a href="/track-start?session_id=${{sessionId}}">🎯 انتخاب رشته</a>
                        </div>
                        <p style="color:#c4c4f0; margin-top: 20px;">✨ بعد از انجام، این صفحه رو رفرش کن</p>
                    </div>
                `;
            }}
        }} catch(e) {{
            console.error('Error:', e);
            document.getElementById('content').innerHTML = '<div class="no-data"><h3>❌ خطا در بارگذاری</h3><p>' + e.message + '</p></div>';
        }}
    }}
    
    async function showDetail(careerKey) {{
        if (!careerKey) {{
            alert('❌ خطا: نام شغل مشخص نیست');
            return;
        }}
        
        try {{
            const res = await fetch(`/api/path-finder/detail?session_id=${{sessionId}}&career=${{careerKey}}`);
            const data = await res.json();
            if (data.status === 'ok' && data.roadmap) {{
                let stepsHtml = '';
                const steps = data.roadmap.steps;
                for (let i = 0; i < steps.length; i++) {{
                    const step = steps[i];
                    stepsHtml += `
                        <div class="step">
                            <div class="step-year">📅 سال ${{step.year}}</div>
                            <div class="step-title">${{this.escapeHtml(step.title)}}</div>
                            <div style="color:#c4c4f0">📖 ${{step.subjects.join('، ')}}</div>
                            <div style="color:#10b981;margin-top:5px">🎯 ${{this.escapeHtml(step.milestone)}}</div>
                        </div>
                    `;
                }}
                
                let skillsHtml = '';
                for (let i = 0; i < data.roadmap.skills.length; i++) {{
                    skillsHtml += '<li>' + this.escapeHtml(data.roadmap.skills[i]) + '</li>';
                }}
                
                let jobsHtml = '';
                for (let i = 0; i < data.roadmap.jobs.length; i++) {{
                    jobsHtml += '<li>' + this.escapeHtml(data.roadmap.jobs[i]) + '</li>';
                }}
                
                let resourcesHtml = '';
                for (let i = 0; i < data.roadmap.recommended_resources.length; i++) {{
                    resourcesHtml += '<li>' + this.escapeHtml(data.roadmap.recommended_resources[i]) + '</li>';
                }}
                
                document.getElementById('modalBody').innerHTML = `
                    <h2>${{this.escapeHtml(data.roadmap.title)}}</h2>
                    <div style="display:flex;gap:15px;margin:20px 0;color:#c4c4f0;flex-wrap:wrap">
                        <span>📅 ${{data.roadmap.duration_years}} سال</span>
                        <span>💰 ${{data.roadmap.income_range}}</span>
                        <span>📈 ${{data.roadmap.job_growth}}</span>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <button class="btn" onclick="saveCareer('${{careerKey}}')" style="background: #10b981;">❤️ ذخیره به علاقه‌مندی‌ها</button>
                    </div>
                    <h3>📚 گام‌های مسیر:</h3>
                    ${{stepsHtml}}
                    <h3>💡 مهارت‌های مورد نیاز:</h3>
                    <ul>${{skillsHtml}}</ul>
                    <h3>💼 مشاغل مرتبط:</h3>
                    <ul>${{jobsHtml}}</ul>
                    <h3>📚 منابع پیشنهادی:</h3>
                    <ul>${{resourcesHtml}}</ul>
                `;
                document.getElementById('detailModal').style.display = 'flex';
            }}
        }} catch(e) {{
            console.error('Error:', e);
            alert('خطا در دریافت جزئیات: ' + e.message);
        }}
    }}
    
    async function saveCareer(careerKey) {{
        if (!careerKey) {{
            alert('❌ خطا: نام شغل مشخص نیست');
            return;
        }}
        
        try {{
            const res = await fetch('/api/save-career-interest', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ session_id: sessionId, career: careerKey }})
            }});
            const data = await res.json();
            if (data.status === 'ok') {{
                alert('✅ به علاقه‌مندی‌های شما اضافه شد');
            }} else {{
                alert('❌ خطا در ذخیره سازی: ' + (data.message || 'خطای ناشناخته'));
            }}
        }} catch(e) {{
            console.error('Error:', e);
            alert('❌ خطا در ارتباط با سرور: ' + e.message);
        }}
    }}
    
    function escapeHtml(text) {{
        if (!text) return '';
        return text.replace(/[&<>]/g, function(m) {{
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        }});
    }}
    
    function closeModal() {{
        document.getElementById('detailModal').style.display = 'none';
    }}
    
    loadData();
</script>
</body>
</html>'''