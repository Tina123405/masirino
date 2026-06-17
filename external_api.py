# external_api.py
# لایه واسط استاندارد برای اتصال به سامانه مدارس

import json
import secrets
import sqlite3
from datetime import datetime
from config import DB_NAME
from school_api_adapter import get_school_api


class SecureSchoolAPIConnector:
    """لایه امن برای اتصال به سامانه مدرسه"""
    
    def __init__(self, provider="mock"):
        """
        provider: "mock" برای شبیه‌سازی، "real" برای API واقعی
        🔥 با تغییر همین یک خط، کل سیستم عوض می‌شود
        """
        self.api = get_school_api(provider)
        self.provider = provider
        self.current_token = None
    
    def authenticate(self, api_key):
        """احراز هویت با API Key"""
        result = self.api.authenticate(api_key)
        if result.get("success"):
            self.current_token = result.get("token")
        return result
    
    def get_student_info(self, national_code, access_token=None):
        """دریافت اطلاعات دانش‌آموز"""
        return self.api.get_student_info(national_code)
    
    def get_grades(self, student_id, access_token=None, term="first"):
        """دریافت نمرات دانش‌آموز"""
        return self.api.get_grades(student_id, term)
    
    def sync_student_data(self, national_code, api_key, target_user_id=None):
        """همگام‌سازی کامل اطلاعات"""
        # مرحله 1: احراز هویت
        auth = self.authenticate(api_key)
        if not auth.get("success"):
            return {
                "success": False,
                "error": "احراز هویت ناموفق. API Key نامعتبر است."
            }
        
        # مرحله 2: دریافت اطلاعات دانش‌آموز
        student = self.get_student_info(national_code, auth.get("token"))
        if student.get("error"):
            return {
                "success": False,
                "error": student.get("error", "اطلاعات دانش‌آموز یافت نشد")
            }
        
        # مرحله 3: دریافت نمرات
        grades_data = self.get_grades(national_code, auth.get("token"))
        
        # مرحله 4: ذخیره در دیتابیس (اگر کاربر وارد شده باشد)
        if target_user_id:
            self._save_to_db(target_user_id, student, grades_data)
        
        # مرحله 5: بازگشت نتیجه
        return {
            "success": True,
            "student": student,
            "grades": grades_data.get("grades", []) if isinstance(grades_data, dict) else [],
            "average": grades_data.get("average", 0) if isinstance(grades_data, dict) else 0,
            "provider": self.provider,
            "ready_for_upgrade": self.provider == "mock",  # اگر mock بود، آماده ارتقاست
            "upgrade_message": "با تغییر provider='real' به API واقعی متصل می‌شوید" if self.provider == "mock" else "",
            "synced_at": datetime.now().isoformat()
        }
    
    def _save_to_db(self, user_id, student, grades_data):
        """ذخیره اطلاعات همگام‌سازی شده در دیتابیس"""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            
            # ایجاد جدول اگر وجود ندارد
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS school_sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    national_code TEXT,
                    student_name TEXT,
                    school_name TEXT,
                    grade TEXT,
                    avg_score REAL,
                    synced_at TIMESTAMP
                )
            ''')
            
            avg_score = grades_data.get("average", 0) if isinstance(grades_data, dict) else 0
            
            cursor.execute('''
                INSERT INTO school_sync_log 
                (user_id, national_code, student_name, school_name, grade, avg_score, synced_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                student.get("national_code", ""),
                student.get("name", ""),
                student.get("school", ""),
                student.get("grade", ""),
                avg_score,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            print(f"✅ اطلاعات دانش‌آموز {student.get('name')} در دیتابیس ذخیره شد")
        except Exception as e:
            print(f"⚠️ خطا در ذخیره دیتابیس: {e}")
    
    def get_upgrade_instructions(self):
        """نشان می‌دهد چگونه به API واقعی مهاجرت کنیم"""
        return {
            "current_provider": self.provider,
            "to_upgrade_to_real": "در فایل main.py یا جایی که connector ساخته می‌شود، بنویسید:",
            "code_example": 'connector = SecureSchoolAPIConnector(provider="real")',
            "note": "کلاس RealSchoolAPI در school_api_adapter.py آماده است. فقط توابع آن را کامل کنید."
        }


# ========== تابع کمکی برای استفاده در کل سیستم ==========

def get_school_connector(provider="mock"):
    """دریافت نمونه connector با provider دلخواه"""
    return SecureSchoolAPIConnector(provider)


def sync_with_school(session_id, national_code, api_key):
    """راحت‌ترین تابع برای همگام‌سازی - فقط همین را صدا بزن"""
    connector = get_school_connector("mock")  # 🔥 اینجا "mock" را به "real" تغییر بده
    return connector.sync_student_data(national_code, api_key, session_id)