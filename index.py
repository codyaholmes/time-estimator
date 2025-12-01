import streamlit as st

st.title("Time Estimator")

tabs = ["Estimator Form", "Free Time Visualization"]
form, viz = st.tabs(tabs)

with form:
    week_options = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    workdays = st.segmented_control(
        "Which days of the week do you (normally) work?",
        week_options,
        selection_mode="multi",
        default=["Mon", "Tue", "Wed", "Thu", "Fri"],
    )

    sleep_icon = ":material/nightlight:"
    work_icon = ":material/schedule:"
    holidays_icon = ":material/event:"
    vacation_icon = ":material/beach_access:"

    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider(
            f"{sleep_icon} Daily Sleep (hrs)",
            value=8.0,
            step=0.25,
            min_value=0.0,
            max_value=24.0,
            help="0.25 increments represent 15 minutes.",
        )
    with col2:
        work = st.slider(
            f"{work_icon} Daily Work (hrs)",
            value=8.0,
            step=0.25,
            min_value=0.0,
            max_value=24.0,
            help="Include commute time.",
        )

    if sleep <= 0:
        st.info(f"{sleep_icon} You're not a vampire. Let's be real here, yeah?")
    elif sleep <= 2:
        st.error(f"{sleep_icon} Congrats. You're on your way to meet Jesus soon.")
    elif sleep <= 4:
        st.warning(f"{sleep_icon} Seriously??? Get more sleep. Now!")
    elif sleep >= 16:
        st.info(f"{sleep_icon} You took the tale of Rip Van Winkle way too literal.")
    elif sleep >= 12:
        st.warning(
            f'{sleep_icon} "As a door turns back and forth on its hinges, so the lazy person turns over in bed" (Prov. 27:16).'
        )

    if work <= 0:
        st.success(f"{work_icon} Oh, so you're retired. Good for you.")
    elif work <= 2:
        st.error(
            f"{work_icon} If anyone isn't willing to work, he should not eat (1 Thess. 3:10)."
        )
    elif work >= 18:
        st.info(f"{work_icon} You're an ice-road trucker, aren't you?")
    elif work >= 12:
        st.warning(f"{work_icon} You might be working too much...")

    col1, col2 = st.columns(2)
    with col1:
        holidays = st.number_input(
            "Work holidays in a year",
            min_value=0,
            max_value=364,
            value=10,
            icon=holidays_icon,
        )
    with col2:
        vacation = st.number_input(
            "Vacation days in a year",
            min_value=0,
            max_value=364,
            value=14,
            icon=vacation_icon,
        )

    with st.container(border=True):
        weekly_extra = st.slider(
            "Extra weekly hours",
            min_value=0.0,
            max_value=40.0,
            step=0.25,
        )
        st.caption(
            "This last input is to capture weekly wild card duties. This could be kids' practices, chores, volunteering, or harrassing your city council. Capture that stuff here. Remember, this is a **weekly** catch-all estimator."
        )

    # Check weekly hourly data
    weekly_sleep = sleep * 7
    weekly_work = len(workdays) * work
    weekly_total = weekly_sleep + weekly_work + weekly_extra
    max_weekly = 24 * 7
    free_time = max_weekly - weekly_total
    pct_busy = weekly_total / max_weekly

    def weekly_time_text(hours):
        hour_part = hours // 1
        minutes_part = (hours - hour_part) * 60
        is_zero_minutes = minutes_part == 0
        minutes_suffix = "" if is_zero_minutes else f" and {minutes_part:.0f} minutes"
        pluralizer = "" if hour_part == 1.0 else "s"
        return f"{hour_part:.0f} hour{pluralizer}{minutes_suffix}"

    st.subheader("Weekly Breakdown")
    st.markdown(
        f"""
        - You sleep about **{weekly_time_text(weekly_sleep)}** a week.
        - You work about **{weekly_time_text(weekly_work)}** a week.
        - You are committed to **{weekly_time_text(weekly_extra)}** of extracurricular activities a week.
        - You are busy about **{pct_busy:.1%}** of the week.
        - You are left with **{weekly_time_text(free_time)}** of free time each week.
    """
    )

    if weekly_total > max_weekly:
        st.error(
            f"Your weekly hour inputs are nonsensical. There's only {max_weekly} hours in a week."
        )


# PREPARE DATES DATA


def calculate_weekly_hours(): ...


with viz:
    ...
