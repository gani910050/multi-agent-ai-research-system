import streamlit as st
from pipeline import run_research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Multi-Agent Research System")
st.write("Enter a research topic and let the multi-agent system search, read, write, and critique the research.")

st.divider()

topic = st.text_input(
    "Research Topic",
    placeholder="Example: Impact of Generative AI on Data Science Jobs"
)

run_button = st.button("🚀 Start Research", type="primary", use_container_width=True)

if run_button:

    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    st.info(f"Research started for: **{topic}**")

    with st.status("Running multi-agent research system...", expanded=True) as status:

        st.write("🔎 Step 1: Search Agent")
        st.write("📖 Step 2: Reader Agent")
        st.write("✍️ Step 3: Writer Agent")
        st.write("🧐 Step 4: Critic Agent")

        try:
            result = run_research_pipeline(topic.strip())

            if not result:
                status.update(
                    label="Research could not be completed",
                    state="error",
                    expanded=True
                )
                st.error(
                    "The pipeline returned no result. "
                    "This may happen if the Gemini API free-tier limit was reached."
                )
                st.stop()

            status.update(
                label="Research completed successfully",
                state="complete",
                expanded=False
            )

        except Exception as e:
            status.update(
                label="Research failed",
                state="error",
                expanded=True
            )
            st.error(f"Error: {e}")
            st.exception(e)
            st.stop()

    st.success("✅ Multi-agent research completed!")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Search Agent", "Completed")

    with col2:
        st.metric("Reader Agent", "Completed")

    with col3:
        st.metric("Writer Agent", "Completed")

    with col4:
        st.metric("Critic Agent", "Completed")

    st.divider()

    # Results
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔎 Search Results",
        "📖 Scraped Content",
        "📝 Final Report",
        "🧐 Critic Feedback"
    ])

    with tab1:
        st.subheader("Search Agent Results")
        st.text_area(
            "Search results",
            result.get("search_results", ""),
            height=500,
            label_visibility="collapsed"
        )

    with tab2:
        st.subheader("Reader Agent Output")
        st.text_area(
            "Scraped content",
            result.get("scraped_content", ""),
            height=500,
            label_visibility="collapsed"
        )

    with tab3:
        st.subheader("Final Research Report")

        report = result.get("report", "")

        st.markdown(report)

        st.download_button(
            label="📥 Download Research Report",
            data=report,
            file_name="research_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with tab4:
        st.subheader("Critic Agent Feedback")

        feedback = result.get("feedback", "")

        st.markdown(feedback)

st.divider()

st.caption("Powered by LangChain + Google Gemini + Tavily + Multi-Agent Research Pipeline")
