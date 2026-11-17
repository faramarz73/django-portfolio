# سایت نمونه‌کار با Django

## راه‌اندازی
```bash
python -m venv venv
source venv/bin/activate        # در ویندوز: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations works
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- سایت: https://code-nevesht.onrender.com
- پنل مدیریت: http://127.0.0.1:8000/admin/

## بعد از اولین اجرا (در پنل مدیریت)
1. **پروفایل** بسازید (نام، عنوان، معرفی، لینک سفارش) – فقط یک رکورد.
2. چند **دسته‌بندی** بسازید (مثلاً: ربات تلگرام / وب‌سایت / اپلیکیشن).
3. **پروژه‌ها** را با تصویر و لینک اضافه کنید.
4. **شبکه‌های اجتماعی** (تلگرام، اینستاگرام، ...) را اضافه کنید تا مشتری بتواند دنبالتان کند.

## انتشار روی سرور
متغیرهای محیطی `DJANGO_SECRET_KEY`، `DJANGO_DEBUG=0` و `DJANGO_ALLOWED_HOSTS` را تنظیم کنید،
`python manage.py collectstatic` بزنید و با gunicorn + nginx اجرا کنید (nginx باید پوشهٔ `media/` و `staticfiles/` را سرو کند).

## امکانات اضافه‌شده
- **وبلاگ** (`/blog/`): از پنل مدیریت، بخش «وبلاگ».
- **فرم سفارش** (`/order/`): سفارش‌ها در پنل مدیریت، بخش «سفارش‌ها» ذخیره می‌شوند و فیلد ضد اسپم دارد.
- **اعلان تلگرام برای سفارش جدید** (اختیاری): دو متغیر محیطی `TELEGRAM_BOT_TOKEN` و `TELEGRAM_CHAT_ID` را تنظیم کنید.
- **تاریخ شمسی** در وبلاگ؛ بدون نیاز به کتابخانهٔ اضافی (`{% load jalali %}` و فیلتر `jdate`).
