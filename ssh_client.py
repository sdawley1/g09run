import paramiko
import socket
import os.path
import os

# Suppress terminal inputs so people don't steal my password
os.system('stty -echo')

def ssh_conn(hostname, username, transferFile, port=22):
    '''
    '''
    # Suppress terminal inputs so people don't steal my password
    os.system('stty -echo')
    log_file = 'SSHConnection.log'
    # Clear contents of log file at each iteration of function
    os.system('> {}'.format(log_file))
    # This function keeps track of everything that goes on behind the scenes
    # I've come to realize this is very helpful for determining if things are working
    # UPDATE: This file is incredibly useful for determining if things are working
    paramiko.util.log_to_file(log_file)

    # Establish socket. Still have no idea what a socket is
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    # Establish transport channel
    # I sort of understand what this thing does. The transport channel is what
    # actually connects us to the SSH server
    try:
        transport = paramiko.Transport(sock)
        transport.start_client()
        transport.auth_interactive_dumb(username=username)
        print('Connecting...\n')
    except paramiko.AuthenticationException:
        print('Failed Authentication. Exiting...')
        sock.close()
        os.system('stty echo')
        return

    # Opening SFTP channel
    # Check `paramiko.log` to see if sftp is opened successfully
    sftp = transport.open_sftp_client()

    # IMPORTANT
    # `localpath` is located in same directory as program
    # `remotepath` is default home directory in ssh server (FileZilla, in our case)
    try:
        sftp.put(localpath=transferFile, remotepath=transferFile)
        print('Transferring file {}...'.format(transferFile))
        sftp.close()
    except paramiko.SSHException:
        print('Cannot locate desired file. Exiting...')
        sock.close()
        os.system('stty echo')
        return

    # Testing
    try:
        channel = transport.open_channel(kind='session')
    except paramiko.ChannelException:
        print('Failed to create channel.')
        transport.close()
        os.system('stty echo')
    try:
        channel.exec_command('sbatch {}'.format(transferFile))  # THIS WORKS
        channel.close()
    except paramiko.SSHException:
        print('File upload failed.')
        channel.close()
        transport.close()
        os.system('stty echo')

    # Checking out what happened/where things could have gone wrong
    print('Successful upload (probably).')
    print('Refer to SSHConnection.log for details on success/failure.')
    # Close everything
    transport.close()
    os.system('stty echo')

    return

if __name__ == '__main__':
    # Fill these in I suppose
    hostname = ''
    username = ''
    transferFile = ''
    os.system('')
    ssh_conn(hostname, username, transferFile, port=22)
