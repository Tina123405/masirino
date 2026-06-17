# adaptive_recommender_advanced.py
# سیستم توصیه‌گر تطبیقی پیشرفته - با الگوریتم‌های Bandit و Collaborative Filtering

import sqlite3 # برای کار با دیتابیس
import json # خوندن و نوشتن داده های مرتب شده
import math
import random
from datetime import datetime, timedelta
from collections import defaultdict
from config import DB_NAME


class AdvancedAdaptiveRecommender:
    """سیستم توصیه‌گر تطبیقی پیشرفته با Multi-Armed Bandit و Collaborative Filtering"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self._init_tables()
    
    def _init_tables(self):
        """ایجاد جدول‌های پیشرفته برای سیستم توصیه‌گر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # جدول بازخورد توصیه‌ها (برای یادگیری)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendation_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    recommended_item TEXT,
                    user_clicked INTEGER DEFAULT 0,
                    user_saved INTEGER DEFAULT 0,
                    user_liked INTEGER DEFAULT 0,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            
            # جدول شباهت کاربران (برای Collaborative Filtering)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_similarity (
                    user_id TEXT,
                    similar_user_id TEXT,
                    similarity_score REAL,
                    calculated_at TIMESTAMP,
                    PRIMARY KEY (user_id, similar_user_id)
                )
            ''')
            
            # جدول آمار بازوها (برای Bandit Algorithm)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bandit_arms (
                    arm_id TEXT PRIMARY KEY,
                    arm_name TEXT,
                    successes INTEGER DEFAULT 0,
                    failures INTEGER DEFAULT 0,
                    last_updated TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطا در ایجاد جدول‌های recommender پیشرفته: {e}")
    
    # ========== Multi-Armed Bandit (Thompson Sampling) ==========
    
    def _initialize_bandit_arms(self):
        """مقداردهی اولیه بازوهای سیستم توصیه‌گر"""
        arms = {
            "career_medical": {"name": "مسیر پزشکی", "successes": 10, "failures": 2},
            "career_engineering": {"name": "مسیر مهندسی", "successes": 8, "failures": 3},
            "career_psychology": {"name": "مسیر روانشناسی", "successes": 6, "failures": 2},
            "career_art": {"name": "مسیر هنر", "successes": 5, "failures": 4},
            "study_method_pomodoro": {"name": "روش مطالعه پومودورو", "successes": 15, "failures": 3},
            "study_method_sq3r": {"name": "روش مطالعه SQ3R", "successes": 8, "failures": 2},
            "study_method_feynman": {"name": "روش مطالعه فاینمن", "successes": 7, "failures": 1},
            "challenge_easy": {"name": "چالش آسان", "successes": 20, "failures": 5},
            "challenge_medium": {"name": "چالش متوسط", "successes": 12, "failures": 4},
            "challenge_hard": {"name": "چالش سخت", "successes": 5, "failures": 3}
        }
        
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            for arm_id, arm_data in arms.items():
                cursor.execute('''
                    INSERT OR REPLACE INTO bandit_arms (arm_id, arm_name, successes, failures, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                ''', (arm_id, arm_data["name"], arm_data["successes"], arm_data["failures"], datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطا در مقداردهی bandit arms: {e}")
    
    def _sample_from_beta(self, alpha, beta):
        """نمونه‌گیری از توزیع بتا (برای Thompson Sampling)"""
        # تقریب ساده برای توزیع بتا
        if alpha + beta == 0:
            return random.random()
        
        # روش ساده: نمونه‌گیری از توزیع با استفاده از random
        # هرچه alpha بزرگتر، احتمال مقدار بالاتر بیشتر است
        samples = []
        for _ in range(100):
            x = random.random()
            # تابع چگالی بتا ساده شده
            weight = (x ** (alpha - 1)) * ((1 - x) ** (beta - 1)) if alpha > 0 and beta > 0 else 1
            samples.append((x, weight))
        
        # انتخاب وزنی
        total_weight = sum(w for _, w in samples)
        r = random.random() * total_weight
        cumulative = 0
        for x, w in samples:
            cumulative += w
            if cumulative >= r:
                return x
        return samples[-1][0] if samples else 0.5
    
    def get_bandit_recommendation(self, arm_category=None):
        """دریافت بهترین توصیه با استفاده از Thompson Sampling"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            if arm_category:
                cursor.execute('''
                    SELECT arm_id, arm_name, successes, failures FROM bandit_arms
                    WHERE arm_id LIKE ?
                ''', (arm_category + '%',))
            else:
                cursor.execute('SELECT arm_id, arm_name, successes, failures FROM bandit_arms')
            
            arms = cursor.fetchall()
            conn.close()
            
            if not arms:
                self._initialize_bandit_arms()
                return self.get_bandit_recommendation(arm_category)
            
            best_arm = None
            best_score = -1
            
            for arm_id, arm_name, successes, failures in arms:
                # Thompson Sampling: نمونه‌گیری از توزیع بتا
                alpha = successes + 1
                beta = failures + 1
                score = self._sample_from_beta(alpha, beta)
                
                # پاداش برای بازوهایی که کاربر قبلاً با آنها تعامل داشته
                personal_bonus = self._get_personal_arm_bonus(arm_id)
                score += personal_bonus * 0.1
                
                if score > best_score:
                    best_score = score
                    best_arm = {"id": arm_id, "name": arm_name, "score": round(score * 100, 1)}
            
            return best_arm
        except Exception as e:
            print(f"خطا در bandit recommendation: {e}")
            return None
    
    def update_bandit_feedback(self, arm_id, success):
        """به‌روزرسانی بازخورد برای Bandit Algorithm"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            if success:
                cursor.execute('''
                    UPDATE bandit_arms 
                    SET successes = successes + 1, last_updated = ?
                    WHERE arm_id = ?
                ''', (datetime.now().isoformat(), arm_id))
            else:
                cursor.execute('''
                    UPDATE bandit_arms 
                    SET failures = failures + 1, last_updated = ?
                    WHERE arm_id = ?
                ''', (datetime.now().isoformat(), arm_id))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطا در به‌روزرسانی bandit: {e}")
    
    def _get_personal_arm_bonus(self, arm_id):
        """امتیاز شخصی برای بازو بر اساس تعاملات کاربر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM recommendation_feedback
                WHERE user_id = ? AND recommended_item = ? AND (user_clicked = 1 OR user_saved = 1)
            ''', (self.user_id, arm_id))
            
            count = cursor.fetchone()[0] or 0
            conn.close()
            return min(5, count)  # حداکثر 5 امتیاز اضافه
        except:
            return 0
    
    # ========== Collaborative Filtering ساده ==========
    
    def _calculate_user_similarity(self, other_user_id):
        """محاسبه شباهت بین دو کاربر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # دریافت تعاملات کاربر فعلی
            cursor.execute('''
                SELECT recommended_item, user_clicked, user_saved 
                FROM recommendation_feedback 
                WHERE user_id = ?
            ''', (self.user_id,))
            user1_items = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
            
            # دریافت تعاملات کاربر دیگر
            cursor.execute('''
                SELECT recommended_item, user_clicked, user_saved 
                FROM recommendation_feedback 
                WHERE user_id = ?
            ''', (other_user_id,))
            user2_items = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
            
            conn.close()
            
            # یافتن آیتم‌های مشترک
            common_items = set(user1_items.keys()) & set(user2_items.keys())
            if len(common_items) < 2:
                return 0
            
            # محاسبه شباهت کسینوسی وزنی
            dot_product = 0
            norm1 = 0
            norm2 = 0
            
            for item in common_items:
                # محاسبه امتیاز برای هر آیتم (کلیک = 1، ذخیره = 2)
                score1 = user1_items[item][0] + (user1_items[item][1] * 2)
                score2 = user2_items[item][0] + (user2_items[item][1] * 2)
                dot_product += score1 * score2
                norm1 += score1 ** 2
                norm2 += score2 ** 2
            
            if norm1 == 0 or norm2 == 0:
                return 0
            
            similarity = dot_product / (math.sqrt(norm1) * math.sqrt(norm2))
            return round(similarity, 3)
        except Exception as e:
            print(f"خطا در محاسبه شباهت: {e}")
            return 0
    
    def get_similar_users_recommendations(self, limit=5):
        """دریافت توصیه‌های مبتنی بر کاربران مشابه (Collaborative Filtering)"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # دریافت همه کاربران دیگر
            cursor.execute('SELECT DISTINCT user_id FROM recommendation_feedback WHERE user_id != ?', (self.user_id,))
            other_users = [row[0] for row in cursor.fetchall()]
            
            if not other_users:
                return []
            
            # محاسبه شباهت با هر کاربر
            similarities = []
            for other_user in other_users[:50]:  # محدودیت برای سرعت
                sim = self._calculate_user_similarity(other_user)
                if sim > 0.3:  # فقط کاربران با شباهت قابل قبول
                    similarities.append((other_user, sim))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_similar_users = similarities[:5]
            
            # جمع‌آوری آیتم‌هایی که کاربران مشابه پسندیده‌اند
            recommended_items = {}
            for similar_user, sim_score in top_similar_users:
                cursor.execute('''
                    SELECT recommended_item, user_clicked, user_saved 
                    FROM recommendation_feedback 
                    WHERE user_id = ? AND (user_clicked = 1 OR user_saved = 1)
                ''', (similar_user,))
                
                for row in cursor.fetchall():
                    item = row[0]
                    # بررسی اینکه کاربر فعلی این آیتم را ندیده باشد
                    cursor.execute('SELECT COUNT(*) FROM recommendation_feedback WHERE user_id = ? AND recommended_item = ?', (self.user_id, item))
                    if cursor.fetchone()[0] == 0:
                        score = sim_score * (1 + row[1] + row[2]*2)
                        if item in recommended_items:
                            recommended_items[item] += score
                        else:
                            recommended_items[item] = score
            
            conn.close()
            
            # مرتب‌سازی بر اساس امتیاز
            sorted_items = sorted(recommended_items.items(), key=lambda x: x[1], reverse=True)
            return [{"item": item, "score": round(score, 2)} for item, score in sorted_items[:limit]]
        except Exception as e:
            print(f"خطا در collaborative filtering: {e}")
            return []
    
    # ========== Contextual Bandit (شرایطی) ==========
    
    def get_contextual_recommendation(self, context):
        """
        توصیه بر اساس شرایط فعلی کاربر
        context: {"time": "morning/afternoon/evening", "day": "weekday/weekend", "mood": "good/bad"}
        """
        try:
            # زمان روز
            time_of_day = context.get("time", "morning")
            day_type = context.get("day", "weekday")
            mood = context.get("mood", "good")
            
            # دریافت عملکردهای قبلی در شرایط مشابه
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # امتیازدهی به بازوها بر اساس شرایط
            arm_scores = {}
            
            cursor.execute('''
                SELECT recommended_item, user_clicked, user_saved, created_at
                FROM recommendation_feedback
                WHERE user_id = ?
            ''', (self.user_id,))
            
            for row in cursor.fetchall():
                arm_id, clicked, saved, created_at = row
                
                # تعیین شرایط بر اساس زمان
                try:
                    hour = datetime.fromisoformat(created_at).hour
                    if 5 <= hour < 12:
                        cond_time = "morning"
                    elif 12 <= hour < 17:
                        cond_time = "afternoon"
                    else:
                        cond_time = "evening"
                    
                    # محاسبه امتیاز برای این بازو در شرایط فعلی
                    if cond_time == time_of_day:
                        score = clicked + (saved * 2)
                        if arm_id in arm_scores:
                            arm_scores[arm_id] += score
                        else:
                            arm_scores[arm_id] = score
                except:
                    pass
            
            conn.close()
            
            if arm_scores:
                best_arm = max(arm_scores.items(), key=lambda x: x[1])
                return {"arm_id": best_arm[0], "score": best_arm[1]}
            
            return None
        except Exception as e:
            print(f"خطا در contextual recommendation: {e}")
            return None
    
    # ========== توابع اصلی ==========
    
    def log_feedback(self, recommended_item, clicked=False, saved=False, liked=False):
        """ثبت بازخورد کاربر برای بهبود توصیه‌ها"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # بررسی وجود بازخورد قبلی
            cursor.execute('''
                SELECT id, user_clicked, user_saved, user_liked FROM recommendation_feedback
                WHERE user_id = ? AND recommended_item = ?
            ''', (self.user_id, recommended_item))
            
            existing = cursor.fetchone()
            
            if existing:
                # به‌روزرسانی
                new_clicked = existing[1] or (1 if clicked else 0)
                new_saved = existing[2] or (1 if saved else 0)
                new_liked = existing[3] or (1 if liked else 0)
                
                cursor.execute('''
                    UPDATE recommendation_feedback
                    SET user_clicked = ?, user_saved = ?, user_liked = ?, updated_at = ?
                    WHERE id = ?
                ''', (new_clicked, new_saved, new_liked, datetime.now().isoformat(), existing[0]))
            else:
                # درج جدید
                cursor.execute('''
                    INSERT INTO recommendation_feedback
                    (user_id, recommended_item, user_clicked, user_saved, user_liked, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.user_id, recommended_item, 1 if clicked else 0, 1 if saved else 0, 1 if liked else 0,
                      datetime.now().isoformat(), datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            # به‌روزرسانی Bandit Arms
            if clicked or saved or liked:
                self.update_bandit_feedback(recommended_item, True)
            
            return True
        except Exception as e:
            print(f"خطا در ثبت بازخورد: {e}")
            return False
    
    def get_personalized_recommendations(self, items_list, limit=5):
        """
        دریافت توصیه‌های شخصی‌سازی شده ترکیبی
        ترکیبی از: Bandit + Collaborative Filtering + تعاملات شخصی
        """
        recommendations = {}
        
        # 1. توصیه از Bandit (40% وزن)
        bandit_rec = self.get_bandit_recommendation()
        if bandit_rec:
            rec_key = bandit_rec["id"]
            recommendations[rec_key] = {
                "item": rec_key,
                "name": bandit_rec["name"],
                "score": bandit_rec["score"] * 0.4,
                "type": "bandit"
            }
        
        # 2. توصیه از Collaborative Filtering (30% وزن)
        cf_recs = self.get_similar_users_recommendations(3)
        for rec in cf_recs:
            if rec["item"] not in recommendations:
                recommendations[rec["item"]] = {
                    "item": rec["item"],
                    "name": self._get_item_name(rec["item"]),
                    "score": rec["score"] * 0.3,
                    "type": "collaborative"
                }
        
        # 3. توصیه از تعاملات شخصی قبلی (30% وزن)
        personal_recs = self._get_personal_history_recommendations()
        for rec in personal_recs:
            if rec["item"] not in recommendations:
                recommendations[rec["item"]] = {
                    "item": rec["item"],
                    "name": rec["name"],
                    "score": rec["score"] * 0.3,
                    "type": "personal"
                }
            else:
                recommendations[rec["item"]]["score"] += rec["score"] * 0.3
        
        # تبدیل به لیست و مرتب‌سازی
        result = list(recommendations.values())
        result.sort(key=lambda x: x["score"], reverse=True)
        
        # تکمیل با آیتم‌های پیش‌فرض اگر تعداد کافی نبود
        if len(result) < limit:
            default_items = self._get_default_items()
            for item in default_items:
                if len(result) >= limit:
                    break
                if item["item"] not in recommendations:
                    result.append(item)
        
        return result[:limit]
    
    def _get_item_name(self, item_id):
        """دریافت نام آیتم بر اساس ID"""
        names = {
            "career_medical": "🩺 مسیر پزشکی",
            "career_engineering": "💻 مسیر مهندسی کامپیوتر",
            "career_psychology": "🧠 مسیر روانشناسی",
            "career_art": "🎨 مسیر هنر",
            "study_method_pomodoro": "🍅 روش مطالعه پومودورو",
            "study_method_sq3r": "📖 روش مطالعه SQ3R",
            "study_method_feynman": "📝 روش مطالعه فاینمن",
            "challenge_easy": "😊 چالش آسان",
            "challenge_medium": "🤔 چالش متوسط",
            "challenge_hard": "💪 چالش سخت"
        }
        return names.get(item_id, item_id)
    
    def _get_personal_history_recommendations(self):
        """دریافت توصیه بر اساس تاریخچه شخصی کاربر"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT recommended_item, COUNT(*) as count
                FROM recommendation_feedback
                WHERE user_id = ? AND (user_clicked = 1 OR user_saved = 1)
                GROUP BY recommended_item
                ORDER BY count DESC
                LIMIT 5
            ''', (self.user_id,))
            
            recommendations = []
            for row in cursor.fetchall():
                recommendations.append({
                    "item": row[0],
                    "name": self._get_item_name(row[0]),
                    "score": row[1] * 10
                })
            
            conn.close()
            return recommendations
        except:
            return []
    
    def _get_default_items(self):
        """آیتم‌های پیش‌فرض برای کاربران جدید"""
        return [
            {"item": "career_medical", "name": "🩺 مسیر پزشکی", "score": 50, "type": "default"},
            {"item": "study_method_pomodoro", "name": "🍅 روش مطالعه پومودورو", "score": 48, "type": "default"},
            {"item": "challenge_medium", "name": "🤔 چالش متوسط", "score": 45, "type": "default"},
            {"item": "career_engineering", "name": "💻 مسیر مهندسی کامپیوتر", "score": 42, "type": "default"},
            {"item": "study_method_feynman", "name": "📝 روش مطالعه فاینمن", "score": 40, "type": "default"}
        ]
    
    def get_adaptive_dashboard_recommendations(self):
        """دریافت توصیه‌های برای داشبورد اصلی (شخصی‌سازی شده)"""
        # دریافت بهترین توصیه از Bandit
        best_bandit = self.get_bandit_recommendation()
        
        # دریافت توصیه‌های collaborative
        cf_recs = self.get_similar_users_recommendations(3)
        
        # دریافت توصیه‌های شخصی
        personal_recs = self._get_personal_history_recommendations()
        
        return {
            "featured": best_bandit,
            "collaborative": cf_recs[:3],
            "personal": personal_recs[:3],
            "total_interactions": len(personal_recs)
        }


# ========== توابع کمکی برای یکپارچه‌سازی ==========

def get_advanced_recommender(user_id):
    """دریافت نمونه توصیه‌گر پیشرفته"""
    return AdvancedAdaptiveRecommender(user_id)

def log_recommendation_feedback(user_id, item, clicked=False, saved=False, liked=False):
    """ثبت بازخورد توصیه"""
    recommender = AdvancedAdaptiveRecommender(user_id)
    return recommender.log_feedback(item, clicked, saved, liked)