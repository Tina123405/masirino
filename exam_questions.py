import random
import json
from datetime import datetime

# ========== بانک سوالات کامل (همراه ابتدایی) ==========
QUESTION_BANK = {
    "ریاضی": {
        "ابتدایی": {
            "آسان": [
                {"question": "۲ + ۳ چند می‌شود؟", "options": ["۴", "۵", "۶", "۷"], "answer": "۵", "explanation": "۲ تا سیب + ۳ تا سیب = ۵ تا سیب"},
                {"question": "۵ - ۲ چند می‌شود؟", "options": ["۲", "۳", "۴", "۵"], "answer": "۳", "explanation": "۵ تا مداد، ۲ تا رو بدیم، ۳ تا می‌مونه"},
                {"question": "کدام عدد بزرگتر است؟", "options": ["۱۲", "۱۵", "۱۰", "۸"], "answer": "۱۵", "explanation": "۱۵ از بقیه بزرگتره"},
                {"question": "۳ × ۴ چند می‌شود؟", "options": ["۱۰", "۱۱", "۱۲", "۱۳"], "answer": "۱۲", "explanation": "۳ تا ۴ تا میشه ۱۲"},
                {"question": "۱۰ ÷ ۲ چند می‌شود؟", "options": ["۳", "۴", "۵", "۶"], "answer": "۵", "explanation": "۱۰ تا آب نبات بین ۲ نفر، هر کدوم ۵ تا"},
                {"question": "کدام یک شکل مربع است؟", "options": ["۴ ضلع مساوی", "۴ ضلع مختلف", "۳ ضلع", "دایره"], "answer": "۴ ضلع مساوی", "explanation": "مربع ۴ ضلع مساوی داره"},
                {"question": "۱ متر چند سانتی‌متر است؟", "options": ["۱۰", "۱۰۰", "۱۰۰۰", "۱۰۰۰۰"], "answer": "۱۰۰", "explanation": "۱ متر = ۱۰۰ سانتی‌متر"},
                {"question": "نصف ۱۰ چند است؟", "options": ["۲", "۳", "۴", "۵"], "answer": "۵", "explanation": "۱۰ را نصف کنیم میشه ۵"},
            ],
            "متوسط": [
                {"question": "۱۲۵ + ۲۳۴ چند می‌شود؟", "options": ["۳۴۹", "۳۵۹", "۳۶۹", "۳۷۹"], "answer": "۳۵۹", "explanation": "۱۲۵ + ۲۳۴ = ۳۵۹"},
                {"question": "۴۵۶ - ۱۲۳ چند می‌شود؟", "options": ["۳۳۳", "۳۴۳", "۳۵۳", "۳۶۳"], "answer": "۳۳۳", "explanation": "۴۵۶ - ۱۲۳ = ۳۳۳"},
                {"question": "اگر یک کیک به ۸ قسمت مساوی تقسیم شود و ۳ قسمت خورده شود، چند قسمت باقی می‌ماند؟", "options": ["۳", "۴", "۵", "۶"], "answer": "۵", "explanation": "۸ - ۳ = ۵ قسمت باقی می‌ماند"},
                {"question": "کسر ۳/۴ یعنی چه؟", "options": ["۳ تا از ۴ قسمت", "۴ تا از ۳ قسمت", "۳ تا از ۳ قسمت", "۴ تا از ۴ قسمت"], "answer": "۳ تا از ۴ قسمت", "explanation": "صورت ۳، مخرج ۴ یعنی ۳ قسمت از ۴ قسمت"},
            ],
            "سخت": [
                {"question": "اگر امروز سه‌شنبه باشد، ۵ روز بعد چه روزی است؟", "options": ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه"], "answer": "یکشنبه", "explanation": "سه‌شنبه + ۵ روز = یکشنبه"},
                {"question": "عدد ۲۵ را به صورت ضرب دو عدد بنویسید.", "options": ["۵×۵", "۴×۶", "۳×۸", "۲×۱۲"], "answer": "۵×۵", "explanation": "۲۵ = ۵×۵"},
                {"question": "مساحت مستطیلی به طول ۵ و عرض ۳ چقدر است؟", "options": ["۸", "۱۵", "۱۶", "۱۰"], "answer": "۱۵", "explanation": "مساحت = طول × عرض = ۵×۳=۱۵"},
            ]
        },
        "هفتم-نهم": {
            "آسان": [
                {"question": "حاصل ۷ + ۳ × ۲ چند است؟", "options": ["۱۳", "۱۷", "۲۰", "۱۰"], "answer": "۱۳", "explanation": "ضرب قبل از جمع انجام میشه: ۳×۲=۶، سپس ۷+۶=۱۳"},
                {"question": "مساحت مربعی به ضلع ۴ سانتی متر چقدر است؟", "options": ["۸", "۱۲", "۱۶", "۲۰"], "answer": "۱۶", "explanation": "مساحت مربع = ضلع × ضلع = ۴×۴=۱۶"},
                {"question": "کدام کسر از همه بزرگتر است؟", "options": ["۱/۲", "۲/۳", "۳/۴", "۴/۵"], "answer": "۴/۵", "explanation": "۴/۵ = ۰.۸ که از بقیه بزرگتر است"},
                {"question": "حاصل ۲۰% از ۵۰ چند است؟", "options": ["۵", "۱۰", "۱۵", "۲۰"], "answer": "۱۰", "explanation": "۲۰% یعنی ۰.۲، ۰.۲×۵۰=۱۰"},
                {"question": "محیط دایره‌ای به شعاع ۷ سانتی متر (با تقریب π=۳.۱۴) چند است؟", "options": ["۲۱.۹۸", "۴۳.۹۶", "۱۴", "۲۸"], "answer": "۴۳.۹۶", "explanation": "محیط دایره = ۲πr = ۲×۳.۱۴×۷ = ۴۳.۹۶"},
            ],
            "متوسط": [
                {"question": "معادله ۲x + ۵ = ۱۵ را حل کنید.", "options": ["x=۳", "x=۴", "x=۵", "x=۶"], "answer": "x=۵", "explanation": "۲x = ۱۵-۵ = ۱۰، x=۱۰/۲=۵"},
                {"question": "اگر یک پیتزا به ۸ قسمت مساوی تقسیم شود و ۳ قسمت خورده شود، چند درصد پیتزا باقی مانده؟", "options": ["۳۷.۵%", "۶۲.۵%", "۵۰%", "۷۵%"], "answer": "۶۲.۵%", "explanation": "باقیمانده ۵ قسمت از ۸ = ۵/۸ = ۰.۶۲۵ = ۶۲.۵%"},
                {"question": "سه عدد فرد متوالی جمعشان ۳۹ است، کوچکترین عدد کدام است؟", "options": ["۱۱", "۱۲", "۱۳", "۱۰"], "answer": "۱۱", "explanation": "اعداد: ۱۱, ۱۳, ۱۵ → ۱۱+۱۳+۱۵=۳۹"},
                {"question": "مساحت مثلثی با قاعده ۱۰ و ارتفاع ۶ چقدر است؟", "options": ["۳۰", "۶۰", "۱۵", "۴۵"], "answer": "۳۰", "explanation": "مساحت مثلث = (قاعده×ارتفاع)/۲ = (۱۰×۶)/۲ = ۳۰"},
            ],
            "سخت": [
                {"question": "در یک دنباله حسابی، جمله پنجم ۱۷ و جمله دهم ۳۲ است. جمله اول دنباله کدام است؟", "options": ["۲", "۳", "۴", "۵"], "answer": "۵", "explanation": "اختلاف ۵ جمله = ۱۵، اختلاف هر جمله = ۳، جمله اول = ۱۷ - ۴×۳ = ۵"},
                {"question": "ریشه‌های معادله x² - ۵x + ۶ = ۰ کدام است؟", "options": ["۲ و ۳", "-۲ و -۳", "۱ و ۶", "-۱ و -۶"], "answer": "۲ و ۳", "explanation": "(x-2)(x-3)=0 → x=2 یا x=3"},
            ]
        },
        "دهم-دوازدهم": {
            "آسان": [
                {"question": "حد عبارت lim (x→۲) (x²-4)/(x-2) را محاسبه کنید.", "options": ["۰", "۲", "۴", "∞"], "answer": "۴", "explanation": "صورت را تجزیه می‌کنیم: (x-2)(x+2)/(x-2) = x+2، حد برابر ۴"},
                {"question": "مشتق تابع f(x)=x³ را بیابید.", "options": ["۳x²", "x²", "۳x³", "۲x²"], "answer": "۳x²", "explanation": "قانون مشتق: d/dx (x^n) = n x^(n-1)"},
            ],
            "متوسط": [
                {"question": "انتگرال ∫(۲x+۳) dx را محاسبه کنید.", "options": ["x²+۳x+C", "۲x²+۳x+C", "x²+۳+C", "۲x+۳+C"], "answer": "x²+۳x+C", "explanation": "∫۲x dx = x²، ∫۳ dx = ۳x"},
            ]
        }
    },
    "فیزیک": {
        "هفتم-نهم": {
            "آسان": [
                {"question": "واحد نیرو در سیستم SI چیست؟", "options": ["نیوتن", "ژول", "وات", "پاسکال"], "answer": "نیوتن", "explanation": "نیرو بر حسب نیوتن (N) اندازه‌گیری می‌شود"},
                {"question": "قانون اول نیوتن چه می‌گوید؟", "options": ["هر عملی عکس‌العملی دارد", "هر جسمی در حالت سکون یا حرکت یکنواخت می‌ماند مگر نیرویی به آن وارد شود", "شتاب با نیرو متناسب و با جرم معکوس است", "هیچکدام"], "answer": "هر جسمی در حالت سکون یا حرکت یکنواخت می‌ماند مگر نیرویی به آن وارد شود", "explanation": "این قانون را قانون لختی نیز می‌نامند"},
            ],
        },
        "دهم-دوازدهم": {
            "آسان": [
                {"question": "فرمول قانون اهم چیست؟", "options": ["V=IR", "P=VI", "I=V/R", "هر دو V=IR و I=V/R"], "answer": "هر دو V=IR و I=V/R", "explanation": "قانون اهم رابطه بین ولتاژ، جریان و مقاومت را بیان می‌کند"},
                {"question": "واحد توان الکتریکی چیست؟", "options": ["ولت", "آمپر", "وات", "اهم"], "answer": "وات", "explanation": "توان الکتریکی بر حسب وات (W) اندازه‌گیری می‌شود"},
            ]
        }
    },
    "زیست": {
        "هفتم-نهم": {
            "آسان": [
                {"question": "کدام یک اندامک سلول نیست؟", "options": ["هسته", "میتوکندری", "دیواره سلولی", "ریبوزوم"], "answer": "دیواره سلولی", "explanation": "دیواره سلولی اندامک نیست، یک ساختار خارج سلولی است"},
                {"question": "عملکرد میتوکندری چیست؟", "options": ["تولید انرژی", "ساخت پروتئین", "ذخیره آب", "تقسیم سلول"], "answer": "تولید انرژی", "explanation": "میتوکندری نیروگاه سلول است و ATP تولید می‌کند"},
            ]
        }
    },
    "شیمی": {
        "دهم-دوازدهم": {
            "آسان": [
                {"question": "نماد شیمیایی طلا چیست؟", "options": ["Go", "Au", "Ag", "Fe"], "answer": "Au", "explanation": "طلا از کلمه لاتین Aurum گرفته شده است"},
            ]
        }
    },
    "علوم": {
        "ابتدایی": {
            "آسان": [
                {"question": "کدام یک از موارد زیر یک ماده است؟", "options": ["آب", "نور", "صدا", "گرما"], "answer": "آب", "explanation": "آب ماده است، نور و صدا و گرما انرژی هستند"},
                {"question": "خورشید چه نوع منبع انرژی است؟", "options": ["منبع تجدیدپذیر", "منبع تجدیدناپذیر", "هر دو", "هیچکدام"], "answer": "منبع تجدیدپذیر", "explanation": "خورشید یک منبع انرژی تجدیدپذیر است"},
                {"question": "کدام حس برای دیدن استفاده می‌شود؟", "options": ["بویایی", "چشایی", "بینایی", "شنوایی"], "answer": "بینایی", "explanation": "برای دیدن از چشم استفاده می‌شود"},
            ]
        }
    },
    "علوم تجربی": {
        "هفتم-نهم": {
            "آسان": [
                {"question": "کدام یک جزء سلول گیاهی است؟", "options": ["دیواره سلولی", "غشا سلولی", "هسته", "همه موارد"], "answer": "همه موارد", "explanation": "سلول گیاهی همه این ساختارها را دارد"},
            ]
        }
    }
}

# سوالات تشریحی
DESCRIPTIVE_BANK = {
    "ریاضی": {
        "ابتدایی": {
            "آسان": [
                {"question": "جمع ۱۲ و ۱۵ را بنویسید.", "answer_template": "۱۲ + ۱۵ = ۲۷"},
                {"question": "عدد ۱۰۰ را به صورت ضرب دو عدد بنویسید.", "answer_template": "۱۰ × ۱۰ = ۱۰۰ یا ۲۰ × ۵ = ۱۰۰"},
            ],
            "متوسط": [
                {"question": "تفاوت بین مربع و مستطیل را توضیح دهید.", "answer_template": "مربع هر ۴ ضلعش مساوی است ولی مستطیل فقط اضلاع روبرو مساوی هستند"},
            ]
        },
        "هفتم-نهم": {
            "آسان": [
                {"question": "قانون بخش‌پذیری بر ۳ را توضیح دهید و مثال بزنید.", "answer_template": "عددی بر ۳ بخش‌پذیر است که مجموع ارقامش بر ۳ بخش‌پذیر باشد."},
                {"question": "فرمول مساحت دایره را بنویسید و یک مثال حل کنید.", "answer_template": "مساحت دایره = πr²، مثال: r=۵ → A=۳.۱۴×۲۵=۷۸.۵"},
            ],
            "متوسط": [
                {"question": "تفاوت بین معادله و نامعادله را توضیح دهید.", "answer_template": "معادله دارای علامت مساوی است، نامعادله دارای علامت ≥,≤,>,<"},
            ]
        }
    }
}

def generate_questions(subject, grade_level, difficulty, question_type, count):
    """تولید سوالات بر اساس پارامترها"""
    questions = []
    
    # بررسی وجود درس
    if subject not in QUESTION_BANK:
        subject = "ریاضی"
    
    # بررسی وجود مقطع
    if grade_level not in QUESTION_BANK[subject]:
        grade_level = list(QUESTION_BANK[subject].keys())[0] if QUESTION_BANK[subject] else "هفتم-نهم"
    
    # بررسی وجود سطح دشواری
    if difficulty not in QUESTION_BANK[subject][grade_level]:
        difficulty = list(QUESTION_BANK[subject][grade_level].keys())[0] if QUESTION_BANK[subject][grade_level] else "آسان"
    
    bank = QUESTION_BANK[subject][grade_level][difficulty]
    available = bank.copy()
    random.shuffle(available)
    
    # تستی
    if question_type in ["test", "both"]:
        for i in range(min(count, len(available))):
            q = available[i].copy()
            q["id"] = i + 1
            q["type"] = "test"
            questions.append(q)
    
    # تشریحی
    if question_type in ["descriptive", "both"]:
        if subject in DESCRIPTIVE_BANK and grade_level in DESCRIPTIVE_BANK[subject] and difficulty in DESCRIPTIVE_BANK[subject][grade_level]:
            desc_bank = DESCRIPTIVE_BANK[subject][grade_level][difficulty]
            for i in range(min(count, len(desc_bank))):
                q = desc_bank[i].copy()
                q["id"] = i + 1
                q["type"] = "descriptive"
                questions.append(q)
    
    return questions[:count]

def get_available_subjects():
    return list(QUESTION_BANK.keys())

def get_available_grade_levels(subject):
    if subject in QUESTION_BANK:
        return list(QUESTION_BANK[subject].keys())
    return ["ابتدایی", "هفتم-نهم"]

def save_exam_result(user_id, exam_data):
    """ذخیره نتیجه آزمون در دیتابیس"""
    try:
        from analytics_core import save_ml_prediction
        import sqlite3
        from config import DB_NAME
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
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
        cursor.execute('''
            INSERT INTO exam_results (user_id, subject, grade_level, questions_count, score, answers, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, exam_data.get("subject"), exam_data.get("grade_level"),
              exam_data.get("questions_count"), exam_data.get("score"),
              json.dumps(exam_data.get("answers", [])), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"خطا در ذخیره نتیجه: {e}")
        return False