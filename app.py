import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعدادات الشاشة العريضة لتناسب عرض جهازين متجاورين بشكل أفقي مريح للجوال
st.set_page_config(page_title="جيم ستيشن برو", page_icon="🎮", layout="wide", initial_sidebar_state="collapsed")

# تصميم الألوان والبطاقات والأزرار المباشرة داخل كل جهاز
st.markdown("""
    <style>
    .reportview-container { background-color: #0e1117; }
    .kpi-box {
        background: linear-gradient(135deg, #1e1e2f, #252538);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #4f46e5;
        margin-bottom: 20px;
    }
    .device-container {
        background-color: #161b22;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    .status-vacant { border-top: 6px solid #2ecc71; }
    .status-busy { border-top: 6px solid #e74c3c; }
    .status-free { border-top: 6px solid #f1c40f; }
    </style>
""", unsafe_allow_html=True)

# إدارة الذاكرة وحفظ الدخل الإجمالي حتى لا يضيع عند التحديث
if 'total_revenue' not in st.session_state:
    st.session_state.total_revenue = 0.0

if 'devices' not in st.session_state:
    st.session_state.devices = {
        f"جهاز {i}": {
            "status": "فارغ", 
            "type": "PlayStation 5" if i <= 5 else "PlayStation 4",
            "base_price": 500 if i <= 5 else 400,
            "extra_controllers": 0,
            "start_time": None,
            "is_free_promo": False,
            "water_count": 0
        } for i in range(1, 13)
    }

# ==================== صندوق الدخل الإجمالي (رأس البرنامج) ====================
st.markdown(f"""
<div class="kpi-box">
    <h3 style="color: #ffffff; margin: 0; font-size: 18px;">💵 صندوق الدخل الإجمالي الحالي</h3>
    <p style="color: #2ecc71; font-size: 28px; font-weight: bold; margin: 5px 0 0 0;">{st.session_state.total_revenue:,.2f} ريال</p>
</div>
""", unsafe_allow_html=True)

st.title("🎮 جيم ستيشن - إدارة الصالة المباشرة")
st.write("---")

# تقسيم الأجهزة ليعرض كل جهازين بجانب بعضهما بشكل أفقي
device_list = list(st.session_state.devices.items())

for row_idx in range(0, len(device_list), 2):
    cols = st.columns(2)
    
    for col_idx in range(2):
        if row_idx + col_idx < len(device_list):
            device_name, info = device_list[row_idx + col_idx]
            
            with cols[col_idx]:
                # تحديد لون البطاقة حسب الحالة الحالية للجهاز
                if info["status"] == "مشغول":
                    status_class = "status-busy"
                elif info["status"] == "1.5 ساعة مجاناً":
                    status_class = "status-free"
                else:
                    status_class = "status-vacant"
                
                # إنشاء كارت الجهاز
                st.markdown(f"<div class='device-container {status_class}'>", unsafe_allow_html=True)
                st.subheader(f"🖥️ {device_name}")
                st.write(f"**النوع:** {info['type']} | **السعر:** {info['base_price']} ريال/ساعة")
                
                # حساب تكلفة الأيادي الإضافية (كل يد بـ 50 ريال إضافي على الساعة)
                extra_rate = info["extra_controllers"] * 50
                total_hourly_rate = info["base_price"] + extra_rate
                
                # ---------------- حالة الجهاز: فارغ ----------------
                if info["status"] == "فارغ":
                    info["extra_controllers"] = st.selectbox("🎮 الأيادي الإضافية:", [0, 1, 2], key=f"ctrl_{device_name}", format_func=lambda x: "بدون أيادي إضافية" if x==0 else f"{x} يد زيادة (+{x*50} ريال)")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🟢 تشغيل عادي", key=f"start_reg_{device_name}", use_container_width=True):
                            st.session_state.devices[device_name]["status"] = "مشغول"
                            st.session_state.devices[device_name]["start_time"] = datetime.now()
                            st.session_state.devices[device_name]["is_free_promo"] = False
                            st.session_state.devices[device_name]["water_count"] = 0
                            st.rerun()
                    with c2:
                        if st.button("🎁 1.5 ساعة مجاناً", key=f"start_free_{device_name}", use_container_width=True):
                            st.session_state.devices[device_name]["status"] = "1.5 ساعة مجاناً"
                            st.session_state.devices[device_name]["start_time"] = datetime.now()
                            st.session_state.devices[device_name]["is_free_promo"] = True
                            st.session_state.devices[device_name]["water_count"] = 0
                            st.rerun()
                            
                # ---------------- حالة الجهاز: مشغول أو عليه عرض مجاني ----------------
                else:
                    elapsed = datetime.now() - info["start_time"]
                    mins_played = int(elapsed.total_seconds() / 60)
                    hours_played = mins_played // 60
                    display_mins = mins_played % 60
                    
                    st.info(f"⏱️ **الوقت الحالي:** {hours_played} ساعة و {display_mins} دقيقة")
                    
                    # قاعـدة الحساب الذكي التي طلبتها:
                    if info["is_free_promo"]:
                        if mins_played <= 90:
                            # إذا لعب في الوقت المجاني ولم يكمله وأراد الخروج، يحسب السعر الفوري كأنه تشغيل عادي
                            play_cost = (mins_played / 60) * total_hourly_rate
                            st.warning(f"🎁 في العرض المجاني (الحساب الفعلي الحالي: {play_cost:.2f} ريال)")
                        else:
                            # إذا تجاوز الـ ساعة ونصف، الـ 90 دقيقة الأولى مجانية تماماً ويحسب فقط ما زاد عنها
                            extra_mins = mins_played - 90
                            play_cost = (extra_mins / 60) * total_hourly_rate
                    else:
                        # الحساب العادي التصاعدي فورياً
                        play_cost = (mins_played / 60) * total_hourly_rate
                    
                    # بوفيه الثلاجة الخاص بالجهاز داخل نفس الخانة
                    st.markdown("**🥤 المبيعات المباشرة للثلاجة:**")
                    cw1, cw2, cw3 = st.columns([1, 2, 1])
                    with cw1:
                        if st.button("➕ ماء", key=f"add_w_{device_name}"):
                            st.session_state.devices[device_name]["water_count"] += 1
                            st.rerun()
                    with cw2:
                        st.write(f"الماء: {info['water_count']} حبة")
                    with cw3:
                        if st.button("➖ ماء", key=f"sub_w_{device_name}") and info["water_count"] > 0:
                            st.session_state.devices[device_name]["water_count"] -= 1
                            st.rerun()
                    
                    # إجمالي الحساب الحالي (الوقت + الماء الحبة بـ 100 ريال)
                    water_cost = info["water_count"] * 100
                    total_current_bill = play_cost + water_cost
                    
                    st.success(f"💰 **الحساب اللحظي الفوري:** {total_current_bill:,.2f} ريال")
                    
                    # أزرار الإيقاف والترحيل أو الإلغاء
                    cx1, cx2 = st.columns(2)
                    with cx1:
                        if st.button("🔴 إنهاء وترحيل للدرج", key=f"stop_{device_name}", use_container_width=True):
                            st.session_state.total_revenue += total_current_bill
                            st.session_state.devices[device_name]["status"] = "فارغ"
                            st.session_state.devices[device_name]["start_time"] = None
                            st.session_state.devices[device_name]["water_count"] = 0
                            st.rerun()
                    with cx2:
                        if st.button("⚪ إلغاء اللعبة", key=f"cancel_{device_name}", use_container_width=True):
                            st.session_state.devices[device_name]["status"] = "فارغ"
                            st.session_state.devices[device_name]["start_time"] = None
                            st.session_state.devices[device_name]["water_count"] = 0
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
