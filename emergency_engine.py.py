# -*- coding: utf-8 -*-
"""
منظومة فاخر 2600 - محرك الطوارئ الهندسية وقوائم الصيانة والأعطال الآلية
تاريخ التحديث: أغسطس 2026
"""

import datetime

class EmergencyAndMaintenanceEngine:
    def __init__(self):
        # -------------------------------------------------------------
        # 1. قوائم الأعطال المحددة مسبقاً (شاحنات متوسطة حتى 6 طن)
        # -------------------------------------------------------------
        self.fault_categories = {
            "الأعطال الكهربائية": [
                "ضعف أو تفريغ البطارية",
                "عطل دينامو الشحن",
                "عطل بادئ التشغيل (السلف)",
                "احتراق أحد الفيوزات الرئيسية",
                "عطل أنوار أو إشارات الشاحنة"
            ],
            "الأعطال الميكانيكية": [
                "ارتفاع درجة حرارة المحرك",
                "ضعف العزم / الشاحنة تمشي بصعوبة",
                "خروج أبخرة / عادم كثيف من المحرك",
                "اهتزاز غير طبيعي أثناء السير",
                "صوت طقطقة في المحرك"
            ],
            "أعطال نظام الوقود والديزل": [
                "انسداد فلاتر الديزل",
                "استهلاك عالي وغير طبيعي للوقود",
                "وجود هواء في دورة الديزل",
                "تسريب في خطوط الوقود"
            ],
            "أعطال المكابح (الفرامل)": [
                "ضعف استجابة المكابح",
                "قسوة دواسة الفرامل",
                "تسريب زيت الفرامل",
                "صوت احتكاك / صفير عند الفرملة"
            ],
            "أعطال الثلاجة وصندوق البودي": [
                "ارتفاع حرارة وحدة تبريد الثلاجة",
                "تسريب مياه داخل الصندوق",
                "عطل في قفل أو مفصلات أبواب الصندوق"
            ]
        }

        # -------------------------------------------------------------
        # 2. خيارات تنفيذ الصيانة الدوري
        # -------------------------------------------------------------
        self.maintenance_actions = [
            "تغيير زيت المحرك مع الفلتر",
            "استبدال فلاتر الديزل",
            "استبدال فلتر الهواء",
            "صيانة / تغيير فحمات الفرامل",
            "فحص وتعيير ضغط الإطارات",
            "تشحيم المحاور والمجاميع"
        ]

    def get_fault_categories(self):
        """ إرجاع أقسام الأعطال الرئيسية """
        return list(self.fault_categories.keys())

    def get_fault_options(self, category):
        """ إرجاع قائمة الأعطال المنسدلة بناءً على القسم المختار """
        return self.fault_categories.get(category, [])

    def get_maintenance_actions(self):
        """ إرجاع قائمة خيارات تنفيذ الصيانة """
        return self.maintenance_actions

    def submit_maintenance_log(self, action_selected, odometer_reading):
        """ تسجيل وإرسال تنفيذ الصيانة مع قراءة العداد """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "type": "تنفيذ صيانة",
            "action": action_selected,
            "odometer": odometer_reading,
            "timestamp": timestamp,
            "status": "تم الإرسال لدفتر العمليات"
        }

    def submit_fault_report(self, category, fault_selected, odometer_reading):
        """ تسجيل وإرسال بلاغ العطل الآلي مع العداد """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "type": "بلاغ عطل",
            "category": category,
            "fault": fault_selected,
            "odometer": odometer_reading,
            "timestamp": timestamp,
            "status": "تم الإرسال لمدير الحركة"
        }

    def ask_ai_engineer_er(self, driver_query, vehicle_info="Isuzu/Mitsubishi 6-Ton"):
        """
        نافذة المهندس المناوب (AI ER):
        ترسل الاستفسار مباشرة للذكاء الاصطناعي لإرجاع الحل التشخيصي الفوري.
        """
        # مسار جاهز لربط API الخاص بالذكاء الاصطناعي مباشرة
        prompt_payload = {
            "role": "AI Emergency Engineer",
            "vehicle": vehicle_info,
            "query": driver_query,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return prompt_payload


# -------------------------------------------------------------
# تجربة التشغيل والتحقق من الآلية
# -------------------------------------------------------------
if __name__ == "__main__":
    engine = EmergencyAndMaintenanceEngine()

    print("=== 1. اختيارات الأعطال الميكانيكية المنسدلة ===")
    mech_faults = engine.get_fault_options("الأعطال الميكانيكية")
    for idx, f in enumerate(mech_faults, 1):
        print(f"{idx}. {f}")

    print("\n=== 2. محاكاة تنفيذ صيانة وإرفاق العداد ===")
    log = engine.submit_maintenance_log("تغيير زيت المحرك مع الفلتر", "142500")
    print(log)

    print("\n=== 3. محاكاة بلاغ عطل آلي ===")
    fault_log = engine.submit_fault_report("الأعطال الكهربائية", "ضعف أو تفريغ البطارية", "142500")
    print(fault_log)