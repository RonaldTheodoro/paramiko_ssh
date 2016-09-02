from decouple import config
from paramiko import client

class SSH:
    client = None

    def __init__(self, address):
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(
            address, 
            username=config('SSHUSER'), 
            password=config('SSHPASSWORD'), 
            look_for_keys=False
        )

    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)

            while not stdout.channel.exit_status_ready():
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)

                    while stdout.channel.recv_ready():
                        alldata += stdout.channel.recv(1024)

                    print(str(alldata, 'utf-8'))
