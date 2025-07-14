import streamlit as st
import subprocess

st.set_page_config(page_title="Docker Tasks", page_icon="🐳", layout="centered")
st.title("🐳 Docker Task Runner")

st.markdown("Use this tool to manage Docker containers and images from your browser.")

# ---------------------- Basic Docker Commands ----------------------
st.header("🔍 Basic Docker Commands")
docker_cmds = {
    "Check Docker Installation": "docker --version",
    "Docker Version Details": "docker version",
    "List Docker Images": "docker images",
    "List Running Containers": "docker ps",
    "List All Containers": "docker ps -a",
    "Prune Unused Data": "docker system prune -f"
}

selected = st.selectbox("Choose a command to run", list(docker_cmds.keys()))
if st.button("Run Command"):
    cmd = docker_cmds[selected]
    st.code(f"$ {cmd}")
    st.text(subprocess.getoutput(cmd))

st.markdown("---")

# ---------------------- Pull Docker Image ----------------------
st.header("📥 Pull Docker Image")
image = st.text_input("Enter image name (e.g., ubuntu)", key="pull_image")
if st.button("Pull Image"):
    st.code(f"$ docker pull {image}")
    st.text(subprocess.getoutput(f"docker pull {image}"))

# ---------------------- Run Docker Container ----------------------
st.header("🚀 Run New Container")
col1, col2 = st.columns(2)
image_name = col1.text_input("Image to use (e.g., ubuntu)", key="image_name")
container_name = col2.text_input("Optional: Container name", key="container_name")

if st.button("Run Container"):
    name_part = f"--name {container_name}" if container_name else ""
    command = f"docker run -dit {name_part} {image_name}"
    st.code(f"$ {command}")
    st.text(subprocess.getoutput(command))

# ---------------------- Manage Existing Containers ----------------------
st.header("🔧 Manage Existing Containers")
container_id = st.text_input("Enter Container ID or Name", key="manage_id")

btns = st.columns(4)
if btns[0].button("Start"):
    st.text(subprocess.getoutput(f"docker start {container_id}"))
if btns[1].button("Stop"):
    st.text(subprocess.getoutput(f"docker stop {container_id}"))
if btns[2].button("Remove"):
    st.text(subprocess.getoutput(f"docker rm {container_id}"))
if btns[3].button("Logs"):
    st.text(subprocess.getoutput(f"docker logs {container_id}"))

# ---------------------- Run Command Inside Container ----------------------
st.header("🧠 Execute Inside Container")
exec_id = st.text_input("Container ID", key="exec_id")
command = st.text_input("Command to run (e.g., ls)", key="exec_command")
if st.button("Execute Command"):
    full_cmd = f"docker exec {exec_id} {command}"
    st.code(f"$ {full_cmd}")
    st.text(subprocess.getoutput(full_cmd))

# ---------------------- Remove Image ----------------------
st.header("🗑️ Remove Docker Image")
remove_image = st.text_input("Enter Image Name to Remove", key="remove_image")
if st.button("Remove Image"):
    st.code(f"$ docker rmi {remove_image}")
    st.text(subprocess.getoutput(f"docker rmi {remove_image}"))
