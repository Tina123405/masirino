# main.py - نسخه کامل با قابلیت مشاهده پروفایل دانش‌آموز برای مشاور
import json
import urllib.parse
import secrets
import hashlib
import time
import logging
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from collections import deque
from analytics_core import AnalyticsEngine, save_ml_prediction
from analytics_html import render_analytics_page

from config import HOST, PORT, TRACKS, SUBJECTS_BY_LEVEL, SUBJECTS_BY_TRACK, DB_NAME
from database import (
    init_db, get_user_from_db, save_user_to_db, update_consent,
    save_conversation, save_track_analysis, save_risk_analysis, save_study_plan,
    save_alert, save_feedback, get_similar_users, get_user_stats_for_comparison,
    generate_user_code, get_dashboard_stats, get_user_goals, create_goal,
    update_goal, update_goal_progress, delete_goal, get_user_points as db_get_user_points,
    add_points_to_user as db_add_points, get_leaderboard, get_gamification_data,
    get_user_groups, get_all_public_groups, get_group_detail, join_group,
    join_group_by_code, save_path_finder_log, get_db_connection
)
from track_risk_logic import (
    RESULT_STORE, CHAT_HISTORY, SESSION_STORE,
    chatbot_respond, build_context, infer_intent, calculate_confidence,
    advanced_sentiment_analysis, compute_risk_fall_detailed, risk_breakdown_detailed,
    recommend_tracks_detailed, track_strengths_weaknesses, compute_career_match_detailed,
    top_risky_subjects_detailed, anti_fall_plan_detailed, get_recommended_resources,
    get_study_tips_by_risk, grade_category, safe_key, cleanup_old_data,
    export_report_to_json, backup_database, smart_online_search
)
from html_pages import (
    render_consent_page, render_homepage, render_chat_only_page,
    render_track_form_page, render_track_result_page,
    render_risk_form_page, render_risk_result_page, render_admin_dashboard,
    render_holland_test_page, render_pomodoro_page, render_smart_goals_page,
    render_exam_questions_page, render_daily_challenges_page,
    render_educational_calendar_page, render_groups_page, render_profile_page,
    render_modern_cards, render_role_select_page
)
from exam_questions import generate_questions, save_exam_result
from challenges import get_daily_challenges, complete_user_challenge, get_user_points as challenges_get_points
from educational_calendar import get_calendar_data, add_user_event
from path_finder import get_path_finder_data, get_roadmap_detail_api
from path_finder_html import render_path_finder_page
from ml_predictor_html import render_ml_predictor_page
from ml_predictor_pure import get_predictor
from smart_summarizer import SmartSummarizer, render_summarizer_page
from dynamic_planner import DynamicStudyPlanner, render_planner_page
from educational_games import render_games_page
from teacher_dashboard import render_teacher_dashboard
from gamification import (
    GamificationSystem, add_points_to_user, update_challenge_completed,
    get_user_gamification_status, get_leaderboard_data
)
from gamification_html import render_gamification_profile_page
from user_manual import render_user_manual_page

logger = logging.getLogger(__name__)

class Handler(BaseHTTPRequestHandler):
    def respond(self, code, content, content_type="text/html; charset=utf-8"):
        try:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except Exception as e:
            logger.error(f"خطا در ارسال پاسخ: {e}")

    def _get_level_name(self, points):
        """تعیین سطح بر اساس امتیاز"""
        if points >= 10000: return "خوارزمی"
        if points >= 7500: return "استاد"
        if points >= 5000: return "افسانه‌ای"
        if points >= 3500: return "الماسی"
        if points >= 2000: return "پلاتینیوم"
        if points >= 1000: return "طلایی"
        if points >= 500: return "نقره‌ای"
        if points >= 250: return "برنزی"
        if points >= 100: return "تلاشگر"
        return "شروع‌کننده"

    def _render_student_profile_html(self, student_id, session_id, profile, gamification, stats):
        return f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پروفایل دانش‌آموز - مسیرینو</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Vazirmatn', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            direction: rtl;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 35px;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        h1 {{
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #c4c4ff;
            margin-bottom: 15px;
            font-size: 1.4rem;
            border-right: 3px solid #6c63ff;
            padding-right: 12px;
        }}
        .info-card {{
            background: rgba(0,0,0,0.35);
            padding: 22px;
            border-radius: 24px;
            margin: 18px 0;
            transition: 0.3s;
        }}
        .info-card:hover {{
            background: rgba(108,99,255,0.15);
        }}
        .btn {{
            display: inline-block;
            padding: 12px 28px;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            color: white;
            text-decoration: none;
            border-radius: 40px;
            margin-top: 20px;
            margin-left: 15px;
            font-weight: 600;
            transition: 0.3s;
        }}
        .btn:hover {{
            transform: scale(1.03);
            box-shadow: 0 5px 20px rgba(108,99,255,0.4);
        }}
        .risk-high {{ color: #ff6b6b; font-weight: bold; }}
        .risk-medium {{ color: #ffd93d; font-weight: bold; }}
        .risk-low {{ color: #6bcb77; font-weight: bold; }}
        .stat-number {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #6c63ff;
        }}
        code {{
            background: #00000055;
            padding: 4px 12px;
            border-radius: 12px;
            font-family: monospace;
        }}
        .flex-buttons {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📘 پروفایل دانش‌آموز</h1>
        <p><strong>🆔 کد یکتا:</strong> <code>{student_id}</code></p>
        
        <div class="info-card">
            <h2>👤 اطلاعات شخصی</h2>
            <p><strong>نام:</strong> {profile.get('first_name', 'نامشخص')} {profile.get('last_name', '')}</p>
            <p><strong>پایه تحصیلی:</strong> {profile.get('grade', 'نامشخص')}</p>
            <p><strong>ایمیل:</strong> {profile.get('email', 'ندارد')}</p>
        </div>
        
        <div class="info-card">
            <h2>🏆 وضعیت گیمیفیکیشن</h2>
            <p><strong>⭐ امتیاز کل:</strong> <span class="stat-number">{gamification.get('total_points', 0)}</span></p>
            <p><strong>📊 سطح:</strong> {gamification.get('level', 'شروع‌کننده')}</p>
            <p><strong>🔥 استریک روزانه:</strong> {gamification.get('streak', 0)} روز</p>
        </div>
        
        <div class="info-card">
            <h2>📊 آمار تحصیلی</h2>
            <p><strong>⚠️ ریسک افت تحصیلی:</strong> 
                <span class="{'risk-high' if stats.get('risk', 0) > 60 else 'risk-medium' if stats.get('risk', 0) > 30 else 'risk-low'}">
                    {stats.get('risk', 0)}%
                </span>
            </p>
            <p><strong>✅ چالش‌های انجام شده:</strong> {stats.get('challenges_completed', 0)}</p>
        </div>
        
        <div class="flex-buttons">
            <a href="/teacher-dashboard?session_id={session_id}" class="btn">← بازگشت به لیست دانش‌آموزان</a>
            <a href="/?session_id={session_id}" class="btn" style="background:#ff6584;">🏠 صفحه اصلی</a>
        </div>
    </div>
</body>
</html>'''

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)
        
        # ========== نمایش پروفایل دانش‌آموز برای مشاور ==========
        # ========== نمایش پروفایل دانش‌آموز برای مشاور ==========
        if path.startswith("/consultant/student/"):
            student_id = path.split("/")[-1]
            session_id = qs.get("session_id", [""])[0]
            self.do_GET_student_profile(student_id, session_id)
            return
            
            # بررسی نقش مشاور
            user = get_user_from_db(session_id)
            if not user or user.get("role") != "counselor":
                self.respond(403, "<h3>⛔ دسترسی غیرمجاز. فقط مشاوران می‌توانند این صفحه را ببینند.</h3><a href='/'>بازگشت</a>")
                return
            
            # بارگذاری داده‌های دانش‌آموز
            student_user = get_user_from_db(student_id)
            if not student_user:
                self.respond(404, f"<h3>❌ دانش‌آموز با کد {student_id} یافت نشد.</h3><a href='/teacher-dashboard?session_id={session_id}'>بازگشت به لیست</a>")
                return
            
            # دریافت آمار اضافی از دیتابیس
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT total_points, weekly_points, streak_days FROM user_points WHERE user_id = ?', (student_id,))
            points_row = cursor.fetchone()
            
            cursor.execute('SELECT risk_percent FROM risk_analysis WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (student_id,))
            risk_row = cursor.fetchone()
            
            cursor.execute('SELECT COUNT(*) FROM user_challenges WHERE user_id = ? AND completed = 1', (student_id,))
            challenges_row = cursor.fetchone()
            challenges_count = challenges_row[0] if challenges_row else 0
            conn.close()
            
            profile = {
                'first_name': student_user.get('name', ''),
                'last_name': student_user.get('lastname', ''),
                'grade': student_user.get('grade_level', 'نامشخص'),
                'email': student_user.get('email', 'ندارد')
            }
            
            points = points_row[0] if points_row else 0
            if points >= 10000: level = "خوارزمی"
            elif points >= 7500: level = "استاد"
            elif points >= 5000: level = "افسانه‌ای"
            elif points >= 3500: level = "الماسی"
            elif points >= 2000: level = "پلاتینیوم"
            elif points >= 1000: level = "طلایی"
            elif points >= 500: level = "نقره‌ای"
            elif points >= 250: level = "برنزی"
            elif points >= 100: level = "تلاشگر"
            else: level = "شروع‌کننده"
            
            risk = risk_row[0] if risk_row else 0
            risk_class = "risk-high" if risk > 60 else ("risk-medium" if risk > 30 else "risk-low")
            
            html = f'''<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پروفایل دانش‌آموز - مسیرینو</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Vazirmatn', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
            padding: 30px;
            direction: rtl;
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 30px;
            padding: 35px;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        h1 {{
            background: linear-gradient(135deg, #6c63ff, #ff6584);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #c4c4ff;
            margin-bottom: 15px;
            font-size: 1.4rem;
            border-right: 3px solid #6c63ff;
            padding-right: 12px;
        }}
        .info-card {{
            background: rgba(0,0,0,0.35);
            padding: 22px;
            border-radius: 24px;
            margin: 18px 0;
            transition: 0.3s;
        }}
        .info-card:hover {{ background: rgba(108,99,255,0.15); }}
        .btn {{
            display: inline-block;
            padding: 12px 28px;
            background: linear-gradient(90deg, #6c63ff, #ff6584);
            color: white;
            text-decoration: none;
            border-radius: 40px;
            margin-top: 20px;
            margin-left: 15px;
            font-weight: 600;
            transition: 0.3s;
        }}
        .btn:hover {{ transform: scale(1.03); box-shadow: 0 5px 20px rgba(108,99,255,0.4); }}
        .risk-high {{ color: #ff6b6b; font-weight: bold; }}
        .risk-medium {{ color: #ffd93d; font-weight: bold; }}
        .risk-low {{ color: #6bcb77; font-weight: bold; }}
        .stat-number {{ font-size: 1.8rem; font-weight: bold; color: #6c63ff; }}
        code {{ background: #00000055; padding: 4px 12px; border-radius: 12px; font-family: monospace; }}
        .flex-buttons {{ display: flex; gap: 15px; flex-wrap: wrap; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📘 پروفایل دانش‌آموز</h1>
        <p><strong>🆔 کد یکتا:</strong> <code>{student_id}</code></p>
        
        <div class="info-card">
            <h2>👤 اطلاعات شخصی</h2>
            <p><strong>نام:</strong> {profile.get('first_name', 'نامشخص')} {profile.get('last_name', '')}</p>
            <p><strong>پایه تحصیلی:</strong> {profile.get('grade', 'نامشخص')}</p>
            <p><strong>ایمیل:</strong> {profile.get('email', 'ندارد')}</p>
        </div>
        
        <div class="info-card">
            <h2>🏆 وضعیت گیمیفیکیشن</h2>
            <p><strong>⭐ امتیاز کل:</strong> <span class="stat-number">{points}</span></p>
            <p><strong>📊 سطح:</strong> {level}</p>
            <p><strong>🔥 استریک روزانه:</strong> {points_row[2] if points_row else 0} روز</p>
        </div>
        
        <div class="info-card">
            <h2>📊 آمار تحصیلی</h2>
            <p><strong>⚠️ ریسک افت تحصیلی:</strong> <span class="{risk_class}">{risk}%</span></p>
            <p><strong>✅ چالش‌های انجام شده:</strong> {challenges_count}</p>
        </div>
        
        <div class="flex-buttons">
            <a href="/teacher-dashboard?session_id={session_id}" class="btn">← بازگشت به لیست دانش‌آموزان</a>
            <a href="/?session_id={session_id}" class="btn" style="background:#ff6584;">🏠 صفحه اصلی</a>
        </div>
    </div>
</body>
</html>'''
            self.respond(200, html)
            return
        
        # ========== سرویس فایل‌های استاتیک ==========
        if path.startswith("/static/"):
            try:
                file_path = path[1:]
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        content = f.read()
                    if path.endswith(".css"):
                        self.send_response(200)
                        self.send_header("Content-Type", "text/css")
                        self.end_headers()
                        self.wfile.write(content)
                    elif path.endswith(".js"):
                        self.send_response(200)
                        self.send_header("Content-Type", "application/javascript")
                        self.end_headers()
                        self.wfile.write(content)
                    else:
                        self.respond(200, content.decode("utf-8"))
                else:
                    self.respond(404, "فایل یافت نشد")
            except Exception as e:
                self.respond(500, f"خطا: {e}")
            return

        # ========== صفحه انتخاب نقش ==========
        if path == "/role-select":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            self.respond(200, render_role_select_page(session_id))
            return

        # ========== صفحه رضایت نامه ==========
        if path == "/consent-page":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            self.respond(200, render_consent_page(session_id))
            return

        # ========== صفحه اصلی (بر اساس نقش کاربر) ==========
        if path == "/":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if not user:
                self.send_response(303)
                self.send_header("Location", f"/role-select?session_id={session_id}")
                self.end_headers()
                return
            if not user.get("consent_given"):
                self.send_response(303)
                self.send_header("Location", f"/consent-page?session_id={session_id}")
                self.end_headers()
                return
            user_role = user.get("role", "student")
            SESSION_STORE.setdefault(session_id, {})
            if user_role == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
            else:
                self.respond(200, render_homepage(session_id))
            return

        # ========== صفحات دانش‌آموزی ==========
        if path == "/chat-only":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_chat_only_page(session_id))
            return

        if path == "/track-start":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE[session_id] = SESSION_STORE.get(session_id, {})
            self.respond(200, render_track_form_page(session_id, 1, SESSION_STORE[session_id]))
            return

        if path == "/risk-start":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE[session_id] = SESSION_STORE.get(session_id, {})
            self.respond(200, render_risk_form_page(session_id, SESSION_STORE[session_id]))
            return

        if path == "/holland-test":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_holland_test_page(session_id))
            return

        if path == "/pomodoro":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_pomodoro_page(session_id))
            return

        if path == "/smart-goals":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_smart_goals_page(session_id))
            return

        if path == "/get-goals":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"goals": []}), "application/json")
                return
            goals = get_user_goals(session_id)
            self.respond(200, json.dumps({"goals": goals}, ensure_ascii=False), "application/json")
            return

        if path == "/exam-questions":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_exam_questions_page(session_id))
            return

        if path == "/daily-challenges":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_daily_challenges_page(session_id))
            return

        if path == "/educational-calendar":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_educational_calendar_page(session_id))
            return

        if path == "/groups":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            SESSION_STORE.setdefault(session_id, {})
            self.respond(200, render_groups_page(session_id))
            return

        if path == "/profile":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_profile_page(session_id))
            return

        if path == "/path-finder":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_path_finder_page(session_id))
            return

        if path == "/ml-predictor":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_ml_predictor_page(session_id))
            return

        if path == "/smart-summarizer":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_summarizer_page(session_id))
            return

        if path == "/dynamic-planner":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_planner_page(session_id))
            return

        if path == "/educational-games":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_games_page(session_id))
            return

        # ========== داشبورد معلم ==========
        if path == "/teacher-dashboard":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if not user or user.get("role") != "counselor":
                self.send_response(303)
                self.send_header("Location", f"/role-select?session_id={session_id}")
                self.end_headers()
                return
            self.respond(200, render_teacher_dashboard(session_id))
            return

        if path == "/gamification-profile":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_gamification_profile_page(session_id))
            return

        if path == "/admin":
            self.respond(200, render_admin_dashboard())
            return

        if path == "/manual":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            self.respond(200, render_user_manual_page(session_id))
            return

        if path == "/react-app":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            try:
                from react_app import REACT_HTML_TEMPLATE
                html = REACT_HTML_TEMPLATE.format(session_id=session_id, title="مسیرینو React")
                self.respond(200, html)
            except ImportError:
                self.respond(200, "<h2>صفحه React در حال آماده‌سازی است</h2><a href='/'>بازگشت</a>")
            return

        # ========== نتایج تحلیل‌ها ==========
        if path == "/track-result":
            token = (qs.get("token") or [""])[0]
            d = RESULT_STORE.get(token)
            self.respond(200, render_track_result_page(d) if d else "نتیجه‌ای یافت نشد")
            return

        if path == "/risk-result":
            token = (qs.get("token") or [""])[0]
            d = RESULT_STORE.get(token)
            self.respond(200, render_risk_result_page(d) if d else "نتیجه‌ای یافت نشد")
            return

        # ========== APIهای دریافت داده ==========
        if path == "/get-challenges":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"challenges": [], "total_points": 0, "weekly_points": 0, "completed_count": 0, "streak_days": 0, "level": "مشاور"}), "application/json")
                return
            level = qs.get("level", ["آسان"])[0]
            challenges = get_daily_challenges(session_id, level)
            points_data = challenges_get_points(session_id)
            gamification = get_user_gamification_status(session_id)
            self.respond(200, json.dumps({
                "challenges": challenges,
                "total_points": points_data.get("total", 0),
                "weekly_points": points_data.get("weekly", 0),
                "completed_count": points_data.get("completed", 0),
                "streak_days": points_data.get("streak", 0),
                "level": gamification.get("level_name", "شروع‌کننده") if gamification else "شروع‌کننده"
            }, ensure_ascii=False), "application/json")
            return

        if path == "/get-calendar-data":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"events": [], "month_days": 31, "first_weekday": 0, "summary": {"total_events": 0}}), "application/json")
                return
            year = int(qs.get("year", [1404])[0])
            month = int(qs.get("month", [1])[0])
            data = get_calendar_data(session_id, year, month)
            self.respond(200, json.dumps(data, ensure_ascii=False), "application/json")
            return

        if path == "/api/path-finder":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "ok", "recommended_roadmaps": [], "user_data": {}}), "application/json")
                return
            save_path_finder_log(session_id)
            data = get_path_finder_data(session_id)
            self.respond(200, json.dumps({"status": "ok", **data}, ensure_ascii=False), "application/json")
            return

        if path == "/api/path-finder/detail":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "error", "message": "دسترسی غیرمجاز"}), "application/json")
                return
            career = qs.get("career", [""])[0]
            data = get_roadmap_detail_api(session_id, career)
            self.respond(200, json.dumps(data, ensure_ascii=False), "application/json")
            return

        if path == "/api/gamification/status":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "ok", "total_points": 0, "current_level": 1, "level_name": "مشاور", "achievements": [], "stats": {}}), "application/json")
                return
            status = get_user_gamification_status(session_id)
            self.respond(200, json.dumps({"status": "ok", **status}, ensure_ascii=False), "application/json")
            return

        if path == "/api/gamification/leaderboard":
            leaderboard = get_leaderboard_data(10)
            self.respond(200, json.dumps({"status": "ok", "leaderboard": leaderboard}, ensure_ascii=False), "application/json")
            return

        if path == "/api/groups/my":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "ok", "groups": []}), "application/json")
                return
            groups = get_user_groups(session_id)
            self.respond(200, json.dumps({"status": "ok", "groups": groups}, ensure_ascii=False), "application/json")
            return

        if path == "/api/groups/detail":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "error", "message": "دسترسی غیرمجاز"}), "application/json")
                return
            group_id = int(qs.get("group_id", [0])[0])
            detail = get_group_detail(group_id, session_id)
            self.respond(200, json.dumps(detail or {"status": "error"}, ensure_ascii=False), "application/json")
            return

        if path == "/api/groups/public":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, json.dumps({"status": "ok", "groups": []}), "application/json")
                return
            groups = get_all_public_groups(session_id)
            self.respond(200, json.dumps({"status": "ok", "groups": groups}, ensure_ascii=False), "application/json")
            return

        if path == "/api/teacher/stats":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if not user or user.get("role") != "counselor":
                self.respond(403, json.dumps({"error": "دسترسی غیرمجاز"}), "application/json")
                return
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users WHERE role != "admin" AND role != "counselor"')
            total = cursor.fetchone()[0] or 0
            cursor.execute('SELECT COUNT(*) FROM risk_analysis WHERE risk_percent >= 55')
            high_risk = cursor.fetchone()[0] or 0
            cursor.execute('SELECT AVG(progress) FROM smart_goals WHERE status != "completed"')
            avg_prog = cursor.fetchone()[0] or 0
            cursor.execute('SELECT AVG(weekly_points) FROM user_points')
            avg_points = cursor.fetchone()[0] or 0
            conn.close()
            self.respond(200, json.dumps({
                "total_students": total,
                "high_risk_count": high_risk,
                "avg_progress": round(avg_prog, 1),
                "avg_points": round(avg_points, 1),
                "track_labels": ["علوم تجربی", "ریاضی فیزیک", "علوم انسانی", "هنر"],
                "track_data": [25, 25, 25, 25],
                "high_risk": high_risk,
                "medium_risk": 10,
                "low_risk": total - high_risk - 10
            }, ensure_ascii=False), "application/json")
            return

        if path == "/api/teacher/students":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            if not user or user.get("role") != "counselor":
                self.respond(403, json.dumps({"error": "دسترسی غیرمجاز"}), "application/json")
                return
            conn = get_db_connection()
            cursor = conn.cursor()
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
                risk_percent = row[6] if row[6] is not None else 0
                risk_level = "high" if risk_percent >= 55 else ("medium" if risk_percent >= 35 else "low")
                students.append({
                    "user_id": row[0],
                    "name": row[1] or (row[2][:8] if row[2] else "کاربر"),
                    "user_code": row[2],
                    "grade_level": row[3] or "-",
                    "track": row[4] or "-",
                    "points": row[5] or 0,
                    "risk_percent": round(risk_percent, 1),
                    "risk_level": risk_level,
                    "progress": 50
                })
            conn.close()
            self.respond(200, json.dumps({"students": students}, ensure_ascii=False), "application/json")
            return

        if path == "/get-user-profile":
            session_id = qs.get("session_id", [""])[0]
            user = get_user_from_db(session_id)
            self.respond(200, json.dumps({
                "status": "ok",
                "first_name": user.get("name", "") if user else "",
                "last_name": user.get("lastname", "") if user else "",
                "grade_level": user.get("grade_level", "") if user else "",
                "email": user.get("email", "") if user else ""
            }, ensure_ascii=False), "application/json")
            return

        if path == "/api/v1/compare":
            session_id = qs.get("session_id", [""])[0]
            similar = get_similar_users(session_id)
            comparison = get_user_stats_for_comparison(session_id)
            self.respond(200, json.dumps({"similar_users": similar, "comparison": comparison}, ensure_ascii=False), "application/json")
            return

        # ========== API اتصال به سامانه مدرسه (شبیه‌سازی شده) ==========
        if path == "/api/school/documentation":
            from external_api import get_api_documentation
            self.respond(200, json.dumps(get_api_documentation(), ensure_ascii=False), "application/json")
            return

        # ========== API توصیه‌گر پیشرفته ==========
        if path == "/api/advanced-recommendations":
            session_id = qs.get("session_id", [""])[0]
            from adaptive_recommender_advanced import get_advanced_recommender
            recommender = get_advanced_recommender(session_id)
            recommendations = recommender.get_adaptive_dashboard_recommendations()
            self.respond(200, json.dumps({"status": "ok", **recommendations}, ensure_ascii=False), "application/json")
            return

        # ========== API آنالیتیکس ==========
        if path == "/api/analytics/data":
            session_id = qs.get("session_id", [""])[0]
            try:
                from analytics_core import AnalyticsEngine
                engine = AnalyticsEngine(session_id)
                data = engine.get_full_analytics()
                self.respond(200, json.dumps({"status": "ok", **data}, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False), "application/json")
            return

        # ========== صفحه HTML آنالیتیکس ==========
        if path == "/analytics":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            from analytics_html import render_analytics_page
            self.respond(200, render_analytics_page(session_id))
            return

        # ========== صفحه اتصال به سامانه مدرسه ==========
        if path == "/school-integration":
            session_id = qs.get("session_id", [secrets.token_urlsafe(16)])[0]
            user = get_user_from_db(session_id)
            if user and user.get("role") == "counselor":
                self.respond(200, render_teacher_dashboard(session_id))
                return
            from school_integration_html import render_school_integration_page
            self.respond(200, render_school_integration_page(session_id))
            return

        # ========== صفحه 404 ==========
        self.respond(404, "صفحه مورد نظر یافت نشد")

    def do_POST(self):
        # ========== چت بات ==========
        if self.path == "/chat":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                message = data.get("message", "")
                session_id = data.get("session_id", "default")
                message_id = data.get("message_id", str(int(time.time() * 1000)))

                response = chatbot_respond(message, session_id)
                save_conversation(session_id, message, response, "chat", 0, "neutral", None)

                self.respond(200, json.dumps({
                    "response": response,
                    "message_id": message_id
                }, ensure_ascii=False), "application/json")
            except Exception as e:
                logger.error(f"خطا در چت: {e}")
                self.respond(500, json.dumps({"response": f"خطای داخلی: {str(e)}"}), "application/json")
            return

        # ========== ذخیره نقش کاربر ==========
        elif self.path == "/save-role":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                role = data.get("role", "student")
                
                existing = get_user_from_db(session_id)
                if existing:
                    save_user_to_db(session_id, existing.get("user_code", ""), role=role)
                else:
                    save_user_to_db(session_id, generate_user_code(), role=role, consent_given=0)
                
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ذخیره نقش: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== رضایت نامه ==========
        elif self.path == "/consent":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                consent = data.get("consent", 0)

                if consent == 1:
                    existing = get_user_from_db(session_id)
                    if existing:
                        save_user_to_db(session_id, existing.get("user_code", ""), consent_given=1)
                    else:
                        save_user_to_db(session_id, generate_user_code(), consent_given=1)
                    update_consent(session_id, 1)
                    self.respond(200, json.dumps({"status": "ok"}), "application/json")
                else:
                    self.respond(200, json.dumps({"status": "declined"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در پردازش رضایت: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        # ========== ذخیره پروفایل ==========
        elif self.path == "/save-profile":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                first_name = data.get("first_name", "")
                last_name = data.get("last_name", "")
                grade_level = data.get("grade_level", "")
                email = data.get("email", "")

                existing = get_user_from_db(session_id)
                if existing:
                    save_user_to_db(session_id, existing.get("user_code", ""),
                                  name=first_name, lastname=last_name,
                                  grade_level=grade_level, email=email)
                else:
                    save_user_to_db(session_id, generate_user_code(),
                                  name=first_name, lastname=last_name,
                                  grade_level=grade_level, email=email, consent_given=1)
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== امتیازدهی به پیام ==========
        elif self.path == "/rate-message":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                message_id = data.get("message_id", "")
                rating = data.get("rating", 0)

                save_feedback(session_id, message_id, rating, "", 0, "")
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ثبت امتیاز: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== API عمومی ==========
        elif self.path == "/api/v1/ask":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                question = data.get("question", "")
                session_id = data.get("session_id", "api_user")
                response = chatbot_respond(question, session_id)
                self.respond(200, json.dumps({"answer": response, "status": "success"}, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        elif self.path == "/api/v1/feedback":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                rating = data.get("rating", 0)
                message_id = data.get("message_id", "")
                session_id = data.get("session_id", "")
                comment = data.get("comment", "")
                is_wrong = data.get("is_wrong_recommendation", 0)
                correct_track = data.get("correct_track", "")
                save_feedback(session_id, message_id, rating, comment, is_wrong, correct_track)
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        # ========== انتخاب رشته ==========
        elif self.path == "/track-submit":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                form = urllib.parse.parse_qs(raw)

                def get_str(k, d=""): return (form.get(k) or [d])[0]
                def get_int(k, d=0): return int(get_str(k, d))
                def get_float(k, d=0): return float(get_str(k, d))

                step = get_int("step", 1)
                sid = get_str("session_id")
                cur = SESSION_STORE.get(sid, {})

                if step == 1:
                    cur["firstName"] = get_str("firstName")
                    cur["lastName"] = get_str("lastName")
                    cur["age"] = get_int("age", 0)
                    cur["gradeLevel"] = get_str("gradeLevel", "هفتم-نهم")
                    cur["dominant_think"] = get_str("dominant_think", "تحلیلی")
                    cur["average_grade"] = get_float("average_grade", 15)
                    if grade_category(cur["gradeLevel"]) == "advanced":
                        cur["track"] = get_str("track", "")
                    SESSION_STORE[sid] = cur
                    self.respond(200, render_track_form_page(sid, 2, cur))
                else:
                    grade = cur.get("gradeLevel", "هفتم-نهم")
                    track = cur.get("track", "")
                    if grade_category(grade) == "basic":
                        subjects = SUBJECTS_BY_LEVEL.get(grade, SUBJECTS_BY_LEVEL["هفتم-نهم"])
                    else:
                        subjects = SUBJECTS_BY_TRACK.get(track, [])

                    subject_scores = {}
                    subject_interests = {}
                    for sub in subjects:
                        k = safe_key(sub)
                        u = get_float(f"{k}__understanding", 3)
                        p = get_float(f"{k}__performance", 3)
                        i = get_float(f"{k}__interest", 3)
                        from track_risk_logic import compute_subject_score_full
                        sd = {"understanding": u, "performance": p, "interest": i}
                        subject_scores[sub] = compute_subject_score_full(sd)
                        subject_interests[sub] = i

                    all_tracks = recommend_tracks_detailed(cur, subject_scores)
                    strengths_weaknesses = {tr: track_strengths_weaknesses(tr, subject_scores) for tr in TRACKS}
                    career_by_track = {}
                    for tr in TRACKS:
                        career_by_track[tr] = compute_career_match_detailed(tr, subject_scores, subject_interests, cur.get("dominant_think", "تحلیلی"))

                    user_code = get_user_from_db(sid).get("user_code", sid[:8]) if get_user_from_db(sid) else sid[:8]

                    result = {
                        "user_code": user_code, "firstName": cur.get("firstName", ""),
                        "lastName": cur.get("lastName", ""), "gradeLevel": grade,
                        "dominant_think": cur.get("dominant_think", "تحلیلی"),
                        "all_tracks": all_tracks, "strengths_weaknesses": strengths_weaknesses,
                        "career_by_track": career_by_track, "subject_interests": subject_interests,
                    }
                    token = hashlib.sha256((json.dumps(result) + str(time.time())).encode()).hexdigest()[:16]
                    RESULT_STORE[token] = result

                    for t in all_tracks:
                        save_track_analysis(sid, t["track"], t["score"], t["ability_score"],
                                           t["interest_score"], t["think_score"],
                                           t["future_score"], t.get("grade_score", 0))

                    self.send_response(303)
                    self.send_header("Location", f"/track-result?token={token}")
                    self.end_headers()
            except Exception as e:
                logger.error(f"خطا در track-submit: {e}")
                self.respond(500, f"خطا: {str(e)}")

        # ========== پیش‌بینی افت ==========
        elif self.path == "/risk-submit":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                form = urllib.parse.parse_qs(raw)

                def get_str(k, d=""): return (form.get(k) or [d])[0]
                def get_float(k, d=0): return float(get_str(k, d))

                sid = get_str("session_id")
                cur = SESSION_STORE.get(sid, {})

                cur["firstName"] = get_str("firstName")
                cur["lastName"] = get_str("lastName")
                cur["age"] = get_float("age", 0)
                cur["gradeLevel"] = get_str("gradeLevel", "هفتم-نهم")
                cur["study_hours_rating"] = get_float("study_hours_rating", 3)
                cur["study_days_week_rating"] = get_float("study_days_week_rating", 3)
                cur["study_mode"] = get_str("study_mode", "منظم")
                cur["distract_rating"] = get_float("distract_rating", 3)
                cur["has_review"] = get_str("has_review", "دارم (منظم)")
                cur["start_days_before_exam"] = get_str("start_days_before_exam", "30+")
                cur["sleep_status"] = get_str("sleep_status", "خوب")
                cur["stress_rating"] = get_float("stress_rating", 3)
                cur["main_weakness_area"] = get_str("main_weakness_area", "محاسباتی / تمرین")
                cur["can_execute_plan"] = get_float("can_execute_plan", 3)
                cur["has_tutor"] = get_str("has_tutor", "ندارم")
                cur["tutor_sessions_week"] = get_float("tutor_sessions_week", 0)
                cur["family_support"] = get_str("family_support", "خوب")
                cur["previous_fail"] = get_str("previous_fail", "ندارم")
                cur["test_anxiety"] = get_float("test_anxiety", 3)

                risk_data = compute_risk_fall_detailed(cur)
                breakdown = risk_breakdown_detailed(cur)

                grade = cur["gradeLevel"]
                track = cur.get("track", "")
                if grade_category(grade) == "basic":
                    subjects = SUBJECTS_BY_LEVEL.get(grade, SUBJECTS_BY_LEVEL["هفتم-نهم"])
                else:
                    subjects = SUBJECTS_BY_TRACK.get(track, [])

                from track_risk_logic import normalize_rating
                subject_scores = {}
                for sub in subjects:
                    k = safe_key(sub)
                    u = get_float(f"{k}__understanding", 3) if f"{k}__understanding" in form else 3
                    p = get_float(f"{k}__performance", 3) if f"{k}__performance" in form else 3
                    i = get_float(f"{k}__interest", 3) if f"{k}__interest" in form else 3
                    subject_scores[sub] = {"ability_score": (normalize_rating(u) + normalize_rating(p)) / 2, "interest_score": normalize_rating(i)}

                risky = top_risky_subjects_detailed(subject_scores, risk_data)
                risky_names = [r["subject"] for r in risky]
                plan = anti_fall_plan_detailed(risk_data["bucket"], risky_names, grade)
                resources = get_recommended_resources(risky_names[:3])
                tips = get_study_tips_by_risk(risk_data["bucket"])

                user_code = get_user_from_db(sid).get("user_code", sid[:8]) if get_user_from_db(sid) else sid[:8]

                result = {
                    "user_code": user_code, "firstName": cur["firstName"],
                    "lastName": cur["lastName"], "gradeLevel": grade,
                    "risk_fall": {
                        "risk_data": risk_data, "breakdown": breakdown,
                        "risky_subjects": risky, "plan": plan,
                        "resources": resources, "tips": tips
                    }
                }
                token = hashlib.sha256((json.dumps(result) + str(time.time())).encode()).hexdigest()[:16]
                RESULT_STORE[token] = result

                save_risk_analysis(sid, risk_data["risk_percent"], risk_data["bucket"],
                                  risk_data["advice"], risk_data.get("study_mode", ""),
                                  risk_data.get("sleep_status", ""), risk_data.get("stress_level", 0))
                save_study_plan(sid, plan)

                if risk_data["risk_percent"] >= 55:
                    save_alert(sid, "risk", risk_data["alert_level"],
                              f"⚠️ هشدار! ریسک افت تحصیلی شما {risk_data['risk_percent']}% است. لطفاً برنامه ضد افت را دنبال کنید.")

                self.send_response(303)
                self.send_header("Location", f"/risk-result?token={token}")
                self.end_headers()
            except Exception as e:
                logger.error(f"خطا در risk-submit: {e}")
                self.respond(500, f"خطا: {str(e)}")

        # ========== ذخیره آزمون هالند ==========
        elif self.path == "/save-holland-test":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                scores = data.get("scores", [])
                primary_type = data.get("primary_type", "")
                percentages = data.get("percentages", [])

                from database import save_holland_result
                save_holland_result(session_id, scores, primary_type, percentages)

                gamification = GamificationSystem(session_id)
                gamification.check_achievements()
                save_conversation(session_id, "آزمون هالند", f"نتیجه: {primary_type}", "holland_test", 95, "neutral")
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در save-holland-test: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== ذخیره پومودورو ==========
        elif self.path == "/save-pomodoro":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                completed = data.get("completed_sessions", 0)
                save_conversation(session_id, "پومودورو", f"تکمیل {completed} جلسه", "pomodoro", 90, "positive")
                add_points_to_user(session_id, completed * 5, f"پومودورو: {completed} جلسه")
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در save-pomodoro: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== اهداف SMART ==========
        elif self.path == "/create-goal":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                result = create_goal(session_id, data)
                if result:
                    add_points_to_user(session_id, 10, "ایجاد هدف جدید SMART")
                self.respond(200, json.dumps({"status": "ok" if result else "error"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ایجاد هدف: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        elif self.path == "/update-goal":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                update_goal(data)
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در به‌روزرسانی هدف: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        elif self.path == "/update-goal-progress":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                update_goal_progress(data)
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در به‌روزرسانی پیشرفت: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        elif self.path == "/delete-goal":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                delete_goal(data.get("goal_id"), data.get("session_id"))
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در حذف هدف: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        # ========== تولید سوالات ==========
        elif self.path == "/generate-questions":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                questions = generate_questions(
                    subject=data.get("subject", "ریاضی"),
                    grade_level=data.get("grade_level", "هفتم-نهم"),
                    difficulty=data.get("difficulty", "متوسط"),
                    question_type=data.get("question_type", "test"),
                    count=min(int(data.get("count", 5)), 20)
                )
                self.respond(200, json.dumps({"questions": questions}, ensure_ascii=False), "application/json")
            except Exception as e:
                logger.error(f"خطا در تولید سوالات: {e}")
                self.respond(500, json.dumps({"error": str(e)}), "application/json")
            return

        elif self.path == "/save-exam-result":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                score = data.get("score", 0)
                session_id = data.get("session_id", "")
                save_exam_result(session_id, data)
                if score >= 80:
                    add_points_to_user(session_id, 20, f"نمره خوب در آزمون {data.get('subject', '')}")
                elif score >= 50:
                    add_points_to_user(session_id, 10, f"شرکت در آزمون {data.get('subject', '')}")
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ذخیره نتیجه: {e}")
                self.respond(500, json.dumps({"status": "error"}), "application/json")
            return

        # ========== چالش‌های روزانه ==========
        elif self.path == "/complete-challenge":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                challenge_id = data.get("challenge_id", "")
                level = data.get("level", "آسان")

                result = complete_user_challenge(session_id, challenge_id, level)

                if result.get("success"):
                    update_challenge_completed(session_id)
                    gamification = GamificationSystem(session_id)
                    new_achievements = gamification.check_achievements()
                    self.respond(200, json.dumps({
                        "status": "ok",
                        "points": result.get("points", 0),
                        "new_achievements": new_achievements
                    }), "application/json")
                else:
                    self.respond(200, json.dumps({
                        "status": "error",
                        "message": result.get("message", "خطا در ثبت چالش")
                    }), "application/json")
            except Exception as e:
                logger.error(f"خطا در تکمیل چالش: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        elif self.path == "/get-certificate":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                from challenges import get_weekly_certificate
                result = get_weekly_certificate(session_id)
                self.respond(200, json.dumps(result, ensure_ascii=False), "application/json")
            except Exception as e:
                logger.error(f"خطا در دریافت گواهی: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== رویدادهای تقویم ==========
        elif self.path == "/add-calendar-event":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                title = data.get("title", "")
                date_str = data.get("date", "")
                description = data.get("description", "")

                add_user_event(session_id, title, date_str, description)
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در افزودن رویداد: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== گروه‌های مطالعه ==========
        elif self.path == "/api/groups/create":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                name = data.get("name", "")
                description = data.get("description", "")
                is_private = data.get("is_private", 0)

                from datetime import datetime

                group_code = secrets.token_hex(4).upper()
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO study_groups (name, description, owner_id, created_at, group_code, is_private)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, description, session_id, datetime.now().isoformat(), group_code, is_private))
                group_id = cursor.lastrowid
                cursor.execute('''
                    INSERT INTO group_members (group_id, user_id, role, joined_at, points_contributed)
                    VALUES (?, ?, 'owner', ?, 0)
                ''', (group_id, session_id, datetime.now().isoformat()))
                conn.commit()
                conn.close()

                gamification = GamificationSystem(session_id)
                gamification.increment_stat("groups_created")
                add_points_to_user(session_id, 50, "ایجاد گروه مطالعه")

                self.respond(200, json.dumps({"status": "ok", "group_id": group_id, "group_code": group_code}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ایجاد گروه: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        elif self.path == "/api/groups/join":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                group_id = data.get("group_id", 0)

                result = join_group(session_id, group_id)
                if result.get("status") == "ok":
                    add_points_to_user(session_id, 10, "پیوستن به گروه مطالعه")
                self.respond(200, json.dumps(result), "application/json")
            except Exception as e:
                logger.error(f"خطا در پیوستن به گروه: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        elif self.path == "/api/groups/join-by-code":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                group_code = data.get("group_code", "")

                result = join_group_by_code(session_id, group_code)
                if result.get("status") == "ok":
                    add_points_to_user(session_id, 10, "پیوستن به گروه با کد")
                self.respond(200, json.dumps(result), "application/json")
            except Exception as e:
                logger.error(f"خطا در پیوستن با کد: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        elif self.path == "/api/groups/send-message":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                group_id = data.get("group_id", 0)
                message = data.get("message", "")

                from datetime import datetime

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO group_messages (group_id, user_id, message, sent_at, is_read)
                    VALUES (?, ?, ?, ?, 0)
                ''', (group_id, session_id, message[:1000], datetime.now().isoformat()))
                conn.commit()
                conn.close()

                gamification = GamificationSystem(session_id)
                gamification.increment_stat("messages_sent")
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در ارسال پیام: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== حذف گروه ==========
        elif self.path == "/api/groups/delete":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                group_id = data.get("group_id", 0)
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('SELECT owner_id FROM study_groups WHERE id = ?', (group_id,))
                row = cursor.fetchone()
                if row and row[0] == session_id:
                    cursor.execute('DELETE FROM group_messages WHERE group_id = ?', (group_id,))
                    cursor.execute('DELETE FROM group_challenges WHERE group_id = ?', (group_id,))
                    cursor.execute('DELETE FROM group_members WHERE group_id = ?', (group_id,))
                    cursor.execute('DELETE FROM study_groups WHERE id = ?', (group_id,))
                    conn.commit()
                    conn.close()
                    self.respond(200, json.dumps({"status": "ok"}), "application/json")
                else:
                    conn.close()
                    self.respond(200, json.dumps({"status": "error", "message": "شما اجازه حذف این گروه را ندارید"}), "application/json")
            except Exception as e:
                logger.error(f"خطا در حذف گروه: {e}")
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== پیش‌بینی با ML ==========
        elif self.path == "/api/ml-predict-pure":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                features = data.get("features", {})
                predictor = get_predictor()
                result = predictor.predict(features)
                self.respond(200, json.dumps(result, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False), "application/json")
            return

        # ========== خلاصه‌ساز هوشمند ==========
        elif self.path == "/api/smart-summarize":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                text = data.get("text", "")

                summary = SmartSummarizer.summarize(text, num_sentences=5)
                key_points = SmartSummarizer.extract_key_points(text, num_points=5)
                flashcards = SmartSummarizer.generate_flashcards(text, num_cards=3)

                self.respond(200, json.dumps({
                    "summary": summary, "key_points": key_points, "flashcards": flashcards
                }, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"error": str(e)}, ensure_ascii=False), "application/json")
            return

        # ========== برنامه‌ریز هوشمند ==========
        elif self.path == "/api/dynamic-planner":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                days_input = data.get("days_input", "5")
                subject = data.get("subject", "ریاضی")
                weak_chapters = data.get("weak_chapters", [])
                strong_chapters = data.get("strong_chapters", [])

                planner = DynamicStudyPlanner(session_id)
                plan = planner.generate_plan(days_input, subject, weak_chapters, strong_chapters)

                if "error" in plan:
                    self.respond(200, json.dumps({"error": plan["error"]}, ensure_ascii=False), "application/json")
                else:
                    add_points_to_user(session_id, 5, "استفاده از برنامه‌ریز هوشمند")
                    self.respond(200, json.dumps(plan, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"error": str(e)}, ensure_ascii=False), "application/json")
            return
        
        elif self.path == "/api/save-career-interest":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                career_key = data.get("career", "")
        
                from adaptive_recommender import get_recommender
                recommender = get_recommender(session_id)
                recommender.log_interaction(career_key, "save")
        
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== ثبت بازخورد توصیه‌گر ==========
        elif self.path == "/api/recommendation-feedback":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                item = data.get("item", "")
                clicked = data.get("clicked", False)
                saved = data.get("saved", False)
                liked = data.get("liked", False)
        
                from adaptive_recommender_advanced import log_recommendation_feedback
                log_recommendation_feedback(session_id, item, clicked, saved, liked)
        
                self.respond(200, json.dumps({"status": "ok"}), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"status": "error", "message": str(e)}), "application/json")
            return

        # ========== همگام‌سازی با سامانه مدرسه ==========
        elif self.path == "/api/school/sync":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                session_id = data.get("session_id", "")
                national_code = data.get("national_code", "")
                api_key = data.get("api_key", "")
        
                from external_api import SecureSchoolAPIConnector
                connector = SecureSchoolAPIConnector()
                result = connector.sync_student_data(national_code, api_key, session_id)
        
                self.respond(200, json.dumps(result, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), "application/json")
            return

        # ========== احراز هویت با سامانه مدرسه ==========
        elif self.path == "/api/school/auth":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                api_key = data.get("api_key", "")

                from external_api import SecureSchoolAPIConnector
                connector = SecureSchoolAPIConnector()
                result = connector.authenticate(api_key)

                self.respond(200, json.dumps(result, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), "application/json")
            return

        # ========== دریافت اطلاعات دانش‌آموز ==========
        elif self.path == "/api/school/student":
            try:
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length).decode("utf-8")
                data = json.loads(raw)
                national_code = data.get("national_code", "")
                access_token = data.get("access_token", "")
        
                from external_api import SecureSchoolAPIConnector
                connector = SecureSchoolAPIConnector()
                result = connector.get_student_info(national_code, access_token)
        
                self.respond(200, json.dumps(result, ensure_ascii=False), "application/json")
            except Exception as e:
                self.respond(500, json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), "application/json")
            return

        else:
            self.respond(404, "Not Found")
    def do_GET_student_profile(self, student_id, session_id):
        """نمایش پروفایل دانش‌آموز برای مشاور"""
        try:
            # بررسی نقش مشاور
            user = get_user_from_db(session_id)
            if not user or user.get("role") != "counselor":
                self.respond(403, "<h3>⛔ دسترسی غیرمجاز. فقط مشاوران می‌توانند این صفحه را ببینند.</h3><a href='/'>بازگشت</a>")
                return
            
            # بارگذاری داده‌های دانش‌آموز
            student_user = get_user_from_db(student_id)
            if not student_user:
                self.respond(404, f"<h3>❌ دانش‌آموز با کد {student_id} یافت نشد.</h3><a href='/teacher-dashboard?session_id={session_id}'>بازگشت به لیست</a>")
                return
            
            # ساخت صفحه HTML ساده
            html = f'''
            <!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <title>پروفایل دانش‌آموز - مسیرینو</title>
                <style>
                    body {{
                        font-family: Tahoma, sans-serif;
                        background: linear-gradient(135deg, #0f0c29, #302b63);
                        color: white;
                        padding: 50px;
                        direction: rtl;
                    }}
                    .card {{
                        background: rgba(255,255,255,0.1);
                        border-radius: 20px;
                        padding: 30px;
                        max-width: 600px;
                        margin: 0 auto;
                    }}
                    h1 {{ color: #ff6584; }}
                    .btn {{
                        display: inline-block;
                        padding: 10px 20px;
                        background: #6c63ff;
                        color: white;
                        text-decoration: none;
                        border-radius: 25px;
                        margin-top: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>📘 پروفایل دانش‌آموز</h1>
                    <p><strong>🆔 کد:</strong> {student_id}</p>
                    <p><strong>👤 نام:</strong> {student_user.get('name', 'نامشخص')}</p>
                    <p><strong>📚 پایه:</strong> {student_user.get('grade_level', 'نامشخص')}</p>
                    <p><strong>📧 ایمیل:</strong> {student_user.get('email', 'ندارد')}</p>
                    <p><strong>🎭 نقش:</strong> {student_user.get('role', 'دانش‌آموز')}</p>
                    <hr>
                    <a href="/teacher-dashboard?session_id={session_id}" class="btn">← بازگشت به لیست</a>
                    <a href="/?session_id={session_id}" class="btn" style="background:#ff6584;">🏠 صفحه اصلی</a>
                </div>
            </body>
            </html>
            '''
            self.respond(200, html)
        except Exception as e:
            self.respond(500, f"خطا: {str(e)}")

def run():
    init_db()
    cleanup_old_data()

    try:
        backup_database()
        get_predictor()
    except:
        pass

    server = HTTPServer((HOST, PORT), Handler)
    print("=" * 70)
    print("🤖 مسیرینو - مشاور هوشمند تحصیلی (نسخه کامل نهایی)")
    print("=" * 70)
    print(f"🌐 سرور در آدرس http://{HOST}:{PORT} اجرا شد")
    print("")
    print("📌 سرویس‌های موجود:")
    print(f"   • صفحه انتخاب نقش: http://{HOST}:{PORT}/role-select")
    print(f"   • صفحه اصلی دانش‌آموز: http://{HOST}:{PORT}/")
    print(f"   • داشبورد مشاور: http://{HOST}:{PORT}/teacher-dashboard")
    print(f"   • چت بات با قابلیت صوتی: http://{HOST}:{PORT}/chat-only")
    print(f"   • انتخاب رشته تخصصی: http://{HOST}:{PORT}/track-start")
    print(f"   • پیش‌بینی افت با 12 فاکتور: http://{HOST}:{PORT}/risk-start")
    print(f"   • آزمون شخصیت هالند (45 سوال): http://{HOST}:{PORT}/holland-test")
    print(f"   • اهداف SMART: http://{HOST}:{PORT}/smart-goals")
    print(f"   • چالش‌های روزانه + گواهی: http://{HOST}:{PORT}/daily-challenges")
    print(f"   • گروه‌های مطالعه (با کد دعوت و حذف): http://{HOST}:{PORT}/groups")
    print(f"   • تقویم آموزشی شمسی: http://{HOST}:{PORT}/educational-calendar")
    print(f"   • مسیرشو (نقشه راه شغلی): http://{HOST}:{PORT}/path-finder")
    print(f"   • پیش‌بینی نمره با AI: http://{HOST}:{PORT}/ml-predictor")
    print(f"   • برنامه‌ریز هوشمند: http://{HOST}:{PORT}/dynamic-planner")
    print(f"   • خلاصه‌ساز هوشمند: http://{HOST}:{PORT}/smart-summarizer")
    print(f"   • بازی‌های آموزشی (8 بازی): http://{HOST}:{PORT}/educational-games")
    print(f"   • پروفایل و افتخارات: http://{HOST}:{PORT}/gamification-profile")
    print(f"   • تایمر پومودورو: http://{HOST}:{PORT}/pomodoro")
    print(f"   • تولید سوال امتحانی: http://{HOST}:{PORT}/exam-questions")
    print(f"   • داشبورد مدیریت: http://{HOST}:{PORT}/admin")
    print(f"   • دفترچه راهنما: http://{HOST}:{PORT}/manual")
    print(f"   • نسخه React SPA: http://{HOST}:{PORT}/react-app")
    print(f"   • مشاهده پروفایل دانش‌آموز (مشاور): http://{HOST}:{PORT}/consultant/student/[user_id]")
    print("")
    print("🎯 APIهای عمومی:")
    print(f"   • POST /api/v1/ask - پرسش از چت بات")
    print(f"   • POST /api/v1/feedback - ثبت بازخورد")
    print(f"   • GET /api/v1/compare - مقایسه با کاربران مشابه")
    print("")
    print("✨ قابلیت‌های ویژه:")
    print("   ✅ سیستم انتخاب نقش (دانش‌آموز / مشاور)")
    print("   ✅ تفکیک کامل دسترسی: مشاور فقط داشبورد معلم را می‌بیند")
    print("   ✅ چت بات با تشخیص صدا، خواندن پیام و امتیازدهی ستاره‌ای")
    print("   ✅ انتخاب رشته با 5 معیار (توانایی، علاقه، سبک، آینده، معدل)")
    print("   ✅ پیش‌بینی افت با 12 فاکتور + برنامه ضد افت + منابع")
    print("   ✅ آزمون شخصیت هالند (45 سوال استاندارد)")
    print("   ✅ تایمر پومودورو با تکنیک 25/5 دقیقه")
    print("   ✅ اهداف SMART با مدیریت پیشرفت")
    print("   ✅ چالش‌های روزانه در 3 سطح با گواهی هفتگی")
    print("   ✅ گروه‌های مطالعه با چت، کد دعوت، و حذف گروه")
    print("   ✅ تقویم آموزشی شمسی با رویدادهای شخصی")
    print("   ✅ مسیرشو - نقشه راه 5 ساله شغلی")
    print("   ✅ پیش‌بینی نمره با مدل Random Forest از صفر")
    print("   ✅ گیمیفیکیشن کامل (امتیاز، سطح، مدال، استریک)")
    print("   ✅ 8 بازی آموزشی مختلف (فلش‌کارت، مسابقه، حافظه و ...)")
    print("   ✅ خلاصه‌ساز هوشمند درس + فلش‌کارت")
    print("   ✅ برنامه‌ریز هوشمند بر اساس زمان امتحان")
    print("   ✅ قابلیت ضبط صدا و خواندن پیام‌ها")
    print("   ✅ مشاهده پروفایل دانش‌آموز برای مشاور (جدید)")
    print("   ✅ تم شب/روز، دیتابیس کامل، گزارش، پشتیبان، لاگ")
    print("=" * 70)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 سرور متوقف شد")
        server.shutdown()

if __name__ == "__main__":
    run()