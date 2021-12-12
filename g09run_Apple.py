import os
from g09_write import write_g09
from ssh_client import ssh_conn
from text_file_creator import infile_2_outfile

# I'm just gonna put this here in case there's some error
# and I don't have it run at the end of my last function
os.system('stty echo')

# Collecting user information
user_info, file_path = write_g09()
outFile = infile_2_outfile(user_info, file_path)
print('Files successfully created.\n')

# Initializing parameters
# I'd be shocked if (hostname, port) needed to be changed at all
hostname, port = 'login.marcc.jhu.edu', 22
username = user_info['email']

# Here's the file we want to transfer
# It's defined above but I redefine it here for clarity
transferFile = outFile
print('Connect to SSH')
print('--------------')

# The hard part
# SSH connection and SFTP
# Uploading data to MARCC through `sbatch`
ssh_conn(hostname, username, transferFile, port=22)


