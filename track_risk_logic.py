import re
import json
import random
import hashlib
import urllib.parse
import urllib.request
from functools import lru_cache
from difflib import SequenceMatcher
from collections import deque
from html import escape
from datetime import datetime, timedelta
import logging
import secrets
import os
import shutil
import zipfile
import random
from collections import deque
from chatbot_knowledge import CHATBOT_KNOWLEDGE
from config import *
from careers_data import RESOURCE_SUGGESTIONS, CAREERS_BY_TRACK

logger = logging.getLogger(__name__)

# ========== کش و حافظه موقت ==========
RESULT_STORE = {}
CHAT_HISTORY = {}
SESSION_STORE = {}
CACHE_ONLINE = {}

# ========== توابع کمکی ==========
def text_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def normalize_text(text: str) -> str:
    text = (text or "").lower().strip()
    replacements = {
        "سلوم": "سلام", "سلااام": "سلام", "سلامم": "سلام", "سلم": "سلام",
        "دروود": "درود", "مرسیی": "مرسی", "ممنونن": "ممنون",
        "خوبیی": "خوبی", "خوبین": "خوبی", "چطوریی": "چطوری", "چطورر": "چطور",
        "مرسیی": "مرسی", "ممنونن": "ممنون", "ممنونم": "ممنون",
        "س": "سلام", "سا": "سلام", "سلا": "سلام", "السلام": "سلام",
        "سلامت": "سلام", "سلامی": "سلام", "سلام علیکم": "سلام",
        "سلام چطوری": "سلام", "سلام خوبی": "سلام", "سلام سلام": "سلام",
        "خوبی چطوری": "سلام", "چطوری خوبی": "سلام",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r'[ًٌٍَُِّّ]', '', text)
    return text

def typo_fix(text: str) -> str:
    common = {
        "سلم": "سلام", "سلوم": "سلام", "رشتع": "رشته", "مطالع": "مطالعه",
        "فیزک": "فیزیک", "ریاظی": "ریاضی", "استر": "استرس", "امحتان": "امتحان",
        "زیس": "زیست", "ادبیاتت": "ادبیات", "شغول": "شغل", "آينده": "آینده",
        "مدرسه": "مدرسه", "کلاس": "کلاس", "کتاب": "کتاب", "معلم": "معلم",
        "دبیرستان": "دبیرستان", "دانشگاه": "دانشگاه", "کنکور": "کنکور",
    }
    for wrong, right in common.items():
        text = text.replace(wrong, right)
    return text

def token_bag(text: str) -> set:
    return set(re.findall(r"[آ-یa-zA-Z0-9]+", text))

def bag_similarity(a: str, b: str) -> float:
    ta = token_bag(a)
    tb = token_bag(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)

def syn_expand(text: str) -> str:
    synonyms = {
        "درس": ["مطالعه", "یادگیری", "آموزش"],
        "رشته": ["مسیر", "گرایش", "شاخه"],
        "شغل": ["کار", "حرفه", "پیشه"],
        "آینده": ["بعد", "بعداً", "آتی"],
        "استرس": ["اضطراب", "نگرانی", "فشار"],
        "تمرکز": ["دقت", "حواس", "توجه"],
        "برنامه": ["روتین", "زمان‌بندی", "نقشه"],
        "خوب": ["عالی", "مرسی", "اوکی"],
        "مدرسه": ["آموزشگاه", "دبیرستان", "دبستان"],
        "کلاس": ["جلسه", "تدریس", "درس"],
        "کتاب": ["منبع", "جزوه", "کتاب درسی"],
        "معلم": ["دبیر", "استاد", "آموزگار"],
    }
    words = set([text])
    for k, vals in synonyms.items():
        if k in text:
            words.update(vals)
    return " ".join(words)

def detect_language(text):
    persian_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF' or c in 'ی ک گ چ پ ژ')
    english_chars = sum(1 for c in text if 'a' <= c.lower() <= 'z')
    if persian_chars > english_chars:
        return "fa"
    return "en"

def simple_translate_to_english(text):
    translations = {
        "سلام": "Hello", "خوبم": "I'm fine", "ممنون": "Thanks", "خداحافظ": "Goodbye",
        "بله": "Yes", "خیر": "No", "لطفا": "Please", "مشاور": "Consultant",
        "تحصیلی": "Educational", "رشته": "Major", "درس": "Lesson", "امتحان": "Exam",
        "کمک": "Help", "سوال": "Question", "پاسخ": "Answer", "خوبی": "How are you",
        "چطوری": "How are you", "خوب": "Good", "عالی": "Excellent", "مرسی": "Thanks",
        "دانشگاه": "University", "دانش آموز": "Student", "معلم": "Teacher",
        "مدرسه": "School", "کلاس": "Class", "کتاب": "Book", "نمره": "Grade",
        "زیست": "Biology", "شیمی": "Chemistry", "فیزیک": "Physics", "ریاضی": "Math",
        "ادبیات": "Literature", "تاریخ": "History", "جغرافیا": "Geography",
    }
    result = text
    for persian, english in translations.items():
        if persian in result:
            result = result.replace(persian, english)
    if any('\u0600' <= c <= '\u06FF' for c in result):
        result = "Hello! I am Kharazmi, your educational consultant. How can I help you?"
    return result

def simple_translate_to_persian(text):
    translations = {
        "Hello": "سلام", "Hi": "سلام", "Hey": "سلام", "Good": "خوب", "Excellent": "عالی",
        "Thanks": "ممنون", "Thank you": "ممنون", "Goodbye": "خداحافظ", "Bye": "خداحافظ",
        "Yes": "بله", "No": "خیر", "Please": "لطفا", "Help": "کمک", "Question": "سوال",
        "School": "مدرسه", "Class": "کلاس", "Book": "کتاب", "Teacher": "معلم", "Grade": "نمره",
        "Biology": "زیست", "Chemistry": "شیمی", "Physics": "فیزیک", "Math": "ریاضی",
        "Literature": "ادبیات", "History": "تاریخ", "Geography": "جغرافیا",
    }
    result = text
    for english, persian in translations.items():
        if english.lower() in result.lower():
            result = re.sub(english, persian, result, flags=re.IGNORECASE)
    return result

def is_inappropriate(text: str) -> bool:
    text = text.lower()
    for pattern in INAPPROPRIATE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

def get_inappropriate_response() -> str:
    return random.choice([
        "🙏 متأسفانه نمی‌توانم در مورد این موضوع صحبت کنم. لطفاً سوال دیگری بپرسید.",
        "📚 من مشاور تحصیلی هستم و فقط در زمینه‌های آموزشی می‌توانم کمک کنم.",
        "🎯 لطفاً سوالتان را درباره درس، رشته یا برنامه‌ریزی بپرسید.",
        "🧠 تمرکز من روی موضوعات تحصیلی، شغل و موفقیت است.",
        "🔞 این سوال در حوزه تخصصی من نیست. لطفاً سوال تحصیلی بپرسید."
    ])

def build_context(message: str) -> str:
    message = normalize_text(message)
    message = typo_fix(message)
    message = message.replace("‌", " ")
    message = syn_expand(message)
    return message

def calculate_confidence(data_points, weights=None):
    if not data_points:
        return 0.0
    if weights is None:
        weights = [1.0] * len(data_points)
    weighted_sum = sum(d * w for d, w in zip(data_points, weights))
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    confidence = (weighted_sum / total_weight) * 100
    return min(100, max(0, round(confidence, 1)))

def advanced_sentiment_analysis(text):
    text = text.lower()
    score = 0
    positive_count = 0
    negative_count = 0
    stress_count = 0
    motivation_count = 0
    
    for word in POSITIVE_WORDS:
        if word in text:
            positive_count += 1
            score += 2
    
    for word in NEGATIVE_WORDS:
        if word in text:
            negative_count += 1
            score -= 3
    
    for word in STRESS_WORDS:
        if word in text:
            stress_count += 1
            score -= 2
    
    for word in MOTIVATION_WORDS:
        if word in text:
            motivation_count += 1
            score += 1
    
    if stress_count > 0:
        return "stressed", score, f"💙 سطح استرس: {min(100, stress_count * 30)}%", stress_count
    elif negative_count > positive_count:
        return "sad", score, "🌸 ناراحت هستی؟ بیا با هم حرف بزنیم", negative_count
    elif motivation_count > 0:
        return "motivated", score, "🔥 انرژی عالی! همینطور ادامه بده", motivation_count
    elif positive_count > 0:
        return "happy", score, "😊 چه خوب! خوشحالم که حالت خوبه", positive_count
    else:
        return "neutral", score, "", 0

def normalize_rating(x: float) -> float:
    if x is None:
        return 0.0
    try:
        return (float(x) - 1) / 4.0
    except:
        return 0.0

def grade_category(grade_level: str) -> str:
    return "basic" if grade_level in ["ابتدایی", "هفتم-نهم"] else "advanced"

def safe_key(text: str) -> str:
    return text.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")

def color_for_percent(p: float) -> str:
    if p >= 75:
        return "#10b981"
    if p >= 45:
        return "#f59e0b"
    return "#ef4444"

@lru_cache(maxsize=256)
def cached_compute_subject_score(understanding, performance, interest):
    understanding_n = (understanding - 1) / 4.0
    performance_n = (performance - 1) / 4.0
    interest_n = (interest - 1) / 4.0
    return {
        "ability_score": (understanding_n + performance_n) / 2,
        "interest_score": interest_n,
        "total": 0.35 * understanding_n + 0.45 * performance_n + 0.20 * interest_n
    }

def compute_subject_score_full(subject_data: dict) -> dict:
    understanding = normalize_rating(subject_data.get("understanding", 3))
    performance = normalize_rating(subject_data.get("performance", 3))
    interest = normalize_rating(subject_data.get("interest", 3))
    ability_score = (understanding + performance) / 2
    return {
        "ability_score": ability_score,
        "interest_score": interest,
        "understanding": understanding,
        "performance": performance,
        "interest": interest,
        "total": 0.35 * understanding + 0.45 * performance + 0.20 * interest
    }

def smart_online_search(query: str) -> str:
    if query in CACHE_ONLINE:
        return CACHE_ONLINE[query]
    try:
        url = f"https://fa.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "KharazmiBot/1.0 (Educational Assistant)"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            if "extract" in data and data["extract"]:
                result = f"📚 بر اساس دانشنامه ویکی‌پدیا:\n\n{data['extract'][:500]}..."
                if len(data.get("extract", "")) > 500:
                    result += "\n\n🔗 برای اطلاعات بیشتر می‌توانید جستجوی بیشتری انجام دهید."
                CACHE_ONLINE[query] = result
                return result
    except Exception as e:
        logger.error(f"خطا در جستجوی ویکی‌پدیا: {e}")
    
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "KharazmiBot/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            if data.get("AbstractText"):
                result = f"🌐 اطلاعات از DuckDuckGo:\n\n{data['AbstractText'][:500]}..."
                CACHE_ONLINE[query] = result
                return result
            elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                first = data["RelatedTopics"][0]
                if "Text" in first:
                    result = f"🌐 اطلاعات مرتبط:\n\n{first['Text'][:400]}..."
                    CACHE_ONLINE[query] = result
                    return result
    except Exception as e:
        logger.error(f"خطا در جستجوی DuckDuckGo: {e}")
    return None

def compute_risk_fall_detailed(payload: dict) -> dict:
    study_mode = payload.get("study_mode", "منظم")
    mode_risk = 1.0 if study_mode == "ضربتی" else (0.6 if study_mode == "نیمه‌منظم" else 0.25)
    
    has_review = payload.get("has_review", "دارم (منظم)")
    review_risk = 1.0 if has_review == "تقریباً نه" else (0.6 if has_review == "بعضی وقت‌ها" else 0.25)
    
    sleep_status = payload.get("sleep_status", "خوب")
    sleep_risk = 1.0 if sleep_status == "کم" else (0.6 if sleep_status == "متوسط" else 0.25)
    
    distract_rating = float(payload.get("distract_rating", 3))
    focus_risk = normalize_rating(distract_rating)
    
    start_days = payload.get("start_days_before_exam", "30+")
    if start_days == "از روز امتحان!":
        start_risk = 1.0
    elif start_days == "3–7":
        start_risk = 0.8
    elif start_days == "10–20":
        start_risk = 0.5
    else:
        start_risk = 0.2
    
    stress_rating = float(payload.get("stress_rating", 3))
    stress_risk = normalize_rating(stress_rating)
    
    can_execute = float(payload.get("can_execute_plan", 3))
    exec_risk = 1.0 - normalize_rating(can_execute)
    
    has_tutor = payload.get("has_tutor", "ندارم")
    tutor_protect = 0.7 if has_tutor == "دارم (کلاس/معلم خصوصی)" else (0.35 if has_tutor == "تا حدی" else 0.1)
    
    weakness_map = {
        "محاسباتی / تمرین": 1.0,
        "مفهومی (درک)": 0.8,
        "تشریحی / نگارش": 0.7,
        "زمان کم می‌آورم": 0.85,
        "بی‌دقتی": 0.75,
    }
    weakness_risk = weakness_map.get(payload.get("main_weakness_area", "محاسباتی / تمرین"), 0.7)
    
    study_hours = float(payload.get("study_hours_rating", 3))
    hours_risk = 1.0 - normalize_rating(study_hours)
    
    family_support = payload.get("family_support", "خوب")
    family_risk = 0.5 if family_support == "ضعیف" else (0.3 if family_support == "متوسط" else 0.1)
    
    previous_fail = payload.get("previous_fail", "ندارم")
    fail_risk = 0.6 if previous_fail == "دارم" else 0.1
    
    test_anxiety = float(payload.get("test_anxiety", 3))
    anxiety_risk = normalize_rating(test_anxiety)
    
    risk_raw = (0.16 * mode_risk + 0.11 * review_risk + 0.10 * sleep_risk +
                0.10 * focus_risk + 0.10 * start_risk + 0.08 * stress_risk +
                0.08 * exec_risk + 0.07 * weakness_risk + 0.07 * hours_risk +
                0.05 * family_risk + 0.04 * fail_risk + 0.04 * anxiety_risk)
    
    risk_raw = max(0.0, min(1.0, risk_raw - 0.12 * tutor_protect))
    risk_percent = round(risk_raw * 100, 1)
    
    if risk_raw >= 0.75:
        bucket = "بالا"
        level_text = "شدید"
        level_color = "#ef4444"
        advice = "⚠️ فوری اقدام کنید! احتمال افت نمره بسیار بالاست. حتماً از یک مشاور کمک بگیرید."
        recommendation = "برنامه فشرده و روزانه با نظارت والدین"
        alert_level = "danger"
    elif risk_raw >= 0.55:
        bucket = "متوسط"
        level_text = "متوسط"
        level_color = "#f59e0b"
        advice = "📌 نیاز به اصلاح عادات مطالعه دارید. با یک برنامه منظم می‌توانید پیشرفت کنید."
        recommendation = "روزانه ۲-۳ ساعت مطالعه هدفمند با برنامه ریزی"
        alert_level = "warning"
    elif risk_raw >= 0.35:
        bucket = "قابل قبول"
        level_text = "قابل قبول"
        level_color = "#10b981"
        advice = "✅ در مسیر نسبتاً خوبی هستید، اما قابل بهبود. نکات مطالعه را جدی بگیرید."
        recommendation = "مرور منظم و رفع اشکالات جزئی"
        alert_level = "info"
    else:
        bucket = "کم"
        level_text = "کم"
        level_color = "#10b981"
        advice = "🎉 وضعیت عالی دارید! همین روال را ادامه دهید و برای پیشرفت بیشتر تلاش کنید."
        recommendation = "حفظ روال فعلی و افزایش تدریجی زمان مطالعه"
        alert_level = "success"
    
    return {
        "risk": risk_raw,
        "risk_percent": risk_percent,
        "bucket": bucket,
        "level_text": level_text,
        "level_color": level_color,
        "advice": advice,
        "recommendation": recommendation,
        "study_mode": study_mode,
        "sleep_status": sleep_status,
        "stress_level": stress_rating,
        "alert_level": alert_level
    }

def risk_breakdown_detailed(payload: dict) -> dict:
    study_mode = payload.get("study_mode", "منظم")
    mode_score = 1.0 - (1.0 if study_mode == "ضربتی" else (0.6 if study_mode == "نیمه‌منظم" else 0.25))
    
    has_review = payload.get("has_review", "دارم (منظم)")
    review_score = 1.0 - (1.0 if has_review == "تقریباً نه" else (0.6 if has_review == "بعضی وقت‌ها" else 0.25))
    
    sleep_status = payload.get("sleep_status", "خوب")
    sleep_score = 1.0 - (1.0 if sleep_status == "کم" else (0.6 if sleep_status == "متوسط" else 0.25))
    
    distract_rating = float(payload.get("distract_rating", 3))
    focus_score = 1.0 - normalize_rating(distract_rating)
    
    stress_rating = float(payload.get("stress_rating", 3))
    stress_score = 1.0 - normalize_rating(stress_rating)
    
    can_execute = float(payload.get("can_execute_plan", 3))
    exec_score = normalize_rating(can_execute)
    
    study_hours = float(payload.get("study_hours_rating", 3))
    hours_score = normalize_rating(study_hours)
    
    start_days = payload.get("start_days_before_exam", "30+")
    if start_days == "از روز امتحان!":
        start_score = 0
    elif start_days == "3–7":
        start_score = 0.3
    elif start_days == "10–20":
        start_score = 0.6
    else:
        start_score = 0.9
    
    weakness_map = {
        "محاسباتی / تمرین": 0.2,
        "مفهومی (درک)": 0.4,
        "تشریحی / نگارش": 0.5,
        "زمان کم می‌آورم": 0.3,
        "بی‌دقتی": 0.4,
    }
    weakness_score = weakness_map.get(payload.get("main_weakness_area", "محاسباتی / تمرین"), 0.4)
    
    family_support = payload.get("family_support", "خوب")
    family_score = 0.8 if family_support == "خوب" else (0.5 if family_support == "متوسط" else 0.2)
    
    return {
        "نظم و برنامه‌ریزی": round(mode_score * 100, 1),
        "مرور و تکرار": round(review_score * 100, 1),
        "خواب کافی": round(sleep_score * 100, 1),
        "تمرکز و دقت": round(focus_score * 100, 1),
        "مدیریت استرس": round(stress_score * 100, 1),
        "اجرای برنامه": round(exec_score * 100, 1),
        "مطالعه منظم": round(hours_score * 100, 1),
        "شروع به موقع": round(start_score * 100, 1),
        "شناخت نقاط ضعف": round(weakness_score * 100, 1),
        "حمایت خانواده": round(family_score * 100, 1),
    }

def recommend_tracks_detailed(payload: dict, subject_scores: dict) -> list:
    dominant = payload.get("dominant_think", "تحلیلی")
    average_grade = float(payload.get("average_grade", 15))
    
    think_style_scores = {
        "علوم تجربی": 1.0 if dominant in ["تحلیلی", "تکنولوژی/پروژه"] else 0.6 if dominant == "کارآفرین" else 0.4,
        "ریاضی فیزیک": 1.0 if dominant in ["تحلیلی", "تکنولوژی/پروژه"] else 0.5,
        "علوم انسانی": 1.0 if dominant in ["انسانی", "تحلیلی"] else 0.6,
        "هنر": 1.0 if dominant in ["خلاق", "کارآفرین"] else 0.5,
    }
    
    career_future_scores = {
        "علوم تجربی": 0.9,
        "ریاضی فیزیک": 0.95,
        "علوم انسانی": 0.7,
        "هنر": 0.75,
    }
    
    grade_score = min(1.0, average_grade / 20)
    
    results = []
    for track in TRACKS:
        weights = TRACK_SUBJECT_WEIGHTS_NINTH.get(track, {})
        ability_score = 0.0
        interest_score = 0.0
        wsum = 0.0
        
        for subj_key, w in weights.items():
            wsum += w
            if subj_key == "خلاقیت":
                proj = 1.0 if dominant in ["تکنولوژی/پروژه", "کارآفرین", "خلاق"] else 0.3
                ability_score += w * proj
                interest_score += w * proj
            else:
                subj_data = subject_scores.get(subj_key, {})
                if isinstance(subj_data, dict):
                    ability = subj_data.get("ability_score", 0.5)
                    interest = subj_data.get("interest_score", 0.5)
                else:
                    ability = subj_data if isinstance(subj_data, (int, float)) else 0.5
                    interest = ability
                ability_score += w * ability
                interest_score += w * interest
        
        if wsum > 0:
            ability_score = ability_score / wsum
            interest_score = interest_score / wsum
        else:
            ability_score = 0.5
            interest_score = 0.5
        
        think_score = think_style_scores.get(track, 0.5)
        future_score = career_future_scores.get(track, 0.5)
        
        total_score = (ability_score * 0.30 + interest_score * 0.25 + 
                       think_score * 0.20 + future_score * 0.15 + grade_score * 0.10) * 100
        
        descriptions = {
            "علوم تجربی": "🔬 مناسب برای علاقه‌مندان به زیست، شیمی و پزشکی. بازار کار خوب و درآمد بالا. رشته پزشکی، دندانپزشکی، داروسازی، پرستاری و بیوتکنولوژی از شاخه‌های آن است.",
            "ریاضی فیزیک": "⚡ مناسب برای علاقه‌مندان به ریاضی، فیزیک و مهندسی. فرصت‌های شغلی بسیار زیاد. مهندسی کامپیوتر، برق، مکانیک، هوافضا و معماری.",
            "علوم انسانی": "📖 مناسب برای علاقه‌مندان به ادبیات، تاریخ و حقوق. رشد شخصی و فرهنگی. حقوق، روانشناسی، مدیریت، اقتصاد و مشاوره.",
            "هنر": "🎨 مناسب برای افراد خلاق و هنرمند. فرصت‌های نوین در دنیای دیجیتال. گرافیک، انیمیشن، طراحی داخلی، موسیقی و طراحی بازی."
        }
        
        results.append({
            "track": track,
            "score": round(total_score, 1),
            "ability_score": round(ability_score * 100, 1),
            "interest_score": round(interest_score * 100, 1),
            "think_score": round(think_score * 100, 1),
            "future_score": round(future_score * 100, 1),
            "grade_score": round(grade_score * 100, 1),
            "level": "مناسب" if total_score >= 65 else "قابل قبول" if total_score >= 45 else "ضعیف",
            "color": color_for_percent(total_score),
            "description": descriptions.get(track, "رشته تحصیلی مناسب"),
            "icon": {"علوم تجربی": "🔬", "ریاضی فیزیک": "⚡", "علوم انسانی": "📖", "هنر": "🎨"}.get(track, "📚")
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def track_strengths_weaknesses(track: str, subject_scores: dict) -> dict:
    weights = TRACK_SUBJECT_WEIGHTS_NINTH.get(track, {})
    strengths = []
    weaknesses = []
    
    for subj, weight in weights.items():
        subj_data = subject_scores.get(subj, {})
        if isinstance(subj_data, dict):
            score = subj_data.get("ability_score", 0.5) * 100
        else:
            score = (subj_data if isinstance(subj_data, (int, float)) else 0.5) * 100
        
        if score >= 65 and weight > 0.15:
            strengths.append({"subject": subj, "score": round(score, 1)})
        elif score <= 40 and weight > 0.15:
            weaknesses.append({"subject": subj, "score": round(score, 1)})
    
    strengths.sort(key=lambda x: x["score"], reverse=True)
    weaknesses.sort(key=lambda x: x["score"])
    
    return {"strengths": strengths[:4], "weaknesses": weaknesses[:3]}

def compute_career_match_detailed(track: str, subject_scores: dict, subject_interests: dict, dominant_think: str) -> list:
    careers = CAREERS_BY_TRACK.get(track, [])
    
    think_bonus = {
        "تحلیلی": ["ریاضی", "علوم", "فیزیک", "شیمی", "زیست", "منطق"],
        "خلاق": ["ادبیات فارسی", "زبان", "خلاقیت", "مبانی هنر", "هنر"],
        "انسانی": ["ادبیات فارسی", "تاریخ", "جغرافیا", "دینی/قرآن", "فلسفه و منطق"],
        "تکنولوژی/پروژه": ["ریاضی", "علوم", "فیزیک", "شیمی", "زیست", "خلاقیت"],
        "کارآفرین": ["تاریخ", "جغرافیا", "زبان", "ادبیات فارسی", "خلاقیت"],
    }
    bonus_keys = think_bonus.get(dominant_think, [])
    
    results = []
    for c in careers:
        keys = c["keys"]
        interest_vals = [subject_interests.get(k, 3) for k in keys if k in subject_interests]
        interest_avg = sum(interest_vals) / len(interest_vals) if interest_vals else 3.0
        interest_component = interest_avg / 5.0
        
        score_vals = []
        for k in keys:
            subj_data = subject_scores.get(k, {})
            if isinstance(subj_data, dict):
                score_vals.append(subj_data.get("ability_score", 0.5))
            else:
                score_vals.append(subj_data if isinstance(subj_data, (int, float)) else 0.5)
        score_avg = sum(score_vals) / len(score_vals) if score_vals else 0.5
        score_component = score_avg
        
        overlap = len([k for k in keys if k in bonus_keys])
        think_component = 1.0 if overlap >= 2 else (0.6 if overlap >= 1 else 0.2)
        
        final = (interest_component * 0.45 + score_component * 0.35 + think_component * 0.20) * 100
        
        if final >= 75:
            recommendation = "عالی"
            rec_color = "#10b981"
        elif final >= 55:
            recommendation = "خوب"
            rec_color = "#f59e0b"
        else:
            recommendation = "قابل قبول"
            rec_color = "#ef4444"
        
        results.append({
            "job": c["job"],
            "percent": round(final, 1),
            "hint": c["hint"],
            "difficulty": c.get("difficulty", "متوسط"),
            "salary": c.get("salary", "متوسط"),
            "icon": c.get("icon", "💼"),
            "growth": c.get("growth", "متوسط"),
            "demand": c.get("demand", "متوسط"),
            "study_time": c.get("study_time", "4 سال"),
            "avg_income": c.get("avg_income", "نامشخص"),
            "recommendation": recommendation,
            "rec_color": rec_color
        })
    
    results.sort(key=lambda x: x["percent"], reverse=True)
    return results[:8]

def top_risky_subjects_detailed(subject_scores: dict, risk_data: dict) -> list:
    items = []
    for subj, data in subject_scores.items():
        if isinstance(data, dict):
            ability = data.get("ability_score", 0.5) * 100
            interest = data.get("interest_score", 0.5) * 100        
        else:
            ability = (data if isinstance(data, (int, float)) else 0.5) * 100
            interest = 50
        
        subject_risk = (100 - ability) * 0.5 + risk_data["risk"] * 35 + (100 - interest) * 0.15
        subject_risk = min(100, max(0, subject_risk))
        
        if subject_risk >= 65:
            reason = "ضعف شدید در فهم و عملکرد - نیاز به توجه ویژه"
            color = "#ef4444"
        elif subject_risk >= 45:
            reason = "کمبود تمرین و مرور - قابل جبران با تلاش بیشتر"
            color = "#f59e0b"
        elif subject_risk >= 25:
            reason = "نیاز به تمرین بیشتر - در مسیر خوبی هستی"
            color = "#10b981"
        elif interest < 40:
            reason = "کمبود علاقه و انگیزه - سعی کن ارتباط درس با علاقه‌هات رو پیدا کنی"
            color = "#f59e0b"
        else:
            reason = "وضعیت خوب - همینطور ادامه بده"
            color = "#10b981"
        
        items.append({
            "subject": subj,
            "ability_score": round(ability, 1),
            "interest_score": round(interest, 1),
            "risk_percent": round(subject_risk, 1),
            "reason": reason,
            "color": color
        })
    
    items.sort(key=lambda x: x["risk_percent"], reverse=True)
    return items[:6]

def anti_fall_plan_detailed(bucket: str, risky_subjects: list = None, grade_level: str = "هفتم-نهم") -> dict:
    if risky_subjects is None or len(risky_subjects) == 0:
        risky_subjects = ["درس اصلی"]
    main_subj = risky_subjects[0]
    second_subj = risky_subjects[1] if len(risky_subjects) > 1 else "درس دوم"
    third_subj = risky_subjects[2] if len(risky_subjects) > 2 else "درس سوم"
    
    if bucket == "بالا":
        days = [
            {"day": "شنبه", "task": f"📝 آزمون تشخیصی از {main_subj} (۲۵ سوال)", "time": "۳۵ دقیقه", "priority": "بسیار مهم", "icon": "📝"},
            {"day": "یکشنبه", "task": f"📖 تحلیل کامل غلط‌ها + تمرین مجدد {main_subj}", "time": "۵۰ دقیقه", "priority": "بسیار مهم", "icon": "📖"},
            {"day": "دوشنبه", "task": f"🔄 مرور عمقی {main_subj} + ۱۵ سوال ترکیبی", "time": "۴۰ دقیقه", "priority": "مهم", "icon": "🔄"},
            {"day": "سه‌شنبه", "task": f"📝 آزمون دوم از {main_subj} + ثبت پیشرفت", "time": "۳۵ دقیقه", "priority": "مهم", "icon": "📊"},
            {"day": "چهارشنبه", "task": f"✏️ تمرین استاندارد روی {second_subj}", "time": "۴۵ دقیقه", "priority": "متوسط", "icon": "✏️"},
            {"day": "پنج‌شنبه", "task": f"🎯 تمرکز روی {third_subj} + رفع اشکال", "time": "۳۵ دقیقه", "priority": "متوسط", "icon": "🎯"},
            {"day": "جمعه", "task": "🧘 مرور کل هفته + آزمون جامع + برنامه‌ریزی هفته بعد", "time": "۵۰ دقیقه", "priority": "مهم", "icon": "🧘"},
        ]
        total_hours = 4.8
        intensity = "شدید"
        recommendation = "روزانه حداقل ۴۵ دقیقه مطالعه هدفمند + یک آزمون هفتگی"
        weekly_tests = 3
    elif bucket == "متوسط":
        days = [
            {"day": "شنبه", "task": f"📝 کوییز کوتاه از {main_subj} (۱۵ سوال)", "time": "۲۵ دقیقه", "priority": "مهم", "icon": "📝"},
            {"day": "یکشنبه", "task": f"📖 رفع اشتباهات + تمرین هدفمند {main_subj}", "time": "۳۵ دقیقه", "priority": "مهم", "icon": "📖"},
            {"day": "دوشنبه", "task": f"🔄 مرور سبک {main_subj}", "time": "۲۵ دقیقه", "priority": "متوسط", "icon": "🔄"},
            {"day": "سه‌شنبه", "task": f"📝 کوییز دوم از {main_subj}", "time": "۲۵ دقیقه", "priority": "متوسط", "icon": "📊"},
            {"day": "چهارشنبه", "task": f"✏️ تمرین استاندارد {second_subj}", "time": "۳۰ دقیقه", "priority": "متوسط", "icon": "✏️"},
            {"day": "پنج‌شنبه", "task": "🎯 رفع اشکالات و بی‌دقتی", "time": "۲۵ دقیقه", "priority": "کم", "icon": "🎯"},
            {"day": "جمعه", "task": "📊 جمع‌بندی و برنامه ریزی هفته بعد", "time": "۲۰ دقیقه", "priority": "کم", "icon": "📊"},
        ]
        total_hours = 3.0
        intensity = "متوسط"
        recommendation = "روزانه ۲۵-۳۰ دقیقه مطالعه منظم + مرور آخر هفته"
        weekly_tests = 1
    else:
        days = [
            {"day": "شنبه", "task": f"🔄 مرور سبک {main_subj}", "time": "۲۰ دقیقه", "priority": "کم", "icon": "🔄"},
            {"day": "یکشنبه", "task": f"✏️ تمرین استاندارد {main_subj}", "time": "۲۵ دقیقه", "priority": "کم", "icon": "✏️"},
            {"day": "دوشنبه", "task": f"📖 مطالعه تفهیمی {second_subj}", "time": "۲۵ دقیقه", "priority": "کم", "icon": "📖"},
            {"day": "سه‌شنبه", "task": f"📝 کوییز کوتاه از {main_subj}", "time": "۲۰ دقیقه", "priority": "کم", "icon": "📝"},
            {"day": "چهارشنبه", "task": "🎯 رفع اشتباهات جزئی", "time": "۲۰ دقیقه", "priority": "کم", "icon": "🎯"},
            {"day": "پنج‌شنبه", "task": "📊 مرور نهایی هفته", "time": "۲۰ دقیقه", "priority": "کم", "icon": "📊"},
            {"day": "جمعه", "task": "🧘 استراحت فعال + برنامه‌ریزی", "time": "۱۵ دقیقه", "priority": "کم", "icon": "🧘"},
        ]
        total_hours = 2.3
        intensity = "سبک"
        recommendation = "روزانه ۱۵-۲۰ دقیقه مرور کافی است - روی نقاط قوتت تمرکز کن"
        weekly_tests = 0
    
    return {"days": days, "total_hours": total_hours, "intensity": intensity, "recommendation": recommendation, "weekly_tests": weekly_tests}

def get_recommended_resources(subjects: list) -> dict:
    resources = {}
    for subj in subjects:
        found = None
        for key in RESOURCE_SUGGESTIONS:
            if key in subj or subj in key:
                found = key
                break
        if found:
            resources[subj] = RESOURCE_SUGGESTIONS[found][:5]
        else:
            resources[subj] = [
                "📘 منابع عمومی توصیه می‌شود",
                "📺 جستجوی آنلاین با کلمات کلیدی",
                "📱 اپلیکیشن‌های آموزشی (نصب رایگان)",
                "🌐 سایت‌های معتبر آموزشی",
                "📚 کتاب‌های کمک درسی انتشارات معتبر"
            ]
    return resources

def get_study_tips_by_risk(bucket: str) -> list:
    if bucket == "بالا":
        return [
            "🎯 اولویت مطلق با دروس ضعیف‌تر باشد (حداقل 60% زمان)",
            "⏰ زمان مطالعه را به بازه‌های ۲۵ دقیقه‌ای تقسیم کن (تکنیک پومودورو)",
            "📝 بعد از هر جلسه مطالعه، یک تست کوتاه (۵-۱۰ سوال) از خودت بگیر",
            "😴 حتماً ۸ ساعت خواب شبانه داشته باش - کمبود خواب تمرکز را ۵۰٪ کاهش می‌دهد",
            "📱 گوشی را در زمان مطالعه در اتاق دیگری بگذار یا در حالت پرواز قرار بده",
            "🗓️ یک برنامه هفتگی دقیق بنویس و به آن پایبند باش (از شب قبل برنامه روز بعد را بنویس)",
            "👨‍👩‍👧 از خانواده کمک بگیر و برات محیط مطالعه مناسب فراهم کنن (بدون سر و صدا)",
            "📞 با یک مشاور تحصیلی صحبت کن - گاهی یک جلسه مشاوره می‌تواند مسیر را عوض کند",
            "📚 از روش SQ3R برای مطالعه عمیق استفاده کن: Survey, Question, Read, Recite, Review"
        ]
    elif bucket == "متوسط":
        return [
            "📚 مطالعه را از درس‌های مورد علاقه شروع کن تا انگیزه بگیری و انرژی بگیری",
            "✅ هر روز ۳ کار اصلی را مشخص کن و انجام بده (قانون ۳ کار مهم)",
            "🧠 از روش خلاصه‌نویسی و نقشه ذهنی (Mind Map) استفاده کن",
            "🎯 هدف‌های کوچک و قابل دسترس تعیین کن (مثلاً امروز ۲۰ تست ریاضی)",
            "💡 بعد از هر ۵۰ دقیقه مطالعه، ۱۰ دقیقه استراحت کن - به مغزت استراحت بده",
            "👥 با دوستانت گروه‌های مطالعاتی تشکیل بده - یادگیری گروهی موثرتر است",
            "📈 پیشرفت هفتگی خود را ثبت کن و به خودت جایزه بده",
            "🎧 از موسیقی بی‌کلام یا صدای طبیعت در حین مطالعه استفاده کن"
        ]
    else:
        return [
            "🌟 روال فعلی خود را حفظ کن و به مرور ادامه بده - عالی کار می‌کنی",
            "📈 می‌توانی زمان مطالعه را ۱۰-۲۰٪ افزایش دهی و پیشرفت بیشتری داشته باشی",
            "🧪 تست‌های زمان‌دار بزن تا با شرایط امتحان آشنا شوی و سرعتت افزایش یابد",
            "👥 با دوستانت گروه‌های مطالعاتی تشکیل بده و تجربیاتت رو به اشتراک بگذار",
            "🎯 برای خودت هدف‌های بزرگتر تعیین کن - می‌تونی بهتر از این باشی",
            "📚 کتاب‌های سطح بالاتر و منابع تکمیلی مطالعه کن",
            "🏆 در المپیادهای علمی شرکت کن - می‌تونه آینده تو رو متحول کنه"
        ]

def cleanup_old_data():
    try:
        import sqlite3
        from datetime import datetime, timedelta
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cutoff_date = (datetime.now() - timedelta(days=180)).isoformat()
        cursor.execute('DELETE FROM conversations WHERE timestamp < ?', (cutoff_date,))
        deleted_conv = cursor.rowcount
        cursor.execute('DELETE FROM track_analysis WHERE timestamp < ?', (cutoff_date,))
        deleted_track = cursor.rowcount
        cursor.execute('DELETE FROM risk_analysis WHERE timestamp < ?', (cutoff_date,))
        deleted_risk = cursor.rowcount
        conn.commit()
        conn.close()
        logger.info(f"پاکسازی اطلاعات قدیمی: {deleted_conv} مکالمه، {deleted_track} تحلیل رشته، {deleted_risk} تحلیل ریسک")
        return True
    except Exception as e:
        logger.error(f"خطا در پاکسازی اطلاعات: {e}")
        return False

def generate_report(user_id):
    try:
        from database import get_user_from_db, get_user_conversations, get_user_statistics
        from datetime import datetime
        user = get_user_from_db(user_id)
        conversations = get_user_conversations(user_id, 10)
        stats = get_user_statistics(user_id)
        report = {
            "generated_at": datetime.now().isoformat(),
            "user_id": user_id,
            "user_info": {
                "user_code": user.get("user_code") if user else "ناشناس",
                "grade_level": user.get("grade_level") if user else "نامشخص",
                "dominant_think": user.get("dominant_think") if user else "نامشخص"
            },
            "statistics": stats,
            "recent_conversations": conversations,
            "recommendations": []
        }
        if stats.get("avg_confidence", 0) < 50:
            report["recommendations"].append("پاسخ‌های با دقت بالاتری نیاز دارید. سوالات خود را دقیق‌تر بپرسید.")
        if stats.get("avg_user_rating", 0) < 3:
            report["recommendations"].append("امتیاز شما به پاسخ‌ها پایین است. لطفاً مشکلات را دقیق‌تر بیان کنید.")
        return report
    except Exception as e:
        logger.error(f"خطا در تولید گزارش: {e}")
        return {"error": str(e)}

def export_report_to_json(user_id):
    report = generate_report(user_id)
    filename = f"report_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    logger.info(f"📄 گزارش ذخیره شد: {filename}")
    return filename

def backup_database():
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"kharazmi_backup_{timestamp}.db")
    shutil.copy2(DB_NAME, backup_file)
    zip_file = os.path.join(backup_dir, f"kharazmi_backup_{timestamp}.zip")
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(backup_file, os.path.basename(backup_file))
    os.remove(backup_file)
    logger.info(f"💾 پشتیبان تهیه شد: {zip_file}")
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.zip')])
    for old_backup in backups[:-5]:
        os.remove(os.path.join(backup_dir, old_backup))
    return zip_file

from chatbot_knowledge import CHATBOT_KNOWLEDGE

def infer_intent(message):
    msg = build_context(message)
    msg_lower = msg.lower()
    
    intent_scores = {
        "greeting": 0.0, "how_are_you": 0.0, "fine": 0.0,
        "thanks": 0.0, "goodbye": 0.0, "study": 0.0,
        "motivation": 0.0, "stress": 0.0, "school": 0.0, "academic": 0.0, "other": 0.0
    }
    
    groups = {
        "greeting": CHATBOT_KNOWLEDGE["greetings"]["patterns"],
        "how_are_you": CHATBOT_KNOWLEDGE["how_are_you"]["patterns"],
        "fine": CHATBOT_KNOWLEDGE["fine"]["patterns"],
        "thanks": CHATBOT_KNOWLEDGE["thanks"]["patterns"],
        "goodbye": CHATBOT_KNOWLEDGE["goodbye"]["patterns"],
        "study": CHATBOT_KNOWLEDGE["study_tips"]["keywords"],
        "motivation": CHATBOT_KNOWLEDGE["motivation"]["keywords"],
        "stress": CHATBOT_KNOWLEDGE["stress"]["keywords"],
        "school": CHATBOT_KNOWLEDGE["school_questions"]["keywords"],
        "academic": CHATBOT_KNOWLEDGE["academic_words"]["keywords"],
    }
    
    for key, words in groups.items():
        exact_hits = sum(1 for w in words if w in msg_lower)
        fuzzy_hits = sum(1 for w in words if text_similarity(msg_lower, w) > 0.75)
        bag = bag_similarity(msg_lower, " ".join(words[:20]))
        intent_scores[key] = exact_hits * 3.0 + fuzzy_hits * 1.5 + bag * 4.0
    
    if "سلام" in msg_lower or "درود" in msg_lower or "hi" in msg_lower or "hello" in msg_lower:
        intent_scores["greeting"] += 10
    
    best = max(intent_scores.items(), key=lambda x: x[1])
    
    if best[1] > 0.5:
        return best[0]
    return "other"

def choose_response(intent):
    if intent == "greeting":
        return random.choice(CHATBOT_KNOWLEDGE["greetings"]["responses"])
    elif intent == "how_are_you":
        return random.choice(CHATBOT_KNOWLEDGE["how_are_you"]["responses"])
    elif intent == "fine":
        return random.choice(CHATBOT_KNOWLEDGE["fine"]["responses"])
    elif intent == "thanks":
        return random.choice(CHATBOT_KNOWLEDGE["thanks"]["responses"])
    elif intent == "goodbye":
        return random.choice(CHATBOT_KNOWLEDGE["goodbye"]["responses"])
    elif intent == "study":
        return random.choice(CHATBOT_KNOWLEDGE["study_tips"]["responses"])
    elif intent == "motivation":
        return random.choice(CHATBOT_KNOWLEDGE["motivation"]["responses"])
    elif intent == "stress":
        return random.choice(CHATBOT_KNOWLEDGE["stress"]["responses"])
    elif intent == "school":
        return random.choice(CHATBOT_KNOWLEDGE["school_questions"]["responses"])
    elif intent == "academic":
        return random.choice(CHATBOT_KNOWLEDGE["academic_words"]["responses"])
    return random.choice(CHATBOT_KNOWLEDGE["default_qa"]["responses"])

# track_risk_logic.py - این تابع را جایگزین کنید:

def get_personalized_greeting(session_id):
    try:
        from database import get_user_from_db
        user = get_user_from_db(session_id)
        if user:
            user_code = user.get("user_code", "")
            first_name = user.get("name", "")
            last_name = user.get("lastname", "")
            
            # اگر اسم وجود داشت، با اسم صدا کن
            if first_name:
                full_name = first_name
                if last_name:
                    full_name = first_name + " " + last_name
                return f"سلام {full_name} جان! 🌟 خوش برگشتی 🎓 چطور با درس‌هات پیش میری؟"
            elif user_code:
                return f"سلام کاربر گرامی ({user_code[:6]})! خوش برگشتی 🎓 چطور با درس‌هات پیش میری؟"
        
        return "سلام! 🌟 من مسیرینو هستم، مشاور هوشمند تحصیلی. لطفاً ابتدا رضایت‌نامه را تایید کنید 🤗"
    except Exception as e:
        print(f"خطا در دریافت اطلاعات کاربر: {e}")
        return "سلام! 🌟 من مسیرینو هستم، مشاور هوشمند تحصیلی. لطفاً ابتدا رضایت‌نامه را تایید کنید 🤗"
    
def learn_from_conversation(user_msg, bot_resp, session_id, intent, confidence, sentiment, user_rating=None):
    try:
        from database import save_conversation
        save_conversation(session_id, user_msg, bot_resp, intent, confidence, sentiment, user_rating)
        logger.info(f"مکالمه ذخیره شد - کاربر: {session_id[:8]}... - intent: {intent}")
    except Exception as e:
        logger.error(f"خطا در یادگیری: {e}")

def chatbot_respond(message: str, session_id: str = "default") -> str:
    raw_message = (message or "").strip()
    
    if not raw_message:
        return "لطفاً یک سوال بپرسید یا پیامی بنویسید. من اینجام تا کمکت کنم 🌟"
    
    if is_inappropriate(raw_message):
        logger.warning(f"محتوای نامناسب از کاربر {session_id[:8]}...: {raw_message[:50]}")
        return get_inappropriate_response()
    
    if session_id not in CHAT_HISTORY:
        CHAT_HISTORY[session_id] = deque(maxlen=50)
        greeting = get_personalized_greeting(session_id)
        CHAT_HISTORY[session_id].append({"role": "bot", "message": greeting})
    
    CHAT_HISTORY[session_id].append({"role": "user", "message": raw_message})
    
    emotion, emotion_score, emotion_response, emotion_count = advanced_sentiment_analysis(raw_message)
    
    cleaned = build_context(raw_message)
    intent = infer_intent(raw_message)
    user_lang = detect_language(raw_message)
    
    user_name = ""
    try:
        from database import get_user_from_db
        user = get_user_from_db(session_id)
        if user:
            user_name = user.get("name", "")
    except:
        pass
    
    confidence_data = [1.0 if intent != "other" else 0.5, 0.8 if user_name else 0.3]
    confidence = calculate_confidence(confidence_data, [0.6, 0.4])
    
    response = ""
    
    if intent != "other":
        response = choose_response(intent)
        if "می‌تونی سوالت را دقیق‌تر بپرسی" in response or "بیشتر توضیح بده" in response:
            online_res = smart_online_search(cleaned)
            if online_res:
                response = online_res
                confidence = min(95, confidence + 20)
    else:
        online_res = smart_online_search(cleaned)
        if online_res:
            response = online_res
            confidence = 85
        else:
            response = random.choice(CHATBOT_KNOWLEDGE["default_qa"]["responses"])
            confidence = 40
    
    if emotion != "neutral" and emotion_response and len(response) < 250:
        response = emotion_response + "\n\n" + response
    
    if intent == "greeting" and user_name:
        response = f"{response}\n\n{user_name} جان، چطور می‌تونم بهت کمک کنم؟ (دقت پاسخ: {confidence}%)"
    elif intent == "greeting":
        response = response + "\n\nلطفاً در پنل بالای صفحه اسم خودت رو وارد کن تا بتونم با اسم صدات کنم 🤗"
    
    if user_lang == "en":
        response = simple_translate_to_english(response)
    
    learn_from_conversation(raw_message, response, session_id, intent, confidence, emotion)
    
    CHAT_HISTORY[session_id].append({"role": "bot", "message": response})
    logger.info(f"پاسخ به کاربر {session_id[:8]}... - intent: {intent} - confidence: {confidence}%")
    
    return response