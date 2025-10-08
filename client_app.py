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
                        st.image(v["thumbnail"]["static"], use_column_width=True)
                        st.markdown(f"**{v.get('title', 'No Title')}**")
                        st.write(f"Channel: [{v['channel']['name']}]({v['channel']['link']})")
                        st.write(f"Published: {v.get('published_date', 'N/A')} | Views: {v.get('views', 'N/A')} | Length: {v.get('length', 'N/A')}")
                        st.write(v.get('description', '')[:150] + "...")

                        # Play / Stop buttons
                        play_key = f"play_{i+j}"
                        stop_key = f"stop_{i+j}"
                        video_url = v.get("link")

                        if st.button("▶️ Play", key=play_key):
                            if video_url:
                                st.video(video_url)

                        if st.button("⏹ Stop", key=stop_key):
                            st.stop()

        else:
            st.error(f"❌ Error {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"⚠️ Exception: {str(e)}")
