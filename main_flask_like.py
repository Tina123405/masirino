# main_flask_like.py - موتور قالب خالص پایتون (بدون نصب Flask)

import re
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class TemplateEngine:
    """موتور قالب‌سازی ساده - جایگزین Jinja2 بدون نصب کتابخانه"""
    
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir
    
    def render(self, template_name, **context):
        """رندر کردن قالب با جایگزینی متغیرها"""
        template_path = os.path.join(self.template_dir, template_name)
        
        if not os.path.exists(template_path):
            return f"<h1>قالب {template_name} یافت نشد</h1>"
        
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # جایگزینی متغیرهای {{ variable }}
        for key, value in context.items():
            placeholder = f"{{{{ {key} }}}}"
            content = content.replace(placeholder, str(value))
        
        # پشتیبانی از حلقه ساده {% for item in items %}
        def replace_for_loop(match):
            loop_content = match.group(1)
            var_name = match.group(2)
            list_name = match.group(3)
            
            items = context.get(list_name, [])
            result = ""
            for item in items:
                result += loop_content.replace(f"{{{{ {var_name} }}}}", str(item))
            return result
        
        for_pattern = r'\{% for (\w+) in (\w+) %\}(.*?)\{% endfor %\}'
        content = re.sub(for_pattern, replace_for_loop, content, flags=re.DOTALL)
        
        # پشتیبانی از شرط ساده {% if condition %}
        def replace_if(match):
            condition = match.group(1)
            true_content = match.group(2)
            false_content = match.group(3) if match.group(3) else ""
            
            if context.get(condition, False):
                return true_content
            return false_content
        
        if_pattern = r'\{% if (\w+) %\}(.*?)(?:\{% else %\}(.*?))?\{% endif %\}'
        content = re.sub(if_pattern, replace_if, content, flags=re.DOTALL)
        
        return content


# ایجاد نمونه موتور قالب
template = TemplateEngine()

# ========== صفحات برنامه ==========

def home_page(session_id):
    return template.render("home.html", 
                         session_id=session_id,
                         title="مسیرینو - صفحه اصلی",
                         features=[
                             {"icon": "💬", "title": "چت هوشمند", "path": "chat"},
                             {"icon": "🎯", "title": "انتخاب رشته", "path": "track"},
                             {"icon": "📉", "title": "پیش‌بینی افت", "path": "risk"},
                         ])

def chat_page(session_id):
    return template.render("chat.html", session_id=session_id, title="چت بات مسیرینو")

def track_page(session_id):
    return template.render("track.html", session_id=session_id, title="انتخاب رشته")

def risk_page(session_id):
    return template.render("risk.html", session_id=session_id, title="پیش‌بینی افت")

# ========== سرور (بدون تغییر زیاد) ==========

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        session_id = qs.get("session_id", ["default"])[0]
        
        if path == "/" or path == "/home":
            self.respond(200, home_page(session_id))
        elif path == "/chat":
            self.respond(200, chat_page(session_id))
        elif path == "/track":
            self.respond(200, track_page(session_id))
        elif path == "/risk":
            self.respond(200, risk_page(session_id))
        elif path.startswith("/static/"):
            self.serve_static(path)
        else:
            self.respond(404, "<h1>صفحه یافت نشد</h1>")
    
    def serve_static(self, path):
        """سرویس فایل‌های استاتیک (CSS, JS)"""
        file_path = path[1:]  # حذف / اول
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            if file_path.endswith(".css"):
                self.send_response(200)
                self.send_header("Content-Type", "text/css")
                self.end_headers()
                self.wfile.write(content)
            elif file_path.endswith(".js"):
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript")
                self.end_headers()
                self.wfile.write(content)
            else:
                self.respond(404, "Not Found")
        else:
            self.respond(404, "Not Found")
    
    def respond(self, code, content, content_type="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

def run():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    print("🚀 سرور با موتور قالب‌سازی ساده اجرا شد (مشابه Flask)")
    print("📍 http://127.0.0.1:8000")
    server.serve_forever()

if __name__ == "__main__":
    run()