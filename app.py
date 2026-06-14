import datetime
import time
import pandas as pd
import streamlit as st

# إعدادات واجهة البرنامج الاحترافية والحديثة
st.set_page_config(
    page_title="Games Station Pro", page_icon="🎮", layout="wide"
)

st.title("🎮 نظام Games Station الاحترافي لإدارة الصالات")
st.markdown("---")

# 1. تهيئة البيانات في الـ Session State لمنع التصفير عند التحديث
if "devices" not in st.session_state:
    devices = {}
    for i in range(1, 16):
        if i in [1, 2, 3]:
            dtype, rate, offer = "PlayStation 5", 500, False
        elif i == 9:
            dtype, rate, offer = "PlayStation 4 (شاشة كبيرة)", 500, False
        else:
            dtype, rate, offer = "PlayStation 4", 400, True

        devices[i] = {
            "type": dtype,
            "rate": rate,
            "has_offer": offer,
            "status": "متاح",  # متاح، مشغول، مؤقت
            "mode": "مفتوح",  # محدد، مفتوح
            "target_minutes": 0.0,
            "elapsed_cached_seconds": 0.0,  # الوقت المستهلك الفعلي المخزن قبل الإيقاف
            "last_start_time": None,  # توقيت آخر ضغطة تشغيل
            "extra_charge": 0.0,  # المشروبات والأيدي الآجلة
            "logged_services": [],
        }
    st.session_state.devices = devices

if "sales_history" not in st.session_state:
    st.session_state.history = []
if "pos_sales" not in st.session_state:
    st.session_state.pos_sales = []
if "expenses" not in st.session_state:
    st.session_state.expenses = []


# 2. دالة حساب الوقت المستغرق الفعلي (دقيقة وثانية) بدقة من وضع التشغيل الحالي والإيقاف المؤقت
def get_device_time(dev):
    total_seconds = dev["elapsed_cached_seconds"]
    if dev["status"] == "مشغول" and dev["last_start_time"] is not None:
        total_seconds += (
            datetime.datetime.now() - dev["last_start_time"]
        ).total_seconds()
    return total_seconds / 60.0


# 3. دالة حساب الأموال بناءً على الوقت ونظام العروض بدقة
def calculate_price(dev, minutes):
    hours_played = int(minutes // 60)
    billable_minutes = minutes

    # تطبيق العرض: خصم نصف ساعة (30 دقيقة) لكل ساعة كاملة مكتملة للـ PS4 العادي
    if dev["has_offer"] and hours_played >= 1:
        free_minutes = hours_played * 30
        if minutes >= free_minutes:
            billable_minutes = minutes - free_minutes
        else:
            billable_minutes = 0

    play_cost = billable_minutes * (dev["rate"] / 60.0)
    return round(play_cost, 2)


# --- التبويبات الرئيسية للبرنامج ---
tab_main, tab_pos, tab_expenses, tab_reports = st.tabs(
    [
        "🖥️ الشاشة الرئيسية للأجهزة",
        "🥤 مبيعات الثلاجة المباشرة",
        "💸 المصاريف وحساب الموظفين",
        "📊 الحسابات والإيرادات اليومية",
    ]
)

# ==================== التبويب الأول: إدارة الأجهزة ====================
with tab_main:
    # عرض الأجهزة على شكل شبكة كروت عصرية
    st.subheader("📊 مراقبة الأجهزة الحالية")
    grid_cols = st.columns(5)

    for i in sorted(st.session_state.devices.keys()):
        dev = st.session_state.devices[i]
        col = grid_cols[(i - 1) % 5]

        with col:
            current_mins = get_device_time(dev)
            play_fee = calculate_price(dev, current_mins)
            total_fee = play_fee + dev["extra_charge"]

            if dev["status"] == "مشغول":
                # إذا كان الوقت محدد ونفذ
                if (
                    dev["mode"] == "محدد"
                    and current_mins >= dev["target_minutes"]
                ):
                    overtime = current_mins - dev["target_minutes"]
                    if overtime <= 5.0:
                        st.warning(
                            f"⚠️ جهاز {i} - فترة سماح ({round(overtime,1)} ق)"
                        )
                    else:
                        st.error(f"🚨 جهاز {i} - انتهى الوقت الفعلي!")
                else:
                    st.error(f"🔴 جهاز {i} - شغال")

                st.caption(f"**النوع:** {dev['type']}")
                if dev["mode"] == "محدد":
                    st.caption(
                        f"**الوقت:** {round(current_mins, 1)} / {dev['target_minutes']} دقيقة"
                    )
                else:
                    st.caption(f"**الوقت (مفتوح):** {round(current_mins, 1)} دقيقة")
                st.caption(f"**الحساب الحالي:** {total_fee} ريال")

            elif dev["status"] == "مؤقت":
                st.warning(f"⏸️ جهاز {i} - إيقاف مؤقت")
                st.caption(f"**النوع:** {dev['type']}")
                st.caption(f"**الوقت المحفوظ:** {round(current_mins, 1)} دقيقة")
                st.caption(f"**الحساب المحفوظ:** {total_fee} ريال")
            else:
                st.success(f"🟢 جهاز {i} - فارغ")
                st.caption(f"**النوع:** {dev['type']}")
                st.caption(f"**السعر:** {dev['rate']} ريال/ساعة")

    st.markdown("---")

    # لوحة التحكم وإجراء العمليات والتمديد والإيقاف
    st.subheader("⚙️ لوحة تحكم ومطالبات الجهاز")
    selected_id = st.selectbox(
        "اختر الجهاز للتحكم به:", sorted(list(st.session_state.devices.keys()))
    )
    current_dev = st.session_state.devices[selected_id]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### ⚡ إدارة تشغيل وإيقاف الجلسة")

        if current_dev["status"] == "متاح":
            play_mode = st.radio(
                "نظام اللعب:", ["وقت مفتوح", "وقت محدد مسبقاً"], key=f"mode_{selected_id}"
            )
            target_mins = 0.0
            if play_mode == "وقت محدد مسبقاً":
                duration_choice = st.selectbox(
                    "اختر المدة المطلوبة:",
                    ["نصف ساعة", "ساعة", "ساعة ونصف", "ساعتين", "3 ساعات"],
                )
                duration_map = {
                    "نصف ساعة": 30.0,
                    "ساعة": 60.0,
                    "ساعة ونصف": 90.0,
                    "ساعتين": 120.0,
                    "3 ساعات": 180.0,
                }
                target_mins = duration_map[duration_choice]

            if st.button("🚀 تشغيل الجهاز الآن", use_container_width=True):
                current_dev["status"] = "مشغول"
                current_dev["mode"] = (
                    "مفتوح" if play_mode == "وقت مفتوح" else "محدد"
                )
                current_dev["target_minutes"] = target_mins
                current_dev["last_start_time"] = datetime.datetime.now()
                current_dev["elapsed_cached_seconds"] = 0.0
                current_dev["extra_charge"] = 0.0
                current_dev["logged_services"] = []
                st.rerun()

        elif current_dev["status"] in ["مشغول", "مؤقت"]:
            current_mins = get_device_time(current_dev)
            play_fee = calculate_price(current_dev, current_mins)
            total_fee = play_fee + current_dev["extra_charge"]

            st.metric(label="الحساب الإجمالي المستحق", value=f"{total_fee} ريال")

            # حل مشكلة الإيقاف المؤقت (تخزين الوقت المنقضي قبل الإيقاف)
            if current_dev["status"] == "مشغول":
                if st.button("⏸️ إيقاف مؤقت للوقت", use_container_width=True):
                    current_dev["elapsed_cached_seconds"] += (
                        datetime.datetime.now() - current_dev["last_start_time"]
                    ).total_seconds()
                    current_dev["status"] = "مؤقت"
                    current_dev["last_start_time"] = None
                    st.rerun()
            else:
                if st.button(
                    "▶️ استئناف اللعب (إكمال الوقت السابق)",
                    use_container_width=True,
                ):
                    current_dev["status"] = "مشغول"
                    current_dev["last_start_time"] = datetime.datetime.now()
                    st.rerun()

            # ميزة التمديد المستمر وإضافة وقت جديد دون تصفير العداد
            if current_dev["mode"] == "محدد":
                st.markdown("**🔄 تمديد الوقت للجلسة:**")
                extend_choice = st.selectbox(
                    "إضافة مدة جديدة وتمديد الوقت:",
                    ["لا شيء", "نصف ساعة", "ساعة", "ساعتين"],
                    key=f"ext_{selected_id}",
                )
                if extend_choice != "لا شيء" and st.button("➕ تأكيد التمديد"):
                    extend_map = {
                        "نصف ساعة": 30.0,
                        "ساعة": 60.0,
                        "ساعتين": 120.0,
                    }
                    current_dev["target_minutes"] += extend_map[extend_choice]
                    st.success(
                        f"تم تمديد وقت الجهاز بنجاح بمقدار {extend_choice}"
                    )
                    st.rerun()

            if st.button("🛑 إنهاء الجلسة وتصفير الحساب", use_container_width=True):
                st.session_state.history.append(
                    {
                        "التاريخ": datetime.datetime.now().strftime(
                            "%Y-%m-%d %I:%M %p"
                        ),
                        "رقم الجهاز": selected_id,
                        "النوع": current_dev["type"],
                        "المدة الإجمالية (دقائق)": round(current_mins, 1),
                        "صافي حساب اللعب": play_fee,
                        "الخدمات الآجلة": current_dev["extra_charge"],
                        "المبلغ المستلم الكلي": total_fee,
                    }
                )
                current_dev["status"] = "متاح"
                current_dev["last_start_time"] = None
                current_dev["elapsed_cached_seconds"] = 0.0
                current_dev["extra_charge"] = 0.0
                current_dev["logged_services"] = []
                st.success("تم إنهاء الجلسة بنجاح وحفظها بالسجل اليومي!")
                st.rerun()

    with c2:
        st.markdown("### 🛒 مبيعات آجلة على الفاتورة")
        if current_dev["status"] in ["مشغول", "مؤقت"]:
            product = st.selectbox(
                "المنتج المطلوب:", ["ماء", "بيبسي", "ريدبول", "سناك"]
            )
            qty = st.number_input("الكمية:", min_value=1, value=1, step=1)
            price_map = {"ماء": 100, "بيبسي": 250, "ريدبول": 600, "سناك": 200}
            unit_p = price_map[product]

            if st.button("🛒 ربط وتثبيت بالفاتورة"):
                total_prod_price = unit_p * qty
                current_dev["extra_charge"] += total_prod_price
                current_dev["logged_services"].append(
                    f"{product} × {qty} ({total_prod_price} ريال)"
                )
                st.success(f"تم ربط {product} بحساب جهاز {selected_id}")
                st.rerun()

            if current_dev["logged_services"]:
                st.markdown("**الخدمات المرتبطة بالفاتورة حالياً:**")
                for item in current_dev["logged_services"]:
                    st.caption(f"• {item}")
        else:
            st.info("الجهاز فارغ، المبيعات الآجلة تتم فقط للأجهزة الشغالة.")

    with c3:
        st.markdown("### 🎮 إضافة أيدي تحكم إضافية")
        if current_dev["status"] in ["مشغول", "مؤقت"]:
            if st.button("➕ إضافة يدتين تحكم (+200 ريال)"):
                current_dev["extra_charge"] += 200
                current_dev["logged_services"].append("يدتين إضافيتين (200 ريال)")
                st.success("تمت إضافة مبلغ اليدتين بنجاح للفاتورة.")
                st.rerun()
        else:
            st.info("يجب تشغيل الجهاز أولاً لإضافة الأيدي.")

# ==================== التبويب الثاني: المبيعات الفورية للثلاجة ====================
with tab_pos:
    st.subheader("🥤 البيع الفوري (كاش ومحاسبة فورية دون ربط بجهاز)")
    pos_prod = st.selectbox("اختر منتج الثلاجة:", ["ماء", "بيبسي", "ريدبول"])
    pos_qty = st.number_input(
        "الكمية المطلوبة للبيع الفوري:", min_value=1, value=1, step=1
    )
    pos_price_map = {"ماء": 100, "بيبسي": 250, "ريدبول": 600}
    pos_total = pos_price_map[pos_prod] * pos_qty

    st.markdown(f"**الحساب الفوري المستحق:** {pos_total} ريال")
    if st.button("💰 تأكيد البيع الفوري واستلام الكاش"):
        st.session_state.pos_sales.append(
            {
                "التاريخ": datetime.datetime.now().strftime(
                    "%Y-%m-%d %I:%M %p"
                ),
                "المنتج": pos_prod,
                "الكمية": pos_qty,
                "العائد الفوري (ريال)": pos_total,
            }
        )
        st.success("تم تسجيل البيع الفوري كاش بنجاح!")
        st.rerun()

# ==================== التبويب الثالث: حساب الموظفين والمصاريف ====================
with tab_expenses:
    st.subheader("💸 إدارة مصاريف الصالة وحساب المقرر اليومي للموظفين")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.markdown("### 🧑‍💼 حساب الموظف والمقرر اليومي")
        emp_name = st.text_input("اسم الموظف / العامل:", "أحمد")
        daily_allowance = st.number_input(
            "المقرر اليومي للموظف (ريال):", value=2000, step=500
        )

        st.markdown("**خصومات سحب منتجات من الثلاجة للموظف:**")
        emp_item = st.selectbox(
            "المنتج الذي سحبه الموظف:", ["ماء", "بيبسي", "أخرى"]
        )
        emp_item_cost = st.number_input(
            "سعر خصم المنتج (ريال):", value=100, step=50
        )

        if st.button("📉 تسجيل الخصم من الموظف"):
            st.session_state.expenses.append(
                {
                    "التاريخ": datetime.datetime.now().strftime(
                        "%Y-%m-%d %I:%M %p"
                    ),
                    "البند": f"سحب منتج ({emp_item}) من قِبل الموظف {emp_name}",
                    "المبلغ المخصوم/المصروف (ريال)": emp_item_cost,
                    "النوع": "خصم موظف",
                }
            )
            st.success(f"تم خصم {emp_item_cost} ريال من مقرر الموظف {emp_name}")

    with col_exp2:
        st.markdown("### 🧱 تسجيل مصاريف صالة عامة")
        exp_title = st.text_input(
            "بند المصروف (كهرباء، نظافة، صيانة يديات...):"
        )
        exp_amount = st.number_input("مبلغ صيانة أو مصروف (ريال):", value=0, step=100)

        if st.button("💸 تسجيل المصروف العام"):
            if exp_title:
                st.session_state.expenses.append(
                    {
                        "التاريخ": datetime.datetime.now().strftime(
                            "%Y-%m-%d %I:%M %p"
                        ),
                        "البند": exp_title,
                        "المبلغ المخصوم/المصروف (ريال)": exp_amount,
                        "النوع": "مصاريف عامة",
                    }
                )
                st.success(f"تم تسجيل {exp_title} بقيمة {exp_amount} ريال")

# ==================== التبويب الرابع: التقارير والحسابات الكلية ====================
with tab_reports:
    st.subheader("📊 كشف الحسابات الكلي والإيرادات اليومية")

    # حساب المجاميع
    total_device_income = 0
    if st.session_state.history:
        total_device_income = sum(
            x["المبلغ المستلم الكلي"] for x in st.session_state.history
        )

    total_pos_income = 0
    if st.session_state.pos_sales:
        total_pos_income = sum(
            x["العائد الفوري (ريال)"] for x in st.session_state.pos_sales
        )

    total_expenses_out = 0
    if st.session_state.expenses:
        total_expenses_out = sum(
            x["المبلغ المخصوم/المصروف (ريال)"] for x in st.session_state.expenses
        )

    grand_total_cash = (
        total_device_income + total_pos_income
    ) - total_expenses_out

    # عرض عدادات كروت الأرقام
    stat1, stat2, stat3, stat4 = st.columns(4)
    stat1.metric("🎮 دخل جلسات الأجهزة", f"{total_device_income} ريال")
    stat2.metric("🥤 دخل الثلاجة الفوري", f"{total_pos_income} ريال")
    stat3.metric("📉 إجمالي الخصومات والمصاريف", f"{total_expenses_out} ريال")
    stat4.metric("💰 الصافي النهائي للكاش بالجرد", f"{grand_total_cash} ريال")

    st.markdown("---")
    st.markdown("### 📃 تفاصيل جلسات اللعب المنتهية")
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    else:
        st.info("لا توجد جلسات لعب مغلقة ومسجلة حتى الآن اليوم.")

    st.markdown("### 📃 تفاصيل البيع الكاش المباشر للثلاجة")
    if st.session_state.pos_sales:
        st.dataframe(
            pd.DataFrame(st.session_state.pos_sales), use_container_width=True
        )
    else:
        st.info("لا توجد عمليات بيع فوري مسجلة.")

    st.markdown("### 📃 كشف تفاصيل المصاريف وخصومات الموظفين")
    if st.session_state.expenses:
        st.dataframe(
            pd.DataFrame(st.session_state.expenses), use_container_width=True
        )
    else:
        st.info("لا توجد مصاريف أو خصومات موظفين مسجلة.")
