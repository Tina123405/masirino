# school_api_adapter.py
# الگوی استاندارد اتصال به سامانه مدرسه

from abc import ABC, abstractmethod
from datetime import datetime


class SchoolAPIProvider(ABC):
    """اینترفیس استاندارد برای همه سامانه‌های مدرسه"""
    
    @abstractmethod
    def authenticate(self, api_key, username="", password=""):
        pass
    
    @abstractmethod
    def get_student_info(self, national_code):
        pass
    
    @abstractmethod
    def get_grades(self, student_id, term="first"):
        pass


class MockSchoolAPI(SchoolAPIProvider):
    """شبیه‌ساز داخلی - برای تست و نمایش"""
    
    def authenticate(self, api_key, username="", password=""):
        # برای تست، هر API کی ای قبول می‌شود
        return {"success": True, "token": "mock_token_" + api_key[:8]}
    
    def get_student_info(self, national_code):
        # داده‌های شبیه‌سازی شده
        mock_students = {
            "0012345678": {
                "name": "محمد رضایی",
                "father_name": "علی",
                "school": "دبیرستان علامه حلی",
                "grade": "دهم",
                "field": "ریاضی فیزیک",
                "national_code": "0012345678"
            },
            "0087654321": {
                "name": "سارا حسینی",
                "father_name": "رضا",
                "school": "دبیرستان فرزانگان",
                "grade": "یازدهم",
                "field": "علوم تجربی",
                "national_code": "0087654321"
            }
        }
        
        if national_code in mock_students:
            return mock_students[national_code]
        return {"error": "دانش‌آموز یافت نشد"}
    
    def get_grades(self, student_id, term="first"):
        # نمرات شبیه‌سازی شده
        return {
            "success": True,
            "grades": [
                {"subject": "ریاضی", "score": 17.5, "term": term},
                {"subject": "فیزیک", "score": 16.8, "term": term},
                {"subject": "شیمی", "score": 18.2, "term": term},
                {"subject": "ادبیات", "score": 15.0, "term": term},
                {"subject": "زبان", "score": 16.5, "term": term}
            ],
            "average": 16.8,
            "term": term
        }


class RealSchoolAPI(SchoolAPIProvider):
    """
    کلاس آماده برای اتصال به API واقعی وزارت آموزش
    
    🔥 وقتی API واقعی در دسترس باشد، فقط همین توابع را کامل کنید.
    🔥 بقیه سیستم بدون تغییر کار می‌کند.
    """
    
    def authenticate(self, api_key, username="", password=""):
        # TODO: در آینده - اتصال به API واقعی
        # مثال:
        # response = requests.post(REAL_API_URL + "/auth", json={...})
        # return response.json()
        return {"success": False, "error": "API واقعی هنوز فعال نشده است"}
    
    def get_student_info(self, national_code):
        # TODO: در آینده - دریافت اطلاعات واقعی
        return {"error": "API واقعی هنوز فعال نشده است"}
    
    def get_grades(self, student_id, term="first"):
        # TODO: در آینده - دریافت نمرات واقعی
        return {"error": "API واقعی هنوز فعال نشده است"}


def get_school_api(provider="mock"):
    """کارخانه - نمونه مناسب را برمی‌گرداند"""
    if provider == "mock":
        return MockSchoolAPI()
    elif provider == "real":
        return RealSchoolAPI()
    else:
        raise ValueError(f"provider '{provider}' شناخته نشد. از 'mock' یا 'real' استفاده کنید.")