import telebot
from telebot import types

# ضع التوكن الخاص بالبوت الخاص بك هنا بين العلامتين
TOKEN = 'YOUR_BOT_TOKEN_HERE' 
bot = telebot.TeleBot(TOKEN)

# إعدادات التسعيرة الخاصة بمشروع ممتاز
BASE_FARE = 16  # فتحة العداد
PER_KM_RATE = 10  # سعر الكيلومتر المربع

# شاشة ترحيبية بالركاب وخيارات الخدمة مباشرة دون مقدمات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_tuktuk = types.KeyboardButton("🛺 توكتوك")
    btn_tricycle = types.KeyboardButton("🏍️ تروسيكل")
    markup.add(btn_tuktuk, btn_tricycle)
    bot.send_message(message.chat.id, "اختر وسيلة النقل المطلوبة لتوصيلتك الخاصة:", reply_markup=markup)

# التعامل مع اختيار المركبة وطلب الموقع
@bot.message_handler(func=lambda message: message.text in ["🛺 توكتوك", "🏍️ تروسيكل"])
def request_location(message):
    vehicle = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # زر إرسال الموقع الحالي تلقائياً لتسهيل التجربة وسرعتها للراكب
    btn_geo = types.KeyboardButton("📍 إرسال موقعي الحالي", request_location=True)
    markup.add(btn_geo)
    bot.send_message(message.chat.id, f"لقد اخترت {vehicle}. يرجى إرسال موقعك الحالي الآن لتحديد نقطة الانطلاق:", reply_markup=markup)

# استقبال موقع الركوب والطلب من العميل كتابة الوجهة
@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    # حفظ الإحداثيات للعميل مؤقتاً لطلب تحديد الوجهة
    msg = bot.send_message(message.chat.id, "تم تحديد موقع الانطلاق بنجاح! 📍\nالآن، يرجى كتابة اسم وجهتك أو المكان الذي تريد الذهاب إليه:")
    bot.register_next_step_handler(msg, handle_destination, lat, lon)

# تأكيد الطلب للراكب وحساب التسعيرة التقديرية بناءً على المسافة والأسعار الثابتة لمنع الاستغلال
def handle_destination(message, lat, lon):
    destination = message.text
    bot.send_message(message.chat.id, f"جاري البحث عن أقرب سائق متاح وتوجيهه إليك..\n\n📝 تفاصيل الرحلة:\n- فتحة العداد الثابتة: {BASE_FARE} جنيه\n- تكلفة الكيلومتر: {PER_KM_RATE} جنيه\n- الوجهة المطلوبة: {destination}\n\nشكرًا لاستخدامك تطبيق ممتاز! رحلة آمنة وبتكلفة عادلة للجميع.")

# تشغيل البوت باستمرار
if __name__ == "__main__":
    bot.infinity_polling()
                                       
