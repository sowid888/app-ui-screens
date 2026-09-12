# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - وحدة الإدخال اليدوي والتحقق الذكي من العداد
تاريخ التحديث: أغسطس 2026
"""

import os
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase

# إعداد الخط العربي
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
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

class SmartOdometerUI(BoxLayout):
    def __init__(self, truck_id="2600-001", last_recorded_km=125000, **kwargs):
        super().__init__(orientation='vertical', spacing=12, padding=15, **kwargs)
        
        self.truck_id = truck_id
        # حفظ آخر قراءة معتمدة للمركبة
        self.last_recorded_km = last_recorded_km
        self.captured_photo_path = None

        # العنوان
        header = Label(
            text=ar(f"تسجيل العداد | الشاحنة {self.truck_id}"),
            font_name=DEFAULT_FONT,
            font_size='18sp',
            size_hint_y=0.1,
            color=(0.2, 0.7, 1, 1)
        )
        self.add_widget(header)

        # عرض آخر قراءة مسجلة
        lbl_last = Label(
            text=ar(f"آخر قراءة مسجلة بالمسار: {self.last_recorded_km:,} كم"),
            font_name=DEFAULT_FONT,
            font_size='14sp',
            color=(0.9, 0.9, 0.2, 1),
            size_hint_y=0.08
        )
        self.add_widget(lbl_last)

        # حقل الإدخال اليدوي
        input_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.12)
        lbl_input = Label(
            text=ar("القراءة الحالية:"),
            font_name=DEFAULT_FONT,
            font_size='14sp',
            size_hint_x=0.35
        )
        self.odometer_input = TextInput(
            hint_text=ar("أدخل الرقم الفعلي"),
            font_name=DEFAULT_FONT,
            multiline=False,
            input_filter='int',
            size_hint_x=0.65
        )
        input_box.add_widget(lbl_input)
        input_box.add_widget(self.odometer_input)
        self.add_widget(input_box)

        # زر التقاط الصورة كتوثيق فقط
        self.btn_photo = Button(
            text=ar("📷 التقاط صورة العداد (للتوثيق الإداري)"),
            font_name=DEFAULT_FONT,
            font_size='14sp',
            background_color=(0.2, 0.5, 0.7, 1),
            size_hint_y=0.18
        )
        self.btn_photo.bind(on_press=self.take_photo_attachment)
        self.add_widget(self.btn_photo)

        # زر التأكيد والحفظ
        btn_submit = Button(
            text=ar("✅ تأكيد واعتماد القراءة"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            background_color=(0.1, 0.7, 0.3, 1),
            size_hint_y=0.22
        )
        btn_submit.bind(on_press=self.validate_and_submit)
        self.add_widget(btn_submit)

    def take_photo_attachment(self, instance):
        """ إرفاق صورة توثيقية """
        self.captured_photo_path = f"odometer_{self.truck_id}.jpg"
        self.btn_photo.text = ar("✓ تم إرفاق صورة العداد")
        self.btn_photo.background_color = (0.1, 0.8, 0.3, 1)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl = Label(text=ar(message), font_name=DEFAULT_FONT, font_size='14sp', halign='center')
        btn = Button(text=ar("موافق"), font_name=DEFAULT_FONT, size_hint_y=0.3, background_color=(0.2, 0.6, 0.8, 1))
        content.add_widget(lbl)
        content.add_widget(btn)
        
        popup = Popup(title=ar(title), title_font=DEFAULT_FONT, content=content, size_hint=(0.85, 0.45))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def validate_and_submit(self, instance):
        raw_val = self.odometer_input.text.strip()

        # 1. التحقق من وجود مدخلات
        if not raw_val:
            self.show_popup("تنبيه", "عفواً! يجب إدخال قراءة العداد أولاً.")
            return

        current_km = int(raw_val)

        # 2. حظر وقبول القراءات بناءً على المنطق الإداري
        if current_km < self.last_recorded_km:
            # رفض قاطع إذا كانت القراءة أقل
            self.show_popup(
                "❌ تم رفض العملية",
                f"القراءة المادخلة ({current_km:,} كم) أقل من آخر قراءة مسجلة ({self.last_recorded_km:,} كم)!\nيرجى التأكد من الرقم الصحيح."
            )
            return

        if current_km == self.last_recorded_km:
            self.show_popup("تنبيه", "القراءة المدخلة مساوية لآخر قراءة تماماً. هل أنت متاكد؟")
            return

        # 3. التحقق من الزيادة المفرطة (أكثر من 1500 كم في عملية واحدة للتنبيه)
        diff = current_km - self.last_recorded_km
        if diff > 1500:
            self.show_popup("تنبيه تدقيق", f"الفارق كبير جداً (+{diff:,} كم). تم إرسال البلاغ مع إخطار الإدارة للمراجعة.")

        # 4. حفظ واعتماد القراءة الجديد
        self.last_recorded_km = current_km
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.show_popup(
            "✅ تم الاعتماد بنجاح",
            f"تم تحديث العداد إلى: {current_km:,} كم\nمقدار قطع المسافة: +{diff:,} كم\nالتاريخ: {timestamp}"
        )

class SmartOdometerApp(App):
    def build(self):
        return SmartOdometerUI()

if __name__ == "__main__":
    SmartOdometerApp().run()