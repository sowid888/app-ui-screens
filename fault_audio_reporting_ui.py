# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - واجهة بلاغات الأعطال والتسجيل الصوتي
مجلد: app_ui_screens / fault_audio_reporting_ui.py
"""

import os
import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.text import LabelBase

# إعداد الخط العربي
local_font = os.path.join(os.path.dirname(os.path.dirname(__file__)), "arial.ttf")
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

class FaultAndAudioReportingEngine:
    def __init__(self, truck_id="2600-001", chassis_number="JAAKP34H2D7P06865"):
        self.truck_id = truck_id
        self.chassis_number = chassis_number
        self.recorded_audio_file = None
        self.attached_fault_photo = None

    def get_fault_categories(self, vehicle_type="TRUCK"):
        if vehicle_type == "TRUCK":
            return [
                ar("1. أعطال المحرك والميكانيكا"),
                ar("2. أعطال الكهرباء والإنارة"),
                ar("3. أعطال الفرامل والمكابح"),
                ar("4. أعطال الثلاجة والتبريد"),
                ar("5. أعطال الإطارات والجنوط"),
                ar("6. غسيل ونظافة صندوق الشاحنة"),
                ar("7. عطل آخر (استخدم الصوت أو النص)")
            ]
        else:
            return [
                ar("1. صيانة دورية (زيت/فلتر)"),
                ar("2. أعطال الميكانيكا والحرارة"),
                ar("3. أعطال الكهرباء والتكييف"),
                ar("4. الفرامل والإطارات"),
                ar("5. عطل آخر (استخدم الصوت أو النص)")
            ]

    def record_voice_note(self, mock_audio_path="voice_note.mp3"):
        self.recorded_audio_file = mock_audio_path
        return ar("🎙️ تم تسجيل الملاحظة الصوتية بنجاح واقترانها بالبلاغ.")

    def submit_fault_report(self, selected_category, free_text_description="", odometer_verified=True):
        if not odometer_verified:
            return {
                "success": False,
                "message": ar("❌ عفواً! يجب تأكيد وتصوير قراءة العداد أولاً.")
            }

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "success": True,
            "message": ar("🚀 تم إرسال بلاغ العطل والتسجيل الصوتي بنجاح إلى الإدارة!"),
            "report_details": {
                "truck_id": self.truck_id,
                "chassis_number": self.chassis_number,
                "category": selected_category,
                "text_note": free_text_description,
                "audio_attachment": "ATTACHED" if self.recorded_audio_file else "NONE",
                "timestamp": timestamp
            }
        }