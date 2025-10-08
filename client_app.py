import streamlit as st
import requests
import os

# -----------------------------------------
# 1️⃣ Server Configuration
# -----------------------------------------
SERVER_URL = "https://super-30-mcp-youtubesearch-server.onrender.com"  # Replace with your MCP server URL

st.title("PragyanAI - YouTube Search MCP Client")
st.write("Connected to:", SERVER_URL)

# -----------------------------------------
# 2️⃣ User Input
# -----------------------------------------
query = st.text_input("Enter your YouTube Search Query", "AI Tutorials")
max_results = st.slider("Max Results", 1, 10, 5)

if st.button("🔍 Search YouTube"):
    payload = {
        "tool": "youtube_search_tool",
        "args": {
            "query": query,
            "max_results": max_results
        }
    }

    try:
        response = requests.post(f"{SERVER_URL}/mcp/run_tool", json=payload, timeout=30)

        if response.status_code == 200:
            videos = response.json()
            st.success(f"✅ Found {len(videos)} videos")

            # Display videos in columns with play button
            for v in videos:
                st.markdown(f"### 🎥 {v.get('title','No Title')}")
                cols = st.columns([1, 3])

                with cols[0]:
                    st.image(v["thumbnail"]["static"], width='stretch')

                with cols[1]:
                    st.markdown(f"**Channel:** [{v['channel']['name']}]({v['channel']['link']})")
                    st.markdown(f"**Published:** {v.get('published_date','-')}")
                    st.markdown(f"**Views:** {v.get('views','-')}")
                    st.markdown(f"**Length:** {v.get('length','-')}")
                    st.markdown(f"**Description:** {v.get('description','-')}")
                    st.markdown(f"[Watch on YouTube]({v['link']})")

                    # Play/Stop embedded YouTube
                    video_id = v['link'].split("v=")[-1]
                    st.video(f"https://www.youtube.com/watch?v={video_id}")

                st.markdown("---")

        else:
            st.error(f"❌ Error {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"⚠️ Exception: {str(e)}")
