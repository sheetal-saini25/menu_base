import streamlit as st

st.set_page_config(page_title="Command Runner", page_icon="🖥️", layout="wide")

# --- Set Online Background via CSS ---
page_bg = """
<style>
.stApp {
    background-image: url("https://i.imgur.com/qZc1j5b.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
.block-container {
    background-color: rgba(0, 0, 0, 0.6); 
    padding: 2rem;
    border-radius: 12px;
}
h1, h2, h3, p {
    color: #ffffff;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Page Content ---
st.title("🧠 Multi-Task Command Web Tool")

st.markdown("""
Welcome to your **centralized developer toolkit** powered by SSH, Docker, Linux & scripting magic.

🔧 Use the sidebar to:
- ⚙️ Run **Linux commands** via SSH  
- 🐳 Control your **Docker containers**  
- 🐍 Access **Python utilities**  
- ☕ Try out **JavaScript-based tools**  
""")

st.markdown("---")

st.subheader("💡 Pro Tip:")
st.info("Use this tool as your daily Swiss Army knife to automate and manage system tasks from one interface.")

st.markdown("---")
st.caption("🔐 Developed by Sheetal Saini • Powered by Streamlit + Linux + Docker + Python")
