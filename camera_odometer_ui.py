# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - واجهة التقاط صورة العداد والفواتير (Kivy UI)
تاريخ التحديث: أغسطس 2026
"""

import os
import sys
import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
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
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. الواجهة الرسومية لالتقاط العداد والفواتير
# -------------------------------------------------------------
class CameraOdometerUI(BoxLayout):
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865", **kwargs):
        super().__init__(orientation='vertical', spacing=12, padding=15, **kwargs)
        
        self.truck_id = truck_id
        self.chassis_number = chassis_number
        self.captured_odometer_photo = None
        self.captured_receipt_photo = None

        # العنوان الرئيسي
        header = Label(
            text=ar(f"تأكيد إجراء - الشاحنة {self.truck_id}"),
            font_name=DEFAULT_FONT,
            font_size='18sp',
            size_hint_y=0.1,
            color=(0.2, 0.7, 1, 1)
        )
        self.add_widget(header)

        # حقل إدخال رقم العداد
        input_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.12)
        lbl_odometer = Label(
            text=ar("قراءة العداد الحالية:"),
            font_name=DEFAULT_FONT,
            font_size='14sp',
            size_hint_x=0.4
        )
        self.odometer_input = TextInput(
            hint_text=ar("أدخل الرقم هنا"),
            font_name=DEFAULT_FONT,
            multiline=False,
            input_filter='int',
            size_hint_x=0.6
        )
        input_box.add_widget(lbl_odometer)
        input_box.add_widget(self.odometer_input)
        self.add_widget(input_box)

        # أزرار التقاط الصور
        self.btn_odometer = Button(
            text=ar("1. اضغط هنا لالتقاط صورة العداد"),
            font_name=DEFAULT_FONT,
            font_size='15sp',
            background_color=(0.2, 0.5, 0.7, 1),
            size_hint_y=0.18
        )
        self.btn_odometer.bind(on_press=self.capture_odometer)
        self.add_widget(self.btn_odometer)

        self.btn_receipt = Button(
            text=ar("2. اضغط هنا لالتقاط صورة الفاتورة (اختياري)"),
            font_name=DEFAULT_FONT,
            font_size='15sp',
            background_color=(0.3, 0.6, 0.5, 1),
            size_hint_y=0.18
        )
        self.btn_receipt.bind(on_press=self.capture_receipt)
        self.add_widget(self.btn_receipt)

        # زر التأكيد والإرسال
        btn_submit = Button(
            text=ar("3. إرسال وتأكيد الإجراء"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            background_color=(0.1, 0.7, 0.3, 1),
            size_hint_y=0.22
        )
        btn_submit.bind(on_press=self.validate_and_submit)
        self.add_widget(btn_submit)

    def capture_odometer(self, instance):
        """ محاكاة التقاط صورة العداد """
        self.captured_odometer_photo = "odometer_photo_mock.jpg"
        self.btn_odometer.text = ar("تم التقاط صورة العداد بنجاح")
        self.btn_odometer.background_color = (0.1, 0.8, 0.3, 1)

    def capture_receipt(self, instance):
        """ محاكاة التقاط صورة الفاتورة """
        self.captured_receipt_photo = "receipt_photo_mock.jpg"
        self.btn_receipt.text = ar("تم التقاط صورة الفاتورة بنجاح")
        self.btn_receipt.background_color = (0.1, 0.8, 0.3, 1)

    def show_popup(self, title, message):
        """ إظهار رسالة تنبيه للمستخدم """
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lbl = Label(text=ar(message), font_name=DEFAULT_FONT, font_size='15sp', halign='center')
        btn = Button(text=ar("موافق"), font_name=DEFAULT_FONT, size_hint_y=0.3, background_color=(0.2, 0.6, 0.8, 1))
        content.add_widget(lbl)
        content.add_widget(btn)
        
        popup = Popup(title=ar(title), title_font=DEFAULT_FONT, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def validate_and_submit(self, instance):
        """ التحقق من الشروط وإرسال البيانات """
        odometer_val = self.odometer_input.text.strip()

        if not odometer_val:
            self.show_popup("تنبيه", "يرجى إدخال قراءة العداد أولاً!")
            return

        if not self.captured_odometer_photo:
            self.show_popup("خطأ في التوثيق", "عذراً! لا يمكنك الإرسال بدون التقاط صورة العداد أولاً.")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"تم إرسال البيانات بنجاح!\nالعداد: {odometer_val} كم\nالوقت: {timestamp}"
        self.show_popup("نجاح العملية", msg)

# -------------------------------------------------------------
# 3. مشغل الواجهة
# -------------------------------------------------------------
class CameraApp(App):
    def build(self):
        return CameraOdometerUI()

if __name__ == "__main__":
    CameraApp().run()