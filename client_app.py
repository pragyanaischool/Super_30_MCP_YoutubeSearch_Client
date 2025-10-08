import streamlit as st
import requests

# -----------------------------------------
# 1️⃣ Server Configuration
# -----------------------------------------
SERVER_URL = "https://super-30-mcp-youtubesearch-server.onrender.com/mcp/run_tool"  # Replace with your MCP server URL

st.title("🎬 YouTube Search MCP Client")
st.write("Connected to MCP Server at:", SERVER_URL)

# -----------------------------------------
# 2️⃣ User Input
# -----------------------------------------
query = st.text_input("Enter your YouTube Search Query", "AI Tutorials")
max_results = st.slider("Max Results", 1, 10, 5)

# Initialize session state
if "play_video" not in st.session_state:
    st.session_state.play_video = None  # stores the currently playing video URL

# -----------------------------------------
# 3️⃣ Search Button
# -----------------------------------------
if st.button("🔍 Search YouTube"):
    payload = {
        "tool": "youtube_search_tool",
        "args": {
            "query": query,
            "max_results": max_results
        }
    }

    try:
        response = requests.post(SERVER_URL, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Response Received")

            videos = result if isinstance(result, list) else result.get("video_results", [])
            if not videos:
                st.info("No videos found.")

            # Display videos in columns (3 per row)
            num_cols = 3
            for i in range(0, len(videos), num_cols):
                cols = st.columns(num_cols)
                for j, v in enumerate(videos[i:i+num_cols]):
                    with cols[j]:
                        # Video info
                        st.image(v["thumbnail"]["static"], use_container_width=True)
                        st.markdown(f"**{v.get('title', 'No Title')}**")
                        st.write(f"Channel: [{v['channel']['name']}]({v['channel']['link']})")
                        st.write(f"Published: {v.get('published_date', 'N/A')} | Views: {v.get('views', 'N/A')} | Length: {v.get('length', 'N/A')}")
                        st.write(v.get('description', '')[:150] + "...")

                        video_url = v.get("link")

                        # Play / Stop buttons using session state
                        if st.button("▶️ Play", key=f"play_{i+j}"):
                            st.session_state.play_video = video_url

                        if st.button("⏹ Stop", key=f"stop_{i+j}"):
                            if st.session_state.play_video == video_url:
                                st.session_state.play_video = None

                        # Render video if this is the currently playing one
                        if st.session_state.play_video == video_url:
                            st.video(video_url)

        else:
            st.error(f"❌ Error {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"⚠️ Exception: {str(e)}")

    except Exception as e:
        st.error(f"⚠️ Exception: {str(e)}")
