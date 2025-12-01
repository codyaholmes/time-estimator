import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

st.title("Free-Time Estimator")

tabs = ["Time Input", "Visualization", "Info"]
form, viz, info = st.tabs(tabs)

with form:
    weekday_dict = {
        "S": "Sunday",
        "M": "Monday",
        "T": "Tuesday",
        "W": "Wednesday",
        "Th": "Thursday",
        "F": "Friday",
        "Sa": "Saturday",
    }
    normal_workday = ["M", "T", "W", "Th", "F"]
    week_options = weekday_dict.keys()
    selected_workdays = st.segmented_control(
        "Which days of the week do you (normally) work?",
        week_options,
        default=normal_workday,
        selection_mode="multi",
        key="workdays",
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
        st.info(f"{sleep_icon} Even vampires sleep. Let's be real here, yeah?")
    elif sleep <= 2:
        st.error(f"{sleep_icon} Congrats. You're on your way to meet Jesus soon.")
    elif sleep <= 4:
        st.warning(f"{sleep_icon} Seriously??? Get more sleep. Now!")
    elif sleep >= 16:
        st.info(f"{sleep_icon} You took the tale of Rip Van Winkle way too literal.")
    elif sleep >= 12:
        st.warning(
            f'{sleep_icon} "As a door turns back and forth on its hinges, so the lazy person turns over in bed" (Prov. 26:14).'
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
        vacation = st.number_input(
            "Vacation days in a year",
            min_value=0,
            max_value=364,
            value=14,
            icon=vacation_icon,
        )
    with col2:
        holidays = st.number_input(
            "Work holidays in a year",
            min_value=0,
            max_value=364,
            value=10,
            icon=holidays_icon,
        )

    with st.expander("See a list of US holidays"):
        st.caption(
            "Not sure how many work holidays you get in a year? Here's a common list to consider."
        )
        st.markdown(
            """
            **Major Holidays**
            - New Year's Day (Jan 1)
                - New Year's Eve sometimes included
            - Memorial Day (last Mon in May)
            - Independence Day (July 4)
            - Labor Day (first Mon in Sep)
            - Thanksgiving Day (fourth Thur in Nov)
                - Some companies inlcude the following Friday
            - Christmas Day (Dec 25)

            **Less Observed Holidays**
            - MLK, Jr. Day (thrid Mon in Jan)
            - Washington's Birthday/President's Day (third Mon in Feb)
            - Juneteenth (June 19)
            - Columbus Day (second Mon in Oct)
            - Veterans Day (Nov 11)
        """
        )

    with st.container(border=True):
        weekly_extra = st.slider(
            "Weekly Extracurriculars",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=0.25,
        )
        st.caption(
            "This last input is to capture wild card activities. This could be kids' practices, chores, phone time, exercising, or harrassing your city council. Total it all up (by week) and put it here."
        )

    # Check weekly hourly data
    weekly_sleep = sleep * 7
    weekly_work = len(selected_workdays) * work
    weekly_total = weekly_sleep + weekly_work + weekly_extra
    max_weekly = 24 * 7
    free_time = max_weekly - weekly_total
    pct_busy = round(weekly_total / max_weekly * 100, 1)
    pct_busy_fmttd = f"{pct_busy:.0f}%" if pct_busy % 1 == 0 else f"{pct_busy:.01f}%"

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
        - You are busy about **{pct_busy_fmttd}** of the week, occupied about {weekly_time_text(weekly_total)} (out of 168)."
        - You are :green-background[free] **{f":red-background[{weekly_time_text(free_time)}]" if weekly_total > 168 else weekly_time_text(free_time)}** each week.
    """,
        unsafe_allow_html=True,
    )

    bad_weekly_data_msg = f"Your weekly inputs are nonsensical. There are only {max_weekly} hours in a week! Readjust."
    if weekly_total > max_weekly:
        st.error(bad_weekly_data_msg)


with viz:
    if weekly_total > max_weekly:
        st.error(
            "Your weekly inputs are nonsensical. If you can't make sense, why would you expect the visuals too?"
        )

    # PREPARE DATES DATA
    curr_year = datetime.now().year
    year_start = date(curr_year, 1, 1)
    year_end = date(curr_year, 12, 31)
    dates = pd.date_range(year_start, year_end)
    df = pd.DataFrame(dates, columns=["Dates"])
    # df["Month"] = df.Dates.dt.strftime("%B")
    df["Weekday"] = df.Dates.dt.strftime("%A")
    df["Dates"] = df.Dates.dt.strftime("%m/%d/%Y")
    df["Sleep"] = sleep

    # Map work hours to selected days
    def work_hour_map():
        selected_wd_count = len(selected_workdays)
        avg_workday_hours = (
            0 if selected_wd_count == 0 else weekly_work / selected_wd_count
        )
        workdays_long = [weekday_dict.get(day_abbr) for day_abbr in selected_workdays]
        return {day: avg_workday_hours for day in workdays_long}

    workday_mapping = work_hour_map()
    df["Work"] = df.Weekday.map(workday_mapping).fillna(0)
    df["Extra"] = round(weekly_extra / 7, 2)
    df["Occupied"] = df.Sleep + df.Work + df.Extra
    df["Free"] = 24 - df["Occupied"]

    # Calculate yearly sleep totals
    yr_sleep = df.Sleep.sum()
    yr_sleep_avg = 7 * len(df)
    yr_sleep_fmttd = f"~ {yr_sleep:,.0f}"
    sleep_delta_fmttd = f"{round(yr_sleep - yr_sleep_avg, 1):,.0f} hrs"

    # Calculate yearly work totals
    yr_work_raw = df.Work.sum()
    yr_offdays = (
        0 if len(selected_workdays) == 0 else (holidays * work) + (vacation * work)
    )
    yr_work = yr_work_raw - yr_offdays
    workdays_long = [weekday_dict.get(day) for day in selected_workdays]
    yr_workdays = (
        0
        if work == 0 or len(selected_workdays) == 0
        else len(df.query(f"Weekday in {workdays_long}")) - holidays - vacation
    )
    normal_workday_long = [weekday_dict.get(day) for day in normal_workday]
    workdays_in_year = len(df.query(f"Weekday in {normal_workday_long}"))
    yr_offdays_avg = (holidays * 8) + (vacation * 8)
    yr_work_avg = (workdays_in_year * 8) - yr_offdays_avg
    yr_work_fmttd = f"~ {yr_work:,.0f}"
    work_delta_fmttd = f"{round(yr_work - yr_work_avg, 1):,.0f} hrs"

    # Calculate free time
    yr_extra = df.Extra.sum()
    yr_holiday_free_time = 0 if work == 0 else holidays * (24 - work)
    yr_vacation_free_time = 0 if work == 0 else vacation * (24 - work)
    yr_max_time = len(df) * 24
    yr_free_time = yr_max_time - yr_sleep - yr_work - yr_extra
    yr_free_time_pct = round(yr_free_time / yr_max_time * 100, 1)
    # st.write(len(df), yr_max_time, yr_free_time)

    # Make new dataframe for pie chart
    # For the visualization
    pie_df = pd.DataFrame(
        {
            "Category": ["Free", "Sleeping", "Working", "Extra"],
            "Hours": [
                yr_free_time,
                yr_sleep,
                yr_work,
                yr_extra,
            ],
        }
    )

    # For the dataframe (human friendly)
    pie_df_wide = pd.DataFrame(
        {
            "Free": [yr_free_time],
            "Sleeping": [yr_sleep],
            "Working": [yr_work],
            "Extra": [yr_extra],
            "Year Max": [yr_max_time],
        }
    )

    with st.container(border=True) as pie_chart:
        margin = 20
        st.markdown(
            "<h6 style='text-align: center'>Yearly Time Breakdown</h6>",
            unsafe_allow_html=True,
        )
        fig = px.pie(pie_df, values="Hours", names="Category")
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont_size=14,
            marker=dict(line=(dict(color="#ffffff", width=1))),
        )
        fig.update_layout(
            showlegend=False, margin=dict(t=margin, l=margin, r=margin, b=margin)
        )
        st.plotly_chart(fig)

        st.dataframe(pie_df_wide, hide_index=True)

    with st.expander("See dates breakdown"):
        st.caption(
            "Here, you can see how hours are broken down by day across the current year. Although you estimated daily and weekly times on the last screen, there are not 52 weeks perfectly in a year, This table outlines how the hours get distributed across selected working days for this year and then totals them up. This distribution allows the yearly estimates to be much more precise"
        )
        presentation_df = df.copy()
        presentation_df["Weekday"] = presentation_df.Weekday.str[:3]
        presentation_df.rename(columns={"Weekday": "Day"}, inplace=True)
        st.dataframe(presentation_df, hide_index=True, height=280)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Yearly Sleep",
            f"{yr_sleep_fmttd} hrs",
            delta=sleep_delta_fmttd,
            border=True,
            help="Value below the main metric is the hours of sleep above/below the national yearly average. If metric is green, you sleep X amount more than the U.S. average. If red, then below. (Most Americans get about 7 hours a sleep a day.)",
        )
    with col2:
        st.metric(
            "Yearly Work",
            f"{yr_work_fmttd} hrs",
            delta=work_delta_fmttd,
            delta_color="inverse",
            border=True,
            help="Value below the main metric is the hours of work above/below the national yearly average. If metric is red, you work X amount more than the U.S. average. If green, then below.",
        )

    col1, col2 = st.columns(2)
    with col1:
        yr_free_time_fmttd = (
            f"{yr_free_time_pct:.0f}%"
            if yr_free_time_pct % 0.25 == 0
            else f"{yr_free_time_pct:.1f}%"
        )
        st.metric("Yearly Free Time %", yr_free_time_fmttd, border=True)
    with col2:
        st.metric("Free Days in Year", len(df) - yr_workdays, border=True)

    col1, col2 = st.columns(2)
    with col1:
        daily_avg_free = yr_free_time / len(df)
        daily_avg_free_fmttd = (
            f"{daily_avg_free:.0f} hrs"
            if daily_avg_free % 1 == 0
            else f"{daily_avg_free:.1f} hrs"
        )
        st.metric("Avg Daily Free Time", daily_avg_free_fmttd, border=True)
    with col2:
        st.metric("Working Days in Year", yr_workdays, border=True)

with info:
    st.markdown(
        """
##### Developer
Cody Holmes
            
##### Issues
Email issues to me at codyaholmes@outlook.com. In a future update, I'll put in a form to submit them.

##### Purpose
The reason this app came about was because I wanted to get my church peers to understand they have much more free time than they think they do. With this free time, they have the ability to read their Bible, memorize Scripture, or serve others.
                
However, the analysis here is general enough that it could apply to anyone, religious and non-religous alike. Most people _convince themselves_ they don't have time to train for that promotion or that they're too busy to call their loved ones. The time is there, I promise. Time is our **most valuable** asset. It's important that you understand where it's all going!

In a future version, I hope to refine the ability to input specific extracurriculars to see how much phones, kids' practices, etc. break out better. _When I have the time_, I'll do so. Terrible pun, I know.

If you like this app and would like to buy me a coffee, don't. Use that money and bless someone else instead. 🙂
"""
    )
    st.space("small")
    st.code(
        '"For everything there is a season, and a time for every matter under heaven."\n- Ecclesiastes 3:1',
        height="stretch",
        language="text",
        wrap_lines=True,
    )
