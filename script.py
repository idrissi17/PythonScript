import time
import paramiko


def connectToRouter(ip, username, password, port, enable_secret):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Connecting to router {ip}...")
        ssh.connect(hostname=ip, username=username, password=password, port=port, timeout=10)
        print("✅ Connected!")
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
    router_ip = "192.168.10.1"
    username = "admin"
    password = "cisco"
    enable_secret = "cisco"
    port = 3080
    connectToRouter(router_ip, username, password, port, enable_secret)
