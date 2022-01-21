import paramiko
import socket
import os.path
import os

def ssh_conn(hostname, username, shFile, gjfFile, port):
    """
    Uploads files to MARCC and submits job request.

    Parameters
    ----------
    hostname (str) = Hostname of server
    username (str) = Username (JHU email)
    shFile (str) = Name of file containing job request instructions
    gjfFile (str) = Data file
    port (int) = Port of server

    Returns
    -------
    Exit code and string of output from command line.
    """
    # Suppress terminal inputs so people don't steal my password
    os.system('stty -echo')
    log_file = 'SSHConnection.log'
    # Clear contents of log file at each iteration of function
    os.system(f"> {log_file}")
    # Logging output for development purposes
    paramiko.util.log_to_file(log_file)

    # Establish socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))

    # Establish transport channel
    # The transport channel is what connects us to the SSH server.
    try:
        transport = paramiko.Transport(sock)
        transport.start_client()
        transport.auth_interactive_dumb(username=username)
        print("Connecting...\n")
    except paramiko.AuthenticationException:
        print("Failed Authentication. Exiting...")
        sock.close()
        os.system('stty echo')
        return

    # Opening SFTP channel
    # Check `SSHConnection.log` to see if sftp is opened/closed successfully
    sftp = transport.open_sftp_client()

    # IMPORTANT
    # `localpath` is located in same directory as program
    # `remotepath` is default home directory in ssh server (if no filepath provided)

    try:
        sftp.put(localpath=shFile, remotepath=shFile)
        print(f"Transferring {shFile}...")
        sftp.put(localpath=gjfFile, remotepath=gjfFile)
        print(f"Transferring {gjfFile}...")
        sftp.close()
    except paramiko.SSHException:
        print('Cannot locate desired file. Exiting...')
        sock.close()
        os.system('stty echo')
        return

    # Opening channel to execute `sbatch` command
    try:
        channel = transport.open_channel(kind='session')
    except paramiko.ChannelException:
        print('Failed to create channel.')
        transport.close()
        os.system('stty echo')
    except paramiko.SSHException:
        transport.close()
        os.system('stty echo')
    try:
        channel.exec_command("sbatch {}".format(shFile))
        stderr = channel.recv(1000)  # Output from the server to our machine
        exit_code = channel.recv_exit_status()
        channel.close()
        print("Submitting job request...")
    except paramiko.SSHException:
        print("File upload failed.")
        channel.close()
        transport.close()
        os.system('stty echo')

    # Checking out what happened/where things could have gone wrong
    if str(exit_code) == '0':
        print(f"Exit code {exit_code}: Successful upload!")
        print("Be sure to remove files from SFTP server when finished.")
    else:
        print(f"Exit code {exit_code}: Upload failed.")
        print(f"Refer to {log_file} for troubleshooting.")

    # Close everything and echo terminal commands again.
    transport.close()
    os.system('stty echo')

    return exit_code, stderr
