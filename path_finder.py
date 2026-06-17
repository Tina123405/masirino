# path_finder.py - نسخه به‌روز شده با توصیه‌گر پیشرفته

from path_finder_data import CAREER_ROADMAPS, get_roadmap, get_roadmaps_by_holland, get_roadmaps_by_track
from adaptive_recommender_advanced import get_advanced_recommender, log_recommendation_feedback


class PathFinder:
    def __init__(self, session_id):
        self.session_id = session_id
        self.recommender = get_advanced_recommender(session_id)
    
    def _load_user_data(self):
        try:
            from database import get_user_from_db, get_holland_results
            user = get_user_from_db(self.session_id)
            holland = get_holland_results(self.session_id)
            
            holland_type = None
            if holland:
                if isinstance(holland, dict):
                    holland_type = holland.get("primary_type")
                elif isinstance(holland, str):
                    holland_type = holland
            
            track = user.get("track") if user else None
            
            return {"holland_type": holland_type, "track": track}
        except Exception as e:
            print(f"Error loading user data: {e}")
            return {"holland_type": None, "track": None}
    
    def get_recommended_roadmaps(self, limit=3):
        user_data = self._load_user_data()
        roadmaps = []
        
        if user_data.get("holland_type"):
            roadmaps = get_roadmaps_by_holland(user_data["holland_type"])
        
        if not roadmaps and user_data.get("track"):
            roadmaps = get_roadmaps_by_track(user_data["track"])
        
        if not roadmaps:
            roadmaps = list(CAREER_ROADMAPS.values())
        
        # استفاده از توصیه‌گر پیشرفته برای رتبه‌بندی
        for i, rm in enumerate(roadmaps):
            # دریافت امتیاز شخصی‌سازی شده از توصیه‌گر
            recommendations = self.recommender.get_personalized_recommendations([], limit=10)
            personal_score = 50
            for rec in recommendations:
                if rec["item"] == rm.get("type", ""):
                    personal_score = rec["score"]
                    break
            
            # ترکیب نمره اصلی با نمره شخصی
            base_match = 90 - (i * 15)
            final_score = (base_match * 0.6) + (personal_score * 0.4)
            rm["match_percent"] = min(99, round(final_score, 1))
            rm["personal_match"] = round(personal_score, 1)
        
        # مرتب‌سازی مجدد بر اساس امتیاز شخصی‌سازی شده
        roadmaps.sort(key=lambda x: x.get("match_percent", 0), reverse=True)
        
        return roadmaps[:limit]
    
    def get_roadmap_detail(self, career_key):
        # ثبت تعامل کاربر با این شغل
        log_recommendation_feedback(self.session_id, f"career_{career_key}", clicked=True)
        return get_roadmap(career_key)
    
    def save_career_interest(self, career_key):
        """ذخیره به عنوان علاقه‌مندی (امتیاز بالاتر)"""
        log_recommendation_feedback(self.session_id, f"career_{career_key}", saved=True)
        return True


def get_path_finder_data(session_id):
    pf = PathFinder(session_id)
    # همچنین دریافت توصیه‌های هوشمند برای داشبورد
    adv_recommender = get_advanced_recommender(session_id)
    dashboard_recs = adv_recommender.get_adaptive_dashboard_recommendations()
    
    return {
        "recommended_roadmaps": pf.get_recommended_roadmaps(),
        "user_data": pf._load_user_data(),
        "smart_recommendations": dashboard_recs
    }

def get_roadmap_detail_api(session_id, career_key):
    pf = PathFinder(session_id)
    roadmap = pf.get_roadmap_detail(career_key)
    if roadmap:
        return {"status": "ok", "roadmap": roadmap}
    return {"status": "error", "message": "not found"}

def save_career_interest_api(session_id, career_key):
    pf = PathFinder(session_id)
    pf.save_career_interest(career_key)
    return {"status": "ok"}