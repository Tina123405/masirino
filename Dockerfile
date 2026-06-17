FROM python:3.11-slim

WORKDIR /app

# کپی همه فایل‌ها به کانتینر
COPY . .

# پورت پیش‌فرض
EXPOSE 8000

# اجرای برنامه
CMD ["python", "main.py"]