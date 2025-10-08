import streamlit as st
import requests
import json

# -----------------------------------------
# 1️⃣ Server Configuration
# -----------------------------------------
SERVER_URL = "https://super-30-mcp-youtubesearch-server.onrender.com"  # Replace with your Render MCP server URL

st.title("🎬 YouTube Search MCP Client")
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
        # Send POST request
        response = requests.post(SERVER_URL, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Response Received")

            # Display as JSON
            st.json(result)

            # Display formatted results
            videos = result if isinstance(result, list) else result.get("videos", [])
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

