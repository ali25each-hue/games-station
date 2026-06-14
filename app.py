import streamlit as st
import pandas as pd
from datetime import datetime, date
import math

# 1. إعدادات الصفحة الاحترافية والعريضة (Modern Quiet Luxury)
st.set_page_config(
    page_title="Games Station Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم الواجهة المتقدم (CSS Custom Styling)
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    /* الهيدر الفاخر */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 15px;
        border-bottom: 3px solid #d4af37;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .main-header h1 {
        font-family: 'Segoe UI', sans-serif;
        color: #d4af37;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 0;
    }
    .main-header p { color: #94a3b8; font-size: 14px; margin-top: 5px; }

    /* كروت الأجهزة الشبكية */
    .device-card {
        background: #151f32;
        border: 1px solid #22324d;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .status-available { border-right: 6px solid #10b981; }
    .status-busy { border-right: 6px solid #ef4444; }
    .status-paused { border-right: 6px solid #f59e0b; }
    
    .device-number { font-size: 24px; font-weight: bold; color: #ffffff; }
    .device-type { font-size: 13px; color: #38bdf8; font-weight: 600; }
    
    /* عداد الوقت الرقمي */
    .timer-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 24px;
        font-weight: bold;
        color: #38bdf8;
        background: #0f172a;
        padding: 6px;
        border-radius: 8px;
        text-align: center;
        margin: 8px 0;
        border: 1px solid #1e293b;
    }
    
    /* شاشة عرض البيانات المالية المباشرة داخل الكارت */
    .finance-display {
        background: #1e293b;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 12px;
        border: 1px solid #d4af37;
    }
    
    /* الصناديق السفلية */
    .kpi-container {
        background: linear-gradient(135deg, #1e293b 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #d4af37;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# دالة ذكية لحساب المبلغ بناءً على نوع شريحة الجهاز والوقت الكلي المستخدم (بالدقائق)
def calculate_device_cost(device_name, total_minutes_used):
    if total_minutes_used <= 0:
        return 0.0
        
    # تحديد نوع الجهاز (PS5 أو الشاشة الكبيرة رقم 9)
    if device_name in ["جهاز 1", "جهاز 2", "جهاز 3", "جهاز 9"]:
        # نظام الـ 12 دقيقة = 100 ريال
        slices = math.ceil(total_minutes_used / 12)
        return float(slices * 100)
    else:
        # نظام الـ PS4 الذكي (كل ساعة ونصف أو 90 دقيقة كدورة سعرية كاملة بـ 400 ريال)
        cycles = total_minutes_used // 90  # عدد الدورات الكاملة (90 دقيقة)
        rem_minutes = total_minutes_used % 90  # الدقائق المتبقية داخل الدورة الحالية
        
        cost = cycles * 400.0
        if rem_minutes > 0:
            if rem_minutes <= 60:
                # داخل الساعة الأولى من الدورة: كل 15 دقيقة بـ 100 ريال
                slices = math.ceil(rem_minutes / 15)
                cost += (slices * 100)
            else:
                # بين الدقيقة 61 و 90 يثبت السعر عند 400 ريال للدورة الحالية
                cost += 400.0
        return float(cost)

# 3. إدارة جلسات النظام وثبات البيانات
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.total_revenue = 0.0
    st.session_state.open_accounts = 0
    st.session_state.daily_expenses = 0.0
    st.session_state.expenses_list = []
    
    # تهيئة الـ 12 جهاز بالبيانات الرياضية المباشرة واختيار الأسماء المناسبة لنوعها تلقائياً
    st.session_state.devices_data = {}
    for i in range(1, 13):
        name = f"جهاز {i}"
        if i in [1, 2, 3]:
            dtype = "PlayStation 5"
        elif i == 9:
            dtype = "PlayStation 4 (الشاشة الكبيرة)"
        else:
            dtype = "PlayStation 4"
            
        st.session_state.devices_data[name] = {
            "status": "متاح",
            "type": dtype,
            "total_minutes_allocated": 0,
            "minutes_used": 0,
            "extra_controllers": "بدون خدمات إضافية",
            "sales_notes": "",
            "current_cost": 0.0
        }

# ==================== رأس البرنامج الفاخر ====================
st.markdown("""
<div class="main-header">
    <h1>GAMES STATION</h1>
    <p>⚡ نظام الإدارة والتحكم الذكي وحساب الإيرادات التلقائي المباشر ⚡</p>
</div>
""", unsafe_allow_html=True)

# ==================== قسم التاريخ المطور ====================
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
    cols = st.columns(2) # تقسيم متناظر ومثالي للواجهة
    
    for col_idx in range(2):
        if row_idx + col_idx < len(device_items):
            dev_name, dev_info = device_items[row_idx + col_idx]
            
            if dev_info["status"] == "متاح":
                card_style = "status-available"
            elif dev_info["status"] == "مشغول":
                card_style = "status-busy"
            else:
                card_style = "status-paused"
                
            with cols[col_idx]:
                st.markdown(f"<div class='device-card {card_style}'>", unsafe_allow_html=True)
                
                c_head1, c_head2 = st.columns([2, 1])
                with c_head1:
                    st.markdown(f"<div class='device-number'>{dev_name} <span class='device-type'>({dev_info['type']})</span></div>", unsafe_allow_html=True)
                with c_head2:
                    if dev_info["status"] == "متاح":
                        st.success("● متاح")
                    elif dev_info["status"] == "مشغول":
                        st.error("● مشغول")
                    else:
                        st.warning("● مؤقت")
                
                # حساب الأوقات التنازلية والتصاعدية المباشرة بناءً على حالة التشغيل
                if dev_info["status"] == "مشغول":
                    # محاكاة لزيادة الوقت المستخدم دقيقة بدقيقة عند كل تحديث تلقائي للبرنامج للسهولة وسرعة الأداء
                    dev_info["minutes_used"] = min(dev_info["total_minutes_allocated"], dev_info["minutes_used"] + 1)
                    # إعادة احتساب المبلغ الحالي تلقائياً بناءً على الوقت المستخدم الفعلي والقواعد المحددة
                    dev_info["current_cost"] = calculate_device_cost(dev_name, dev_info["minutes_used"])

                remaining_mins = max(0, dev_info["total_minutes_allocated"] - dev_info["minutes_used"])
                
                # تحويل الدقائق إلى تنسيق عرض فخم (ساعات:دقائق:ثواني)
                rem_h, rem_m = remaining_mins // 60, remaining_mins % 60
                used_h, used_m = dev_info["minutes_used"] // 60, dev_info["minutes_used"] % 60
                
                # عرض شاشة العداد الرقمية
                st.markdown(f"<div class='timer-display'>⏱️ الوقت المتبقي: {rem_h:02d}:{rem_m:02d}:00</div>", unsafe_allow_html=True)
                
                # شاشة عرض الحسابات المخفية عن الخارج والمدمجة داخل البطاقة للمدير
                st.markdown(f"""
                <div class="finance-display">
                    <span style="color:#94a3b8; font-size:13px;">الوقت المستخدم: {used_h:02d}ساعة و {used_m:02d}دقيقة</span>
                    <br/>
                    <span style="color:#10b981; font-size:18px; font-weight:bold;">المبلغ الحالي: {dev_info['current_cost']:,.0f} ريال</span>
                </div>
                """, unsafe_allow_html=True)
                
                # أدوات التخصيص عند التمديد أو التشغيل الجديد
                if dev_info["status"] == "متاح":
                    st.markdown("**⚙️ تحديد وقت اللعب للزبون:**")
                    c_t1, c_t2 = st.columns(2)
                    with c_t1:
                        hr_in = st.number_input("الساعات:", min_value=0, max_value=12, value=1, key=f"hr_{dev_name}")
                    with c_t2:
                        min_in = st.number_input("الدقائق:", min_value=0, max_value=59, value=0, key=f"min_{dev_name}")
                else:
                    # خانة التمديد السريع أثناء عمل الجهاز دون تصفير العداد
                    extend_mins = st.number_input("➕ تمديد وقت إضافي (بالدقائق):", min_value=0, max_value=300, value=0, step=15, key=f"ext_{dev_name}")
                    if extend_mins > 0:
                        if st.button("🔄 تأكيد تمديد الوقت", key=f"btn_ext_confirm_{dev_name}"):
                            st.session_state.devices_data[dev_name]["total_minutes_allocated"] += extend_mins
                            st.success("تم تمديد الوقت بنجاح وبدء الحساب المتواصل المباشر!")
                            st.rerun()

                services = st.selectbox("🎮 خدمات الأيادي الإضافية:", ["بدون خدمات إضافية", "يد إضافية واحدة", "يدين إضافيتين"], key=f"serv_{dev_name}")
                sales = st.text_input("🥤 مبيعات وطلبات الثلاجة:", value=dev_info["sales_notes"], key=f"sale_{dev_name}")
                
                st.write("")
                # أزرار التحكم المباشرة الاحترافية
                btn_c1, btn_c2, btn_c3 = st.columns(3)
                
                with btn_c1:
                    if st.button("🟢 تشغيل", key=f"btn_str_{dev_name}", use_container_width=True):
                        if dev_info["status"] == "متاح":
                            allocated = (hr_in * 60) + min_in
                            if allocated > 0:
                                st.session_state.devices_data[dev_name]["status"] = "مشغول"
                                st.session_state.devices_data[dev_name]["total_minutes_allocated"] = allocated
                                st.session_state.devices_data[dev_name]["minutes_used"] = 0
                                st.session_state.devices_data[dev_name]["sales_notes"] = sales
                                st.session_state.devices_data[dev_name]["current_cost"] = calculate_device_cost(dev_name, 0)
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
                            # ترحيل الحساب المحسوب تلقائياً إلى الخزنة والصناديق السفلية فوراً
                            st.session_state.total_revenue += dev_info["current_cost"]
                            
                            # إعادة تصفير الجهاز لاستقبال زبون جديد
                            st.session_state.devices_data[dev_name]["status"] = "متاح"
                            st.session_state.devices_data[dev_name]["total_minutes_allocated"] = 0
                            st.session_state.devices_data[dev_name]["minutes_used"] = 0
                            st.session_state.devices_data[dev_name]["sales_notes"] = ""
                            st.session_state.devices_data[dev_name]["current_cost"] = 0.0
                            st.session_state.open_accounts = max(0, st.session_state.open_accounts - 1)
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

if st.session_state.expenses_list:
    st.markdown("**📋 قائمة بنود المصاريف الحالية:**")
    st.dataframe(pd.DataFrame(st.session_state.expenses_list), use_container_width=True)

st.write("---")

# ==================== أسفل البرنامج: صناديق الإيرادات والتحليلات ====================
st.subheader("📊 لوحة الحسابات الختامية والإيرادات المباشرة")
bot_c1, bot_c2, bot_c3 = st.columns(3)

with bot_c1:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">💵 إجمالي الدخل الحالي للمحل (الدرج)</h4>
        <p style="color: #10b981; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.total_revenue:,.2f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with bot_c2:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">⏳ مجموع الحسابات المفتوحة</h4>
        <p style="color: #38bdf8; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.open_accounts} أجهزة قيد اللعب</p>
    </div>
    """, unsafe_allow_html=True)

with bot_c3:
    st.markdown(f"""
    <div class="kpi-container">
        <h4 style="color: #94a3b8; margin:0; font-size:16px;">📉 مجموع الإيرادات اليومية صافي</h4>
        <p style="color: #f59e0b; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{(st.session_state.total_revenue - st.session_state.daily_expenses):,.2f} ريال</p>
    </div>
    """, unsafe_allow_html=True)
