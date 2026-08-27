# -*- coding: utf-8 -*-
"""
منظومة فاخر السيادية الكبرى 2600 - المحرك التنفيذي التفاعلي للأندرويد
تاريخ التحديث: أغسطس 2026
"""

import sys
import os

# إضافة المسار الحالي لضمان استيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase

# -------------------------------------------------------------
# 1. إعداد الخط العربي بمعالجة المسارات (بعد استيراد os)
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
    """ دالة معالجة النصوص العربية وحمايتها """
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(str(text))
        return get_display(reshaped)
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. الواجهة الرسومية التفاعلية لمنظومة 2600
# -------------------------------------------------------------
class FakherFleetUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        
        # الشريط العلوي الرئيسي
        header = Label(
            text=ar("منظومة فاخر 2600 - الأسطول الموحد"),
            font_size='20sp',
            font_name=DEFAULT_FONT,
            size_hint_y=0.1,
            color=(0.2, 0.7, 1, 1)
        )
        self.add_widget(header)

        # شبكة الأزرار (40 مربع تفاعلي)
        grid = GridLayout(cols=4, spacing=8, size_hint_y=0.9)
        
        for i in range(1, 41):
            btn_text = ar(f"مركبة {i}")
            btn = Button(
                text=f"{btn_text}\n{i}",
                font_name=DEFAULT_FONT,
                font_size='14sp',
                background_color=(0.1, 0.4, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda instance, vehicle_num=i: self.on_vehicle_click(vehicle_num))
            grid.add_widget(btn)

        self.add_widget(grid)

    def on_vehicle_click(self, vehicle_id):
        """ النافذة المنبثقة مجهزة بالخط العربي لكافة عناصرها """
        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        info_label = Label(
            text=ar(f"بيانات المركبة رقم: {vehicle_id}\nالحالة: جاهزة للعمل\nالعداد: 125,400 كم"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            halign='center'
        )
        content.add_widget(info_label)

        btn_fuel = Button(
            text=ar("تسجيل صرف ديزل"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            size_hint_y=0.3,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_fuel.bind(on_press=lambda x: self.process_action(vehicle_id, "تسجيل وقود"))
        content.add_widget(btn_fuel)

        btn_maint = Button(
            text=ar("طلب صيانة عاجلة"),
            font_name=DEFAULT_FONT,
            font_size='16sp',
            size_hint_y=0.3,
            background_color=(0.9, 0.4, 0.2, 1)
        )
        btn_maint.bind(on_press=lambda x: self.process_action(vehicle_id, "طلب صيانة"))
        content.add_widget(btn_maint)

        popup = Popup(
            title=ar(f"إدارة المركبة {vehicle_id}"),
            title_font=DEFAULT_FONT,
            content=content,
            size_hint=(0.85, 0.6)
        )
        popup.open()

    def process_action(self, vehicle_id, action_type):
        print(f"تم تنفيذ إجراء ({action_type}) للمركبة {vehicle_id}")

# -------------------------------------------------------------
# 3. مشغل التطبيق الأساسي
# -------------------------------------------------------------
class FakherFleetApp(App):
    def build(self):
        return FakherFleetUI()

if __name__ == "__main__":
    FakherFleetApp().run()