import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

# 1. إعدادات النظام الفاخرة والعريضة للشاشات والجوالات
st.set_page_config(
    page_title="Games Station Ultimate Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم الهوية البصرية الحصرية (Modern Quiet Luxury) بألوان داكنة ملكية ولمسات ذهبية وزرقاء
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    /* الهيدر الفاخر الرئيسي للمحل */
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        border-bottom: 4px solid #d4af37;
        margin-bottom: 25px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.5);
    }
    .main-header h1 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #d4af37;
        font-size: 36px;
        font-weight: bold;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }
    .main-header p { color: #94a3b8; font-size: 14px; margin-top: 5px; font-weight: 500; }

    /* تنسيق كروت الأجهزة بنظام الصفوف الثنائية المتناظرة والفواصل القوية */
    .device-card {
        background: #131a26;
        border: 2px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .status-available { border-left: 8px solid #10b981; }
    .status-busy { border-left: 8px solid #ef4444; }
    .status-paused { border-left: 8px solid #f59e0b; }
    
    .device-title { font-size: 24px; font-weight: 800; color: #ffffff; }
    .device-subtitle { font-size: 13px; color: #38bdf8; font-weight: bold; }
    
    /* العداد الرقمي المباشر وحركة الثواني الحية */
    .live-timer {
        font-family: 'Courier New', Courier, monospace;
        font-size: 30px;
        font-weight: bold;
        color: #38bdf8;
        background: #090d16;
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        margin: 12px 0;
        border: 1px solid #22324d;
    }
    
    /* الصناديق المالية والتقارير الشاملة أسفل البرنامج */
    .report-box {
        background: linear-gradient(135deg, #162235 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #d4af37;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 3. جافا سكريبت لتحريك عدادات الـ 15 جهاز في نفس الوقت بثوانٍ حقيقية حية دون عمل Refresh
st.markdown("""
    <script>
    setInterval(function() {
        const timers = document.querySelectorAll('.live-timer-js');
        timers.forEach(timer => {
            let status = timer.getAttribute('data-status');
            if (status === 'مشغول') {
                let sec = parseInt(timer.getAttribute('data-seconds'));
                if (sec > 0) {
                    sec--;
                    timer.setAttribute('data-seconds', sec);
                    let h = Math.floor(sec / 3600);
                    let m = Math.floor((sec % 3600) / 60);
                    let s = sec % 60;
                    timer.innerHTML = "⏱️ " + 
                        (h < 10 ? "0" + h : h) + ":" + 
                        (m < 10 ? "0" + m : m) + ":" + 
                        (s < 10 ? "0" + s : s);
                }
            }
        });
    }, 1000);
    </script>
""", unsafe_allow_html=True)

# 4. محرك الاحتساب المالي الصارم (الدورات والشرائح الزمنية)
def calculate_precise_cost(device_name, minutes_used):
    if minutes_used <= 0:
        return 0.0
    
    # أجهزة PS5 (1، 2، 3) والجهاز رقم 9 (الشاشة الكبيرة) -> شريحة 12 دقيقة بـ 100 ريال
    if device_name in ["جهاز 1", "جهاز 2", "جهاز 3", "جهاز 9"]:
        slices = int((minutes_used + 11) // 12)
        return float(slices * 100)
    
    # أجهزة PS4 الأخرى -> دورة مجمعة لكل ساعة ونصف (90 دقيقة) بـ 400 ريال
    else:
        cycles = minutes_used // 90
        remainder = minutes_used % 90
        cost = cycles * 400.0
        if remainder > 0:
            cost += 400.0  # أول 60 دقيقة والـ 30 دقيقة التي تليها تقع ضمن دورة الـ 400 ريال الثابتة
        return float(cost)

# 5. تثبيت وتهيئة جلسة العمل والـ 15 جهازاً لمنع فقدان البيانات عند نقرات التشغيل
if 'sys_init' not in st.session_state:
    st.session_state.sys_init = True
    st.session_state.shift_start_time = datetime.now().strftime("%I:%M:%S %p")
    st.session_state.sys_revenue = 0.0
    st.session_state.sys_expenses = 0.0
    st.session_state.expenses_records = []
    st.session_state.active_sessions = 0
    
    # بناء مصفوفة الـ 15 جهازاً حسب المواصفات المطلوبة بدقة
    st.session_state.devices = {}
    for i in range(1, 16):
        name = f"جهاز {i}"
        if i in [1, 2, 3]:
            dtype = "PlayStation 5"
        elif i == 9:
            dtype = "PlayStation 4 [الشاشة الكبيرة]"
        else:
            dtype = "PlayStation 4"
            
        st.session_state.devices[name] = {
            "status": "متاح",
            "type": dtype,
            "allocated_seconds": 0,
            "seconds_used": 0,
            "extra_controllers": 0,
            "buffet_sales": 0.0
        }

# ==================== الواجهة الرئيسية: رأس البرنامج الملكي ====================
st.markdown("""
<div class="main-header">
    <h1>GAMES STATION</h1>
    <p>⚡ النظام الموحد المتكامل لإدارة الأجهزة، الوقت، المبيعات والمصروفات ⚡</p>
</div>
""", unsafe_allow_html=True)

# ==================== قسم التوقيت، تاريخ اليوم، وساعة الدوام المطور ====================
st.subheader("⏰ توقيت صالة العرض وبداية الدوام")
col_time1, col_time2, col_time3 = st.columns(3)
with col_time1:
    user_day = st.number_input("اليوم الحالي:", min_value=1, max_value=31, value=datetime.now().day)
with col_time2:
    user_month = st.number_input("الشهر الحالي:", min_value=1, max_value=12, value=datetime.now().month)
    # السنة ثابتة ومقفلة 2026 حسب شروطك
    st.session_state.current_year = "2026"
with col_time3:
    st.markdown(f"""
    <div style="background:#1e293b; padding:10px; border-radius:8px; border:1px solid #38bdf8; text-align:center;">
        <span style="color:#94a3b8; font-size:12px; font-weight:bold;">🕒 بداية الدوام الحالي</span><br/>
        <span style="color:#38bdf8; font-size:16px; font-weight:bold;">{st.session_state.shift_start_time}</span>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ==================== ترتيب الأجهزة داخل البرنامج (نظام صفوف ثنائية متناظرة) ====================
st.subheader("🖥️ شاشة التحكم المباشر بالأجهزة (15 جهاز)")

dev_list = list(st.session_state.devices.items())

for row in range(0, len(dev_list), 2):
    columns_pair = st.columns(2)  # وضع جهازين متجاورين في كل صف أفقي لسهولة مراقبة الصالة والسرعة
    
    for idx in range(2):
        if row + idx < len(dev_list):
            d_name, d_info = dev_list[row + idx]
            
            # تحديد لون الفاصل الجانبي حسب الحالة
            if d_info["status"] == "متاح":
                border_cls = "status-available"
            elif d_info["status"] == "مشغول":
                border_cls = "status-busy"
            else:
                border_cls = "status-paused"
                
            with columns_pair[idx]:
                # كارت الجهاز المستقل
                st.markdown(f"<div class='device-card {border_cls}'>", unsafe_allow_html=True)
                
                head_c1, head_c2 = st.columns([2, 1])
                with head_c1:
                    st.markdown(f"<div class='device-title'>{d_name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='device-subtitle'>🎮 {d_info['type']}</div>", unsafe_allow_html=True)
                with head_c2:
                    if d_info["status"] == "متاح":
                        st.success("● متاح")
                    elif d_info["status"] == "مشغول":
                        st.error("● مشغول")
                    else:
                        st.warning("● مؤقت")
                
                # ترحيل وحساب الدقائق والثواني المستهلكة في الخلفية بشكل صامت
                if d_info["status"] == "مشغول":
                    d_info["seconds_used"] = min(d_info["allocated_seconds"], d_info["seconds_used"] + 60)
                
                rem_seconds = max(0, d_info["allocated_seconds"] - d_info["seconds_used"])
                h_rem, m_rem, s_rem = rem_seconds // 3600, (rem_seconds % 3600) // 60, rem_seconds % 60
                
                used_minutes = d_info["seconds_used"] // 60
                h_used, m_used = used_minutes // 60, used_minutes % 60
                
                # احتساب الفاتورة الجارية بناءً على قواعد الدورة الخاصة بـ PS4 والشرائح الخاصة بـ PS5
                current_time_cost = calculate_precise_cost(d_name, used_minutes)
                total_current_bill = current_time_cost + d_info["buffet_sales"]
                
                # عداد الوقت الاحترافي التنازلي ذو الحركة الحية ثانية بثانية
                st.markdown(f"<div class='live-timer live-timer-js' data-status='{d_info['status']}' data-seconds='{rem_seconds}'>⏱️ {h_rem:02d}:{m_rem:02d}:{s_rem:02d}</div>", unsafe_allow_html=True)
                
                # شاشة الحسابات الداخلية التفصيلية المستورة داخل الكارت لإدارة المحل
                st.markdown(f"""
                <div style="background:#1e293b; padding:10px; border-radius:10px; text-align:center; border:1px solid #d4af37; margin-bottom:12px;">
                    <span style="color:#94a3b8; font-size:12px;">المستغرق: {h_used:02d}ساعة و {m_used:02d}دقيقة</span> | 
                    <span style="color:#10b981; font-size:16px; font-weight:bold;">المبلغ الحالي: {total_current_bill:,.0f} ريال</span>
                </div>
                """, unsafe_allow_html=True)
                
                # تحديد وقت اللعب يدوياً للزبون (تظهر عند الإتاحة فقط لمنع تشوش الأزرار)
                if d_info["status"] == "متاح":
                    st.markdown("**⏱️ تحديد مدة اللعب للزبون:**")
                    in_c1, in_c2 = st.columns(2)
                    with in_c1:
                        st_hours = st.number_input("الساعات:", min_value=0, max_value=24, value=1, key=f"h_in_{d_name}")
                    with in_c2:
                        st_mins = st.number_input("الدقائق:", min_value=0, max_value=59, value=0, key=f"m_in_{d_name}")
                else:
                    # خانة التمديد السريع الفوري دون تصفير الجلسة الجارية
                    ext_mins = st.number_input("➕ إضافة وقت للجلسة الجارية (دقائق):", min_value=0, max_value=240, value=0, step=15, key=f"ext_{d_name}")
                    if ext_mins > 0:
                        if st.button("🔄 تأكيد التمديد الفوري", key=f"btn_ext_{d_name}", use_container_width=True):
                            st.session_state.devices[d_name]["allocated_seconds"] += (ext_mins * 60)
                            st.success("تم تمديد وقت الزبون والحفظ المتواصل جارٍ!")
                            st.rerun()

                # خانة الأيدي الإضافية وخانة المبيعات والبوفيه وإدخال الأسعار يدوياً حسب الرغبة
                st.markdown("**🍿 المبيعات والأيادي الإضافية:**")
                sel_c1, sel_c2 = st.columns(2)
                with sel_c1:
                    ctrl_count = st.selectbox("🎮 الأيدي الإضافية:", [0, 1, 2], index=d_info["extra_controllers"], key=f"ctrl_{d_name}", format_func=lambda x: "بدون يد إضافية" if x==0 else f"يد واحدة (+1)" if x==1 else "يدين إضافيتين (+2)")
                    d_info["extra_controllers"] = ctrl_count
                with sel_c2:
                    # ميزة إدخال سعر مبيعات البوفيه يدوياً وإضافتها للفاتورة مباشرة
                    buffet_price = st.number_input("🥤 مبيعات ومشروبات (ريال):", min_value=0.0, value=d_info["buffet_sales"], step=50.0, key=f"buf_{d_name}")
                    d_info["buffet_sales"] = buffet_price
                
                st.write("")
                # أزرار التحكم الثلاثية الفخمة والمستقلة لكل كارت
                ctrl_btn_c1, ctrl_btn_c2, ctrl_btn_c3 = st.columns(3)
                
                with ctrl_btn_c1:
                    if st.button("🟢 تشغيل", key=f"start_btn_{d_name}", use_container_width=True):
                        if d_info["status"] == "متاح":
                            total_target_secs = (st_hours * 3600) + (st_mins * 60)
                            if total_target_secs > 0:
                                st.session_state.devices[d_name]["status"] = "مشغول"
                                st.session_state.devices[d_name]["allocated_seconds"] = total_target_secs
                                st.session_state.devices[d_name]["seconds_used"] = 0
                                st.session_state.active_sessions += 1
                                st.rerun()
                        elif d_info["status"] == "إيقاف مؤقت":
                            st.session_state.devices[d_name]["status"] = "مشغول"
                            st.rerun()
                            
                with ctrl_btn_c2:
                    if st.button("🟠 إيقاف مؤقت", key=f"pause_btn_{d_name}", use_container_width=True):
                        if d_info["status"] == "مشغول":
                            st.session_state.devices[d_name]["status"] = "إيقاف مؤقت"
                            st.rerun()
                            
                with ctrl_btn_c3:
                    if st.button("🔴 إنهاء", key=f"end_btn_{d_name}", use_container_width=True):
                        if d_info["status"] != "متاح":
                            # ترحيل وإضافة مستحقات هذه الفاتورة بالكامل للدرج والخزنة السفلية للمحل
                            st.session_state.sys_revenue += total_current_bill
                            
                            # إعادة تهيئة وتصفير كارت الجهاز للزبون التالي
                            st.session_state.devices[d_name]["status"] = "متاح"
                            st.session_state.devices[d_name]["allocated_seconds"] = 0
                            st.session_state.devices[d_name]["seconds_used"] = 0
                            st.session_state.devices[d_name]["extra_controllers"] = 0
                            st.session_state.devices[d_name]["buffet_sales"] = 0.0
                            st.session_state.active_sessions = max(0, st.session_state.active_sessions - 1)
                            st.success("تم إنهاء الجلسة بنجاح وترحيل المستحقات للخزنة اليومية!")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True) # نهاية كارت الجهاز الفاخر

st.write("---")

# ==================== قسم المصروفات والبيانات المتقدم للمحل ====================
st.subheader("💸 قسم إدارة الصرفيات والمصاريف العامة")
with st.expander("📥 اضغط هنا لفتح واجهة تسجيل بند صرف أو مبالغ مسحوبة"):
    exp_col1, exp_col2, exp_col3 = st.columns(3)
    with exp_col1:
        actor_name = st.selectbox("اسم الشخص المسؤول عن الصرف:", ["العامل", "صاحب المحل", "مصروفات للمحل"])
    with exp_col2:
        exp_reason = st.text_input("سبب الصرف / تفاصيل المستلزمات المعنية:")
    with exp_col3:
        exp_value = st.number_input("المبلغ الإجمالي المخصوم (ريال):", min_value=0.0, step=100.0)
        
    if st.button("💾 ترحيل البند وتحديث السجل المالي للمحل", use_container_width=True):
        if exp_reason and exp_value > 0:
            st.session_state.expenses_records.append({
                "المسؤول": actor_name,
                "السبب / البيان": exp_reason,
                "قيمة الصرف": exp_value,
                "التاريخ": f"2026-{user_month:02d}-{user_day:02d}"
            })
            st.session_state.sys_expenses += exp_value
            st.success("📊 تم الحفظ بنجاح وتحديث الصناديق المالية الختامية بالأسفل.")
            st.rerun()

if st.session_state.expenses_records:
    st.markdown("**📋 السجل الدفتري للمصروفات الحالية للدوام:**")
    st.dataframe(pd.DataFrame(st.session_state.expenses_records), use_container_width=True)

st.write("---")

# ==================== التقارير المالية والإجماليات لـ Games Station ====================
st.subheader("📊 لوحة الحسابات الختامية وصافي الأرباح")
rep_col1, rep_col2, rep_col3, rep_col4 = st.columns(4)

with rep_col1:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px; font-weight:bold;">💵 إجمالي دخل المحل الحالي</h4>
        <p style="color: #10b981; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.sys_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col2:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px; font-weight:bold;">📈 الإيرادات اليومية</h4>
        <p style="color: #38bdf8; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.sys_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col3:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px; font-weight:bold;">⏳ مجموع الجلسات المفتوحة</h4>
        <p style="color: #e2e8f0; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.active_sessions} أجهزة نشطة</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col4:
    # صافي الإيرادات بعد خصم المصروفات بدقة بالغة
    net_profit = st.session_state.sys_revenue - st.session_state.sys_expenses
    st.markdown(f"""
    <div class="report-box" style="border: 2px solid #10b981;">
        <h4 style="color: #94a3b8; margin:0; font-size:14px; font-weight:bold;">📉 صافي الربح بعد المصروفات</h4>
        <p style="color: #f59e0b; font-size: 26px; font-weight: bold; margin: 10px 0 0 0;">{net_profit:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)
