import time
import paramiko


def connectToRouter():
    router_ip = "192.168.10.1"
    username = "admin"
    password = "cisco"
    enable_secret = "cisco"
    port = 3080

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Connecting to router {router_ip}...")
        ssh.connect(hostname=router_ip, username=username, password=password, port=3080, timeout=10)

        session = ssh.invoke_shell()
        commands = [
            b"enable\n",
            enable_secret.encode() + b"\n",
            b"show running-config\n"
        ]

        print("Sending commands to router...")

        for command in commands:
            session.send(command)
            time.sleep(0.5)

        time.sleep(2)
        output = session.recv(65535).decode(encoding="utf-8")
        print(output)

        ssh.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error connecting to router ===> {str(e)}")


if __name__ == "__main__":
    connectToRouter()