# adaptive_recommender.py
# سیستم پیشنهاددهنده تطبیقی - بدون هیچ کتابخانه اضافی

import sqlite3
import json
from datetime import datetime
from config import DB_NAME

class AdaptiveRecommender:
    """سیستم پیشنهاددهنده مبتنی بر تعامل کاربر (Collaborative & Content-based)"""
    
    # بردار ویژگی‌های هر شغل (بدون کتابخانه)
    CAREER_FEATURES = {
        "پزشکی": {
            "vector": [0.9, 0.8, 0.2, 0.1, 0.3, 0.9],  # [علمی, تحلیلی, هنری, اجتماعی, کارآفرین, سلامت]
            "holland": "پژوهشی",
            "track": "علوم تجربی"
        },
        "دندان‌پزشکی": {
            "vector": [0.85, 0.85, 0.2, 0.2, 0.3, 0.85],
            "holland": "پژوهشی",
            "track": "علوم تجربی"
        },
        "مهندسی کامپیوتر": {
            "vector": [0.9, 0.9, 0.2, 0.3, 0.7, 0.1],
            "holland": "تحلیلی",
            "track": "ریاضی فیزیک"
        },
        "هوش مصنوعی": {
            "vector": [0.95, 0.95, 0.2, 0.2, 0.8, 0.1],
            "holland": "تحلیلی",
            "track": "ریاضی فیزیک"
        },
        "روانشناسی": {
            "vector": [0.5, 0.6, 0.3, 0.9, 0.5, 0.7],
            "holland": "اجتماعی",
            "track": "علوم انسانی"
        },
        "حقوق": {
            "vector": [0.6, 0.85, 0.2, 0.7, 0.8, 0.2],
            "holland": "متهور",
            "track": "علوم انسانی"
        },
        "گرافیک": {
            "vector": [0.2, 0.3, 0.95, 0.4, 0.6, 0.1],
            "holland": "هنری",
            "track": "هنر"
        },
        "انیمیشن": {
            "vector": [0.3, 0.4, 0.95, 0.4, 0.6, 0.1],
            "holland": "هنری",
            "track": "هنر"
        }
    }
    
    def __init__(self, user_id):
        self.user_id = user_id
        self._init_tables()
    
    def _init_tables(self):
        """ایجاد جدول‌های لازم برای سیستم پیشنهاددهنده"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # جدول تعاملات کاربر با شغل‌ها
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_career_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    career_name TEXT,
                    interaction_type TEXT,
                    weight INTEGER DEFAULT 1,
                    created_at TIMESTAMP
                )
            ''')
            
            # جدول پروفایل ترجیحات کاربر (بردار علاقه)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preference_vectors (
                    user_id TEXT PRIMARY KEY,
                    feature_vector TEXT,
                    last_updated TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطا در ایجاد جدول‌های recommender: {e}")
    
    def _cosine_similarity(self, vec_a, vec_b):
        """محاسبه شباهت کسینوسی بین دو بردار - از صفر"""
        if not vec_a or not vec_b:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        mag_a = sum(a * a for a in vec_a) ** 0.5
        mag_b = sum(b * b for b in vec_b) ** 0.5
        
        if mag_a == 0 or mag_b == 0:
            return 0.0
        
        return dot_product / (mag_a * mag_b)
    
    def log_interaction(self, career_name, interaction_type="view"):
        """ثبت تعامل کاربر با یک شغل"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # وزن تعامل: مشاهده=1, کلیک روی جزئیات=3, ذخیره=5
            weights = {
                "view": 1,
                "detail": 3,
                "save": 5,
                "like": 4
            }
            weight = weights.get(interaction_type, 1)
            
            cursor.execute('''
                INSERT INTO user_career_interactions (user_id, career_name, interaction_type, weight, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.user_id, career_name, interaction_type, weight, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            # به‌روزرسانی بردار ترجیحات کاربر
            self._update_user_preference_vector()
            
            return True
        except Exception as e:
            print(f"خطا در ثبت تعامل: {e}")
            return False
    
    def _update_user_preference_vector(self):
        """محاسبه بردار ترجیحات کاربر بر اساس تعاملات گذشته"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # دریافت همه تعاملات کاربر
            cursor.execute('''
                SELECT career_name, SUM(weight) as total_weight
                FROM user_career_interactions
                WHERE user_id = ?
                GROUP BY career_name
                ORDER BY total_weight DESC
            ''', (self.user_id,))
            
            interactions = cursor.fetchall()
            
            if not interactions:
                # کاربر هنوز تعاملی نداشته → بردار پیش‌فرض
                default_vector = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                cursor.execute('''
                    INSERT OR REPLACE INTO user_preference_vectors (user_id, feature_vector, last_updated)
                    VALUES (?, ?, ?)
                ''', (self.user_id, json.dumps(default_vector), datetime.now().isoformat()))
                conn.commit()
                conn.close()
                return
            
            # محاسبه میانگین وزنی بردارها
            total_weight = 0
            avg_vector = [0.0] * 6
            
            for career_name, weight in interactions:
                if career_name in self.CAREER_FEATURES:
                    vec = self.CAREER_FEATURES[career_name]["vector"]
                    for i in range(6):
                        avg_vector[i] += vec[i] * weight
                    total_weight += weight
            
            if total_weight > 0:
                for i in range(6):
                    avg_vector[i] /= total_weight
            
            # ذخیره بردار جدید
            cursor.execute('''
                INSERT OR REPLACE INTO user_preference_vectors (user_id, feature_vector, last_updated)
                VALUES (?, ?, ?)
            ''', (self.user_id, json.dumps(avg_vector), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"خطا در به‌روزرسانی بردار: {e}")
    
    def get_user_preference_vector(self):
        """دریافت بردار ترجیحات کاربر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('SELECT feature_vector FROM user_preference_vectors WHERE user_id = ?', (self.user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return json.loads(row[0])
            return [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        except Exception as e:
            print(f"خطا در دریافت بردار: {e}")
            return [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    
    def get_personalized_recommendations(self, careers_list, limit=5):
        """
        رتبه‌بندی شغل‌ها بر اساس شباهت به ترجیحات کاربر
        careers_list: لیست دیکشنری‌های شغل (با کلید "job")
        """
        if not careers_list:
            return []
        
        user_vector = self.get_user_preference_vector()
        
        scored_careers = []
        for career in careers_list:
            career_name = career.get("job", "")
            if career_name in self.CAREER_FEATURES:
                career_vector = self.CAREER_FEATURES[career_name]["vector"]
                similarity = self._cosine_similarity(user_vector, career_vector)
                # ترکیب نمره اصلی با شباهت (70% نمره اصلی، 30% شباهت شخصی)
                original_score = career.get("percent", 50)
                final_score = (original_score * 0.7) + (similarity * 100 * 0.3)
                career["match_percent"] = round(final_score, 1)
                career["personal_match"] = round(similarity * 100, 1)
            else:
                career["match_percent"] = career.get("percent", 50)
                career["personal_match"] = 0
            
            scored_careers.append(career)
        
        # مرتب‌سازی بر اساس نمره نهایی
        scored_careers.sort(key=lambda x: x.get("match_percent", 0), reverse=True)
        return scored_careers[:limit]
    
    def get_similar_careers(self, career_name, limit=3):
        """پیدا کردن شغل‌های مشابه با یک شغل خاص"""
        if career_name not in self.CAREER_FEATURES:
            return []
        
        target_vector = self.CAREER_FEATURES[career_name]["vector"]
        similarities = []
        
        for name, data in self.CAREER_FEATURES.items():
            if name != career_name:
                sim = self._cosine_similarity(target_vector, data["vector"])
                similarities.append((name, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [{"career": name, "similarity": round(sim * 100, 1)} for name, sim in similarities[:limit]]


# تابع کمکی برای استفاده در path_finder.py
def get_recommender(user_id):
    return AdaptiveRecommender(user_id)