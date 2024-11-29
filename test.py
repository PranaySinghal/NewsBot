import streamlit as st
import openai
from haxor import HackerNews

# Initialize Hacker News API client
hn = HackerNews()

# Streamlit UI
st.title("Multi-Agent AI News Researcher")
st.caption("Explore top Hacker News stories and generate reports using OpenAI GPT.")

# Input: OpenAI API Key
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Set OpenAI API key
if openai_api_key:
    openai.api_key = openai_api_key

    # Input: User query
    query = st.text_input("Enter your report query")

    # Fetch top stories from Hacker News
    if st.button("Fetch Top Stories"):
        with st.spinner("Fetching top stories..."):
            try:
                # Get top stories
                top_stories = hn.top_stories(limit=5)
                stories = [
                    f"{story.title} (Score: {story.score}, URL: {story.url})"
                    for story in top_stories
                ]

                st.subheader("Top 5 Hacker News Stories")
                for i, story in enumerate(stories, start=1):
                    st.write(f"{i}. {story}")
            except Exception as e:
                st.error(f"Error fetching stories: {e}")

    # Generate report using OpenAI
    if query and st.button("Generate Report"):
        with st.spinner("Generating report..."):
            try:
                # Call OpenAI GPT
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Generate a report for the following query based on Hacker News stories:\n\n{query}",
                    max_tokens=500,
                    temperature=0.7,
                )
                st.subheader("Generated Report")
                st.write(response.choices[0].text.strip())
            except Exception as e:
                st.error(f"Error generating report: {e}")
