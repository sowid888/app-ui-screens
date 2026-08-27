# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - الواجهة الرئيسية المباشرة
"""

import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase

# -------------------------------------------------------------
# 1. إعداد الخط العربي
# -------------------------------------------------------------
local_font = os.path.join(os.path.dirname(__file__), "arial.ttf")
win_font = r"C:\Windows\Fonts\arial.ttf"

if os.path.exists(local_font):
    LabelBase.register(name="ArabicFont", fn_regular=local_font)
    DEFAULT_FONT = "ArabicFont"
elif os.path.exists(win_font):
    LabelBase.register(name="ArabicFont", fn_regular=win_font)
    DEFAULT_FONT = "ArabicFont"
else:
    DEFAULT_FONT = "Roboto"

def ar(text):
    if not text:
        return ""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        return get_display(arabic_reshaper.reshape(str(text)))
    except Exception:
        return str(text)

# -------------------------------------------------------------
# 2. تخصيص العناصر للدعم العربي
# -------------------------------------------------------------
class ArabicSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = DEFAULT_FONT
        self.font_size = '15sp'

class ArabicTextInput(TextInput):
    pass

# -------------------------------------------------------------
# 3. شاشات الواجهة (مُعرّفة قبل استخدامها)
# -------------------------------------------------------------
class MainMenuScreen(Screen):
    def __init__(self, truck_id="2600-001", driver_name="سائق الميدان", **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=15)

        header = Label(
            text=ar(f"شاحنة: {truck_id} | السائق: {driver_name}"),
            font_size='18sp',
            font_name=DEFAULT_FONT,
            size_hint_y=0.1,
            color=(0.1, 0.9, 0.5, 1)
        )
        main_layout.add_widget(header)

        grid = GridLayout(cols=2, spacing=10, size_hint_y=0.9)

        buttons = [
            ("screen_odometer", "1. قراءة العداد والتنبيهات", (0.1, 0.4, 0.6, 1)),
            ("screen_fuel", "2. التزود بالوقود والإيصال", (0.2, 0.6, 0.3, 1)),
            ("screen_wash", "3. الصيانة وغسيل الشاحنة", (0.5, 0.4, 0.2, 1)),
            ("screen_truck_faults", "4. أعطال الشاحنات", (0.8, 0.3, 0.2, 1)),
            ("screen_car_faults", "5. أعطال السيارات الصغرى", (0.7, 0.2, 0.5, 1)),
            ("screen_messages", "6. صندوق الرسائل", (0.3, 0.3, 0.7, 1)),
        ]

        for s_name, title, color in buttons:
            btn = Button(
                text=ar(title),
                font_name=DEFAULT_FONT,
                font_size='15sp',
                background_color=color
            )
            btn.bind(on_press=lambda inst, name=s_name: setattr(self.manager, 'current', name))
            grid.add_widget(btn)

        main_layout.add_widget(grid)
        self.add_widget(main_layout)

class FaultsScreen(Screen):
    def __init__(self, title_name, options_list, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        main_layout.add_widget(Label(
            text=ar(title_name),
            font_name=DEFAULT_FONT,
            font_size='18sp',
            size_hint_y=0.1,
            color=(0.2, 0.7, 1, 1)
        ))

        form = GridLayout(cols=2, spacing=10, size_hint_y=0.75)

        form.add_widget(Label(text=ar("اختر العطل / الخدمة:"), font_name=DEFAULT_FONT, font_size='15sp'))
        formatted_options = [ar(opt) for opt in options_list]
        self.spinner_fault = Spinner(
            text=formatted_options[0] if formatted_options else ar("اختر العطل"),
            values=formatted_options,
            font_name=DEFAULT_FONT,
            font_size='15sp',
            option_cls=ArabicSpinnerOption
        )
        form.add_widget(self.spinner_fault)

        form.add_widget(Label(text=ar("درجة الأهمية:"), font_name=DEFAULT_FONT, font_size='15sp'))
        priorities = [ar("عادي"), ar("متوسط"), ar("طوارئ / عاجل")]
        self.spinner_priority = Spinner(
            text=priorities[0],
            values=priorities,
            font_name=DEFAULT_FONT,
            font_size='15sp',
            option_cls=ArabicSpinnerOption
        )
        form.add_widget(self.spinner_priority)

        form.add_widget(Label(text=ar("ملاحظات إضافية:"), font_name=DEFAULT_FONT, font_size='15sp'))
        self.input_notes = ArabicTextInput(
            font_name=DEFAULT_FONT,
            font_size='15sp',
            multiline=True,
            base_direction='rtl',
            halign='right'
        )
        form.add_widget(self.input_notes)

        main_layout.add_widget(form)

        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        btn_send = Button(text=ar("إرسال البلاغ"), font_name=DEFAULT_FONT, background_color=(0.1, 0.6, 0.3, 1))
        btn_send.bind(on_press=self.send_data)
        
        btn_back = Button(text=ar("الرجوع للقائمة"), font_name=DEFAULT_FONT, background_color=(0.7, 0.2, 0.2, 1))
        btn_back.bind(on_press=lambda inst: setattr(self.manager, 'current', 'main_menu'))

        btns.add_widget(btn_send)
        btns.add_widget(btn_back)
        main_layout.add_widget(btns)

        self.add_widget(main_layout)

    def send_data(self, instance):
        raw_notes = self.input_notes.text
        formatted_notes = ar(raw_notes) if raw_notes else ar("لا يوجد")
        msg = f"تم تسجيل البلاغ:\n{self.spinner_fault.text}\nدرجة الأهمية: {self.spinner_priority.text}\nالملاحظات: {formatted_notes}"
        pop = Popup(title=ar("تأكيد البلاغ"), content=Label(text=msg, font_name=DEFAULT_FONT), size_hint=(0.8, 0.4))
        pop.open()

class FuelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        layout.add_widget(Label(text=ar("تعبئة الوقود وتوثيق الإيصال"), font_name=DEFAULT_FONT, font_size='18sp', size_hint_y=0.1))

        form = GridLayout(cols=2, spacing=10, size_hint_y=0.75)

        form.add_widget(Label(text=ar("نوع الوقود:"), font_name=DEFAULT_FONT, font_size='15sp'))
        self.fuel_type = Spinner(
            text=ar("ديزل"), 
            values=[ar("ديزل"), ar("بنزين 90"), ar("بنزين 95")], 
            font_name=DEFAULT_FONT,
            font_size='15sp',
            option_cls=ArabicSpinnerOption
        )
        form.add_widget(self.fuel_type)

        form.add_widget(Label(text=ar("كمية اللترات:"), font_name=DEFAULT_FONT, font_size='15sp'))
        self.liters_input = TextInput(font_name=DEFAULT_FONT, multiline=False, input_filter='float', font_size='15sp')
        form.add_widget(self.liters_input)

        form.add_widget(Label(text=ar("إجمالي المبلغ:"), font_name=DEFAULT_FONT, font_size='15sp'))
        self.cost_input = TextInput(font_name=DEFAULT_FONT, multiline=False, input_filter='float', font_size='15sp')
        form.add_widget(self.cost_input)

        layout.add_widget(form)

        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        btn_save = Button(text=ar("حفظ الإيصال"), font_name=DEFAULT_FONT, background_color=(0.1, 0.6, 0.3, 1))
        btn_back = Button(text=ar("الرجوع للقائمة"), font_name=DEFAULT_FONT, background_color=(0.7, 0.2, 0.2, 1))
        btn_back.bind(on_press=lambda inst: setattr(self.manager, 'current', 'main_menu'))

        btns.add_widget(btn_save)
        btns.add_widget(btn_back)
        layout.add_widget(btns)

        self.add_widget(layout)

# -------------------------------------------------------------
# 4. كلاس التطبيق الرئيسي والتشغيل (يُوضع في الأسفل دائماً)
# -------------------------------------------------------------
class MainUIApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainMenuScreen(name='main_menu'))

        truck_fault_list = ["عطل محرك", "عطل فرامل", "عطل كهرباء / بطارية", "عطل هيدروليك", "عطل إطارات / بنشر"]
        car_fault_list = ["عطل محرك", "عطل تكييف", "عطل فرامل", "زيت / صيانة دورية"]
        wash_list = ["غسيل كامل", "تشحيم وتغيير زيت", "صيانة دورية كل أسبوع"]

        sm.add_widget(FaultsScreen(title_name="أعطال الشاحنات", options_list=truck_fault_list, name="screen_truck_faults"))
        sm.add_widget(FaultsScreen(title_name="أعطال السيارات الصغرى", options_list=car_fault_list, name="screen_car_faults"))
        sm.add_widget(FaultsScreen(title_name="الصيانة وغسيل الشاحنة", options_list=wash_list, name="screen_wash"))

        sm.add_widget(FuelScreen(name="screen_fuel"))
        sm.add_widget(Screen(name="screen_odometer"))
        sm.add_widget(Screen(name="screen_messages"))

        return sm

if __name__ == "__main__":
    MainUIApp().run()