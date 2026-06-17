# database.py
# مدیریت دیتابیس کامل مسیرینو

import sqlite3
import hashlib
import secrets
import json
import logging
from datetime import datetime, timedelta
from config import DB_NAME

logger = logging.getLogger(__name__)

def get_db_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    """ساخت تمام جداول دیتابیس از صفر"""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # حذف جداول قدیمی (برای ساخت مجدد تمیز)
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS conversations')
        cursor.execute('DROP TABLE IF EXISTS track_analysis')
        cursor.execute('DROP TABLE IF EXISTS risk_analysis')
        cursor.execute('DROP TABLE IF EXISTS feedback')
        cursor.execute('DROP TABLE IF EXISTS learning')
        cursor.execute('DROP TABLE IF EXISTS study_plans')
        cursor.execute('DROP TABLE IF EXISTS user_roles')
        cursor.execute('DROP TABLE IF EXISTS reports')
        cursor.execute('DROP TABLE IF EXISTS alerts')
        cursor.execute('DROP TABLE IF EXISTS holland_results')
        cursor.execute('DROP TABLE IF EXISTS smart_goals')
        cursor.execute('DROP TABLE IF EXISTS goal_checkpoints')
        cursor.execute('DROP TABLE IF EXISTS goal_progress_log')
        cursor.execute('DROP TABLE IF EXISTS user_calendar_events')
        cursor.execute('DROP TABLE IF EXISTS daily_challenges')
        cursor.execute('DROP TABLE IF EXISTS user_points')
        cursor.execute('DROP TABLE IF EXISTS certificates')
        cursor.execute('DROP TABLE IF EXISTS study_groups')
        cursor.execute('DROP TABLE IF EXISTS group_members')
        cursor.execute('DROP TABLE IF EXISTS group_challenges')
        cursor.execute('DROP TABLE IF EXISTS group_messages')
        cursor.execute('DROP TABLE IF EXISTS exam_results')
        cursor.execute('DROP TABLE IF EXISTS points_history')
        cursor.execute('DROP TABLE IF EXISTS gamification')
        cursor.execute('DROP TABLE IF EXISTS path_finder_logs')
        
        # ========== جدول 1: users ==========
        cursor.execute('''
            CREATE TABLE users (
                user_id TEXT PRIMARY KEY,
                user_code TEXT UNIQUE,
                name TEXT,
                lastname TEXT,
                grade_level TEXT,
                track TEXT,
                dominant_think TEXT,
                average_grade REAL,
                role TEXT DEFAULT 'student',
                consent_given INTEGER DEFAULT 0,
                created_at TIMESTAMP,
                last_active TIMESTAMP
            )
        ''')
        
        # ========== جدول 2: conversations ==========
        cursor.execute('''
            CREATE TABLE conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                question TEXT,
                answer TEXT,
                intent TEXT,
                confidence REAL,
                sentiment TEXT,
                user_rating INTEGER,
                timestamp TIMESTAMP
            )
        ''')
        
        # ========== جدول 3: track_analysis ==========
        cursor.execute('''
            CREATE TABLE track_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                track TEXT,
                score REAL,
                ability_score REAL,
                interest_score REAL,
                think_score REAL,
                future_score REAL,
                grade_score REAL,
                timestamp TIMESTAMP
            )
        ''')
        
        # ========== جدول 4: risk_analysis ==========
        cursor.execute('''
            CREATE TABLE risk_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                risk_percent REAL,
                bucket TEXT,
                advice TEXT,
                study_mode TEXT,
                sleep_status TEXT,
                stress_level REAL,
                timestamp TIMESTAMP
            )
        ''')
        
        # ========== جدول 5: feedback ==========
        cursor.execute('''
            CREATE TABLE feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message_id TEXT,
                rating INTEGER,
                comment TEXT,
                is_wrong_recommendation INTEGER DEFAULT 0,
                correct_track TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        # ========== جدول 6: learning ==========
        cursor.execute('''
            CREATE TABLE learning (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT,
                recommended_track TEXT,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0,
                confidence REAL DEFAULT 0.5
            )
        ''')
        
        # ========== جدول 7: study_plans ==========
        cursor.execute('''
            CREATE TABLE study_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                subject TEXT,
                planned_date TEXT,
                duration INTEGER,
                priority TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 8: user_roles ==========
        cursor.execute('''
            CREATE TABLE user_roles (
                user_id TEXT PRIMARY KEY,
                role TEXT DEFAULT 'student',
                permissions TEXT,
                granted_by TEXT,
                granted_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 9: reports ==========
        cursor.execute('''
            CREATE TABLE reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                report_type TEXT,
                report_data TEXT,
                file_path TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 10: alerts ==========
        cursor.execute('''
            CREATE TABLE alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                alert_type TEXT,
                alert_level TEXT,
                message TEXT,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 11: holland_results ==========
        cursor.execute('''
            CREATE TABLE holland_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                scores TEXT,
                primary_type TEXT,
                percentages TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        # ========== جدول 12: smart_goals ==========
        cursor.execute('''
            CREATE TABLE smart_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                description TEXT,
                specific TEXT,
                measurable TEXT,
                achievable TEXT,
                relevant TEXT,
                time_bound TEXT,
                deadline DATE,
                progress REAL DEFAULT 0,
                status TEXT DEFAULT 'active',
                category TEXT,
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 13: goal_checkpoints ==========
        cursor.execute('''
            CREATE TABLE goal_checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER,
                title TEXT,
                completed INTEGER DEFAULT 0,
                completed_at TIMESTAMP,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 14: goal_progress_log ==========
        cursor.execute('''
            CREATE TABLE goal_progress_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER,
                progress_percent REAL,
                note TEXT,
                logged_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 15: user_calendar_events ==========
        cursor.execute('''
            CREATE TABLE user_calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                date TEXT,
                description TEXT,
                event_type TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 16: daily_challenges ==========
        cursor.execute('''
            CREATE TABLE daily_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                challenge_id TEXT,
                title TEXT,
                category TEXT,
                points INTEGER,
                date TEXT,
                status TEXT DEFAULT 'pending',
                completed_at TIMESTAMP,
                proof TEXT
            )
        ''')
        
        # ========== جدول 17: user_points ==========
        cursor.execute('''
            CREATE TABLE user_points (
                user_id TEXT PRIMARY KEY,
                total_points INTEGER DEFAULT 0,
                weekly_points INTEGER DEFAULT 0,
                monthly_points INTEGER DEFAULT 0,
                level TEXT DEFAULT 'برنزی',
                last_updated TIMESTAMP
            )
        ''')
        
        # ========== جدول 18: certificates ==========
        cursor.execute('''
            CREATE TABLE certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                certificate_type TEXT,
                earned_at TIMESTAMP,
                file_path TEXT
            )
        ''')
        
        # ========== جدول 19: study_groups ==========
        cursor.execute('''
            CREATE TABLE study_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                owner_id TEXT NOT NULL,
                created_at TIMESTAMP,
                group_code TEXT UNIQUE,
                max_members INTEGER DEFAULT 20,
                is_private INTEGER DEFAULT 0
            )
        ''')
        
        # ========== جدول 20: group_members ==========
        cursor.execute('''
            CREATE TABLE group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                user_id TEXT,
                role TEXT DEFAULT 'member',
                joined_at TIMESTAMP,
                points_contributed INTEGER DEFAULT 0
            )
        ''')
        
        # ========== جدول 21: group_challenges ==========
        cursor.execute('''
            CREATE TABLE group_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                title TEXT,
                description TEXT,
                points_award INTEGER DEFAULT 10,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                status TEXT DEFAULT 'active',
                created_by TEXT,
                completed_by TEXT
            )
        ''')
        
        # ========== جدول 22: group_messages ==========
        cursor.execute('''
            CREATE TABLE group_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                user_id TEXT,
                message TEXT,
                sent_at TIMESTAMP,
                is_read INTEGER DEFAULT 0
            )
        ''')
        
        # ========== جدول 23: exam_results ==========
        cursor.execute('''
            CREATE TABLE exam_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                subject TEXT,
                grade_level TEXT,
                questions_count INTEGER,
                score REAL,
                answers TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 24: points_history ==========
        cursor.execute('''
            CREATE TABLE points_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                points INTEGER,
                reason TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # ========== جدول 25: gamification ==========
        cursor.execute('''
            CREATE TABLE gamification (
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
        
        # ========== جدول 26: path_finder_logs ==========
        cursor.execute('''
            CREATE TABLE path_finder_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                viewed_at TIMESTAMP
            )
        ''')
        
        # ========== ایجاد ایندکس‌ها برای سرعت ==========
        cursor.execute('CREATE INDEX idx_conversations_user_id ON conversations(user_id)')
        cursor.execute('CREATE INDEX idx_conversations_timestamp ON conversations(timestamp)')
        cursor.execute('CREATE INDEX idx_holland_results_user_id ON holland_results(user_id)')
        cursor.execute('CREATE INDEX idx_smart_goals_user_id ON smart_goals(user_id)')
        cursor.execute('CREATE INDEX idx_group_members_user_id ON group_members(user_id)')
        cursor.execute('CREATE INDEX idx_group_members_group_id ON group_members(group_id)')
        cursor.execute('CREATE INDEX idx_group_messages_group_id ON group_messages(group_id)')
        cursor.execute('CREATE INDEX idx_daily_challenges_user_id ON daily_challenges(user_id)')
        cursor.execute('CREATE INDEX idx_daily_challenges_date ON daily_challenges(date)')
        
        conn.commit()
        print("✅ دیتابیس با 26 جدول ساخته شد")
        logger.info("✅ دیتابیس با موفقیت مقداردهی شد")
        
    except Exception as e:
        print(f"❌ خطا در ساخت دیتابیس: {e}")
        logger.error(f"خطا در ساخت دیتابیس: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


# ========== توابع پایه کاربر ==========

def generate_user_code():
    return secrets.token_hex(8)


def hash_user_code(user_code):
    return hashlib.sha256(user_code.encode()).hexdigest()[:16]


def save_user_to_db(user_id, user_code, name="", lastname="", grade_level="", track="", dominant_think="", average_grade=0, role="student", consent_given=0, email=""):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # اضافه کردن ستون email و role اگر وجود نداشت
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN email TEXT')
        except:
            pass
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "student"')
        except:
            pass
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, user_code, name, lastname, grade_level, track, dominant_think, average_grade, role, consent_given, email, created_at, last_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM users WHERE user_id=?), ?), ?)
        ''', (user_id, user_code, name, lastname, grade_level, track, dominant_think, average_grade, role, consent_given, email, user_id, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره کاربر: {e}")
        return False

def get_user_from_db(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "user_id": result[0],
                "user_code": result[1],
                "name": result[2],
                "lastname": result[3],
                "grade_level": result[4],
                "track": result[5],
                "dominant_think": result[6],
                "average_grade": result[7],
                "role": result[8],
                "consent_given": result[9]
            }
        return None
    except Exception as e:
        print(f"❌ خطا در دریافت کاربر: {e}")
        return None


def update_consent(user_id, consent_given):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET consent_given = ? WHERE user_id = ?', (consent_given, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ خطا در به‌روزرسانی رضایت: {e}")
        return False


# ========== توابع گروه‌ها ==========

def get_user_groups(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT g.id, g.name, g.description, g.owner_id, g.group_code, g.is_private,
                   COUNT(DISTINCT gm2.user_id) as member_count,
                   gm.role, COALESCE(gm.points_contributed, 0) as points_contributed
            FROM study_groups g
            JOIN group_members gm ON g.id = gm.group_id
            LEFT JOIN group_members gm2 ON g.id = gm2.group_id
            WHERE gm.user_id = ?
            GROUP BY g.id
            ORDER BY gm.joined_at DESC
        ''', (user_id,))
        
        groups = []
        for row in cursor.fetchall():
            groups.append({
                "id": row[0],
                "name": row[1],
                "description": row[2] or "",
                "owner_id": row[3],
                "group_code": row[4],
                "is_private": row[5],
                "member_count": row[6] or 1,
                "role": row[7],
                "my_points": row[8] or 0
            })
        
        conn.close()
        return groups
    except Exception as e:
        print(f"خطا در دریافت گروه‌های کاربر: {e}")
        return []


def get_all_public_groups(user_id):
    """دریافت همه گروه‌های عمومی (بدون نیاز به کد دعوت)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # اول ببین اصلاً گروه عمومی وجود دارد؟
        cursor.execute("SELECT COUNT(*) FROM study_groups WHERE is_private = 0")
        public_count = cursor.fetchone()[0]
        print(f"📊 تعداد گروه‌های عمومی در دیتابیس: {public_count}")
        
        cursor.execute('''
            SELECT g.id, g.name, g.description, g.owner_id, g.group_code, 
                   COUNT(DISTINCT gm.user_id) as member_count,
                   (SELECT COUNT(*) FROM group_messages WHERE group_id = g.id) as message_count
            FROM study_groups g
            LEFT JOIN group_members gm ON g.id = gm.group_id
            WHERE g.is_private = 0
            GROUP BY g.id
            ORDER BY g.created_at DESC
        ''')
        
        groups = []
        for row in cursor.fetchall():
            groups.append({
                "id": row[0],
                "name": row[1],
                "description": row[2] or "",
                "owner_id": row[3],
                "group_code": row[4],
                "is_private": 0,
                "member_count": row[5] or 1,
                "message_count": row[6] or 0
            })
        
        print(f"📊 گروه‌های عمومی برگشتی از دیتابیس: {len(groups)}")
        conn.close()
        return groups
    except Exception as e:
        print(f"❌ خطا در دریافت گروه‌های عمومی: {e}")
        return []

def get_group_detail(group_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, description, owner_id, group_code, is_private, created_at FROM study_groups WHERE id = ?', (group_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        group = {
            "id": row[0],
            "name": row[1],
            "description": row[2] or "",
            "owner_id": row[3],
            "group_code": row[4],
            "is_private": row[5],
            "created_at": row[6]
        }
        
        cursor.execute('''
            SELECT gm.user_id, gm.role, COALESCE(gm.points_contributed, 0) as points, gm.joined_at,
                   COALESCE(u.name, u.user_code, gm.user_id) as name
            FROM group_members gm
            LEFT JOIN users u ON gm.user_id = u.user_id
            WHERE gm.group_id = ?
            ORDER BY gm.points_contributed DESC, gm.joined_at ASC
        ''', (group_id,))
        
        members = []
        for r in cursor.fetchall():
            members.append({
                "user_id": r[0],
                "role": r[1],
                "points": r[2],
                "joined_at": r[3],
                "name": r[4][:15] if r[4] else r[0][:8]
            })
        
        cursor.execute('''
            SELECT gm.id, gm.user_id, gm.message, gm.sent_at,
                   COALESCE(u.name, u.user_code, gm.user_id) as user_name
            FROM group_messages gm
            LEFT JOIN users u ON gm.user_id = u.user_id
            WHERE gm.group_id = ?
            ORDER BY gm.sent_at ASC
            LIMIT 100
        ''', (group_id,))
        
        messages = []
        for r in cursor.fetchall():
            messages.append({
                "id": r[0],
                "user_id": r[1],
                "message": r[2],
                "sent_at": r[3],
                "user_name": r[4][:15] if r[4] else r[1][:8]
            })
        
        conn.close()
        
        is_member = any(m["user_id"] == user_id for m in members)
        is_owner = group["owner_id"] == user_id
        
        return {
            "group": group,
            "members": members,
            "messages": messages,
            "is_member": is_member,
            "is_owner": is_owner,
            "user_role": "owner" if is_owner else "member"
        }
    except Exception as e:
        print(f"خطا در دریافت جزئیات گروه: {e}")
        return None


def join_group(user_id, group_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, user_id))
        if cursor.fetchone():
            conn.close()
            return {"status": "error", "message": "شما قبلاً عضو این گروه هستید"}
        
        cursor.execute('SELECT name FROM study_groups WHERE id = ?', (group_id,))
        group_row = cursor.fetchone()
        if not group_row:
            conn.close()
            return {"status": "error", "message": "گروه یافت نشد"}
        
        cursor.execute('''
            INSERT INTO group_members (group_id, user_id, role, joined_at, points_contributed)
            VALUES (?, ?, 'member', ?, 0)
        ''', (group_id, user_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return {"status": "ok", "message": f"شما به گروه {group_row[0]} پیوستید"}
    except Exception as e:
        print(f"خطا در پیوستن به گروه: {e}")
        return {"status": "error", "message": str(e)}


def join_group_by_code(user_id, group_code):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, is_private FROM study_groups WHERE group_code = ?', (group_code,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return {"status": "error", "message": "گروه با این کد یافت نشد"}
        
        group_id = row[0]
        group_name = row[1]
        
        cursor.execute('SELECT id FROM group_members WHERE group_id = ? AND user_id = ?', (group_id, user_id))
        if cursor.fetchone():
            conn.close()
            return {"status": "error", "message": "شما قبلاً عضو این گروه هستید"}
        
        cursor.execute('''
            INSERT INTO group_members (group_id, user_id, role, joined_at, points_contributed)
            VALUES (?, ?, 'member', ?, 0)
        ''', (group_id, user_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return {"status": "ok", "message": f"شما به گروه {group_name} پیوستید", "group_id": group_id}
    except Exception as e:
        print(f"خطا در پیوستن با کد: {e}")
        return {"status": "error", "message": str(e)}

def delete_group(group_id, user_id):
    """حذف گروه توسط مالک (owner)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # بررسی کن که آیا این کاربر واقعاً مالک گروه هست
        cursor.execute('''
            SELECT id FROM study_groups 
            WHERE id = ? AND owner_id = ?
        ''', (group_id, user_id))
        
        if not cursor.fetchone():
            conn.close()
            return {"status": "error", "message": "فقط مدیر گروه می‌تواند گروه را حذف کند"}
        
        # حذف پیام‌های گروه
        cursor.execute('DELETE FROM group_messages WHERE group_id = ?', (group_id,))
        
        # حذف اعضای گروه
        cursor.execute('DELETE FROM group_members WHERE group_id = ?', (group_id,))
        
        # حذف چالش‌های گروه (اگه داری)
        cursor.execute('DELETE FROM group_challenges WHERE group_id = ?', (group_id,))
        
        # حذف خود گروه
        cursor.execute('DELETE FROM study_groups WHERE id = ?', (group_id,))
        
        conn.commit()
        conn.close()
        
        return {"status": "ok", "message": "گروه با موفقیت حذف شد"}
        
    except Exception as e:
        print(f"خطا در حذف گروه: {e}")
        return {"status": "error", "message": str(e)}
# ========== توابع ذخیره‌سازی دیگر ==========

def save_conversation(user_id, question, answer, intent, confidence, sentiment, user_rating=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, question, answer, intent, confidence, sentiment, user_rating, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, question[:1000], answer[:1000], intent, confidence, sentiment, user_rating, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره مکالمه: {e}")
        return False


def save_holland_result(user_id, scores, primary_type, percentages):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM holland_results WHERE user_id = ?', (user_id,))
        
        cursor.execute('''
            INSERT INTO holland_results (user_id, scores, primary_type, percentages, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, json.dumps(scores), primary_type, json.dumps(percentages), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"✅ نتیجه هالند ذخیره شد - کاربر: {user_id[:8]}... - نوع: {primary_type}")
        return True
    except Exception as e:
        print(f"❌ خطا در ذخیره نتیجه هالند: {e}")
        return False


def get_holland_results(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT scores, primary_type, percentages, timestamp FROM holland_results WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "scores": json.loads(result[0]),
                "primary_type": result[1],
                "percentages": json.loads(result[2]),
                "timestamp": result[3]
            }
        return None
    except Exception as e:
        print(f"خطا در دریافت نتایج هالند: {e}")
        return None


def save_track_analysis(user_id, track, score, ability_score, interest_score, think_score, future_score, grade_score):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO track_analysis (user_id, track, score, ability_score, interest_score, think_score, future_score, grade_score, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, track, score, ability_score, interest_score, think_score, future_score, grade_score, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره تحلیل رشته: {e}")
        return False


def save_risk_analysis(user_id, risk_percent, bucket, advice, study_mode, sleep_status, stress_level):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO risk_analysis (user_id, risk_percent, bucket, advice, study_mode, sleep_status, stress_level, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, risk_percent, bucket, advice, study_mode, sleep_status, stress_level, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره تحلیل ریسک: {e}")
        return False


def save_feedback(user_id, message_id, rating, comment="", is_wrong_recommendation=0, correct_track=""):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (user_id, message_id, rating, comment, is_wrong_recommendation, correct_track, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, message_id, rating, comment, is_wrong_recommendation, correct_track, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        print(f"✅ بازخورد ثبت شد - کاربر: {user_id[:8]}... - امتیاز: {rating}")
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره بازخورد: {e}")
        return False


def save_alert(user_id, alert_type, alert_level, message):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (user_id, alert_type, alert_level, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, alert_type, alert_level, message, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره هشدار: {e}")
        return False


def save_study_plan(user_id, plan_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO study_plans (user_id, plan_data, created_at)
            VALUES (?, ?, ?)
        ''', (user_id, json.dumps(plan_data, ensure_ascii=False), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ذخیره برنامه مطالعه: {e}")
        return False


def get_user_conversations(user_id, limit=20):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT question, answer, timestamp FROM conversations 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        results = cursor.fetchall()
        conn.close()
        return [{"question": r[0], "answer": r[1], "time": r[2]} for r in results]
    except Exception as e:
        logger.error(f"خطا در دریافت مکالمات: {e}")
        return []


def get_user_statistics(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations WHERE user_id = ?', (user_id,))
        total_conversations = cursor.fetchone()[0]
        cursor.execute('SELECT AVG(confidence) FROM conversations WHERE user_id = ?', (user_id,))
        avg_confidence = cursor.fetchone()[0] or 0
        cursor.execute('SELECT AVG(user_rating) FROM conversations WHERE user_id = ? AND user_rating IS NOT NULL', (user_id,))
        avg_rating = cursor.fetchone()[0] or 0
        conn.close()
        return {
            "total_conversations": total_conversations,
            "avg_confidence": round(avg_confidence, 1),
            "avg_user_rating": round(avg_rating, 1)
        }
    except Exception as e:
        logger.error(f"خطا در دریافت آمار: {e}")
        return {}


def get_similar_users(user_id, limit=10):
    try:
        user = get_user_from_db(user_id)
        if not user:
            return []
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_id, grade_level, dominant_think, average_grade, track
            FROM users 
            WHERE grade_level = ? AND dominant_think = ? AND user_id != ?
            ORDER BY average_grade DESC
            LIMIT ?
        ''', (user.get('grade_level', ''), user.get('dominant_think', ''), user_id, limit))
        results = cursor.fetchall()
        conn.close()
        return [{"user_id": r[0], "grade_level": r[1], "dominant_think": r[2], "average_grade": r[3], "track": r[4]} for r in results]
    except Exception as e:
        logger.error(f"خطا در یافتن کاربران مشابه: {e}")
        return []


def get_dashboard_stats(role="admin", user_id=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        stats = {}
        if role == "admin":
            cursor.execute('SELECT COUNT(*) FROM users')
            stats["total_users"] = cursor.fetchone()[0] or 0
            cursor.execute('SELECT COUNT(*) FROM conversations')
            stats["total_conversations"] = cursor.fetchone()[0] or 0
            cursor.execute('SELECT AVG(confidence) FROM conversations')
            avg_conf = cursor.fetchone()[0]
            stats["avg_confidence"] = round(avg_conf or 0, 1)
            cursor.execute('SELECT AVG(rating) FROM feedback WHERE rating > 0')
            avg_rat = cursor.fetchone()[0]
            stats["avg_satisfaction"] = round(avg_rat or 0, 1)
        conn.close()
        return stats
    except Exception as e:
        logger.error(f"خطا در آمار داشبورد: {e}")
        return {}


def create_goal(user_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO smart_goals 
            (user_id, title, description, specific, measurable, achievable, relevant, time_bound, deadline, category, priority, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data.get("title", ""), data.get("description", ""), data.get("specific", data.get("title", "")),
              data.get("measurable", ""), data.get("achievable", ""), data.get("relevant", ""),
              data.get("time_bound", data.get("deadline", "")), data.get("deadline", ""),
              data.get("category", "تحصیلی"), data.get("priority", "medium"),
              datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در ایجاد هدف: {e}")
        return False


def get_user_goals(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, measurable, achievable, relevant, deadline, progress, status, category, priority
            FROM smart_goals WHERE user_id = ? ORDER BY 
            CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END,
            deadline ASC NULLS LAST
        ''', (user_id,))
        results = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "title": r[1], "measurable": r[2], "achievable": r[3], "relevant": r[4],
                 "deadline": r[5], "progress": r[6] or 0, "status": r[7], "category": r[8], "priority": r[9]} for r in results]
    except Exception as e:
        logger.error(f"خطا در دریافت اهداف: {e}")
        return []


def delete_goal(goal_id, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM smart_goals WHERE id=? AND user_id=?', (goal_id, user_id))
        cursor.execute('DELETE FROM goal_checkpoints WHERE goal_id=?', (goal_id,))
        cursor.execute('DELETE FROM goal_progress_log WHERE goal_id=?', (goal_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در حذف هدف: {e}")
        return False


def update_goal_progress(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        progress = data.get("progress", 0)
        status = "completed" if progress >= 100 else "active"
        cursor.execute('''
            UPDATE smart_goals SET progress=?, status=?, updated_at=? WHERE id=? AND user_id=?
        ''', (progress, status, datetime.now().isoformat(), data.get("goal_id"), data.get("session_id")))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"خطا در به‌روزرسانی پیشرفت: {e}")
        return False


# ========== توابع مقایسه و آمار ==========

def get_user_stats_for_comparison(user_id):
    """دریافت آمار کاربر برای مقایسه با دیگران"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(average_grade), COUNT(*)
            FROM users 
            WHERE grade_level = (SELECT grade_level FROM users WHERE user_id = ?)
            AND dominant_think = (SELECT dominant_think FROM users WHERE user_id = ?)
        ''', (user_id, user_id))
        row = cursor.fetchone()
        avg_grade = row[0] if row else 0
        count = row[1] if row else 0
        
        cursor.execute('''
            SELECT track, AVG(score), COUNT(*)
            FROM track_analysis 
            WHERE user_id IN (SELECT user_id FROM users WHERE grade_level = (SELECT grade_level FROM users WHERE user_id = ?))
            GROUP BY track
        ''', (user_id,))
        track_success = cursor.fetchall()
        
        conn.close()
        return {
            "similar_users_avg_grade": round(avg_grade or 0, 1),
            "similar_users_count": count or 0,
            "track_success_rates": [{"track": t[0], "avg_score": round(t[1] or 0, 1), "count": t[2]} for t in track_success]
        }
    except Exception as e:
        print(f"خطا در آمار مقایسه: {e}")
        return {}


def update_goal(data):
    """به‌روزرسانی هدف SMART"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE smart_goals SET title=?, measurable=?, achievable=?, relevant=?, deadline=?, category=?, priority=?, updated_at=?
            WHERE id=? AND user_id=?
        ''', (
            data.get("title"), data.get("measurable"), data.get("achievable"),
            data.get("relevant"), data.get("deadline"), data.get("category"),
            data.get("priority"), datetime.now().isoformat(),
            data.get("goal_id"), data.get("session_id")
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در به‌روزرسانی هدف: {e}")
        return False


def update_learning_from_feedback(user_id, wrong_recommendation, correct_track):
    """یادگیری از بازخورد منفی کاربران"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE learning 
            SET fail_count = fail_count + 1,
                confidence = (success_count * 1.0) / (success_count + fail_count + 1)
            WHERE recommended_track = ? AND pattern LIKE ?
        ''', (wrong_recommendation, f'%{user_id[:8]}%'))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"خطا در به‌روزرسانی یادگیری: {e}")


# Note: get_dashboard_stats is already defined above. Remove duplicate if exists.


def get_user_points(user_id):
    """دریافت امتیازات کاربر"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT total_points, weekly_points, monthly_points, level FROM user_points WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            points = {
                "total": row[0] or 0,
                "weekly": row[1] or 0,
                "monthly": row[2] or 0,
                "level": row[3] or "برنزی"
            }
        else:
            points = {"total": 0, "weekly": 0, "monthly": 0, "level": "برنزی"}
        
        # تعداد چالش‌های امروز
        today = datetime.now().date().isoformat()
        cursor.execute('SELECT COUNT(*) FROM daily_challenges WHERE user_id = ? AND date = ? AND status = "completed"', (user_id, today))
        points["completed_today"] = cursor.fetchone()[0] or 0
        
        # استریک
        cursor.execute('SELECT streak_days FROM gamification WHERE user_id = ?', (user_id,))
        streak_row = cursor.fetchone()
        points["streak"] = streak_row[0] if streak_row else 0
        
        conn.close()
        return points
    except Exception as e:
        print(f"خطا در دریافت امتیازات: {e}")
        return {"total": 0, "weekly": 0, "monthly": 0, "level": "برنزی", "completed_today": 0, "streak": 0}


def add_points_to_user(user_id, points, reason):
    """افزودن امتیاز به کاربر"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        today = datetime.now().date().isoformat()
        week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).date().isoformat()
        month_start = datetime.now().date().replace(day=1).isoformat()
        
        # به‌روزرسانی امتیازات
        cursor.execute('''
            INSERT INTO user_points (user_id, total_points, weekly_points, monthly_points, last_updated)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                total_points = total_points + ?,
                weekly_points = weekly_points + ?,
                monthly_points = monthly_points + ?,
                last_updated = ?
        ''', (user_id, points, points, points, now, points, points, points, now))
        
        # ثبت تاریخچه
        cursor.execute('''
            INSERT INTO points_history (user_id, points, reason, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, points, reason, now))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در افزودن امتیاز: {e}")
        return False


def get_leaderboard(limit=10):
    """دریافت لیدربرد کاربران برتر"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.user_id, u.user_code, u.name, COALESCE(up.total_points, 0) as points,
                   COALESCE(up.level, 'برنزی') as level
            FROM users u
            LEFT JOIN user_points up ON u.user_id = up.user_id
            WHERE u.consent_given = 1
            ORDER BY points DESC
            LIMIT ?
        ''', (limit,))
        
        leaderboard = []
        for i, row in enumerate(cursor.fetchall()):
            leaderboard.append({
                "rank": i + 1,
                "user_id": row[0],
                "user_code": row[1],
                "name": row[2] or row[1][:8],
                "points": row[3] or 0,
                "level": row[4]
            })
        
        conn.close()
        return leaderboard
    except Exception as e:
        print(f"خطا در دریافت لیدربرد: {e}")
        return []


def save_path_finder_log(user_id):
    """ذخیره لاگ مشاهده مسیریاب"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO path_finder_logs (user_id, viewed_at)
            VALUES (?, ?)
        ''', (user_id, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در ذخیره لاگ مسیریاب: {e}")
        return False


def get_gamification_data(user_id):
    """دریافت داده‌های گیمیفیکیشن کاربر"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT total_points, current_level, streak_days, achievements, unlocked_titles,
                   total_challenges, total_exams, avg_exam_score, total_messages, groups_created, mentor_count
            FROM gamification WHERE user_id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "total_points": row[0] or 0,
                "current_level": row[1] or 1,
                "streak_days": row[2] or 0,
                "achievements": json.loads(row[3]) if row[3] else [],
                "unlocked_titles": json.loads(row[4]) if row[4] else [],
                "total_challenges": row[5] or 0,
                "total_exams": row[6] or 0,
                "avg_exam_score": row[7] or 0,
                "total_messages": row[8] or 0,
                "groups_created": row[9] or 0,
                "mentor_count": row[10] or 0
            }
        return None
    except Exception as e:
        print(f"خطا در دریافت گیمیفیکیشن: {e}")
        return None


print("✅ ماژول database.py بارگذاری شد")