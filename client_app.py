# client.py
import streamlit as st
import requests

st.set_page_config(page_title="🎥 YouTube MCP Client", layout="wide")
st.title("🤝 Streamlit Client — YouTube Search via MCP Server")

SERVER_URL = "https://super-30-mcp-youtubesearch-server.onrender.com"  # your Render URL

query = st.text_input("Enter a YouTube search query:")

if st.button("Search YouTube"):
    if query:
        with st.spinner("Searching..."):
            try:
                response = requests.post(
                    f"{SERVER_URL}/mcp/run_tool",
                    json={"tool_name": "youtube_search", "args": {"query": query}},
                )
                if response.status_code == 200:
                    data = response.json()
                    for v in data.get("results", []):
                        st.markdown(f"🎬 **[{v['title']}]({v['link']})** — {v['channel']}")
                        st.caption(f"👁 {v['views']} | 📅 {v['published']}")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please enter a search term.")
