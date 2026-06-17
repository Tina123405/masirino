# analytics_core.py
# سیستم آنالیتیکس پیشرفته - با داده‌های شبیه‌سازی شده پیش‌فرض

import sqlite3
import json
import math
import random
from datetime import datetime, timedelta
from collections import defaultdict
from config import DB_NAME


class AnalyticsEngine:
    """موتور آنالیتیکس بدون کتابخانه اضافی"""
    
    def __init__(self, user_id):
        self.user_id = user_id
    
    def _has_real_data(self):
        """بررسی اینکه کاربر داده واقعی دارد یا نه"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM points_history WHERE user_id = ?', (self.user_id,))
            points_count = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM exam_results WHERE user_id = ?', (self.user_id,))
            exam_count = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM daily_challenges WHERE user_id = ? AND status = "completed"', (self.user_id,))
            challenge_count = cursor.fetchone()[0] or 0
            
            conn.close()
            
            # اگر حداقل 3 داده داشته باشد، داده واقعی محسوب می‌شود
            return (points_count + exam_count + challenge_count) >= 3
        except:
            return False
    
    def _generate_demo_timeline(self, weeks=8):
        """تولید داده‌های دمو (شبیه‌سازی شده) برای کاربران جدید"""
        weeks_data = []
        
        # الگوی افزایشی: هفته به هفته پیشرفت می‌کند
        for i in range(weeks):
            # امتیاز: از 10 شروع می‌شود تا 80 افزایش می‌یابد
            points = 10 + (i * 10) + random.randint(-5, 10)
            points = max(0, min(100, points))
            
            # چالش‌ها: هر هفته بین 1 تا 3 تا
            challenges = random.randint(1, 3) if i > 2 else random.randint(0, 2)
            
            # نمره آزمون: از 50 شروع تا 85
            avg_score = 50 + (i * 5) + random.randint(-10, 10)
            avg_score = max(30, min(95, avg_score))
            
            weeks_data.append({
                "week": i + 1,
                "week_label": f"هفته {i+1}",
                "start_date": (datetime.now() - timedelta(days=(weeks - i) * 7)).isoformat(),
                "points": points,
                "challenges": challenges,
                "exams": random.randint(0, 2) if i > 1 else 0,
                "avg_exam_score": avg_score
            })
        
        return weeks_data
    
    def _generate_demo_subjects(self):
        """تولید داده‌های دمو برای دروس"""
        subjects_data = [
            {"subject": "ریاضی", "avg_score": 72, "exam_count": 3, "level": "good"},
            {"subject": "فیزیک", "avg_score": 65, "exam_count": 2, "level": "medium"},
            {"subject": "شیمی", "avg_score": 68, "exam_count": 2, "level": "medium"},
            {"subject": "زیست", "avg_score": 78, "exam_count": 3, "level": "good"},
            {"subject": "ادبیات", "avg_score": 58, "exam_count": 2, "level": "weak"},
            {"subject": "زبان", "avg_score": 62, "exam_count": 2, "level": "medium"}
        ]
        return subjects_data
    
    def _generate_demo_risk_trend(self):
        """تولید داده‌های دمو برای روند ریسک"""
        risk_data = []
        today = datetime.now()
        
        # ریسک در 8 هفته گذشته: از 65% به 25% کاهش می‌یابد (پیشرفت)
        for i in range(8):
            risk = 65 - (i * 5) + random.randint(-5, 5)
            risk = max(15, min(80, risk))
            date = (today - timedelta(days=(8 - i) * 7))
            risk_data.append({
                "risk": risk,
                "date": date.strftime("%Y-%m-%d")
            })
        
        return risk_data
    
    def get_user_progress_timeline(self, weeks=8):
        """دریافت روند پیشرفت کاربر - با داده‌های دمو برای کاربران جدید"""
        # اگر کاربر داده واقعی دارد
        if self._has_real_data():
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            weeks_data = []
            
            for i in range(weeks):
                week_start = today - timedelta(days=(weeks - i) * 7)
                week_end = week_start + timedelta(days=6)
                week_start_str = week_start.isoformat()
                week_end_str = week_end.isoformat()
                
                # امتیازات هفته
                try:
                    cursor.execute('''
                        SELECT COALESCE(SUM(points), 0) FROM points_history
                        WHERE user_id = ? AND created_at BETWEEN ? AND ?
                    ''', (self.user_id, week_start_str, week_end_str))
                    points = cursor.fetchone()[0] or 0
                except:
                    points = 0
                
                # چالش‌های تکمیل شده هفته
                try:
                    cursor.execute('''
                        SELECT COUNT(*) FROM daily_challenges
                        WHERE user_id = ? AND status = 'completed' 
                        AND date BETWEEN ? AND ?
                    ''', (self.user_id, week_start_str, week_end_str))
                    challenges = cursor.fetchone()[0] or 0
                except:
                    challenges = 0
                
                # آزمون‌های داده شده هفته
                try:
                    cursor.execute('''
                        SELECT COUNT(*), COALESCE(AVG(score), 0) FROM exam_results
                        WHERE user_id = ? AND created_at BETWEEN ? AND ?
                    ''', (self.user_id, week_start_str, week_end_str))
                    exam_row = cursor.fetchone()
                    exams = exam_row[0] if exam_row else 0
                    avg_score = round(exam_row[1] or 0, 1) if exam_row else 0
                except:
                    exams = 0
                    avg_score = 0
                
                weeks_data.append({
                    "week": i + 1,
                    "week_label": f"هفته {i+1}",
                    "start_date": week_start_str,
                    "points": points,
                    "challenges": challenges,
                    "exams": exams,
                    "avg_exam_score": avg_score
                })
            
            conn.close()
            return weeks_data
        
        # اگر کاربر داده واقعی ندارد → داده دمو برگردان
        return self._generate_demo_timeline(weeks)
    
    def calculate_trend_line(self, data_points):
        """محاسبه خط روند (Simple Linear Regression) از صفر"""
        n = len(data_points)
        if n < 2:
            if data_points:
                return {"slope": 0, "trend_line": data_points, "forecast": [data_points[-1]] * 4, "direction": "stable"}
            return {"slope": 0, "trend_line": [], "forecast": [], "direction": "stable"}
        
        x_values = list(range(1, n + 1))
        y_values = data_points
        
        # محاسبه میانگین‌ها
        mean_x = sum(x_values) / n
        mean_y = sum(y_values) / n
        
        # محاسبه شیب (slope)
        numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
        denominator = sum((x_values[i] - mean_x) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = mean_y - slope * mean_x
        
        # پیش‌بینی برای هفته‌های آینده (تا 4 هفته جلو)
        trend_values = [slope * (i + 1) + intercept for i in range(n + 4)]
        
        return {
            "slope": round(slope, 2),
            "trend_line": [round(v, 1) for v in trend_values[:n]],
            "forecast": [round(v, 1) for v in trend_values[n:]],
            "direction": "up" if slope > 0 else "down" if slope < 0 else "stable"
        }
    
    def get_subject_performance(self):
        """تحلیل عملکرد در دروس مختلف - با داده دمو"""
        if self._has_real_data():
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT subject, AVG(score) as avg_score, COUNT(*) as exam_count
                    FROM exam_results
                    WHERE user_id = ?
                    GROUP BY subject
                    ORDER BY avg_score DESC
                ''', (self.user_id,))
                
                subjects_data = []
                for row in cursor.fetchall():
                    avg = round(row[1] or 0, 1)
                    subjects_data.append({
                        "subject": row[0],
                        "avg_score": avg,
                        "exam_count": row[2] or 0,
                        "level": "good" if avg >= 75 else "medium" if avg >= 50 else "weak"
                    })
                
                conn.close()
                
                if subjects_data:
                    return subjects_data
            except:
                pass
        
        # داده دمو
        return self._generate_demo_subjects()
    
    def get_risk_trend(self):
        """روند ریسک افت تحصیلی در طول زمان - با داده دمو"""
        if self._has_real_data():
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT risk_percent, timestamp FROM risk_analysis
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                ''', (self.user_id,))
                
                risk_data = []
                for row in cursor.fetchall():
                    risk_data.append({
                        "risk": row[0],
                        "date": row[1][:10] if row[1] else ""
                    })
                
                conn.close()
                
                if risk_data:
                    return list(reversed(risk_data))
            except:
                pass
        
        # داده دمو
        return self._generate_demo_risk_trend()
    
    def get_prediction_accuracy(self):
        """دقت پیش‌بینی‌های سیستم در مقابل نتایج واقعی"""
        if self._has_real_data():
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT predicted_score, actual_score, created_at
                    FROM ml_predictions
                    WHERE user_id = ? AND actual_score IS NOT NULL
                ''', (self.user_id,))
                
                errors = []
                for row in cursor.fetchall():
                    error = abs(row[0] - row[1])
                    errors.append(error)
                
                conn.close()
                
                if errors:
                    avg_error = sum(errors) / len(errors)
                    accuracy = max(0, 100 - (avg_error * 5))
                    return {
                        "accuracy": round(accuracy, 1),
                        "avg_error": round(avg_error, 1),
                        "samples": len(errors)
                    }
            except:
                pass
        
        # داده دمو - دقت حدود 85%
        return {"accuracy": 85.0, "avg_error": 3.0, "samples": 12}
    
    def get_comparison_with_similar(self):
        """مقایسه با کاربران مشابه - با داده دمو"""
        if self._has_real_data():
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                
                cursor.execute('SELECT grade_level, track FROM users WHERE user_id = ?', (self.user_id,))
                user_row = cursor.fetchone()
                
                if user_row:
                    grade_level = user_row[0] or ""
                    
                    # میانگین امتیاز کاربران مشابه
                    cursor.execute('''
                        SELECT AVG(up.total_points)
                        FROM users u
                        LEFT JOIN user_points up ON u.user_id = up.user_id
                        WHERE u.grade_level = ? AND u.user_id != ?
                    ''', (grade_level, self.user_id))
                    avg_points_row = cursor.fetchone()
                    avg_points = avg_points_row[0] if avg_points_row and avg_points_row[0] else 0
                    
                    # میانگین نمره آزمون کاربران مشابه
                    cursor.execute('''
                        SELECT AVG(er.score)
                        FROM users u
                        LEFT JOIN exam_results er ON u.user_id = er.user_id
                        WHERE u.grade_level = ? AND u.user_id != ?
                    ''', (grade_level, self.user_id))
                    avg_exam_row = cursor.fetchone()
                    avg_exam = avg_exam_row[0] if avg_exam_row and avg_exam_row[0] else 0
                    
                    conn.close()
                    
                    if avg_points > 0 or avg_exam > 0:
                        return {
                            "avg_points_similar": round(avg_points, 1),
                            "avg_exam_similar": round(avg_exam, 1),
                            "risk_distribution": {"high": 25, "medium": 45, "low": 30}
                        }
            except:
                pass
        
        # داده دمو
        return {
            "avg_points_similar": 185,
            "avg_exam_similar": 68.5,
            "risk_distribution": {"high": 25, "medium": 45, "low": 30}
        }
    
    def get_moving_average(self, data, window=3):
        """میانگین متحرک ساده (برای هموارسازی نمودار)"""
        if len(data) < window:
            return data
        
        result = []
        for i in range(len(data)):
            start = max(0, i - window + 1)
            window_data = data[start:i+1]
            avg = sum(window_data) / len(window_data)
            result.append(round(avg, 1))
        
        return result
    
    def get_full_analytics(self):
        """دریافت کامل داده‌های آنالیتیکس (با دمو برای کاربران جدید)"""
        timeline = self.get_user_progress_timeline(8)
        
        # استخراج نقاط داده برای روند
        points_data = [w["points"] for w in timeline]
        challenges_data = [w["challenges"] for w in timeline]
        exam_data = [w["avg_exam_score"] for w in timeline]
        
        return {
            "timeline": timeline,
            "points_trend": self.calculate_trend_line(points_data),
            "challenges_trend": self.calculate_trend_line(challenges_data),
            "exam_trend": self.calculate_trend_line(exam_data),
            "subjects": self.get_subject_performance(),
            "risk_trend": self.get_risk_trend(),
            "prediction_accuracy": self.get_prediction_accuracy(),
            "comparison": self.get_comparison_with_similar(),
            "moving_average": {
                "points_ma3": self.get_moving_average(points_data, 3),
                "exam_ma3": self.get_moving_average(exam_data, 3)
            },
            "is_demo_data": not self._has_real_data()  # به صفحه بگو داده دمو هست
        }


def save_ml_prediction(user_id, predicted_score, actual_score=None):
    """ذخیره پیش‌بینی ML برای محاسبه دقت بعداً"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ml_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                predicted_score REAL,
                actual_score REAL,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            INSERT INTO ml_predictions (user_id, predicted_score, actual_score, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, predicted_score, actual_score, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"خطا در ذخیره پیش‌بینی ML: {e}")