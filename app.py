import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

# 1. إعدادات الصفحة الاحترافية والعريضة (Quiet Luxury)
st.set_page_config(
    page_title="Games Station Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم الواجهة المتقدم (CSS Custom Styling) باللون الأزرق الفاخر والذهبي
st.markdown("""
    <style>
    /* الخلفية العامة للنظام */
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    /* تصميم الهيدر الفاخر لـ Games Station */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 15px;
        border-bottom: 3px solid #d4af37; /* لمسة ذهبية فاخرة */
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .main-header h1 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #d4af37;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }
    .main-header p { color: #94a3b8; font-size: 14px; margin-top: 5px; }

    /* كروت الأجهزة الذكية والشبكية */
    .device-card {
        background: #151f32;
        border: 1px solid #22324d;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .status-available { border-right: 6px solid #10b981; } /* أخضر متاح */
    .status-busy { border-right: 6px solid #ef4444; }      /* أحمر مشغول */
    .status-paused { border-right: 6px solid #f59e0b; }    /* برتقالي مؤقت */
    
    /* أرقام الأجهزة الكبيرة */
    .device-number {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    /* عداد الوقت الرقمي */
    .timer-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 26px;
        font-weight: bold;
        color: #38bdf8;
        background: #0f172a;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #1e293b;
    }
    
    /* الصناديق السفلية للإيرادات */
    .kpi-container {
        background: linear-gradient(135deg, #1e293b 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #d4af37;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الذاكرة وجلسات النظام (Session State)
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.total_revenue = 0.0
    st.session_state.open_accounts = 0
    st.session_state.daily_expenses = 0.0
    st.session_state.expenses_list = []
    
    # بناء الأجهزة (12 جهاز كمثال)
    st.session_state.devices_data = {
        f"جهاز {i}": {
            "status": "متاح",
            "total_hours": 0,
            "total_minutes": 0,
            "remaining_seconds": 0,
            "extra_controllers": "بدون خدمات إضافية",
            "sales_notes": "",
            "last_update": None
        } for i in range(1, 13)
    }

# ==================== رأس البرنامج الفاخر ====================
st.markdown("""
<div class="main-header">
    <h1>GAMES STATION</h1>
    <p>⚡ نظام الإدارة الفاخر والمطور لـ صالة الألعاب المباشرة ⚡</p>
</div>
""", unsafe_allow_html=True)

# ==================== قسم التاريخ المطور (السنة ثابتة 2026) ====================
st.subheader("📆 إدارة توقيت النظام")
col_d1, col_d2, col_d3 = st.columns(3)
with col_d1:
    day_input = st.number_input("اليوم:", min_value=1, max_value=31, value=datetime.now().day)
with col_d2:
    month_input = st.number_input("الشهر:", min_value=1, max_value=12, value=datetime.now().month)
with col_d3:
    st.text_input("السنة:", value="2026", disabled=True)

st.write("---")

# ==================== عرض الأجهزة بشكل شبكي (2 بجانب بعض) ====================
st.subheader("🖥️ شاشة مراقبة وتشغيل الأجهزة المباشرة")

device_items = list(st.session_state.devices_data.items())

for row_idx in range(0, len(device_items), 2):
    cols = st.columns(2) # تقسيم الشاشة إلى عمودين متساويين هندسياً
    
    for col_idx in range(2):
        if row_idx + col_idx < len(device_items):
            dev_name, dev_info = device_items[row_idx + col_idx]
            
            # تحديد نمط الحافة الجانبية بناءً على حالة الجهاز
            if dev_info["status"] == "متاح":
                card_style = "status-available"
            elif dev_info["status"] == "مشغول":
                card_style = "status-busy"
            else:
                card_style = "status-paused"
                
            with cols[col_idx]:
                st.markdown(f"<div class='device-card {card_style}'>", unsafe_allow_html=True)
                
                # صف رأس بطاقة الجهاز
                c_head1, c_head2 = st.columns([2, 1])
                with c_head1:
                    st.markdown(f"<div class='device-number'>{dev_name}</div>", unsafe_allow_html=True)
                with c_head2:
                    if dev_info["status"] == "متاح":
                        st.success("● متاح")
                    elif dev_info["status"] == "مشغول":
                        st.error("● مشغول")
                    else:
                        st.warning("● مؤقت")
                
                # تحديث العداد التنازلي بشكل لحظي تقريبي إذا كان مشغولاً
                if dev_info["status"] == "مشغول" and dev_info["remaining_seconds"] > 0:
                    # محاكاة بسيطة للوقت المنقضي منذ آخر ضغطة زر
                    dev_info["remaining_seconds"] = max(0, dev_info["remaining_seconds"] - 1)
                
                # حساب الساعات والدقائق والثواني المتبقية للعرض
                rem_sec = dev_info["remaining_seconds"]
                h_disp = rem_sec // 3600
                m_disp = (rem_sec % 3600) // 60
                s_disp = rem_sec % 60
                
                # عرض شاشة العداد الرقمية الفخمة
                st.markdown(f"<div class='timer-display'>⏱️ {h_disp:02d}:{m_disp:02d}:{s_disp:02d}</div>", unsafe_allow_html=True)
                
                # إعدادات وقت اللعب والخدمات (تظهر وتعدل في كل الحالات بشكل منظم)
                if dev_info["status"] == "متاح":
                    st.markdown("**⚙️ تحديد مدة الجلسة والخدمات:**")
                    c_t1, c_t2 = st.columns(2)
                    with c_t1:
                        hr_in = st.number_input("الساعات:", min_value=0, max_value=12, value=1, key=f"hr_{dev_name}")
                    with c_t2:
                        min_in = st.number_input("الدقائق:", min_value=0, max_value=59, value=0, key=f"min_{dev_name}")
                
                # خدمات وأيادي إضافية + مبيعات داخل البطاقة
                services = st.selectbox("🎮 إضافة الخدمات:", ["بدون خدمات إضافية", "يد إضافية واحدة (1)", "يدين إضافيتين (2)"], key=f"serv_{dev_name}")
                sales = st.text_input("🥤 مبيعات وطلبات أخرى للجهاز:", value=dev_info["sales_notes"], key=f"sale_{dev_name}")
                
                st.write("")
                # أزرار التحكم الثلاثية الملونة والمستقلة أسفل البطاقة
                btn_c1, btn_c2, btn_c3 = st.columns(3)
                
                with btn_c1:
                    if st.button("🟢 تشغيل", key=f"btn_str_{dev_name}", use_container_width=True):
                        if dev_info["status"] == "متاح":
                            st.session_state.devices_data[dev_name]["status"] = "مشغول"
                            st.session_state.devices_data[dev_name]["remaining_seconds"] = (hr_in * 3600) + (min_in * 60)
                            st.session_state.devices_data[dev_name]["sales_notes"] = sales
                            st.session_state.open_accounts += 1
                            st.rerun()
                        elif dev_info["status"] == "موقف مؤقتاً":
                            st.session_state.devices_data[dev_name]["status"] = "مشغول"
                            st.rerun()
                            
                with btn_c2:
                    if st.button("🟠 مؤقت", key=f"btn_pau_{dev_name}", use_container_width=True):
                        if dev_info["status"] == "مشغول":
                            st.session_state.devices_data[dev_name]["status"] = "موقف مؤقتاً"
                            st.rerun()
                            
                with btn_c3:
                    if st.button("🔴 إنهاء", key=f"btn_end_{dev_name}", use_container_width=True):
                        if dev_info["status"] != "متاح":
                            st.session_state.devices_data[dev_name]["status"] = "متاح"
                            st.session_state.devices_data[dev_name]["remaining_seconds"] = 0
                            st.session_state.devices_data[dev_name]["sales_notes"] = ""
                            st.session_state.open_accounts = max(0, st.session_state.open_accounts - 1)
                            # الحسابات تتم خلف الكواليس وتضاف هنا تلقائياً لخانة الإيرادات اليومية المفترضة
                            st.session_state.total_revenue += 150.0 # مثال لحفظ القيمة في الصندوق السفلي
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# ==================== قسم الصرفيات والمصاريف الفاخر ====================
st.subheader("💸 قسم إدارة الصرفيات والمصاريف العامة")
with st.expander("📥 اضغط هنا لتسجيل عملية صرف أو مستلزمات جديدة للمحل"):
    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        person_role = st.selectbox("اسم الشخص المسؤول:", ["صاحب المحل", "رئيس العمل", "العامل"])
        expense_reason = st.text_input("سبب الصرف / البيان:")
    with exp_col2:
        expense_val = st.number_input("قيمة الصرف الفعلي (ريال):", min_value=0.0, step=10.0)
        expense_date = st.date_input("التاريخ:", value=date(2026, month_input, day_input))
        
    if st.button("💾 ترحيل وحفظ بند الصرف", use_container_width=True):
        if expense_reason and expense_val > 0:
            st.session_state.expenses_list.append({
                "الشخص": person_role,
                "السبب": expense_reason,
                "القيمة": expense_val,
                "التاريخ": expense_date.strftime("%Y-%m-%d")
            })
            st.session_state.daily_expenses += expense_val
            st.success("📊 تم تسجيل البند بنجاح وترحيله لجدول المصاريف.")
            st.rerun()

# عرض جدول المصاريف بشكل مرتب إن وجد
if st.session_state.expenses_list:
    st.markdown("**📋 قائمة بنود المصاريف الحالية:**")
    st.dataframe(pd.DataFrame(st.session_state.expenses_list), use_container_width=True)

st.write("---")

# ==================== أسفل البرنامج: صناديق الإيرادات والتحليلات المخفية الأسعار ====================
st.subheader("📊 لوحة الحسابات الختامية والإيرادات المباشرة")
bot_c1, bot_c2, bot_c3 = st.columns(3)

with bot_c1:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">💵 إجمالي الدخل الحالي للمحل</h4>
        <p style="color: #10b981; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.total_revenue:,.2f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with bot_c2:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">⏳ مجموع الحسابات المفتوحة</h4>
        <p style="color: #38bdf8; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.open_accounts} أجهزة شغالة</p>
    </div>
    """, unsafe_allow_html=True)

with bot_c3:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">📉 مجموع الإيرادات اليومية صافي</h4>
        <p style="color: #f59e0b; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{(st.session_state.total_revenue - st.session_state.daily_expenses):,.2f} ريال</p>
    </div>
    """, unsafe_allow_html=True)
