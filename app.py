import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# 1. إعدادات النظام العريضة والفخمة (Modern Quiet Luxury)
st.set_page_config(
    page_title="Games Station Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تصميم الواجهة الاحترافي بالكامل (CSS) - صفوف متناظرة وفواصل واضحة
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    /* الهيدر الملكي للمحل */
    .main-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 16px;
        border-bottom: 4px solid #d4af37;
        margin-bottom: 30px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.5);
    }
    .main-header h1 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #d4af37;
        font-size: 38px;
        font-weight: bold;
        letter-spacing: 3px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }
    .main-header p { color: #94a3b8; font-size: 15px; margin-top: 8px; font-weight: 500; }

    /* كروت الأجهزة بنظام الإطارات الفاصلة الواضحة */
    .device-card {
        background: #131a26;
        border: 2px solid #1e293b;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .status-available { border-left: 8px solid #10b981; }
    .status-busy { border-left: 8px solid #ef4444; }
    .status-paused { border-left: 8px solid #f59e0b; }
    
    .device-title { font-size: 26px; font-weight: 800; color: #ffffff; margin-bottom: 2px; }
    .device-subtitle { font-size: 13px; color: #38bdf8; font-weight: bold; }
    
    /* عداد التوقيت الرقمي الحي */
    .live-timer {
        font-family: 'Courier New', Courier, monospace;
        font-size: 32px;
        font-weight: bold;
        color: #38bdf8;
        background: #090d16;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        border: 1px solid #22324d;
        letter-spacing: 1px;
    }
    
    /* خانة الحساب المالي اللحظي */
    .live-finance {
        background: #1e293b;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #d4af37;
    }

    /* الصناديق الختامية والتقارير بالأسفل */
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

# 3. محرك الـ JavaScript السحري لتحديث العدادات ثانية بثانية بدون تعليق البرنامج
st.markdown("""
    <script>
    setInterval(function() {
        const timers = document.querySelectorAll('.live-timer-js');
        timers.forEach(timer => {
            let status = timer.getAttribute('data-status');
            if (status === 'مشغول') {
                let seconds = parseInt(timer.getAttribute('data-seconds'));
                if (seconds > 0) {
                    seconds--;
                    timer.setAttribute('data-seconds', seconds);
                    
                    let h = Math.floor(seconds / 3600);
                    let m = Math.floor((seconds % 3600) / 60);
                    let s = seconds % 60;
                    
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

# 4. دالة الحسابات والأسعار التلقائية الصارمة حسب شروطك
def calculate_precise_cost(device_name, minutes_used):
    if minutes_used <= 0:
        return 0.0
    
    # أجهزة PS5 (1، 2، 3) والجهاز رقم 9 (الشاشة الكبيرة) -> شريحة 12 دقيقة بـ 100 ريال
    if device_name in ["جهاز 1", "جهاز 2", "جهاز 3", "جهاز 9"]:
        slices = int((minutes_used + 11) // 12)  # إضافة شريحة فور دخول أول دقيقة منها
        return float(slices * 100)
    
    # أجهزة PS4 الأخرى -> دورة مجمعة لكل ساعة ونصف (90 دقيقة) بـ 400 ريال
    else:
        cycles = minutes_used // 90
        remainder = minutes_used % 90
        
        cost = cycles * 400.0
        if remainder > 0:
            if remainder <= 60:
                cost += 400.0  # الساعة الأولى كاملة بـ 400
            else:
                cost += 400.0  # النصف ساعة الإضافية مجانية تظل 400
        return float(cost)

# 5. تهيئة الذاكرة الداخلية المؤقتة لحفظ البيانات وضمان عدم تصفيرها
if 'sys_revenue' not in st.session_state:
    st.session_state.sys_revenue = 0.0
if 'sys_expenses' not in st.session_state:
    st.session_state.sys_expenses = 0.0
if 'expenses_records' not in st.session_state:
    st.session_state.expenses_records = []
if 'active_sessions' not in st.session_state:
    st.session_state.active_sessions = 0

if 'devices' not in st.session_state:
    st.session_state.devices = {}
    for i in range(1, 13):
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
            "buffet_sales": 0.0,
            "start_timestamp": None
        }

# ==================== 10) رأس البرنامج الفاخر ====================
st.markdown("""
<div class="main-header">
    <h1>GAMES STATION</h1>
    <p>👑 النظام الملكي الموحد لإدارة وتشغيل صالة الألعاب الاحترافية 👑</p>
</div>
""", unsafe_allow_html=True)

# ==================== 9) قسم إدارة التاريخ المطور ====================
st.subheader("📆 توقيت النظام المعتمد")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    user_day = st.number_input("اليوم الحالي:", min_value=1, max_value=31, value=datetime.now().day)
with col_t2:
    user_month = st.number_input("الشهر الحالي:", min_value=1, max_value=12, value=datetime.now().month)
with col_t3:
    st.text_input("السنة المتبثة للبرنامج:", value="2026", disabled=True)

st.write("---")

# ==================== 1) & 2) عرض الأجهزة بنظام صفوف (جهازين بكل صف) مع فواصل واضحة ====================
st.subheader("🖥️ مراقبة الصالة والأجهزة المباشرة")

dev_list = list(st.session_state.devices.items())

for row in range(0, len(dev_list), 2):
    columns_pair = st.columns(2)  # جهازين متجاورين متناسقين هندسياً
    
    for idx in range(2):
        if row + idx < len(dev_list):
            d_name, d_info = dev_list[row + idx]
            
            # تحديد نمط الهوية البصرية للكارت
            if d_info["status"] == "متاح":
                border_cls = "status-available"
            elif d_info["status"] == "مشغول":
                border_cls = "status-busy"
            else:
                border_cls = "status-paused"
                
            with columns_pair[idx]:
                # بداية البطاقة المنفصلة لكل جهاز مع خطوط فاصلة واضحة جداً
                st.markdown(f"<div class='device-card {border_cls}'>", unsafe_allow_html=True)
                
                head_c1, head_c2 = st.columns([2, 1])
                with head_c1:
                    st.markdown(f"<div class='device-title'>{d_name}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='device-subtitle'>🎮 {d_info['type']}</div>", unsafe_allow_html=True)
                with head_c2:
                    if d_info["status"] == "متاح":
                        st.success("🟢 متاح للعب")
                    elif d_info["status"] == "مشغول":
                        st.error("🔴 قيد الاستخدام")
                    else:
                        st.warning("🟡 إيقاف مؤقت")
                
                # تحديث عداد الوقت الحقيقي المستهلك في الخلفية دقيقة بدقيقة عند التحديث
                if d_info["status"] == "مشغول":
                    d_info["seconds_used"] = min(d_info["allocated_seconds"], d_info["seconds_used"] + 60)
                
                # حساب الأوقات وعرضها
                rem_seconds = max(0, d_info["allocated_seconds"] - d_info["seconds_used"])
                h_rem, m_rem, s_rem = rem_seconds // 3600, (rem_seconds % 3600) // 60, rem_seconds % 60
                
                used_minutes = d_info["seconds_used"] // 60
                h_used, m_used = used_minutes // 60, used_minutes % 60
                
                # حساب التكلفة المباشرة للوقت الحالي + مبيعات الخدمات الإضافية الفورية (يد بـ 50 ريال إضافي كمثال)
                controller_fee = (d_info["extra_controllers"] * 50) * (used_minutes / 60)
                current_time_cost = calculate_precise_cost(d_name, used_minutes)
                total_current_bill = current_time_cost + controller_fee + d_info["buffet_sales"]
                
                # 2) عرض العداد التنازلي الاحترافي ذو الحركة اللحظية للثواني
                st.markdown(f"<div class='live-timer live-timer-js' data-status='{d_info['status']}' data-seconds='{rem_seconds}'>⏱️ {h_rem:02d}:{m_rem:02d}:{s_rem:02d}</div>", unsafe_allow_html=True)
                
                # عرض شاشة الحسابات الداخلية التفصيلية (الوقت المستخدم والمبلغ المالي اللحظي)
                st.markdown(f"""
                <div class="live-finance">
                    <span style="color:#94a3b8; font-size:13px; font-weight:bold;">⏳ الوقت المستهلك: {h_used:02d}ساعة و {m_used:02d}دقيقة</span>
                    <br/>
                    <span style="color:#10b981; font-size:19px; font-weight:800;">💰 الحساب الحالي فوري: {total_current_bill:,.0f} ريال</span>
                </div>
                """, unsafe_allow_html=True)
                
                # ==================== 3) نظام تحديد وقت اللعب والمدخلات والخدمات ====================
                if d_info["status"] == "متاح":
                    st.markdown("**⚙️ خيارات حجز الجلسة الجديدة:**")
                    in_c1, in_c2 = st.columns(2)
                    with in_c1:
                        st_hours = st.number_input("عدد الساعات المطلوب:", min_value=0, max_value=24, value=1, key=f"h_in_{d_name}")
                    with in_c2:
                        st_mins = st.number_input("عدد الدقائق المطلوب:", min_value=0, max_value=59, value=0, key=f"m_in_{d_name}")
                else:
                    # ميزة التمديد السريع الفوري دون إعادة العداد أو تصفير الحسابات السابقة
                    ext_mins = st.number_input("➕ تمديد وقت للجلسة الحالية (بالدقائق):", min_value=0, max_value=240, value=0, step=15, key=f"ext_{d_name}")
                    if ext_mins > 0:
                        if st.button("🔄 تأكيد تمديد الوقت وتحديث العداد", key=f"btn_ext_{d_name}", use_container_width=True):
                            st.session_state.devices[d_name]["allocated_seconds"] += (ext_mins * 60)
                            st.success("تم تمديد وقت الزبون بنجاح!")
                            st.rerun()

                # 6) المبيعات والإضافات (الأيادي والمشروبات الفورية) داخل نفس الفاتورة
                sel_c1, sel_c2 = st.columns(2)
                with sel_c1:
                    ctrl_count = st.selectbox("🎮 الأيادي الإضافية للجلسة:", [0, 1, 2], index=d_info["extra_controllers"], key=f"ctrl_{d_name}", format_func=lambda x: "بدون يد إضافية" if x==0 else f"+{x} يد إضافية")
                    d_info["extra_controllers"] = ctrl_count
                with sel_c2:
                    buffet_input = st.number_input("🥤 مبيعات بوفيه ومشروبات (ريال):", min_value=0.0, value=d_info["buffet_sales"], step=50.0, key=f"buf_{d_name}")
                    d_info["buffet_sales"] = buffet_input
                
                st.write("")
                # ==================== 4) أزرار التحكم الحديثة والفخمة بالألوان والأيقونات ====================
                ctrl_btn_c1, ctrl_btn_c2, ctrl_btn_c3 = st.columns(3)
                
                with ctrl_btn_c1:
                    # زر التشغيل الأخضر المميز
                    if st.button("🟢 تشغيل الجلسة", key=f"start_btn_{d_name}", use_container_width=True):
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
                    # زر إيقاف مؤقت البرتقالي الأنيق (يحفظ الوقت المتبقي والحساب بالكامل للعودة له)
                    if st.button("🟠 إيقاف مؤقت", key=f"pause_btn_{d_name}", use_container_width=True):
                        if d_info["status"] == "مشغول":
                            st.session_state.devices[d_name]["status"] = "إيقاف مؤقت"
                            st.rerun()
                            
                with ctrl_btn_c3:
                    # زر الإنهاء الأحمر الصارخ (يرحل المبالغ فوراً للدرج الختامي ويصفر كارت الجهاز)
                    if st.button("🔴 إنهاء وترحيل", key=f"end_btn_{d_name}", use_container_width=True):
                        if d_info["status"] != "متاح":
                            # إضافة فاتورة هذا الجهاز بالكامل متضمنة الوقت والمبيعات والأيادي للدرج المالي
                            st.session_state.sys_revenue += total_current_bill
                            
                            # إعادة تهيئة وتصفير الكارت بالكامل لاستقبال زبون جديد
                            st.session_state.devices[d_name]["status"] = "متاح"
                            st.session_state.devices[d_name]["allocated_seconds"] = 0
                            st.session_state.devices[d_name]["seconds_used"] = 0
                            st.session_state.devices[d_name]["extra_controllers"] = 0
                            st.session_state.devices[d_name]["buffet_sales"] = 0.0
                            st.session_state.active_sessions = max(0, st.session_state.active_sessions - 1)
                            st.success("تم إنهاء الجلسة وترحيل كامل مستحقات الفاتورة للخزنة الحالية.")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True) # نهاية كارت الجهاز الفاخر

st.write("---")

# ==================== 7) نظام المصروفات والبيانات المتقدم للمحل ====================
st.subheader("💸 قسم إدارة المصاريف والمستلزمات العامة")
with st.expander("📥 اضغط هنا لفتح واجهة تسجيل بند صرف أو مبالغ مسحوبة"):
    exp_col1, exp_col2, exp_col3 = st.columns(3)
    with exp_col1:
        actor_name = st.selectbox("اسم الشخص المسؤول عن الصرف:", ["رئيس العمل", "العامل", "صاحب المحل"])
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
    st.markdown("**📋 السجل الدفتري للمصروفات التي تم تسجيلها اليوم:**")
    st.dataframe(pd.DataFrame(st.session_state.expenses_records), use_container_width=True)

st.write("---")

# ==================== 8) الصناديق السفلية والتقارير المالية الختامية الشاملة ====================
st.subheader("📊 لوحة الحسابات الختامية وصافي الأرباح")
rep_col1, rep_col2, rep_col3, rep_col4 = st.columns(4)

with rep_col1:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:15px; font-weight:bold;">💵 إجمالي دخل المحل الحالي (الدرج)</h4>
        <p style="color: #10b981; font-size: 28px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.sys_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col2:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:15px; font-weight:bold;">📈 الإيرادات اليومية الشاملة</h4>
        <p style="color: #38bdf8; font-size: 28px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.sys_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col3:
    st.markdown(f"""
    <div class="report-box">
        <h4 style="color: #94a3b8; margin:0; font-size:15px; font-weight:bold;">⏳ مجموع الجلسات المفتوحة</h4>
        <p style="color: #e2e8f0; font-size: 28px; font-weight: bold; margin: 10px 0 0 0;">{st.session_state.active_sessions} أجهزة نشطة</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col4:
    # صافي الإيرادات التلقائي المخصوم منه المصاريف بدقة بالغة
    net_profit = st.session_state.sys_revenue - st.session_state.sys_expenses
    st.markdown(f"""
    <div class="report-box" style="border: 2px solid #10b981;">
        <h4 style="color: #94a3b8; margin:0; font-size:15px; font-weight:bold;">📉 صافي الربح بعد المصروفات</h4>
        <p style="color: #f59e0b; font-size: 28px; font-weight: bold; margin: 10px 0 0 0;">{net_profit:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)
