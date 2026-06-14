import streamlit as st
import pandas as pd
from datetime import datetime, date

# 1. إعدادات النظام وتثبيت الرؤية العريضة
st.set_page_config(
    page_title="Games Station Ultimate",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. هندسة التصميم الصارم (إجبار العرض الأفقي الثنائي 2 في كل صف + الفواصل)
st.markdown("""
    <style>
    /* الخلفية العامة الفاخرة */
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    /* الهيدر المبسط والفخم في المنتصف */
    .brand-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #131a26 0%, #0f172a 100%);
        border-radius: 12px;
        border: 1px solid #d4af37;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .brand-header h1 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #d4af37;
        font-size: 38px;
        font-weight: bold;
        margin: 0;
        letter-spacing: 2px;
    }
    
    /* سطر التوقيت والتاريخ الموحد */
    .datetime-row {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 25px;
        background: #151f32;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #22324d;
    }

    /* إجبار المتصفح على نظام الشبكة الأفجقية الثنائية (جهازين في كل صف) حتى على الجوال */
    .devices-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 20px !important;
        width: 100%;
    }
    
    /* بطاقة الجهاز المستقلة ذات الإطار والفواصل الواضحة */
    .device-card {
        background: #111827;
        border: 2px solid #1e293b;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        position: relative;
    }
    .status-available { border-right: 6px solid #10b981; }
    .status-busy { border-right: 6px solid #ef4444; }
    .status-paused { border-right: 6px solid #f59e0b; }
    
    .device-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .device-title { font-size: 22px; font-weight: bold; color: #ffffff; }
    .device-badge { font-size: 12px; font-weight: bold; padding: 4px 8px; border-radius: 6px; }

    /* عداد الوقت الرقمي الاحترافي */
    .live-timer {
        font-family: 'Courier New', Courier, monospace;
        font-size: 28px;
        font-weight: bold;
        color: #38bdf8;
        background: #070a12;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        margin: 10px 0;
        border: 1px solid #1e293b;
    }
    
    /* الصناديق المالية الختامية */
    .kpi-box {
        background: #151f32;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d4af37;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك الـ JavaScript الخارق للعدادات الحية والساعة المباشرة ثانية بثانية
st.markdown("""
    <script>
    // تحديث الساعة والعدادات كل ثانية
    setInterval(function() {
        // 1. تحديث الساعة الحقيقية للنظام
        const sysClock = document.getElementById('sys-live-clock');
        if (sysClock) {
            let now = new Date();
            let hours = now.getHours();
            let minutes = now.now ? now.getMinutes() : now.getMinutes();
            let seconds = now.getSeconds();
            let ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; 
            minutes = minutes < 10 ? '0'+minutes : minutes;
            seconds = seconds < 10 ? '0'+seconds : seconds;
            sysClock.innerHTML = "⏰ الساعة الآن: " + hours + ":" + minutes + ":" + seconds + " " + ampm;
        }

        // 2. تحديث عدادات الأجهزة التنازلية
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

# 4. محرك احتساب الأسعار الصارم بناءً على الفترات المحددة للدوام
def calculate_device_bill(device_name, minutes_used):
    if minutes_used <= 0:
        return 0.0
    if device_name in ["جهاز 1", "جهاز 2", "جهاز 3", "جهاز 9"]:
        # نظام الـ 12 دقيقة = 100 ريال لأجهزة PS5 والجهاز 9
        slices = int((minutes_used + 11) // 12)
        return float(slices * 100)
    else:
        # نظام الـ PS4: دورة 400 ريال لكل ساعة ونصف (90 دقيقة)
        cycles = minutes_used // 90
        remainder = minutes_used % 90
        cost = cycles * 400.0
        if remainder > 0:
            cost += 400.0
        return float(cost)

# 5. بناء وحفظ حالة الـ 15 جهازاً لمنع إعادة التحميل أو تصفير الوقت
if 'system_revenue' not in st.session_state:
    st.session_state.system_revenue = 0.0
    st.session_state.system_expenses = 0.0
    st.session_state.expense_log = []
    st.session_state.open_sessions = 0
    
    st.session_state.device_store = {}
    for i in range(1, 16):
        name = f"جهاز {i}"
        dtype = "PS5" if i in [1, 2, 3] else "PS4 [شاشة كبيرة]" if i == 9 else "PS4"
        st.session_state.device_store[name] = {
            "status": "متاح",
            "type": dtype,
            "allocated_seconds": 0,
            "seconds_used": 0,
            "item_name": "",
            "item_price": 0.0,
            "controllers": "بدون يد إضافية"
        }

# ==================== 5) واجهة وسطح البرنامج (مبسط وفخم وفي المنتصف) ====================
st.markdown("""
<div class="brand-header">
    <h1>Games Station</h1>
</div>
""", unsafe_allow_html=True)

# ==================== 6) & 7) سطر التاريخ الموحد والساعة الحقيقية المستمرة ====================
col_d1, col_d2, col_d3 = st.columns([1, 1, 2])
with col_d1:
    day_val = st.number_input("اليوم:", min_value=1, max_value=31, value=datetime.now().day)
with col_d2:
    month_val = st.number_input("الشهر:", min_value=1, max_value=12, value=datetime.now().month)
with col_d3:
    # عرض سطر التاريخ والساعة الحية جنباً إلى جنب
    st.markdown(f"""
    <div class="datetime-row">
        <span>📅 التاريخ: {day_val:02d} / {month_val:02d} / 2026</span>
        <span style="margin-left: 20px; color: #d4af37;" id="sys-live-clock">⏰ الساعة الآن: جاري التحميل...</span>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ==================== 1) ترتيب الأجهزة الأفقي الصارم (جهازين في كل صف) ====================
st.subheader("🖥️ لوحة تحكم وتشغيل الأجهزة")

# فتح وعاء خارجي يجبر التنسيق الأفقي لـ CSS
st.markdown('<div class="devices-grid">', unsafe_allow_html=True)

dev_items = list(st.session_state.device_store.items())

# مصفوفة لرسم خطوط الأجهزة بشكل شبكي ثنائي صارم
for i in range(0, len(dev_items), 2):
    row_cols = st.columns(2)  # توليد عمودين دائماً بجانب بعضهما البعض
    
    for c_idx in range(2):
        if i + c_idx < len(dev_items):
            d_name, d_info = dev_items[i + c_idx]
            
            # تحديد لون الفاصل والبطاقة حسب حالة الجهاز الحالية
            if d_info["status"] == "متاح":
                card_style = "status-available"
            elif d_info["status"] == "مشغول":
                card_style = "status-busy"
            else:
                card_style = "status-paused"
                
            with row_cols[c_idx]:
                # رسم كارت الجهاز المستقل مع خطوط الفاصل الواضحة والتصميم المرتب
                st.markdown(f"<div class='device-card {card_style}'>", unsafe_allow_html=True)
                
                # رأس الكارت: الرقم + النوع + الحالة
                st.markdown(f"""
                <div class="device-header">
                    <div class="device-title">{d_name} <span style="font-size:14px; color:#38bdf8;">({d_info['type']})</span></div>
                    <div class="device-badge" style="background: {'#10b981' if d_info['status']=='متاح' else '#ef4444' if d_info['status']=='مشغول' else '#f59e0b'};">
                        {d_info['status']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # تحديث الوقت المستخدم دقيقة بدقيقة عند كل تفاعل مع الصفحة
                if d_info["status"] == "مشغول":
                    d_info["seconds_used"] = min(d_info["allocated_seconds"], d_info["seconds_used"] + 60)
                
                # حساب الميقات والعرض التنازلي التلقائي
                rem_sec = max(0, d_info["allocated_seconds"] - d_info["seconds_used"])
                h_rem, m_rem, s_rem = rem_sec // 3600, (rem_sec % 3600) // 60, rem_sec % 60
                
                used_mins = d_info["seconds_used"] // 60
                h_used, m_used = used_mins // 60, used_mins % 60
                
                # الحساب المالي الجاري للجلسة خلف الكواليس
                current_game_cost = calculate_device_bill(d_name, used_minutes)
                total_current_bill = current_game_cost + d_info["item_price"]
                
                # 4) العداد الحقيقي الذي يتحرك ثانية بثانية عبر الجافا سكريبت المدمج
                st.markdown(f"<div class='live-timer live-timer-js' data-status='{d_info['status']}' data-seconds='{rem_sec}'>⏱️ {h_rem:02d}:{m_rem:02d}:{s_rem:02d}</div>", unsafe_allow_html=True)
                
                # إظهار الموقف المالي والزمني الحالي داخل بطاقة المستودع
                st.markdown(f"""
                <div style="background:#131a26; padding:8px; border-radius:6px; text-align:center; border:1px solid #1e293b; margin-bottom:10px; font-size:14px;">
                    ⏳ مستهلك: {h_used:02d}:{m_used:02d} | 💰 مستحق حالي: <span style="color:#10b981; font-weight:bold;">{total_current_bill:,.0f} ريال</span>
                </div>
                """, unsafe_allow_html=True)
                
                # ==================== 3) خانة تحديد الوقت اليدوية الفراغية ====================
                if d_info["status"] == "متاح":
                    st.markdown("<p style='font-size:12px; margin:0; color:#94a3b8;'>⏱️ أدخل وقت الجلسة يدويًا للزبون:</p>", unsafe_allow_html=True)
                    in_c1, in_c2 = st.columns(2)
                    with in_c1:
                        # الخانات تبدأ بقيم افتراضية نظيفة ومجهزة للإدخال الفوري
                        hr_input = st.number_input("الساعات:", min_value=0, max_value=12, value=0, step=1, key=f"hr_in_{d_name}")
                    with in_c2:
                        min_input = st.number_input("الدقائق:", min_value=0, max_value=59, value=0, step=5, key=f"min_in_{d_name}")
                else:
                    # ميزة تمديد وقت إضافي سريع في حالة الشغل دون تصفير العداد
                    ext_mins = st.number_input("➕ تمديد وقت (بالدقائق):", min_value=0, max_value=180, value=0, step=15, key=f"ext_{d_name}")
                    if ext_mins > 0:
                        if st.button("🔄 تأكيد التمديد", key=f"btn_ext_{d_name}", use_container_width=True):
                            st.session_state.device_store[d_name]["allocated_seconds"] += (ext_mins * 60)
                            st.success("تم التمديد!")
                            st.rerun()

                # خانات الخدمات، الأيادي الإضافية، والمبيعات اليدوية داخل بطاقة كل جهاز
                st.markdown("<p style='font-size:12px; margin:5px 0 0 0; color:#94a3b8;'>🛒 المبيعات والخدمات الإضافية:</p>", unsafe_allow_html=True)
                serv_c1, serv_c2 = st.columns(2)
                with serv_c1:
                    ctrl_select = st.selectbox("🎮 الأيادي:", ["بدون يد إضافية", "يد واحدة", "يدين إضافيتين"], key=f"ctrl_{d_name}")
                    d_info["controllers"] = ctrl_select
                with serv_c2:
                    it_name = st.text_input("الصنف:", value=d_info["item_name"], placeholder="مثال: بيبسي", key=f"itn_{d_name}")
                    it_price = st.number_input("السعر (ريال):", min_value=0.0, value=d_info["item_price"], step=50.0, key=f"itp_{d_name}")
                    d_info["item_name"] = it_name
                    d_info["item_price"] = it_price
                
                st.write("")
                # ==================== 2) أزرار التحكم الفنية والأنيقة بالألوان والأيقونات ====================
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    if st.button("🟢 تشغيل", key=f"btn_s_{d_name}", use_container_width=True):
                        if d_info["status"] == "متاح":
                            total_secs = (hr_input * 3600) + (min_input * 60)
                            if total_secs > 0:
                                st.session_state.device_store[d_name]["status"] = "مشغول"
                                st.session_state.device_store[d_name]["allocated_seconds"] = total_secs
                                st.session_state.device_store[d_name]["seconds_used"] = 0
                                st.session_state.open_sessions += 1
                                st.rerun()
                        elif d_info["status"] == "إيقاف مؤقت":
                            st.session_state.device_store[d_name]["status"] = "مشغول"
                            st.rerun()
                with b_col2:
                    if st.button("🟠 مؤقت", key=f"btn_p_{d_name}", use_container_width=True):
                        if d_info["status"] == "مشغول":
                            st.session_state.device_store[d_name]["status"] = "إيقاف مؤقت"
                            st.rerun()
                with b_col3:
                    if st.button("🔴 إنهاء", key=f"btn_e_{d_name}", use_container_width=True):
                        if d_info["status"] != "متاح":
                            # ترحيل وإغلاق الفاتورة فوراً للدرج المالي العام بالأسفل
                            st.session_state.system_revenue += total_current_bill
                            
                            # تصفير وإتاحة الكارت لاستقبال زبون جديد
                            st.session_state.device_store[d_name]["status"] = "متاح"
                            st.session_state.device_store[d_name]["allocated_seconds"] = 0
                            st.session_state.device_store[d_name]["seconds_used"] = 0
                            st.session_state.device_store[d_name]["item_name"] = ""
                            st.session_state.device_store[d_name]["item_price"] = 0.0
                            st.session_state.open_sessions = max(0, st.session_state.open_sessions - 1)
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True) # غلق كارت الجهاز

st.markdown('</div>', unsafe_allow_html=True) # غلق الشبكة الهندسية الكاملة

st.write("---")

# ==================== قسم إدارة المصروفات العامة للمحل ====================
st.subheader("💸 سجل المصروفات والنثريات اليومية")
with st.expander("📥 اضغط هنا لتسجيل بند مصروفات جديد"):
    ex_c1, ex_c2, ex_c3 = st.columns(3)
    with ex_c1:
        staff_person = st.selectbox("اسم الشخص المسؤول:", ["العامل", "صاحب المحل", "رئيس العمل", "مصروفات للمحل"])
    with ex_c2:
        reason_text = st.text_input("سبب الصرف / البيان:")
    with ex_c3:
        value_amount = st.number_input("قيمة المبلغ المصروف (ريال):", min_value=0.0, step=50.0)
        
    if st.button("💾 حفظ وترحيل بند الصرف المالي", use_container_width=True):
        if reason_text and value_amount > 0:
            st.session_state.expense_log.append({
                "المسؤول": staff_person,
                "البيان / السبب": reason_text,
                "المبلغ المخصوم": value_amount,
                "التاريخ": f"2026-{month_val:02d}-{day_val:02d}"
            })
            st.session_state.system_expenses += value_amount
            st.success("تم تسجيل بند الصرف وتحديث الحساب الختامي!")
            st.rerun()

if st.session_state.expense_log:
    st.dataframe(pd.DataFrame(st.session_state.expense_log), use_container_width=True)

st.write("---")

# ==================== التقارير المالية والإجماليات الشاملة للمحل ====================
st.subheader("📊 لوحة الحسابات الختامية وصافي الأرباح")
rep_col1, rep_col2, rep_col3, rep_col4 = st.columns(4)

with rep_col1:
    st.markdown(f"""
    <div class="kpi-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px;">💵 إجمالي دخل المحل (الدرج)</h4>
        <p style="color: #10b981; font-size: 26px; font-weight: bold; margin: 8px 0 0 0;">{st.session_state.system_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col2:
    st.markdown(f"""
    <div class="kpi-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px;">📈 الإيرادات اليومية</h4>
        <p style="color: #38bdf8; font-size: 26px; font-weight: bold; margin: 8px 0 0 0;">{st.session_state.system_revenue:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col3:
    st.markdown(f"""
    <div class="kpi-box">
        <h4 style="color: #94a3b8; margin:0; font-size:14px;">⏳ الجلسات المفتوحة</h4>
        <p style="color: #f1f5f9; font-size: 26px; font-weight: bold; margin: 8px 0 0 0;">{st.session_state.open_sessions} أجهزة نشطة</p>
    </div>
    """, unsafe_allow_html=True)

with rep_col4:
    net_cash = st.session_state.system_revenue - st.session_state.system_expenses
    st.markdown(f"""
    <div class="kpi-box" style="border: 2px solid #10b981;">
        <h4 style="color: #94a3b8; margin:0; font-size:14px;">📉 صافي الربح بعد المصروفات</h4>
        <p style="color: #f59e0b; font-size: 26px; font-weight: bold; margin: 8px 0 0 0;">{net_cash:,.0f} ريال</p>
    </div>
    """, unsafe_allow_html=True)
