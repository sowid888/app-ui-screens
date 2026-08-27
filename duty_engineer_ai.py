import os
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# =========================================================
# 1. إعداد مفتاح API
# =========================================================
# يفضل وضع المفتاح في متغيرات البيئة Environment Variable
# أو استبدال النص بـ المفتاح الحقيقي الذي يبدأ بـ AIzaSy...
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "ضع_مفتاح_جوجل_API_الحقيقي_هنا")


class DutyEngineerScreen(BoxLayout):
    def __init__(self, truck_id="2600-001", truck_model="Isuzu Truck", **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.truck_id = truck_id
        self.truck_model = truck_model
        
        # خلفية النافذة الداكنة
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Header Title
        title_label = Label(
            text=f"المهندس المناوب (جسر Google المباشر) | الشاحنة: {self.truck_id}",
            font_name="Arabic",  # أو الخط المعتمد في مشروعك
            font_size='20sp',
            color=(0.2, 0.7, 1, 1),
            size_hint_y=0.1
        )
        self.add_widget(title_label)

        # منطقة المحادثة (ScrollView)
        self.scroll_view = ScrollView(size_hint=(1, 0.75))
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.scroll_view.add_widget(self.chat_layout)
        self.add_widget(self.scroll_view)

        # رسالة الترحيب الأولى
        self._add_message("المهندس المناوب", "متصل بحساب Google الذكي. اضغط للتحدث وسينقل كلامك فوراً للتحليل.")

        # زر المحادثة (Speak Button)
        self.action_button = Button(
            text="🎙️ اضغط للتحدث مع المهندس المناوب",
            font_name="Arabic",
            font_size='18sp',
            size_hint=(1, 0.15),
            background_color=(0.08, 0.25, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.action_button.bind(on_press=self.on_speak_button_pressed)
        self.add_widget(self.action_button)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _add_message(self, sender, text):
        """ إضافة نص للواجهة """
        msg_label = Label(
            text=f"[b]{sender}:[/b] {text}",
            markup=True,
            font_name="Arabic",
            font_size='16sp',
            size_hint_y=None,
            text_size=(self.width * 0.9, None),
            halign='right' if sender == "السائق" else 'left'
        )
        msg_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.chat_layout.add_widget(msg_label)
        
        # التمرير لأسفل تلقائياً عند إضافة رسالة
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 0))

    def on_speak_button_pressed(self, instance):
        """ محاكاة استقبال بلاغ السائق وبدء التحليل """
        driver_query = "الماكينة تخرج دخان أسود والسرعة ضعيفة"
        self._add_message("السائق", driver_query)
        
        # تعطيل الزر مؤقتاً أثناء الاتصال
        self.action_button.disabled = True
        self.action_button.text = "جاري الاتصال بـ Google AI..."

        # تشغيل طلب ה-API في Thread مستقل منعاً لتجميد الواجهة
        threading.Thread(target=self._fetch_gemini_response, args=(driver_query,), daemon=True).start()

    def _fetch_gemini_response(self, query):
        """ الاتصال المباشر والآمن بـ Google Gemini API """
        prompt = (
            f"أنت مهندس صيانة شاحنات خبير. الشاحنة: {self.truck_model} ({self.truck_id}). "
            f"المشكلة التي يواجهها السائق حالياً: {query}. "
            f"أعطِ السائق إجابة فنية مباشرة، مختصرة جداً وعملية في نقاط بدون مقدمات."
        )

        # Endpoint لنموذج gemini-1.5-flash
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        # إرسال المفتاح في ה-Header لتفادي مشاكل الـ URL encoding
        headers = {
            'Content-Type': 'application/json',
            'x-goog-api-key': GEMINI_API_KEY
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=12)
            if response.status_code == 200:
                result = response.json()
                ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            else:
                error_detail = response.json().get('error', {}).get('message', response.text)
                ai_reply = f"خطأ في الاستجابة من جوجل (كود {response.status_code}): {error_detail}"
        except Exception as err:
            ai_reply = f"فشل الاتصال بالإنترنت: ({str(err)})"

        # إرجاع النتيجة للـ Main Thread في Kivy
        Clock.schedule_once(lambda dt: self._display_ai_reply(ai_reply))

    def _display_ai_reply(self, reply_text):
        """ عرض رد المهندس المناوب وإعادة تفعيل الزر """
        self._add_message("المهندس المناوب (Google AI)", reply_text)
        self.action_button.disabled = False
        self.action_button.text = "🎙️ اضغط للتحدث مع المهندس المناوب"


class DutyEngineerApp(App):
    def build(self):
        self.title = "DutyEngineer"
        return DutyEngineerScreen()

if __name__ == '__main__':
    DutyEngineerApp().run()