"""Job Radar: a Streamlit dashboard to search job listings by sector and country."""

import pandas as pd
import plotly.express as px
import streamlit as st

from job_scraper import config
from job_scraper.aggregator import fetch_jobs
from job_scraper.countries import ADZUNA_COUNTRIES, REMOTE_OPTION

st.set_page_config(page_title="Job Radar", page_icon="🧭", layout="wide")

st.title("🧭 Job Radar")
st.caption("Search job listings by sector and country, combining several public sources.")

with st.sidebar:
    st.header("Search filters")
    sector = st.text_input(
        "Sector / role",
        placeholder="e.g. backend developer, data scientist...",
    )
    country_options = [REMOTE_OPTION] + sorted(ADZUNA_COUNTRIES.keys())
    country = st.selectbox("Country", country_options)
    results_per_source = st.slider("Results per source", 5, 50, 20, step=5)
    search = st.button("Search jobs", type="primary", use_container_width=True)

    if not config.adzuna_configured():
        st.info(
            "Set ADZUNA_APP_ID and ADZUNA_APP_KEY in a .env file to include "
            "results from Adzuna (more accurate country-based search). "
            "Without it, only Arbeitnow and RemoteOK are used.",
            icon="ℹ️",
        )

if "jobs_df" not in st.session_state:
    st.session_state.jobs_df = pd.DataFrame()
if "last_query" not in st.session_state:
    st.session_state.last_query = ("", "")

if search:
    if not sector:
        st.warning("Enter a sector or role to search for.")
    else:
        with st.spinner("Searching for jobs..."):
            st.session_state.jobs_df = fetch_jobs(sector, country, results_per_source)
            st.session_state.last_query = (sector, country)

df = st.session_state.jobs_df

if df.empty:
    st.info("Enter a sector and country in the sidebar, then click 'Search jobs' to get started.")
else:
    sector_q, country_q = st.session_state.last_query

    col1, col2, col3 = st.columns(3)
    col1.metric("Jobs found", len(df))
    col2.metric("Distinct companies", df["company"].nunique())

    salaries = df.dropna(subset=["salary_min", "salary_max"], how="all")
    if not salaries.empty:
        avg_salary = salaries[["salary_min", "salary_max"]].mean(axis=1).mean()
        col3.metric("Estimated average salary", f"{avg_salary:,.0f}")
    else:
        col3.metric("Estimated average salary", "N/A")

    st.subheader("Job listings")
    st.dataframe(
        df,
        column_config={
            "url": st.column_config.LinkColumn("Link", display_text="View job"),
            "salary_min": st.column_config.NumberColumn("Min salary"),
            "salary_max": st.column_config.NumberColumn("Max salary"),
        },
        hide_index=True,
        use_container_width=True,
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        top_companies = df["company"].value_counts().head(10).reset_index()
        top_companies.columns = ["company", "jobs"]
        if not top_companies.empty:
            fig = px.bar(top_companies, x="company", y="jobs", title="Companies with the most listings")
            st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        top_locations = df["location"].value_counts().head(10).reset_index()
        top_locations.columns = ["location", "jobs"]
        if not top_locations.empty:
            fig = px.bar(top_locations, x="location", y="jobs", title="Most common locations")
            st.plotly_chart(fig, use_container_width=True)

    if not salaries.empty:
        st.subheader("Salary distribution (max salary reported)")
        fig = px.histogram(salaries, x="salary_max", nbins=20)
        st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download results as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=f"jobs_{sector_q.replace(' ', '_')}_{country_q}.csv",
        mime="text/csv",
    )

    st.subheader("Sources used")
    st.bar_chart(df["source"].value_counts())
