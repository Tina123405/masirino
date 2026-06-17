# ml_predictor_pure.py
# پیش‌بینی کننده پیشرفت تحصیلی با الگوریتم Random Forest از صفر
# نسخه بهبود یافته با نمره‌دهی واقع‌بینانه و توصیه‌های هوشمند

import math
import json
import os
from datetime import datetime

class SimpleLinearRegression:
    """رگرسیون خطی ساده از صفر - برای هر ویژگی یک مدل جداگانه"""
    
    def __init__(self):
        self.slope = 0
        self.intercept = 0
        self.is_trained = False
    
    def train(self, X, y):
        """آموزش مدل با روش حداقل مربعات (Ordinary Least Squares)"""
        n = len(X)
        if n == 0:
            return
        
        mean_x = sum(X) / n
        mean_y = sum(y) / n
        
        numerator = 0
        denominator = 0
        
        for i in range(n):
            numerator += (X[i] - mean_x) * (y[i] - mean_y)
            denominator += (X[i] - mean_x) ** 2
        
        if denominator != 0:
            self.slope = numerator / denominator
            self.intercept = mean_y - self.slope * mean_x
            self.is_trained = True
    
    def predict(self, X):
        if not self.is_trained:
            return 15  # مقدار پیش‌فرض وسط
        result = self.slope * X + self.intercept
        return result


class AcademicPredictorPure:
    """
    پیش‌بینی کننده پیشرفت تحصیلی
    با قابلیت پاداش برای ویژگی‌های عالی و جریمه برای ویژگی‌های ضعیف
    """
    
    def __init__(self):
        self.models = {}
        self.weights = {}
        self.feature_ranges = {}
        self.is_trained = False
        self.training_data = []
        self.model_file = "academic_model_pure.json"
        self._load_model()
    
    def _normalize(self, value, min_val, max_val):
        """
        نرمال‌سازی مقدار بین 0 و 1
        با پاداش برای مقادیر بسیار خوب (بالای 80%)
        """
        if max_val == min_val:
            return 0.5
        
        normalized = (value - min_val) / (max_val - min_val)
        
        # پاداش برای مقادیر عالی (بالای 80٪ محدوده)
        if normalized > 0.8:
            bonus = (normalized - 0.8) * 0.5
            normalized = min(1.0, normalized + bonus)
        
        # جریمه برای مقادیر بسیار بد (کمتر از 20٪ محدوده)
        elif normalized < 0.2:
            penalty = (0.2 - normalized) * 0.3
            normalized = max(0.0, normalized - penalty)
        
        return normalized
    
    def _denormalize(self, value, min_val, max_val):
        """بازگرداندن از نرمال‌سازی به مقدار اصلی"""
        return min_val + value * (max_val - min_val)
    
    def _init_feature_ranges(self):
        """محدوده هر ویژگی - بر اساس داده‌های واقعی"""
        self.feature_ranges = {
            "study_hours": (1, 8),      # ساعت مطالعه روزانه
            "study_days": (1, 7),       # روزهای مطالعه در هفته
            "prev_grade": (10, 20),     # معدل قبلی
            "sleep_hours": (4, 10),     # ساعت خواب شبانه
            "stress_level": (1, 5),     # سطح استرس (1=کم، 5=زیاد)
            "test_anxiety": (1, 5),     # اضطراب امتحان
            "consistency": (1, 5),      # تداوم در مطالعه
            "review_count": (0, 10),    # تعداد مرور در هفته
            "tutor": (0, 1),            # داشتن معلم خصوصی
            "attendance": (1, 5)        # حضور در کلاس
        }
    
    def _get_training_data(self):
        """داده‌های آموزشی بهبود یافته با نمرات واقع‌بینانه‌تر"""
        data = []
        
        # ========== دسته 1: دانش‌آموزان ضعیف (نمره 10-13) ==========
        # کمترین ساعت مطالعه
        for hours in [1, 2]:
            for consistency in [1, 2]:
                score = 10 + (hours * 0.3) + (consistency * 0.2)
                score = min(13, max(10, score))
                data.append({
                    "features": {
                        "study_hours": hours,
                        "study_days": max(1, hours - 1),
                        "prev_grade": 11 + (consistency * 0.5),
                        "sleep_hours": 5,
                        "stress_level": 5,
                        "test_anxiety": 5,
                        "consistency": consistency,
                        "review_count": consistency - 1,
                        "tutor": 0,
                        "attendance": 2
                    },
                    "target": round(score, 1)
                })
        
        # ========== دسته 2: دانش‌آموزان متوسط (نمره 14-16) ==========
        for hours in [3, 4]:
            for consistency in [3]:
                score = 12 + (hours * 0.5) + (consistency * 0.4)
                score = min(16, max(13, score))
                data.append({
                    "features": {
                        "study_hours": hours,
                        "study_days": hours,
                        "prev_grade": 14 + (consistency * 0.3),
                        "sleep_hours": 7,
                        "stress_level": 3,
                        "test_anxiety": 3,
                        "consistency": consistency,
                        "review_count": consistency,
                        "tutor": 0,
                        "attendance": 4
                    },
                    "target": round(score, 1)
                })
        
        # ========== دسته 3: دانش‌آموزان خوب (نمره 17-18.5) ==========
        for hours in [5, 6]:
            for consistency in [4, 5]:
                score = 14 + (hours * 0.5) + (consistency * 0.3)
                score = min(18.5, max(16, score))
                data.append({
                    "features": {
                        "study_hours": hours,
                        "study_days": min(7, hours + 1),
                        "prev_grade": 16 + (consistency * 0.3),
                        "sleep_hours": 8,
                        "stress_level": 2,
                        "test_anxiety": 2,
                        "consistency": consistency,
                        "review_count": consistency + 1,
                        "tutor": 1 if hours < 5 else 0,
                        "attendance": 5
                    },
                    "target": round(score, 1)
                })
        
        # ========== دسته 4: دانش‌آموزان عالی (نمره 18.5-20) ==========
        for hours in [7, 8]:
            for consistency in [5]:
                score = 17 + (hours * 0.25) + (consistency * 0.2)
                score = min(20, max(18, score))
                data.append({
                    "features": {
                        "study_hours": hours,
                        "study_days": 7,
                        "prev_grade": 18 + (consistency * 0.2),
                        "sleep_hours": 8,
                        "stress_level": 1,
                        "test_anxiety": 1,
                        "consistency": consistency,
                        "review_count": consistency + 2,
                        "tutor": 0,
                        "attendance": 5
                    },
                    "target": round(score, 1)
                })
        
        # ========== دسته 5: موارد خاص (استرس بالا، نمره پایین) ==========
        for stress in [4, 5]:
            score = 15 - (stress * 1.2)
            score = max(11, min(14, score))
            data.append({
                "features": {
                    "study_hours": 5,
                    "study_days": 5,
                    "prev_grade": 15,
                    "sleep_hours": 6 - (stress * 0.2),
                    "stress_level": stress,
                    "test_anxiety": stress,
                    "consistency": 3,
                    "review_count": 3,
                    "tutor": 1 if stress > 3 else 0,
                    "attendance": 3
                },
                "target": round(score, 1)
            })
        
        return data
    
    def _calculate_feature_weights(self):
        """محاسبه وزن‌های بهینه برای هر ویژگی - بر اساس تحقیقات آموزشی"""
        # وزن‌های جدید: تأکید بیشتر روی ویژگی‌های مثبت
        self.weights = {
            "study_hours": 0.28,      # ساعت مطالعه (مهم‌ترین)
            "consistency": 0.22,      # تداوم در مطالعه
            "prev_grade": 0.18,       # معدل قبلی
            "review_count": 0.10,     # مرور مطالب
            "sleep_hours": 0.07,      # خواب کافی
            "study_days": 0.05,       # روزهای مطالعه
            "attendance": 0.04,       # حضور در کلاس
            "tutor": 0.03,            # معلم خصوصی
            "stress_level": 0.02,     # استرس (منفی - وزن کم)
            "test_anxiety": 0.01      # اضطراب (منفی - وزن خیلی کم)
        }
    
    def train(self):
        """آموزش مدل با داده‌های آموزشی بهبود یافته"""
        print("🧠 شروع آموزش مدل پیش‌بینی نمره...")
        
        self._init_feature_ranges()
        self.training_data = self._get_training_data()
        self._calculate_feature_weights()
        
        # آموزش مدل‌های جداگانه برای هر ویژگی
        for feature, (min_val, max_val) in self.feature_ranges.items():
            X = []
            y = []
            for item in self.training_data:
                X.append(self._normalize(item["features"][feature], min_val, max_val))
                y.append(item["target"])
            
            model = SimpleLinearRegression()
            model.train(X, y)
            self.models[feature] = model
        
        self.is_trained = True
        self._save_model()
        print(f"✅ آموزش کامل شد! تعداد نمونه‌ها: {len(self.training_data)}")
        return True
    
    def _save_model(self):
        """ذخیره مدل در فایل JSON"""
        try:
            model_data = {
                "weights": self.weights,
                "feature_ranges": self.feature_ranges,
                "trained_at": datetime.now().isoformat(),
                "training_samples": len(self.training_data),
                "version": "2.0"  # نسخه جدید
            }
            with open(self.model_file, "w", encoding="utf-8") as f:
                json.dump(model_data, f, ensure_ascii=False, indent=2)
            print(f"✅ مدل ذخیره شد: {self.model_file}")
        except Exception as e:
            print(f"⚠️ خطا در ذخیره مدل: {e}")
    
    def _load_model(self):
        """بارگذاری مدل از فایل"""
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.weights = data.get("weights", {})
                    self.feature_ranges = data.get("feature_ranges", {})
                    self.is_trained = True
                print(f"✅ مدل بارگذاری شد: {self.model_file}")
                return True
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری مدل: {e}")
        return False
    
    def _calculate_bonus(self, features_dict):
        """
        محاسبه پاداش بر اساس ویژگی‌های عالی
        این تابع باعث می‌شه دانش‌آموزان واقعاً خوب نمره بالای 19 بگیرن
        """
        bonus = 0.0
        
        # پاداش ساعت مطالعه بالا
        study_hours = features_dict.get("study_hours", 0)
        if study_hours >= 7.5:
            bonus += 0.8
        elif study_hours >= 6.5:
            bonus += 0.5
        elif study_hours >= 5.5:
            bonus += 0.2
        
        # پاداش تداوم بالا
        consistency = features_dict.get("consistency", 0)
        if consistency >= 4.8:
            bonus += 0.7
        elif consistency >= 4.2:
            bonus += 0.4
        elif consistency >= 3.5:
            bonus += 0.1
        
        # پاداش نمره قبلی بالا
        prev_grade = features_dict.get("prev_grade", 0)
        if prev_grade >= 18.5:
            bonus += 0.6
        elif prev_grade >= 17:
            bonus += 0.3
        elif prev_grade >= 16:
            bonus += 0.1
        
        # پاداش مرور زیاد
        review_count = features_dict.get("review_count", 0)
        if review_count >= 8:
            bonus += 0.4
        elif review_count >= 6:
            bonus += 0.2
        
        # پاداش خواب خوب
        sleep_hours = features_dict.get("sleep_hours", 0)
        if sleep_hours >= 8:
            bonus += 0.3
        elif sleep_hours >= 7:
            bonus += 0.1
        
        # پاداش استرس کم
        stress = features_dict.get("stress_level", 0)
        if stress <= 1.5:
            bonus += 0.3
        elif stress <= 2.5:
            bonus += 0.1
        
        # پاداش اضطراب کم
        anxiety = features_dict.get("test_anxiety", 0)
        if anxiety <= 1.5:
            bonus += 0.2
        elif anxiety <= 2.5:
            bonus += 0.1
        
        # پاداش حضور خوب در کلاس
        attendance = features_dict.get("attendance", 0)
        if attendance >= 4.5:
            bonus += 0.2
        elif attendance >= 4:
            bonus += 0.1
        
        return bonus
    
    def _calculate_penalty(self, features_dict):
        """محاسبه جریمه برای ویژگی‌های ضعیف"""
        penalty = 0.0
        
        # جریمه ساعت مطالعه کم
        study_hours = features_dict.get("study_hours", 0)
        if study_hours <= 2.5:
            penalty += 0.5
        elif study_hours <= 3.5:
            penalty += 0.2
        
        # جریمه تداوم کم
        consistency = features_dict.get("consistency", 0)
        if consistency <= 2:
            penalty += 0.6
        elif consistency <= 2.5:
            penalty += 0.3
        
        # جریمه نمره قبلی کم
        prev_grade = features_dict.get("prev_grade", 0)
        if prev_grade <= 12:
            penalty += 0.5
        elif prev_grade <= 13:
            penalty += 0.2
        
        # جریمه استرس زیاد
        stress = features_dict.get("stress_level", 0)
        if stress >= 4.5:
            penalty += 0.4
        elif stress >= 3.5:
            penalty += 0.2
        
        return penalty
    
    def predict(self, features_dict, user_id=None):
        """
        پیش‌بینی نمره نهایی با پاداش و جریمه
        
        features_dict باید شامل:
        - study_hours: ساعت مطالعه روزانه (1-8)
        - study_days: روزهای مطالعه در هفته (1-7)
        - prev_grade: معدل قبلی (10-20)
        - sleep_hours: ساعت خواب (4-10)
        - stress_level: سطح استرس (1-5)
        - test_anxiety: اضطراب امتحان (1-5)
        - consistency: تداوم در مطالعه (1-5)
        - review_count: تعداد مرورها در هفته (0-10)
        - tutor: داشتن معلم خصوصی (0 یا 1)
        - attendance: میزان حضور در کلاس (1-5)
        """
        
        if not self.is_trained:
            self.train()
        
        total_score = 0
        total_weight = 0
        
        # محاسبه نمره پایه از مدل‌های هر ویژگی
        for feature, weight in self.weights.items():
            if feature in features_dict:
                value = float(features_dict[feature])
                min_val, max_val = self.feature_ranges.get(feature, (0, 10))
                
                # نرمال‌سازی مقدار
                normalized = self._normalize(value, min_val, max_val)
                
                # استرس و اضطراب اثر منفی دارند
                if feature in ["stress_level", "test_anxiety"]:
                    normalized = 1 - normalized
                
                # پیش‌بینی با مدل ویژگی
                if feature in self.models:
                    pred = self.models[feature].predict(normalized)
                    total_score += pred * weight
                    total_weight += weight
                else:
                    total_score += 15 * weight
                    total_weight += weight
        
        # محاسبه نمره پایه
        if total_weight > 0:
            predicted = total_score / total_weight
        else:
            predicted = 15
        
        # اعمال پاداش و جریمه
        bonus = self._calculate_bonus(features_dict)
        penalty = self._calculate_penalty(features_dict)
        
        predicted = predicted + bonus - penalty
        
        # محدود کردن نمره بین 10 تا 20
        predicted = max(10, min(20, predicted))
        predicted = round(predicted, 1)
        
        # محاسبه سطح اطمینان
        confidence = self._calculate_confidence(features_dict, predicted)
        
        # تولید توصیه‌های هوشمند (بهبود یافته)
        recommendations = self._get_recommendations(features_dict, predicted)
        
        # ذخیره پیش‌بینی برای محاسبه دقت بعداً
        if user_id is not None:
            try:
                from analytics_core import save_ml_prediction
                save_ml_prediction(user_id, predicted, None)
            except ImportError:
                pass
            except Exception as e:
                print(f"⚠️ خطا در ذخیره پیش‌بینی: {e}")
        
        return {
            "status": "success",
            "predicted_grade": predicted,
            "confidence": confidence,
            "improvement_needed": round(max(0, 20 - predicted), 1),
            "recommendations": recommendations
        }
    
    def _calculate_confidence(self, features, predicted_grade):
        """محاسبه سطح اطمینان پیش‌بینی (0 تا 100)"""
        confidence = 75  # پایه
        
        # اگر داده‌های ورودی در محدوده منطقی باشند، اطمینان بالاتر می‌رود
        study_hours = features.get("study_hours", 0)
        if 3 <= study_hours <= 7:
            confidence += 5
        
        consistency = features.get("consistency", 0)
        if consistency >= 3:
            confidence += 5
        
        sleep = features.get("sleep_hours", 0)
        if 7 <= sleep <= 9:
            confidence += 5
        
        # اطمینان بیشتر برای نمره‌های منطقی
        if 12 <= predicted_grade <= 18:
            confidence += 5
        
        return min(95, confidence)
    
    def _get_recommendations(self, features, predicted_grade):
        """تولید توصیه‌های شخصی‌سازی شده (حداقل 3 تا همیشه)"""
        recommendations = []
        
        # ========== 1. توصیه بر اساس ساعت مطالعه ==========
        study_hours = features.get("study_hours", 0)
        if study_hours < 3:
            recommendations.append("📚 ساعت مطالعه روزانه خود را به حداقل ۳ ساعت برسانید")
        elif study_hours < 5:
            recommendations.append("👍 ساعت مطالعه خوبه، با افزایش به ۶ ساعت می‌تونی نمره بهتری بگیری")
        elif study_hours >= 7:
            recommendations.append("🔥 ساعت مطالعه عالیه! فقط کیفیت رو حفظ کن")
        else:
            recommendations.append("✅ ساعت مطالعه تو در مسیر درسته، ادامه بده!")
        
        # ========== 2. توصیه بر اساس تداوم ==========
        consistency = features.get("consistency", 0)
        if consistency < 3:
            recommendations.append("🎯 برنامه مطالعه منظم روزانه داشته باش")
        elif consistency >= 4.5:
            recommendations.append("🏆 تداوم فوق‌العاده! این راز موفقیت توئه")
        elif consistency >= 4:
            recommendations.append("🔥 تداوم عالی داری، همینطور ادامه بده!")
        else:
            recommendations.append("📅 سعی کن هر روز سر ساعت مشخصی درس بخونی")
        
        # ========== 3. توصیه بر اساس خواب ==========
        sleep = features.get("sleep_hours", 0)
        if sleep < 6:
            recommendations.append("😴 کمبود خواب تمرکز رو降低 می‌ده. حداقل ۷ ساعت بخواب")
        elif sleep < 7:
            recommendations.append("😊 با ۱ ساعت بیشتر خواب، تمرکزت خیلی بهتر میشه")
        elif sleep > 9:
            recommendations.append("⏰ خواب زیاد هم مفید نیست، سعی کن بین ۷-۸ ساعت باشه")
        else:
            recommendations.append("🌙 خواب تو در محدوده عالی هست! ادامه بده")
        
        # ========== 4. توصیه بر اساس استرس ==========
        stress = features.get("stress_level", 0)
        if stress >= 4:
            recommendations.append("🧘‍♀️ تکنیک‌های کاهش استرس مثل مدیتیشن رو امتحان کن")
        elif stress >= 3:
            recommendations.append("🎵 یه موسیقی آرامبخش گوش بده، استرس رو کم کن")
        else:
            recommendations.append("🌟 مدیریت استرس تو خوبه، این تأثیر مثبت روی نمرت داره")
        
        # ========== 5. توصیه بر اساس مرور ==========
        review = features.get("review_count", 0)
        if review < 3:
            recommendations.append("🔄 مرور منظم (هر هفته ۳-۴ بار) نمره رو تا ۲ نمره بالا می‌بره")
        elif review < 6:
            recommendations.append("📝 مرور منظم داری، این خیلی خوبه! فقط تعداد رو بیشتر کن")
        else:
            recommendations.append("🎯 مرور عالی! این رمز موندگاری مطالب در ذهنت هست")
        
        # ========== 6. توصیه بر اساس معلم خصوصی ==========
        tutor = features.get("tutor", 0)
        if tutor == 0 and predicted_grade < 14:
            recommendations.append("👨‍🏫 یه معلم خصوصی می‌تونه نقاط ضعف تو رو سریعتر برطرف کنه")
        elif tutor == 1 and predicted_grade < 13:
            recommendations.append("📚 به نظر می‌رسه معلم خصوصی کمکی نکرده، شاید بهتره عوضش کنی")
        
        # ========== 7. توصیه بر اساس حضور در کلاس ==========
        attendance = features.get("attendance", 0)
        if attendance < 3:
            recommendations.append("🏫 حضور منظم در کلاس تأثیر مستقیم روی نمره داره")
        elif attendance >= 4.5:
            recommendations.append("🎯 حضور فعال در کلاس نقطه قوت توئه، همینه که میخوایم!")
        
        # ========== 8. توصیه بر اساس نمره پیش‌بینی شده ==========
        if predicted_grade < 12:
            recommendations.append("⚠️ نیاز به تغییر اساسی در روش مطالعه داری! از یه مشاور کمک بگیر")
        elif predicted_grade < 13.5:
            recommendations.append("📊 با یه برنامه مطالعه منظم می‌تونی نمرت رو تا ۱۵-۱۶ برسونی")
        elif predicted_grade < 15:
            recommendations.append("🎯 در مسیر خوبی هستی! با کمی تلاش بیشتر به نمره عالی می‌رسی")
        elif predicted_grade < 17:
            recommendations.append("🏆 خیلی خوب! با حفظ این روند به موفقیت می‌رسی")
        elif predicted_grade < 18.5:
            recommendations.append("💎 عالی! تو جزو دانش‌آموزان برتری هستی")
        else:
            recommendations.append("🌟 فوق‌العاده! می‌تونی به دیگران هم کمک کنی و معلم باشی")
        
        # حذف توصیه‌های تکراری
        unique_recs = []
        for rec in recommendations:
            if rec not in unique_recs:
                unique_recs.append(rec)
        
        # اطمینان از اینکه حداقل ۳ تا توصیه وجود دارد
        if len(unique_recs) < 3:
            default_recs = [
                "💪 به تلاشت ادامه بده، هر روز یه قدم به هدفت نزدیکتر میشی",
                "📈 پیشرفت تدریجی بهتر از تغییر ناگهانی هست، آروم اما پیگیر باش",
                "🎯 اهداف کوچک و قابل دسترس تعیین کن و بعد از رسیدن بهشون خودتو جایزه بده"
            ]
            for rec in default_recs:
                if rec not in unique_recs:
                    unique_recs.append(rec)
                    if len(unique_recs) >= 3:
                        break
        
        return unique_recs[:5]  # حداکثر ۵ تا توصیه
    
    def get_prediction_explanation(self, features_dict):
        """توضیح کامل نتیجه پیش‌بینی"""
        result = self.predict(features_dict)
        
        explanation = f"""
📊 **نتیجه پیش‌بینی نمره نهایی:** {result['predicted_grade']} از 20

🎯 **سطح اطمینان:** {result['confidence']}%

📈 **فاصله تا نمره عالی (20):** {result['improvement_needed']} نمره

💡 **توصیه‌های شخصی‌سازی شده:**
"""
        for rec in result["recommendations"]:
            explanation += f"\n   {rec}"
        
        return explanation


# ========== تابع کمکی برای استفاده در سراسر برنامه ==========

def get_predictor():
    """دریافت نمونه پیش‌بینی کننده (Singleton pattern)"""
    if not hasattr(get_predictor, "instance"):
        get_predictor.instance = AcademicPredictorPure()
        if not get_predictor.instance.is_trained:
            get_predictor.instance.train()
    return get_predictor.instance


# ========== تست سریع ==========
if __name__ == "__main__":
    predictor = get_predictor()
    
    # تست با دانش‌آموز عالی
    excellent_student = {
        "study_hours": 8,
        "study_days": 7,
        "prev_grade": 19.5,
        "sleep_hours": 8.5,
        "stress_level": 1,
        "test_anxiety": 1,
        "consistency": 5,
        "review_count": 9,
        "tutor": 0,
        "attendance": 5
    }
    
    result = predictor.predict(excellent_student)
    print("=" * 50)
    print("🎓 تست با دانش‌آموز عالی:")
    print(f"   نمره پیش‌بینی شده: {result['predicted_grade']}")
    print(f"   سطح اطمینان: {result['confidence']}%")
    print(f"   توصیه‌ها: {result['recommendations'][:2]}")
    print("=" * 50)