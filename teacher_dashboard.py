# teacher_dashboard.py - نسخه کامل با نمودارها و دکمه مشاهده دانش‌آموز

import sqlite3
import json
from config import DB_NAME

def render_teacher_dashboard(session_id):
    """داشبورد مشاور با نمودارهای تحلیلی و لیست دانش‌آموزان"""
    
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # آمار کلی
    cursor.execute('SELECT COUNT(*) FROM users WHERE role != "admin" AND role != "counselor"')
    total_students = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM risk_analysis WHERE risk_percent >= 55')
    high_risk_count = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT COUNT(*) FROM risk_analysis WHERE risk_percent >= 35 AND risk_percent < 55')
    medium_risk_count = cursor.fetchone()[0] or 0
    
    low_risk_count = total_students - high_risk_count - medium_risk_count
    
    cursor.execute('SELECT AVG(weekly_points) FROM user_points')
    avg_points_row = cursor.fetchone()
    avg_points = round(avg_points_row[0], 1) if avg_points_row and avg_points_row[0] else 0
    
    # توزیع رشته‌ها
    cursor.execute('''
        SELECT track, COUNT(*) FROM users 
        WHERE track IS NOT NULL AND track != '' AND role != "admin" AND role != "counselor"
        GROUP BY track
    ''')
    track_data = cursor.fetchall()
    track_labels = [row[0] for row in track_data]
    track_counts = [row[1] for row in track_data]
    
    # لیست دانش‌آموزان
    cursor.execute('''
        SELECT u.user_id, u.name, u.user_code, u.grade_level, u.track,
               COALESCE(up.total_points, 0) as points,
               COALESCE(ra.risk_percent, 0) as risk
        FROM users u
        LEFT JOIN user_points up ON u.user_id = up.user_id
        LEFT JOIN risk_analysis ra ON u.user_id = ra.user_id
        WHERE u.role != "admin" AND u.role != "counselor"
        ORDER BY ra.risk_percent DESC NULLS LAST
        LIMIT 50
    ''')
    
    students = []
    for row in cursor.fetchall():
        risk_percent = row['risk'] if row['risk'] is not None else 0
        students.append({
            "user_id": row['user_id'],
            "name": row['name'] or (row['user_code'][:8] if row['user_code'] else "کاربر"),
            "user_code": row['user_code'],
            "grade_level": row['grade_level'] or "-",
            "track": row['track'] or "-",
            "points": row['points'] or 0,
            "risk_percent": round(risk_percent, 1),
            "progress": 50
        })
    
    conn.close()
    
    # آماده‌سازی داده برای نمودارها
    chart_data = {
        "total_students": total_students,
        "high_risk": high_risk_count,
        "medium_risk": medium_risk_count,
        "low_risk": low_risk_count,
        "avg_points": avg_points,
        "track_labels": track_labels if track_labels else ["علوم تجربی", "ریاضی فیزیک", "علوم انسانی"],
        "track_data": track_counts if track_counts else [0, 0, 0]
    }
    
    html = f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد مشاور - مسیرینو</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Vazirmatn', sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
            color: #fff;
            line-height: 1.6;
            padding: 20px;
            direction: rtl;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* هدر */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        
        h1 {{
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            font-size: 2rem;
        }}
        
        .btn-back {{
            display: inline-block;
            padding: 10px 25px;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            color: white;
            text-decoration: none;
            border-radius: 40px;
            font-weight: 600;
            transition: 0.3s;
        }}
        
        .btn-back:hover {{
            transform: scale(1.03);
            box-shadow: 0 5px 20px rgba(108,99,255,0.4);
        }}
        
        /* کارت‌های آمار */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            transition: 0.3s;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            background: rgba(108,99,255,0.2);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff, #6c63ff);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #c4c4f0;
            margin-top: 10px;
        }}
        
        /* نمودارها */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        
        .chart-card h3 {{
            margin-bottom: 15px;
            color: #c4c4ff;
            text-align: center;
        }}
        
        canvas {{
            max-height: 300px;
        }}
        
        /* جدول دانش‌آموزان */
        .students-section {{
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            margin-top: 20px;
        }}
        
        .students-section h3 {{
            margin-bottom: 20px;
            color: #c4c4ff;
            font-size: 1.4rem;
        }}
        
        .table-container {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        th {{
            background: rgba(108,99,255,0.3);
            font-weight: 600;
        }}
        
        tr:hover {{
            background: rgba(108,99,255,0.15);
        }}
        
        .risk-high {{ color: #ff6b6b; font-weight: bold; }}
        .risk-medium {{ color: #ffd93d; font-weight: bold; }}
        .risk-low {{ color: #6bcb77; font-weight: bold; }}
        
        .btn-view {{
            display: inline-block;
            padding: 6px 15px;
            background: #6c63ff;
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-size: 0.85rem;
            transition: 0.3s;
        }}
        
        .btn-view:hover {{
            background: #ff6584;
            transform: scale(1.05);
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #888;
            font-size: 0.8rem;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            h1 {{
                font-size: 1.4rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- هدر -->
        <div class="header">
            <h1>📊 داشبورد مشاور تحصیلی</h1>
            <a href="/?session_id={session_id}" class="btn-back">← بازگشت به صفحه اصلی</a>
        </div>
        
        <!-- کارت‌های آمار -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_students}</div>
                <div class="stat-label">👥 تعداد دانش‌آموزان</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{high_risk_count}</div>
                <div class="stat-label">⚠️ ریسک افت بالا</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_points}</div>
                <div class="stat-label">⭐ میانگین امتیاز</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(students)}</div>
                <div class="stat-label">📋 دانش‌آموز فعال</div>
            </div>
        </div>
        
        <!-- نمودارها -->
        <div class="charts-grid">
            <div class="chart-card">
                <h3>📉 وضعیت ریسک افت تحصیلی</h3>
                <canvas id="riskChart"></canvas>
            </div>
            <div class="chart-card">
                <h3>🎓 توزیع رشته‌های تحصیلی</h3>
                <canvas id="trackChart"></canvas>
            </div>
        </div>
        
        <!-- جدول دانش‌آموزان -->
        <div class="students-section">
            <h3>📋 لیست دانش‌آموزان</h3>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>نام</th>
                            <th>کد یکتا</th>
                            <th>پایه</th>
                            <th>رشته</th>
                            <th>پیشرفت</th>
                            <th>ریسک افت</th>
                            <th>امتیاز</th>
                            <th>عملیات</th>
                        </tr>
                    </thead>
                    <tbody>
    '''
    
    for student in students:
        risk_class = "risk-high" if student['risk_percent'] > 60 else ("risk-medium" if student['risk_percent'] > 30 else "risk-low")
        html += f'''
                        <tr>
                            <td>{student['name']}</td>
                            <td><code>{student['user_code']}</code></td>
                            <td>{student['grade_level']}</td>
                            <td>{student['track']}</td>
                            <td>{student['progress']}%</td>
                            <td class="{risk_class}">{student['risk_percent']}%</td>
                            <td>{student['points']}</td>
                            <td>
                                <a href="/consultant/student/{student['user_id']}?session_id={session_id}" class="btn-view">🔍 مشاهده</a>
                            </td>
                        </tr>
        '''
    
    html += f'''
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>🎓 مسیرینو - سامانه هوشمند مشاوره تحصیلی</p>
            <p>نسخه ۴.۰ | © ۱۴۰۴</p>
        </div>
    </div>
    
    <script>
        // نمودار ریسک افت تحصیلی
        const riskCtx = document.getElementById('riskChart').getContext('2d');
        new Chart(riskCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['ریسک بالا (>55%)', 'ریسک متوسط (35-55%)', 'ریسک کم (<35%)'],
                datasets: [{{
                    data: [{high_risk_count}, {medium_risk_count}, {low_risk_count}],
                    backgroundColor: ['#ff6b6b', '#ffd93d', '#6bcb77'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{ color: '#fff', font: {{ family: 'Vazirmatn' }} }}
                    }}
                }}
            }}
        }});
        
        // نمودار توزیع رشته‌ها
        const trackCtx = document.getElementById('trackChart').getContext('2d');
        new Chart(trackCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(chart_data['track_labels'])},
                datasets: [{{
                    label: 'تعداد دانش‌آموزان',
                    data: {json.dumps(chart_data['track_data'])},
                    backgroundColor: 'rgba(108, 99, 255, 0.7)',
                    borderRadius: 10
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ labels: {{ color: '#fff', font: {{ family: 'Vazirmatn' }} }} }}
                }},
                scales: {{
                    y: {{ ticks: {{ color: '#fff' }}, grid: {{ color: 'rgba(255,255,255,0.1)' }} }},
                    x: {{ ticks: {{ color: '#fff', font: {{ family: 'Vazirmatn' }} }}, grid: {{ display: false }} }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    return html