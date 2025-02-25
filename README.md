# CyberStrike v3.0 - أداة اختبار الاختراق

أداة متقدمة لاختبار تحمل الأنظمة ضد هجمات DDoS باستخدام تقنيات حديثة.

## المميزات
- هجوم متعدد الطبقات (L3/L7)
- تشفير AES-256 لجميع الاتصالات
- واجهة مستخدم تمويهية
- دعم TOR المدمج
- تقارير أداء في الوقت الحقيقي

## التثبيت

```bash
# إنشاء بيئة افتراضية
python3 -m venv .venv && source .venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# التشغيل
python tool.py [--cli للوحة الأوامر]
```

## الاستخدام
```bash
# الوضع العادي (GUI)
python tool.py

# الوضع المتقدم (Terminal)
python tool.py --cli

# خيارات الهجوم:
# --target      تحديد الهدف (IP/URL)
# --intensity   شدة الهجوم (1-10)
# --duration    المدة بالثواني
# --tor         استخدام شبكة TOR

# مثال:
python tool.py --target example.com --intensity 9 --duration 60 --tor
```

## التحذير
**يُحظر استخدام هذه الأداة لأغراض غير قانونية.**  
جميع الاختبارات يجب أن تتم بموافقة كتابية من مالك النظام المستهدف.
