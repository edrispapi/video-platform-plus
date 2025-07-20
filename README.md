# Video Streaming Platform (پلتفرم ویدئویی مشابه آپارات/یوتیوب)

این پروژه یک سامانه پیشرفته برای پخش، ذخیره و مدیریت ویدئو است که امکاناتی همچون استریم زنده، آرشیو ویدئویی، پرداخت آنلاین، چت بلادرنگ، جستجوی قدرتمند و مانیتورینگ سیستم را در سطح صنعتی ارائه می‌کند.

## ✨ امکانات و کارکردهای اصلی
- آپلود ویدیوی کاربر، آرشیو و پخش با پردازش حرفه‌ای
- پخش زنده و استریم حرفه‌ای با HLS/DASH
- پرداخت آنلاین با زرین‌پال و بلاکچین/NFT
- احراز هویت امن با JWT
- چت و تعامل بلادرنگ با WebSocket
- جستجو با ElasticSearch
- مانیتورینگ با Prometheus/Grafana
- پیشنهاد و دسته‌بندی هوشمند محتوا
- پردازش ویدئو و صوت با Celery و FFmpeg
- سیستم کامنت‌ها و رأی‌دهی
- مدیریت کانال‌ها و اشتراک
- لیست پخش سفارشی

## 🚀 شروع سریع
1. پیش‌نیاز: Docker، Kubernetes، Python 3.9+
2. تنظیم فایل `.env` با کلیدهای API (مثال: `API_KEY=your_infura_key`)
3. اجرای محلی: `docker-compose up --build`
4. استقرار Kubernetes:
   - اعمال `kubectl apply -f Kubernetes/web-deployment.yaml`
   - تنظیم Ingress برای HTTPS با Certbot
5. نصب پکیج‌ها: `pip install -r requirements.txt`

## 📚 مستندات API
- API عمومی در `api/dev_api.py` برای توسعه‌دهندگان
- مستندات Swagger: `http://yourdomain.com/api/docs`
- نمونه درخواست: `curl -X GET http://yourdomain.com/api/videos/?q=test`

## 🌐 چندزبانه
- پشتیبانی از فارسی و انگلیسی با `django-i18n`
- ایجاد فایل‌های ترجمه: `python manage.py makemessages -l fa` و `python manage.py compilemessages`

## ⚙️ پیش‌نیازها
- Docker, Kubernetes, NGINX, FFmpeg
- پکیج‌ها: `pip install django djangorestframework channels redis celery`

## 🚧 نکات امنیتی
- HTTPS با Let’s Encrypt
- رمزنگاری داده‌ها با AES-256

## 🛠️ عیب‌یابی
- اگر Docker اجرا نشد: مطمئن شوید پورت 80 آزاد است.
- خطای API: کلیدهای `.env` را چک کنید.
