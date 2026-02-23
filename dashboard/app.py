"""
Interactive Data Visualization Dashboard - Online Learning Platform Analytics.
Run: streamlit run dashboard/app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Learning Platform Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load sample data (in production: connect to Snowflake or Parquet)
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"


@st.cache_data
def load_data():
    learners = pd.read_csv(DATA / "sample_learners.csv") if (DATA / "sample_learners.csv").exists() else pd.DataFrame()
    enrollments = pd.read_csv(DATA / "sample_enrollments.csv") if (DATA / "sample_enrollments.csv").exists() else pd.DataFrame()
    courses = pd.read_csv(DATA / "sample_courses.csv") if (DATA / "sample_courses.csv").exists() else pd.DataFrame()
    return learners, enrollments, courses


def main():
    st.title("📊 Online Learning Platform Analytics")
    st.markdown("Star/Snowflake DW • ETL • Spark • Snowflake • Security • Performance")

    learners, enrollments, courses = load_data()
    if enrollments.empty or courses.empty:
        st.info("Using sample data from `data/`. Add CSV files or connect to Snowflake for live data.")
        if learners.empty:
            learners = pd.read_csv(DATA / "sample_learners.csv") if (DATA / "sample_learners.csv").exists() else pd.DataFrame()
        if enrollments.empty:
            enrollments = pd.read_csv(DATA / "sample_enrollments.csv") if (DATA / "sample_enrollments.csv").exists() else pd.DataFrame()
        if courses.empty:
            courses = pd.read_csv(DATA / "sample_courses.csv") if (DATA / "sample_courses.csv").exists() else pd.DataFrame()

    sidebar = st.sidebar
    sidebar.header("Filters & Navigation")
    page = sidebar.radio(
        "Page",
        ["Overview", "Enrollments", "Courses & Categories", "Learner Progress", "Data Tables"],
        index=0,
    )

    # Merge for analytics
    enr = enrollments.merge(courses, on="course_id", how="left") if not enrollments.empty and not courses.empty else enrollments

    if page == "Overview":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Enrollments", len(enrollments))
        with c2:
            completed = enrollments.get("certificate_issued", pd.Series(dtype=bool))
            if completed.dtype == bool or completed.astype(str).str.lower().eq("true").any():
                st.metric("Completed", enrollments["certificate_issued"].astype(str).str.lower().eq("true").sum())
            else:
                st.metric("Completed", (enrollments.get("progress_pct", 0) >= 100).sum() if "progress_pct" in enrollments.columns else 0)
        with c3:
            st.metric("Unique Learners", enrollments["learner_id"].nunique() if "learner_id" in enrollments.columns else 0)
        with c4:
            st.metric("Unique Courses", enrollments["course_id"].nunique() if "course_id" in enrollments.columns else 0)

        if not enr.empty and "progress_pct" in enr.columns:
            fig = px.histogram(enr, x="progress_pct", nbins=20, title="Distribution of Progress %")
            st.plotly_chart(fig, use_container_width=True)
        if not enr.empty and "course_name" in enr.columns:
            agg = enr.groupby("course_name").agg(enrollments=("enrollment_id", "count"), avg_progress=("progress_pct", "mean")).reset_index()
            fig = px.bar(agg, x="course_name", y="enrollments", color="avg_progress", title="Enrollments by Course (color = avg progress %)")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Enrollments":
        st.subheader("Enrollments Over Time & by Course")
        if "enroll_date" in enrollments.columns:
            enrollments["enroll_date"] = pd.to_datetime(enrollments["enroll_date"])
            by_date = enrollments.groupby("enroll_date").size().reset_index(name="count")
            fig = px.line(by_date, x="enroll_date", y="count", title="Enrollments by Date")
            st.plotly_chart(fig, use_container_width=True)
        if not enr.empty:
            by_course = enr.groupby("course_name").size().reset_index(name="enrollments")
            fig = px.pie(by_course, values="enrollments", names="course_name", title="Share by Course")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Courses & Categories":
        st.subheader("Courses and Categories")
        if not courses.empty:
            if "category_name" in courses.columns:
                cat = courses.groupby("category_name").size().reset_index(name="courses")
                fig = px.bar(cat, x="category_name", y="courses", title="Courses per Category")
                st.plotly_chart(fig, use_container_width=True)
            st.dataframe(courses, use_container_width=True)

    elif page == "Learner Progress":
        st.subheader("Learner Progress")
        if not enr.empty and "learner_id" in enr.columns:
            learner_id = st.selectbox("Select learner", enr["learner_id"].unique())
            subset = enr[enr["learner_id"] == learner_id][["course_name", "progress_pct", "time_spent_minutes", "certificate_issued"]]
            st.dataframe(subset, use_container_width=True)
            fig = go.Figure(data=[go.Bar(x=subset["course_name"], y=subset["progress_pct"], name="Progress %")])
            fig.update_layout(title=f"Progress for {learner_id}")
            st.plotly_chart(fig, use_container_width=True)

    elif page == "Data Tables":
        st.subheader("Raw Data Tables")
        tab1, tab2, tab3 = st.tabs(["Learners", "Enrollments", "Courses"])
        with tab1:
            st.dataframe(learners, use_container_width=True)
        with tab2:
            st.dataframe(enrollments, use_container_width=True)
        with tab3:
            st.dataframe(courses, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Schema:** Star/Snowflake • **ETL:** Python • **Spark:** Batch + Streaming • **Security:** RBAC + Masking")


if __name__ == "__main__":
    main()
