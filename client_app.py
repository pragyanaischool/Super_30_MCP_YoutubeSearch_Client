import streamlit as st
import requests

# -----------------------------------------
# 1️⃣ Server Configuration
# -----------------------------------------
SERVER_URL = "https://super-30-mcp-youtubesearch-server.onrender.com/mcp/run_tool"

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
        # Send POST request to the correct MCP endpoint
        response = requests.post(SERVER_URL, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Response Received")

            # Display raw JSON for debugging
            st.json(result)

            # Display formatted video results
            videos = result if isinstance(result, list) else result.get("video_results", [])
            if not videos:
                st.info("No videos found.")
            for v in videos:
                st.markdown(f"🎥 **{v.get('title', 'No Title')}**")
                if v.get("link"):
                    st.write(f"[Watch on YouTube]({v['link']})")
                st.write("---")

        else:
            st.error(f"❌ Error {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error(f"⚠️ Exception: {str(e)}")
