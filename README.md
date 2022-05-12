# get_servers
Python script to get server info from list of servers

## Dependencies
- Python 3
- argparse
- paramiko
- json

## Input
"-f"/"--file", Path of server file, required.
"-k"/"--ssh-key", Key for login, required.
"-o"/"--output-path", Path for JSON output, required.

## Server list
Write the server list file as a .txt file in the form of:
user@server
user@server
user@server

## Outputs
The information will be output into a .json file with information containing:
- cpu_info
- nic_info
- disk_info
