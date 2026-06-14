import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime

# إعدادات المظهر العام للبرنامج (فخامة حديثة)
ctk.set_appearance_mode("dark")  # النمط الداكن الأساسي
ctk.set_default_color_theme("blue")  # لون العناصر التفاعلية

class GamesStationUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة الرئيسية
        self.title("Games Station Management System")
        self.geometry("1100x650")
        self.resizable(False, False)  # الحفاظ على أبعاد التصميم ثابتة ومنظمة
        self.configure(fg_color="#0b0f19")  # خلفية كحلي داكنة جدًا وفخمة (Midnight Blue)

        # -------------------------------------------------------------
        # 1. الجزء العلوي: الهوية البصرية (اسم المحل)
        # -------------------------------------------------------------
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=25)

        # اسم المحل بتصميم فخم وبارز
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="GAMES STATION", 
            font=ctk.CTkFont(family="Segoe UI", size=42, weight="bold", slant="italic"),
            text_color="#00d2ff"  # لون نيون عصري ومضيء يناسب الجيمنج
        )
        self.title_label.pack()

        # خط زخرفي أنيق أسفل الاسم لإبراز الفخامة
        self.line_decorator = ctk.CTkFrame(self.header_frame, height=3, width=280, fg_color="#00d2ff")
        self.line_decorator.pack(pady=5)

        # -------------------------------------------------------------
        # 2. الجزء الأوسط: عرض الوقت والتاريخ (Live Clock & Editable Date)
        # -------------------------------------------------------------
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="#131926", corner_radius=15, border_width=1, border_color="#1e293b")
        self.dashboard_frame.pack(pady=20, padx=50, fill="x")

        # --- قسم الساعة الحية (Live Clock) ---
        self.clock_section = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.clock_section.pack(side="left", expand=True, pady=20)

        self.clock_title = ctk.CTkLabel(self.clock_section, text="LIVE TIME", font=("Segoe UI", 12, "bold"), text_color="#64748b")
        self.clock_title.pack()

        self.clock_label = ctk.CTkLabel(self.clock_section, text="", font=("Consolas", 32, "bold"), text_color="#ffffff")
        self.clock_label.pack(pady=5)

        # زر لتعديل الوقت يدويًا عند الحاجة
        self.btn_edit_time = ctk.CTkButton(self.clock_section, text="Adjust Time", size=(100, 25), fg_color="#1e293b", hover_color="#334155", text_color="#cbd5e1", command=self.manual_time_adjust)
        self.btn_edit_time.pack(pady=2)

        # --- قسم التاريخ (Date Section) ---
        self.date_section = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.date_section.pack(side="right", expand=True, pady=20)

        self.date_title = ctk.CTkLabel(self.date_section, text="SYSTEM DATE (DD/MM/YYYY)", font=("Segoe UI", 12, "bold"), text_color="#64748b")
        self.date_title.pack()

        # حقول إدخال وتعديل التاريخ بشكل منفصل وأنيق
        self.date_inputs_frame = ctk.CTkFrame(self.date_section, fg_color="transparent")
        self.date_inputs_frame.pack(pady=5)

        # القوالب الحالية للتاريخ تلقائيًا بناءً على اليوم
        current_date = datetime.now()

        self.entry_day = ctk.CTkEntry(self.date_inputs_frame, width=50, font=("Consolas", 18, "bold"), justify="center", fg_color="#0b0f19", border_color="#334155")
        self.entry_day.pack(side="left", padx=2)
        self.entry_day.insert(0, current_date.strftime("%d"))

        self.slash1 = ctk.CTkLabel(self.date_inputs_frame, text="/", font=("Consolas", 18), text_color="#64748b")
        self.slash1.pack(side="left", padx=2)

        self.entry_month = ctk.CTkEntry(self.date_inputs_frame, width=50, font=("Consolas", 18, "bold"), justify="center", fg_color="#0b0f19", border_color="#334155")
        self.entry_month.pack(side="left", padx=2)
        self.entry_month.insert(0, current_date.strftime("%m"))

        self.slash2 = ctk.CTkLabel(self.date_inputs_frame, text="/", font=("Consolas", 18), text_color="#64748b")
        self.slash2.pack(side="left", padx=2)

        self.entry_year = ctk.CTkEntry(self.date_inputs_frame, width=75, font=("Consolas", 18, "bold"), justify="center", fg_color="#0b0f19", border_color="#334155")
        self.entry_year.pack(side="left", padx=2)
        self.entry_year.insert(0, current_date.strftime("%Y"))

        # -------------------------------------------------------------
        # 3. الجزء السفلي: مساحة الصور الجمالية (Visual Elements)
        # -------------------------------------------------------------
        self.visual_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.visual_frame.pack(pady=30, padx=50, fill="both", expand=True)

        # ملاحظة توضيحية لـ مكان وضع البوستر الجمالي للألعاب
        # تم استخدام لوحة (Frame) ذات لون متدرج خفيف ومظهر زجاجي عصري لتمثيل مكان الصور لعدم التشويش على الأداء
        self.image_placeholder_1 = ctk.CTkFrame(self.visual_frame, fg_color="#131926", border_width=1, border_color="#00d2ff", corner_radius=12)
        self.image_placeholder_1.pack(side="left", expand=True, fill="both", padx=15)
        
        self.img_lbl_1 = ctk.CTkLabel(self.image_placeholder_1, text="[ CINEMATIC GAME POSTER 1 ]\n(GTA VI / FIFA Showcase)", font=("Segoe UI", 14, "italic"), text_color="#475569")
        self.img_lbl_1.place(relx=0.5, rely=0.5, anchor="center")

        self.image_placeholder_2 = ctk.CTkFrame(self.visual_frame, fg_color="#131926", border_width=1, border_color="#00d2ff", corner_radius=12)
        self.image_placeholder_2.pack(side="right", expand=True, fill="both", padx=15)

        self.img_lbl_2 = ctk.CTkLabel(self.image_placeholder_2, text="[ CINEMATIC GAME POSTER 2 ]\n(PS5 Exclusive Visual)", font=("Segoe UI", 14, "italic"), text_color="#475569")
        self.img_lbl_2.place(relx=0.5, rely=0.5, anchor="center")

        # تشغيل تحديث الساعة التلقائي
        self.is_manual_time = False
        self.manual_time_str = ""
        self.update_clock()

    # دالة لتحديث الساعة بشكل حي ومستمر ثانية بثانية
    def update_clock(self):
        if not self.is_manual_time:
            # النمط الافتراضي: جلب وقت الجهاز الفعلي وتنسيقه حسب طلبك (Seconds : Minutes : Hours AM/PM)
            now = datetime.now()
            current_time = now.strftime("%S : %M : %I %p")
            self.clock_label.configure(text=current_time)
        else:
            # في حال تم التعديل يدويًا (يتم تثبيت الوقت المختار أو معالجته)
            self.clock_label.configure(text=self.manual_time_str)
            
        # إعادة استدعاء الدالة كل 1000 ملي ثانية (ثانية واحدة) لتظل الساعة حية
        self.after(1000, self.update_clock)

    # دالة بسيطة كمثال لكيفية إتاحة تعديل الوقت يدويًا بنظام منبثق
    def manual_time_adjust(self):
        dialog = ctk.CTkInputDialog(text="Enter Time (HH:MM:SS AM/PM):", title="Manual Time Override")
        input_val = dialog.get_input()
        if input_val:
            self.is_manual_time = True
            self.manual_time_str = input_val
        else:
            self.is_manual_time = False

# تشغيل البرنامج
if __name__ == "__main__":
    app = GamesStationUI()
    app.mainloop()
