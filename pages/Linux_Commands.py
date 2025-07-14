import streamlit as st
import subprocess
import shlex

st.set_page_config(page_title="Linux & Docker Menu Tool", page_icon="🐧")
st.title("🐧 Linux & Docker Menu Tool")

if "ssh_ready" not in st.session_state:
    st.session_state.ssh_ready = False

if not st.session_state.ssh_ready:
    with st.sidebar:
        st.title("🔐 SSH Login")
        username = st.text_input("Linux Username")
        remote_ip = st.text_input("Remote IP")
        root_user = st.checkbox("Connect as root")

        if st.button("Save SSH Credentials"):
            if username and remote_ip:
                st.session_state.username = "root" if root_user else username
                st.session_state.remote_ip = remote_ip
                st.session_state.ssh_ready = True
                st.success("SSH Credentials Saved")
            else:
                st.warning("Please fill in both fields.")
    st.stop()

username = st.session_state.username
remote_ip = st.session_state.remote_ip


def run_ssh_command(command):
    try:
        safe_command = command.replace('"', '\\"')
        full_command = f'ssh {username}@{remote_ip} "{safe_command}"'
        result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
        st.code(f"$ {command}")
        if result.returncode == 0:
            st.text(result.stdout)
        else:
            st.error(f"Error: {result.stderr}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def run_local_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.code(f"$ {command}")
        if result.returncode == 0:
            st.text(result.stdout)
        else:
            st.error(f"Error: {result.stderr}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


tasks = [
    (1, "date"), (2, "cal"), (3, "ifconfig"), (4, "ls"), (5, "pwd"), (6, "rm"), (7, "rmdir"),
    (8, "mkdir"), (9, "touch"), (10, "rm -rf"), (11, "gedit"), (12, "vi"), (13, "echo"),
    (14, "cd"), (15, "cd .."), (16, "cat"), (17, "df"), (18, "ping google.com"),
    (19, "yum repolist"), (20, "yum install httpd"), (21, "rpm -q httpd"), (22, "whoami"),
    (23, "history"), (24, "rmdir --help"), (25, "ssh-keygen -t rsa"), (26, "notepad id_rsa.pub"),
    (27, "notepad pp.py"), (28, "notepad menu.html"), (29, "head file.txt"),
    (30, "head -n 2 file.txt"), (31, "grep 2 file.txt"), (32, "systemctl start httpd"),
    (33, "systemctl status httpd"), (34, "systemctl stop firewalld"), (35, "pip install pywhatkit"),
    (36, "python3 -c 'import pywhatkit'"), (37, "Send WhatsApp Message"),
    (38, "Send WhatsApp to Group"), (39, "pip install streamlit"), (40, "python3 -c 'import streamlit'"),
    (41, "python3 -c 'import os'"), (42, "streamlit run app.py"), (43, "su - user"),
    (44, "echo 'hello' >> file.txt"), (45, "exit"), (46, "sudo yum install httpd"),
    (47, "sudo yum remove httpd"), (48, "ls -l"), (49, "chmod 755 file.txt"),
    (50, "chgrp users file.txt"), (51, "usermod -G group user"), (52, "usermod -g group user"),
    (53, "pip install package"), (54, "python3 -c 'import module'"), (55, "python3 -c 'print(\\\"Hello\\\")'"),
    (56, "ssh root@localhost"), (57, "Docker run"), (58, "Docker start"),
    (59, "Docker stop"), (60, "Docker attach"), (61, "Docker remove"), (62, "docker images"),
    (63, "docker ps -a"), (64, "Exit")
]

choice_dict = {f"{num}. {desc}": num for num, desc in tasks}
selected_option = st.selectbox("Select a command:", list(choice_dict.keys()))

if st.button("Run Command"):
    choice = choice_dict[selected_option]

    if choice == 64:
        st.success("Exiting... Goodbye!")
        st.stop()

    if choice in set(range(1, 36)) | set(range(39, 57)):
        if choice == 18:
            run_ssh_command("ping -c 4 google.com")
        elif choice == 37:
            phone = st.text_input("Phone (+91...):")
            msg = st.text_input("Message:")
            if st.button("Send WhatsApp"):
                command = f"python3 -c \"import pywhatkit; pywhatkit.sendwhatmsg_instantly('{phone}', '{msg}')\""
                run_local_command(command)
        elif choice == 38:
            group_id = st.text_input("Group ID:", value="team 38")
            msg = st.text_input("Message:", value="hello")
            if st.button("Send to Group"):
                command = f"python3 -c \"import pywhatkit; pywhatkit.sendwhatmsg_to_group_instantly('{group_id}', '{msg}')\""
                run_local_command(command)
        else:
            cmd = [desc for num, desc in tasks if num == choice][0]
            run_ssh_command(cmd)

    elif choice in [26, 27, 28]:
        local_cmd = [desc for num, desc in tasks if num == choice][0]
        run_local_command(local_cmd)

    elif choice in range(57, 64):
        if choice == 57:
            name = st.text_input("Container Name")
            image = st.text_input("Image Name")
            if st.button("Run Docker Container"):
                run_ssh_command(f"docker run -dit --name {name} {image}")
        else:
            name = st.text_input("Container Name")
            if st.button("Execute Docker Command"):
                docker_cmds = {
                    58: f"docker start {name}",
                    59: f"docker stop {name}",
                    60: f"docker attach {name}",
                    61: f"docker rm {name}"
                }
                run_ssh_command(docker_cmds.get(choice, ""))
    elif choice == 62:
        run_ssh_command("docker images")
    elif choice == 63:
        run_ssh_command("docker ps -a")