# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - واجهة المهندس المناوب (Google AI ER)
تاريخ التحديث: أغسطس 2026
"""

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
from kivy.core.text import LabelBase

# -------------------------------------------------------------
# 1. إعداد الخط العربي ومعالجة المسارات تلقائياً
# -------------------------------------------------------------
local_font = os.path.join(os.path.dirname(__file__), "arial.ttf")
win_system_font = r"C:\Windows\Fonts\arial.ttf"

if os.path.exists(local_font):
    LabelBase.register(name="ArabicFont", fn_regular=local_font)
    DEFAULT_FONT = "ArabicFont"
elif os.path.exists(win_system_font):
    LabelBase.register(name="ArabicFont", fn_regular=win_system_font)
    DEFAULT_FONT = "ArabicFont"
else:
    DEFAULT_FONT = "Roboto"

def ar(text):
    """ دالة معالجة النصوص العربية """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. إعداد مفتاح API الخاص بجوجل
# -------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "ضع_مفتاح_جوجل_API_الحقيقي_هنا")

# -------------------------------------------------------------
# 3. الواجهة الرسومية للمهندس المناوب
# -------------------------------------------------------------
class DutyEngineerScreen(BoxLayout):
    def __init__(self, truck_id="2600-001", truck_model="Isuzu/Mitsubishi 6-Ton", **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.truck_id = truck_id
        self.truck_model = truck_model
        
        # خلفية النافذة الداكنة
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # العنوان الرئيسي
        title_label = Label(
            text=ar(f"المهندس المناوب (الطوارئ الهندسية) | الشاحنة: {self.truck_id}"),
            font_name=DEFAULT_FONT,
            font_size='18sp',
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
        self._add_message("المهندس المناوب", ar("أهلاً بك. اكتب المشكلة أو اضغط للتحدث وسأقوم بتحليل العطل فوراً."))

        # زر التواصل
        self.action_button = Button(
            text=ar("🎙️ اضغط للتحدث / إرسال المشكلة للمهندس المناوب"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
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
        sender_ar = ar(sender)
        msg_label = Label(
            text=f"[b]{sender_ar}:[/b] {text}",
            markup=True,
            font_name=DEFAULT_FONT,
            font_size='15sp',
            size_hint_y=None,
            text_size=(self.width * 0.9, None),
            halign='right' if sender == "السائق" else 'left'
        )
        msg_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.chat_layout.add_widget(msg_label)
        
        Clock.schedule_once(lambda dt: setattr(self.scroll_view, 'scroll_y', 0))

    def on_speak_button_pressed(self, instance):
        """ استقبال بلاغ السائق وبدء التحليل """
        driver_query = ar("الماكينة تخرج دخان أسود والسرعة ضعيفة")
        self._add_message("السائق", driver_query)
        
        self.action_button.disabled = True
        self.action_button.text = ar("جاري الاتصال بالطوارئ الهندسية...")

        threading.Thread(target=self._fetch_gemini_response, args=(driver_query,), daemon=True).start()

    def _fetch_gemini_response(self, query):
        """ الاتصال المباشر والآمن بـ Google Gemini API """
        prompt = (
            f"أنت مهندس صيانة شاحنات خبير. الشاحنة: {self.truck_model} ({self.truck_id}). "
            f"المشكلة التي يواجهها السائق حالياً: {query}. "
            f"أعطِ السائق إجابة فنية مباشرة، مختصرة جداً وعملية في نقاط بدون مقدمات."
        )

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
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
                ai_reply = f"خطأ في الاستجابة (كود {response.status_code}): {error_detail}"
        except Exception as err:
            ai_reply = f"فشل الاتصال بالإنترنت: ({str(err)})"

        Clock.schedule_once(lambda dt: self._display_ai_reply(ar(ai_reply)))

    def _display_ai_reply(self, reply_text):
        """ عرض رد المهندس المناوب وإعادة تفعيل الزر """
        self._add_message("المهندس المناوب", reply_text)
        self.action_button.disabled = False
        self.action_button.text = ar("🎙️ اضغط للتحدث / إرسال المشكلة للمهندس المناوب")


class DutyEngineerApp(App):
    def build(self):
        self.title = "DutyEngineer"
        return DutyEngineerScreen()

if __name__ == '__main__':
    DutyEngineerApp().run()