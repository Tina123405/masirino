# gamification.py
# سیستم گیمیفیکیشن کامل برای مسیرینو

import json
import sqlite3
from datetime import datetime, timedelta
from config import DB_NAME

class GamificationSystem:
    """سیستم بازی‌وارسازی پیشرفته"""
    
    # سطوح و امتیازات مورد نیاز
    LEVELS = {
        1: {"name": "شروع‌کننده", "icon": "🌱", "min_points": 0, "color": "#a0a0a0"},
        2: {"name": "تلاشگر", "icon": "📚", "min_points": 50, "color": "#cd7f32"},
        3: {"name": "برنزی", "icon": "🥉", "min_points": 100, "color": "#cd7f32"},
        4: {"name": "نقره‌ای", "icon": "🥈", "min_points": 250, "color": "#c0c0c0"},
        5: {"name": "طلایی", "icon": "🥇", "min_points": 500, "color": "#ffd700"},
        6: {"name": "پلاتینیوم", "icon": "💎", "min_points": 800, "color": "#e5e4e2"},
        7: {"name": "الماسی", "icon": "💎", "min_points": 1200, "color": "#00b4d8"},
        8: {"name": "افسانه‌ای", "icon": "🏆", "min_points": 2000, "color": "#ff6b6b"},
        9: {"name": "استاد", "icon": "🎓", "min_points": 3000, "color": "#9b59b6"},
        10: {"name": "خوارزمی", "icon": "🌟", "min_points": 5000, "color": "#ff00ff"}
    }
    
    # مدال‌ها و شرایط دریافت
    ACHIEVEMENTS = {
        "first_challenge": {
            "name": "شروع کننده",
            "icon": "🎯",
            "description": "اولین چالش روزانه را انجام دادی",
            "condition": {"type": "challenges_completed", "value": 1},
            "bonus": 10
        },
        "streak_3": {
            "name": "سه روز پیاپی",
            "icon": "🔥",
            "description": "۳ روز متوالی چالش انجام دادی",
            "condition": {"type": "streak_days", "value": 3},
            "bonus": 20
        },
        "streak_7": {
            "name": "هفته طلایی",
            "icon": "⭐",
            "description": "۷ روز متوالی چالش انجام دادی",
            "condition": {"type": "streak_days", "value": 7},
            "bonus": 50
        },
        "streak_30": {
            "name": "ماه بی‌نظیر",
            "icon": "🏅",
            "description": "۳۰ روز متوالی چالش انجام دادی",
            "condition": {"type": "streak_days", "value": 30},
            "bonus": 200
        },
        "perfect_exam": {
            "name": "نابغه",
            "icon": "🧠",
            "description": "در یک آزمون نمره ۱۰۰ گرفتی",
            "condition": {"type": "exam_score", "value": 100},
            "bonus": 100
        },
        "points_100": {
            "name": "جمع‌کننده امتیاز",
            "icon": "💰",
            "description": "۱۰۰ امتیاز جمع کردی",
            "condition": {"type": "total_points", "value": 100},
            "bonus": 50
        },
        "points_500": {
            "name": "میلیونر امتیاز",
            "icon": "💵",
            "description": "۵۰۰ امتیاز جمع کردی",
            "condition": {"type": "total_points", "value": 500},
            "bonus": 100
        },
        "points_1000": {
            "name": "امپراتور امتیاز",
            "icon": "👑",
            "description": "۱۰۰۰ امتیاز جمع کردی",
            "condition": {"type": "total_points", "value": 1000},
            "bonus": 200
        },
        "holland_done": {
            "name": "خودشناسی",
            "icon": "🧘",
            "description": "آزمون هالند را کامل کردی",
            "condition": {"type": "holland_test", "value": 1},
            "bonus": 30
        },
        "track_done": {
            "name": "انتخاب رشته",
            "icon": "🎓",
            "description": "رشته تحصیلی خود را انتخاب کردی",
            "condition": {"type": "track_selected", "value": 1},
            "bonus": 30
        },
        "group_creator": {
            "name": "رهبر گروه",
            "icon": "👥",
            "description": "یک گروه مطالعه ایجاد کردی",
            "condition": {"type": "created_group", "value": 1},
            "bonus": 50
        },
        "roadmap_viewer": {
            "name": "آینده‌نگر",
            "icon": "🗺️",
            "description": "مسیرشو رو مشاهده کردی",
            "condition": {"type": "roadmap_viewed", "value": 1},
            "bonus": 20
        },
        "helpful_member": {
            "name": "عضو مفید",
            "icon": "💬",
            "description": "۵۰ پیام در گروه‌ها فرستادی",
            "condition": {"type": "messages_sent", "value": 50},
            "bonus": 100
        },
        "master_mentor": {
            "name": "استاد راهنما",
            "icon": "🎯",
            "description": "به ۵ نفر در مسیرشو کمک کردی",
            "condition": {"type": "mentor_count", "value": 5},
            "bonus": 200
        }
    }
    
    def __init__(self, user_id):
        self.user_id = user_id
        self._init_user_gamification()
        self._recursion_guard = False  # جلوگیری از حلقه بی‌نهایت
    
    def _init_user_gamification(self):
        """ایجاد رکورد گیمیفیکیشن برای کاربر جدید"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gamification (
                    user_id TEXT PRIMARY KEY,
                    total_points INTEGER DEFAULT 0,
                    current_level INTEGER DEFAULT 1,
                    streak_days INTEGER DEFAULT 0,
                    last_challenge_date TEXT,
                    achievements TEXT DEFAULT '[]',
                    unlocked_titles TEXT DEFAULT '[]',
                    total_challenges INTEGER DEFAULT 0,
                    total_exams INTEGER DEFAULT 0,
                    avg_exam_score REAL DEFAULT 0,
                    total_messages INTEGER DEFAULT 0,
                    groups_created INTEGER DEFAULT 0,
                    mentor_count INTEGER DEFAULT 0,
                    updated_at TIMESTAMP
                )
            ''')
            
            cursor.execute('SELECT user_id FROM gamification WHERE user_id = ?', (self.user_id,))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO gamification (user_id, updated_at)
                    VALUES (?, ?)
                ''', (self.user_id, datetime.now().isoformat()))
                conn.commit()
            
            conn.close()
        except Exception as e:
            print(f"خطا در init گیمیفیکیشن: {e}")
    
    def add_points(self, points, reason):
        """افزودن امتیاز و بررسی سطح‌آپ (بدون حلقه بازگشتی)"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('SELECT total_points, current_level FROM gamification WHERE user_id = ?', (self.user_id,))
            row = cursor.fetchone()
            old_points = row[0] if row else 0
            old_level = row[1] if row else 1
            
            new_points = old_points + points
            new_level = self._calculate_level(new_points)
            
            cursor.execute('''
                UPDATE gamification 
                SET total_points = ?, current_level = ?, updated_at = ?
                WHERE user_id = ?
            ''', (new_points, new_level, datetime.now().isoformat(), self.user_id))
            
            conn.commit()
            conn.close()
            
            # ثبت تاریخچه امتیاز (بدون بازگشت)
            self._log_points_history(points, reason)
            
            # بررسی مدال‌های جدید (بدون بازگشت)
            new_achievements = self._check_achievements_no_recursion()
            
            return {
                "points_added": points,
                "new_total": new_points,
                "level_up": new_level > old_level,
                "new_level": self.get_level_info(new_level),
                "new_achievements": new_achievements
            }
        except Exception as e:
            print(f"خطا در افزودن امتیاز: {e}")
            return {"points_added": 0, "new_total": 0, "level_up": False}
    
    def _check_achievements_no_recursion(self):
        """بررسی مدال‌های جدید بدون بازگشت (اضافه کردن امتیاز مستقیم)"""
        if self._recursion_guard:
            return []
        
        self._recursion_guard = True
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('SELECT achievements FROM gamification WHERE user_id = ?', (self.user_id,))
            row = cursor.fetchone()
            earned = json.loads(row[0]) if row and row[0] else []
            
            # جمع‌آوری آمار کاربر
            stats = self._get_user_stats(cursor)
            new_achievements = []
            
            for ach_id, ach_info in self.ACHIEVEMENTS.items():
                if ach_id not in earned:
                    if self._check_condition(ach_info["condition"], stats):
                        earned.append(ach_id)
                        new_achievements.append({
                            "id": ach_id,
                            "name": ach_info["name"],
                            "icon": ach_info["icon"],
                            "description": ach_info["description"],
                            "bonus": ach_info.get("bonus", 0)
                        })
            
            if new_achievements:
                # به‌روزرسانی مدال‌ها در دیتابیس
                cursor.execute('''
                    UPDATE gamification SET achievements = ? WHERE user_id = ?
                ''', (json.dumps(earned, ensure_ascii=False), self.user_id))
                conn.commit()
                
                # اضافه کردن امتیاز پاداش مدال‌ها (بدون بازگشت)
                total_bonus = sum(ach["bonus"] for ach in new_achievements)
                if total_bonus > 0:
                    conn2 = sqlite3.connect(DB_NAME)
                    cursor2 = conn2.cursor()
                    cursor2.execute('SELECT total_points FROM gamification WHERE user_id = ?', (self.user_id,))
                    current_points_row = cursor2.fetchone()
                    current_points = current_points_row[0] if current_points_row else 0
                    cursor2.execute('''
                        UPDATE gamification 
                        SET total_points = ?, updated_at = ?
                        WHERE user_id = ?
                    ''', (current_points + total_bonus, datetime.now().isoformat(), self.user_id))
                    conn2.commit()
                    conn2.close()
                    # ثبت تاریخچه پاداش
                    self._log_points_history(total_bonus, f"پاداش مدال‌ها: {', '.join(ach['name'] for ach in new_achievements)}")
            
            conn.close()
            return new_achievements
        except Exception as e:
            print(f"خطا در بررسی مدال‌ها: {e}")
            return []
        finally:
            self._recursion_guard = False
    
    def _calculate_level(self, points):
        """محاسبه سطح بر اساس امتیاز"""
        for level_num, level_info in sorted(self.LEVELS.items(), reverse=True):
            if points >= level_info["min_points"]:
                return level_num
        return 1
    
    def update_streak(self):
        """بروزرسانی استریک روزانه"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            today = datetime.now().date().isoformat()
            cursor.execute('SELECT last_challenge_date, streak_days FROM gamification WHERE user_id = ?', (self.user_id,))
            row = cursor.fetchone()
            
            last_date = row[0] if row else None
            current_streak = row[1] if row else 0
            
            if last_date == today:
                new_streak = current_streak
            elif last_date == (datetime.now().date() - timedelta(days=1)).isoformat():
                new_streak = current_streak + 1
            else:
                new_streak = 1
            
            cursor.execute('''
                UPDATE gamification 
                SET streak_days = ?, last_challenge_date = ?, updated_at = ?
                WHERE user_id = ?
            ''', (new_streak, today, datetime.now().isoformat(), self.user_id))
            
            conn.commit()
            conn.close()
            
            # پاداش استریک (بدون بازگشت)
            if new_streak in [3, 7, 14, 30, 100]:
                bonus_points = {3: 20, 7: 50, 14: 100, 30: 200, 100: 500}.get(new_streak, 0)
                if bonus_points > 0:
                    self._add_points_direct(bonus_points, f"پاداش استریک {new_streak} روزه")
                    return {"streak": new_streak, "bonus": bonus_points}
            
            return {"streak": new_streak, "bonus": 0}
        except Exception as e:
            print(f"خطا در بروزرسانی استریک: {e}")
            return {"streak": 0, "bonus": 0}
    
    def _add_points_direct(self, points, reason):
        """افزودن مستقیم امتیاز بدون بازگشت"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('SELECT total_points FROM gamification WHERE user_id = ?', (self.user_id,))
            row = cursor.fetchone()
            current_points = row[0] if row else 0
            cursor.execute('''
                UPDATE gamification 
                SET total_points = ?, updated_at = ?
                WHERE user_id = ?
            ''', (current_points + points, datetime.now().isoformat(), self.user_id))
            conn.commit()
            conn.close()
            self._log_points_history(points, reason)
        except Exception as e:
            print(f"خطا در افزودن مستقیم امتیاز: {e}")
    
    def _log_points_history(self, points, reason):
        """ثبت تاریخچه امتیازات"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS points_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    points INTEGER,
                    reason TEXT,
                    created_at TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO points_history (user_id, points, reason, created_at)
                VALUES (?, ?, ?, ?)
            ''', (self.user_id, points, reason[:200], datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطا در ثبت تاریخچه: {e}")
    
    def check_achievements(self):
        """بررسی مدال‌های جدید (رابط عمومی)"""
        return self._check_achievements_no_recursion()
    
    def _get_user_stats(self, cursor):
        """دریافت آمار کاربر برای بررسی مدال‌ها"""
        try:
            cursor.execute('''
                SELECT 
                    total_points, streak_days, total_challenges, total_exams, avg_exam_score,
                    total_messages, groups_created, mentor_count,
                    (SELECT COUNT(*) FROM holland_results WHERE user_id = ?) as holland_count,
                    (SELECT COUNT(*) FROM users WHERE user_id = ? AND track IS NOT NULL AND track != '') as track_exists,
                    (SELECT COUNT(*) FROM path_finder_logs WHERE user_id = ?) as roadmap_count
                FROM gamification 
                WHERE user_id = ?
            ''', (self.user_id, self.user_id, self.user_id, self.user_id))
            
            row = cursor.fetchone()
            if row:
                return {
                    "total_points": row[0] or 0,
                    "streak_days": row[1] or 0,
                    "challenges_completed": row[2] or 0,
                    "total_exams": row[3] or 0,
                    "avg_exam_score": row[4] or 0,
                    "messages_sent": row[5] or 0,
                    "groups_created": row[6] or 0,
                    "mentor_count": row[7] or 0,
                    "holland_test": row[8] or 0,
                    "track_selected": row[9] or 0,
                    "roadmap_viewed": row[10] or 0
                }
            return {}
        except Exception as e:
            print(f"خطا در دریافت آمار: {e}")
            return {}
    
    def _check_condition(self, condition, stats):
        """بررسی یک شرط مدال"""
        cond_type = condition.get("type")
        cond_value = condition.get("value", 1)
        
        if cond_type == "challenges_completed":
            return stats.get("challenges_completed", 0) >= cond_value
        elif cond_type == "streak_days":
            return stats.get("streak_days", 0) >= cond_value
        elif cond_type == "exam_score":
            return stats.get("avg_exam_score", 0) >= cond_value
        elif cond_type == "total_points":
            return stats.get("total_points", 0) >= cond_value
        elif cond_type in ["holland_test", "track_selected", "roadmap_viewed"]:
            return stats.get(cond_type, 0) >= cond_value
        elif cond_type in ["messages_sent", "groups_created", "mentor_count"]:
            return stats.get(cond_type, 0) >= cond_value
        return False
    
    def get_level_info(self, level_num=None):
        """دریافت اطلاعات سطح"""
        if level_num is None:
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('SELECT current_level FROM gamification WHERE user_id = ?', (self.user_id,))
                row = cursor.fetchone()
                level_num = row[0] if row else 1
                conn.close()
            except:
                level_num = 1
        
        level_info = self.LEVELS.get(level_num, self.LEVELS[1])
        next_level_info = self.LEVELS.get(level_num + 1)
        
        points_needed = 0
        if next_level_info:
            try:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute('SELECT total_points FROM gamification WHERE user_id = ?', (self.user_id,))
                row = cursor.fetchone()
                current_points = row[0] if row else 0
                conn.close()
                points_needed = next_level_info["min_points"] - current_points
            except:
                points_needed = 0
        
        return {
            "level": level_num,
            "name": level_info["name"],
            "icon": level_info["icon"],
            "color": level_info["color"],
            "points_needed_next": max(0, points_needed)
        }
    
    def get_full_status(self):
        """دریافت وضعیت کامل کاربر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT total_points, current_level, streak_days, achievements, total_challenges,
                       total_exams, avg_exam_score, total_messages, groups_created, mentor_count
                FROM gamification WHERE user_id = ?
            ''', (self.user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return {}
            
            earned_achievements = json.loads(row[3]) if row[3] else []
            achievements_list = []
            for ach_id in earned_achievements:
                if ach_id in self.ACHIEVEMENTS:
                    a = self.ACHIEVEMENTS[ach_id]
                    achievements_list.append({
                        "id": ach_id,
                        "name": a["name"],
                        "icon": a["icon"],
                        "description": a["description"]
                    })
            
            level_info = self.get_level_info(row[1])
            
            return {
                "total_points": row[0] or 0,
                "current_level": row[1] or 1,
                "level_name": level_info["name"],
                "level_icon": level_info["icon"],
                "level_color": level_info["color"],
                "points_to_next_level": level_info["points_needed_next"],
                "streak_days": row[2] or 0,
                "achievements": achievements_list,
                "achievements_count": len(achievements_list),
                "total_achievements": len(self.ACHIEVEMENTS),
                "stats": {
                    "challenges_completed": row[4] or 0,
                    "exams_taken": row[5] or 0,
                    "avg_exam_score": row[6] or 0,
                    "messages_sent": row[7] or 0,
                    "groups_created": row[8] or 0,
                    "mentor_count": row[9] or 0
                }
            }
        except Exception as e:
            print(f"خطا در دریافت وضعیت: {e}")
            return {}
    
    def increment_stat(self, stat_name, value=1):
        """افزایش یک آمار خاص"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            stat_columns = {
                "challenges_completed": "total_challenges",
                "exams_taken": "total_exams",
                "messages_sent": "total_messages",
                "groups_created": "groups_created",
                "mentor_count": "mentor_count"
            }
            
            if stat_name in stat_columns:
                column = stat_columns[stat_name]
                cursor.execute(f'''
                    UPDATE gamification 
                    SET {column} = {column} + ?, updated_at = ?
                    WHERE user_id = ?
                ''', (value, datetime.now().isoformat(), self.user_id))
                conn.commit()
            
            conn.close()
        except Exception as e:
            print(f"خطا در افزایش آمار: {e}")
    
    def get_leaderboard(self, limit=10):
        """دریافت لیدربرد کاربران برتر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT g.user_id, g.total_points, g.current_level, u.name, u.user_code
                FROM gamification g
                LEFT JOIN users u ON g.user_id = u.user_id
                ORDER BY g.total_points DESC
                LIMIT ?
            ''', (limit,))
            
            leaderboard = []
            for i, row in enumerate(cursor.fetchall()):
                leaderboard.append({
                    "rank": i + 1,
                    "user_id": row[0],
                    "points": row[1] or 0,
                    "level": row[2] or 1,
                    "name": row[3] or row[4][:8] if row[4] else row[0][:8]
                })
            
            conn.close()
            return leaderboard
        except Exception as e:
            print(f"خطا در دریافت لیدربرد: {e}")
            return []


# ========== توابع کمکی برای یکپارچه‌سازی ==========

def add_points_to_user(user_id, points, reason):
    """افزودن امتیاز به کاربر"""
    gamification = GamificationSystem(user_id)
    return gamification.add_points(points, reason)

def update_challenge_completed(user_id):
    """بروزرسانی پس از انجام چالش"""
    gamification = GamificationSystem(user_id)
    gamification.update_streak()
    gamification.increment_stat("challenges_completed")
    return gamification.check_achievements()

def get_user_gamification_status(user_id):
    """دریافت وضعیت گیمیفیکیشن کاربر"""
    gamification = GamificationSystem(user_id)
    return gamification.get_full_status()

def get_leaderboard_data(limit=10):
    """دریافت لیدربرد"""
    gamification = GamificationSystem("")
    return gamification.get_leaderboard(limit)