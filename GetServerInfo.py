import argparse
import paramiko
import json

def get_args(argv=None) -> dict:
    parser = argparse.ArgumentParser(description="Outputs server information when given a text file with a list of servers in the form of user@host\nuser@host.")
    parser.add_argument("-f", "--file", help="Path of server file.", required=True)
    parser.add_argument("-k", "--ssh-key", help="Key for login.", required=True)
    parser.add_argument("-o", "--output-path", help="Path for JSON output.", required=True)
    return parser.parse_args(argv)

def read_file(path: str) -> list:
    data = open(file=path).readlines()
    return data

def create_session(server: str, key_path: str) -> paramiko.SSHClient:
    username = server.split("@")[0].strip()
    host = server.split("@")[1].strip()
    pkey = paramiko.RSAKey.from_private_key_file(key_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=22, username=username, pkey=pkey)
    return ssh

def run_command(command: str, session: paramiko.SSHClient) -> str:
    try:
        _stdin, stdout, _stderr = session.exec_command(command=command)
        lines = stdout.read().decode()
        return lines
    except:
        print(_stderr)

def iterate_list(server_list: list, key_path: str) -> dict:
    server_dict = {"servers": []}
    cpu_info_cmd = "lscpu -J"
    nic_info_cmd = "/usr/sbin/lspci"
    disk_info_cmd = "lsblk -J"
    for server in server_list:
        host = server.split("@")[1].strip()
        client = create_session(server=server, key_path=key_path)
        cpu_info_json = json.loads(run_command(command=cpu_info_cmd, session=client))
        nic_info_json = json.dumps(list(run_command(command=nic_info_cmd, session=client).split("\n")))
        disk_info_json = json.loads(run_command(command=disk_info_cmd, session=client))
        server_dict["servers"].append( { host: {
            "cpu_info": cpu_info_json,
            "nic_info": nic_info_json,
            "disk_info": disk_info_json
        }})
        client.close()
    return server_dict

def output_file(output_path: str, data: str) -> None:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def work(args: dict) -> None:
    data = read_file(path=args.file)
    server_data = iterate_list(server_list=data, key_path=args.ssh_key)
    output_file(output_path=args.output_path, data=server_data)

if __name__ == "__main__":
    argvals = None
    args = get_args(argvals)
    work(args)