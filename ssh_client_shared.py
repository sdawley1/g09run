import paramiko
import socket
import os.path
import os

# Suppress terminal inputs so people don't steal my password
os.system('stty -echo')

def ssh_shared(hostname, username, shFiles, gjfFiles, port=22):
    """
    """
    # Suppress terminal inputs so people don't steal my password
    os.system('stty -echo')
    log_file = 'SSHConnection.log'
    # Clear contents of log file at each iteration of function
    os.system('> {}'.format(log_file))
    # This function keeps track of everything that goes on behind the scenes
    # I've come to realize this is very helpful for determining if things are working
    # UPDATE: This file is incredibly useful for determining if things are working
    paramiko.util.log_to_file(log_file)

    # Establish socket.
    # This initializes the `endpoints` of the connection
    # between our machine and the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    # Establish transport
    # The transport is what actually connects to the SSH server
    # In particular, a transport attaches to the socket
    # to transfer data through a channel, defined later
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
    # IMPORTANT
    # `localpath` is located in same directory as program
    # `remotepath` is default home directory in ssh server (FileZilla)
    try:
        for index in range(len(shFiles)):
            sftp = transport.open_sftp_client()
            sftp.put(localpath=shFiles[index], remotepath=shFiles[index])
            print('Transferring file {}...'.format(shFiles[index]))
            sftp.put(localpath=gjfFiles[index], remotepath=gjfFiles[index])
            print('Transferring file {}...'.format(gjfFiles[index]))
            sftp.close()
    except FileNotFoundError:
        print('Could not locate desired file. Exiting...')
        sock.close()
        os.system('stty echo')
        return
    except paramiko.SSHException:
        print('Could not locate desired file. Exiting...')
        sock.close()
        os.system('stty echo')
        return

    # Opening channel to execute `sbatch` command, i.e., submit batch request
    try:
        for index in range(len(shFiles)):
            channel = transport.open_channel(kind='session')
            channel.exec_command('sbatch {}'.format(shFiles[index]))
            channel.close()
            print('Submitting batch request for {}'.format(shFiles[index]))
    except paramiko.ChannelException:
        print('Failed to create channel.')
        transport.close()
        os.system('stty echo')

    # Checking out what happened/where things could have gone wrong
    print('')
    print('Successful upload.')
    print('Refer to SSHConnection.log for details on success/failure.')

    # Close everything
    transport.close()
    os.system('stty echo')

    return

if __name__ == '__main__':
    hostname = 'login.marcc.jhu.edu'
    username = ''
    shFiles = []
    gjfFiles = []
    ssh_shared(hostname, username, shFiles, gjfFiles, port=22)
