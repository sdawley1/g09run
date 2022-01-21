import os
from user_info import write_g09
from ssh_client import ssh_conn
from instructions import gaussian09

# Collecting user information
user_info = write_g09()
shFile, gjfFile = gaussian09(user_info)
print("Files successfully created.\n")

# Initializing parameters
hostname, port = "ENTER HOSTNAME HERE", (ENTER INTEGER PORT HERE)
username = user_info['email']

# Connecting to SSH
print('Connect to SSH')
print('--------------')
ssh_conn(hostname, username, shFile, gjfFile, port)


