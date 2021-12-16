import os
from g09_shared import write_g09_shared
from ssh_client_shared import ssh_shared
from text_file_shared import infile_outfile_shared

# I'm just gonna put this here in case there's some error
# and I don't have it run at the end of my last function
os.system('stty echo')

# Determining the number of files to analyze
while True:
    try:
        N = input('Number of files we\'re working with: ')
        N = int(N)
        print('')
        break
    except ValueError:
        print('That\'s not a number.')


# Collecting user information
user_info, file_path = write_g09_shared(N)
shFiles, gjfFiles = infile_outfile_shared(user_info, file_path)
print('Files successfully created.\n')

# Initializing parameters
# I'd be shocked if (hostname, port) needed to be changed at all
hostname, port = 'login.marcc.jhu.edu', 22
username = user_info['email']

# The hard part
# SSH connection and SFTP
# Uploading data to MARCC through `sbatch`
print('Connect to SSH')
print('--------------')
ssh_shared(hostname, username, shFiles, gjfFiles, port=22)


