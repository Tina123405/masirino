# path_finder_data.py
# داده‌های مسیرشو

CAREER_ROADMAPS = {
    "پزشکی": {
        "title": "🩺 مسیر تخصصی پزشکی",
        "type": "پزشکی",
        "duration_years": 7,
        "income_range": "۵۰-۱۵۰ میلیون تومان",
        "job_growth": "عالی",
        "steps": [
            {"year": 1, "title": "پایه", "subjects": ["زیست شناسی", "شیمی", "آناتومی"], "milestone": "معدل ۱۶+"},
            {"year": 2, "title": "فیزیوپاتولوژی", "subjects": ["فیزیولوژی", "پاتولوژی"], "milestone": "قبولی در علوم پایه"},
            {"year": 3, "title": "کارآموزی", "subjects": ["طب داخلی", "جراحی"], "milestone": "ارزیابی بالینی مثبت"},
            {"year": 4, "title": "کارورزی", "subjects": ["بخش‌های تخصصی"], "milestone": "تکمیل کارورزی"},
            {"year": 5, "title": "طرح", "subjects": ["خدمت در مناطق محروم"], "milestone": "اتمام طرح"},
            {"year": 6, "title": "تخصص", "subjects": ["انتخاب تخصص"], "milestone": "قبولی در آزمون دستیاری"},
            {"year": 7, "title": "فوق تخصص", "subjects": ["تخصص پیشرفته"], "milestone": "اخذ پروانه تخصص"}
        ],
        "skills": ["تحلیل مسائل پزشکی", "کار تیمی", "تاب‌آوری بالا"],
        "jobs": ["پزشک عمومی", "متخصص", "پژوهشگر"],
        "recommended_resources": ["📘 گایتون فیزیولوژی", "📱 Medscape", "🌐 UpToDate"]
    },
    "مهندسی کامپیوتر": {
        "title": "💻 مسیر تخصصی کامپیوتر",
        "type": "مهندسی کامپیوتر",
        "duration_years": 4,
        "income_range": "۵۰-۲۰۰ میلیون تومان",
        "job_growth": "بسیار عالی",
        "steps": [
            {"year": 1, "title": "مبانی برنامه‌نویسی", "subjects": ["پایتون", "ریاضی"], "milestone": "تسلط بر پایتون"},
            {"year": 2, "title": "ساختمان داده", "subjects": ["الگوریتم", "پایگاه داده"], "milestone": "حل ۱۰۰ مسئله"},
            {"year": 3, "title": "شاخه تخصصی", "subjects": ["هوش مصنوعی", "وب"], "milestone": "پروژه عملی"},
            {"year": 4, "title": "پروژه و کارآموزی", "subjects": ["پایان‌نامه", "کارآموزی"], "milestone": "پورتفولیو حرفه‌ای"}
        ],
        "skills": ["برنامه‌نویسی", "حل مسئله", "یادگیری مستمر"],
        "jobs": ["توسعه‌دهنده", "متخصص AI", "مدیر فنی"],
        "recommended_resources": ["📘 Clean Code", "🌐 LeetCode", "🎥 CodeWithMosh"]
    },
    "روانشناسی": {
        "title": "🧠 مسیر تخصصی روانشناسی",
        "type": "روانشناسی",
        "duration_years": 5,
        "income_range": "۳۰-۸۰ میلیون تومان",
        "job_growth": "خوب",
        "steps": [
            {"year": 1, "title": "مبانی روانشناسی", "subjects": ["روانشناسی عمومی", "آمار"], "milestone": "درک مفاهیم پایه"},
            {"year": 2, "title": "روانشناسی رشد", "subjects": ["نظریه‌های شخصیت"], "milestone": "تحلیل مطالعه موردی"},
            {"year": 3, "title": "آسیب‌شناسی", "subjects": ["روان‌درمانی"], "milestone": "۲۰ جلسه کارآموزی"},
            {"year": 4, "title": "کارورزی", "subjects": ["مشاوره"], "milestone": "دریافت تأییدیه"},
            {"year": 5, "title": "پروژه", "subjects": ["پایان‌نامه"], "milestone": "اخذ پروانه نظام"}
        ],
        "skills": ["همدلی", "مهارت گوش دادن", "تحلیل رفتار"],
        "jobs": ["روانشناس بالینی", "مشاور مدرسه"],
        "recommended_resources": ["📘 هیلگارد", "🌐 APA", "🎥 Psych2Go"]
    }
}

def get_roadmap(career_key):
    return CAREER_ROADMAPS.get(career_key)

def get_roadmaps_by_holland(holland_type):
    mapping = {
        "پژوهشی": ["پزشکی"],
        "تحلیلی": ["مهندسی کامپیوتر"],
        "اجتماعی": ["روانشناسی"],
        "واقع‌گرا": ["مهندسی کامپیوتر"],
        "هنری": ["روانشناسی"],
        "متهور": ["مهندسی کامپیوتر"],
        "سازمانی": ["روانشناسی"]
    }
    keys = mapping.get(holland_type, ["پزشکی", "مهندسی کامپیوتر", "روانشناسی"])
    return [CAREER_ROADMAPS[k] for k in keys if k in CAREER_ROADMAPS]

def get_roadmaps_by_track(track):
    mapping = {
        "علوم تجربی": ["پزشکی"],
        "ریاضی فیزیک": ["مهندسی کامپیوتر"],
        "علوم انسانی": ["روانشناسی"],
        "هنر": ["روانشناسی"]
    }
    keys = mapping.get(track, ["پزشکی", "مهندسی کامپیوتر", "روانشناسی"])
    return [CAREER_ROADMAPS[k] for k in keys if k in CAREER_ROADMAPS]