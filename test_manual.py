# test_manual.py
# تست‌های واحد بدون هیچ کتابخانه اضافی

import sys

def run_all_tests():
    print("\n🧪 شروع تست‌های واحد...\n")
    passed = 0
    failed = 0
    
    # تست 1: پیش‌بینی ریسک
    try:
        from track_risk_logic import compute_risk_fall_detailed
        test_data = {
            "study_mode": "منظم",
            "has_review": "دارم (منظم)",
            "sleep_status": "خوب",
            "distract_rating": 3,
            "stress_rating": 3,
            "can_execute_plan": 3,
            "study_hours_rating": 4,
            "start_days_before_exam": "30+",
            "main_weakness_area": "محاسباتی / تمرین",
            "family_support": "خوب",
            "previous_fail": "ندارم",
            "test_anxiety": 3
        }
        result = compute_risk_fall_detailed(test_data)
        assert 0 <= result["risk_percent"] <= 100, "ریسک باید بین 0 تا 100 باشد"
        assert result["bucket"] in ["کم", "قابل قبول", "متوسط", "بالا"], "باکت نامعتبر"
        print(f"   ✅ تست 1 پاس شد - ریسک: {result['risk_percent']}%")
        passed += 1
    except Exception as e:
        print(f"   ❌ تست 1 شکست خورد: {e}")
        failed += 1
    
    # تست 2: خلاصه‌ساز هوشمند
    try:
        from smart_summarizer import SmartSummarizer
        test_text = "پایتون یک زبان برنامه‌نویسی سطح بالا است. این زبان ساده و قدرتمند است. پایتون برای یادگیری ماشین و علم داده کاربرد دارد."
        summary = SmartSummarizer.summarize(test_text, num_sentences=2)
        assert len(summary) > 0, "خلاصه نباید خالی باشد"
        print(f"   ✅ تست 2 پاس شد - طول خلاصه: {len(summary)} کاراکتر")
        passed += 1
    except Exception as e:
        print(f"   ❌ تست 2 شکست خورد: {e}")
        failed += 1
    
    # تست 3: پیش‌بینی ML
    try:
        from ml_predictor_pure import get_predictor
        predictor = get_predictor()
        test_features = {
            "study_hours": 5, "study_days": 6, "prev_grade": 16,
            "sleep_hours": 8, "stress_level": 2, "test_anxiety": 2,
            "consistency": 4, "review_count": 5, "tutor": 1, "attendance": 5
        }
        result = predictor.predict(test_features)
        assert "predicted_grade" in result, "پیش‌بینی باید شامل نمره باشد"
        assert 10 <= result["predicted_grade"] <= 20, "نمره باید بین 10 تا 20 باشد"
        print(f"   ✅ تست 3 پاس شد - نمره پیش‌بینی شده: {result['predicted_grade']}")
        passed += 1
    except Exception as e:
        print(f"   ❌ تست 3 شکست خورد: {e}")
        failed += 1
    
    # تست 4: دیتابیس
    try:
        from database import get_db_connection, init_db
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        assert len(tables) >= 20, "حداقل 20 جدول باید وجود داشته باشد"
        conn.close()
        print(f"   ✅ تست 4 پاس شد - {len(tables)} جدول در دیتابیس")
        passed += 1
    except Exception as e:
        print(f"   ❌ تست 4 شکست خورد: {e}")
        failed += 1
    
    # تست 5: چت بات
    try:
        from track_risk_logic import chatbot_respond
        response = chatbot_respond("سلام", "test_user")
        assert len(response) > 0, "پاسخ نباید خالی باشد"
        print(f"   ✅ تست 5 پاس شد - پاسخ چت بات: {response[:50]}...")
        passed += 1
    except Exception as e:
        print(f"   ❌ تست 5 شکست خورد: {e}")
        failed += 1
    
    print(f"\n📊 نتیجه نهایی: {passed} پاس, {failed} شکست")
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)