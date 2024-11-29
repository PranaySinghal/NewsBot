import streamlit as st
import os
from phi.assistant import Assistant
from phi.tools.hackernews import HackerNews
from phi.llm.openai import OpenAIChat

st.title("Multi-Agent AI news researcher")
st.caption("Hi human, This app lets you explore top hackernews stories and users, and create blog posts and reports.")

openai_api_key=st.text_input("OpenAi API Key",type="password")

if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    try:
        story_researcher=Assistant(
            name="HackerNews Story Reseacher",
            role="Researches hackernews stories and users.",
            tools=[HackerNews()],
        )

        user_researcher=Assistant(
            name="HackerNews User Reseacher",
            role="Reads articles from URLs.",
            tools=[HackerNews()],
        )

        hn_assistant=Assistant(
            name="Hackernews Team",
            team=[story_researcher,user_researcher],
            llm=OpenAIChat(
                model="gpt-4o-mini",
                max_tokens=1024,
                temperature=0.5,
                api_key=openai_api_key
            ),
        
        )
        st.write("Assistant initialized successfully.")
    except Exception as e:
        st.error(f"Error initializing assistants: {e}")

    query=st.text_input("Enter your report query")

    if query:
        try: 
            response=hn_assistant.run(query,stream=False)
            st.write(response)
        except Exception as e:
            st.error(f"Error processing query: {e}")

# from openai import OpenAI
# client = OpenAI(api_key="")

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )

# print(completion.choices[0].message)