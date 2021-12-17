# G09 Run

## Brief Background
Normally I like to spend time on things I'm passionate about, like chemistry, or... that's about it. Today, however, I've taken on a spite-driven project to try and automate uploading files to the Maryland Advanced Research Computing Center (MARCC).

In particular, this program is designed to optimize communication with MARCC and the upload of data acquired in Gaussian09 to the SSH server to be analyzed.

If there are any problems, fixes, optimizations, etc. anyone has to offer, feel free to email me: sdawley1@jhu.edu

Also, I'll note that this program (and this README, I suppose) were all made with Mac in mind (part of the spite thing). I'm sure anyone with even a remote knowledge of Python can alter anything to have it fit their machine, though.

## Dependencies
[Python](https://www.python.org/) 3.0+ 

[Paramiko](https://www.paramiko.org/index.html) 2.8.0 (Primary means of communicating with the SSH server and opening an SFTP)

[Cryptography](https://cryptography.io/en/latest/) 3.4.7

[PyNaCl](https://pypi.org/project/PyNaCl/) 1.4.0

For all of these dependencies, installing is as simple as running `pip install [LIBRARY]` in the command line. The website for each library is linked, all of which have installation instructions. If you're interested in checking the libraries already installed on your computer, you can run `pip list` from the command line.

## Some Commentary and Guidelines

### The Code

There are three key aspects of the program: Opening a `socket`, initializing a `transport`, and beginning the secure file transfer protocol (SFTP). The `socket` allows communication between two different machines and forms the basis of every other communication channel that’s built between the local machine and the remote server. In our case, the socket is allowing our machine (the client) to request commands be performed on a remote server (MARCC). The particular type of socket I used was a STREAM socket which guarantees the delivery of information in the same order it was sent. This is important because otherwise we might try and submit a job request to MARCC before the data was uploaded via SFTP by accident.

The `transport` attaches to the socket we just built and authenticates our machine, so the server bothers to interact with us. The transport channel is what transfers data from our machine to the server, such as commands, data structures, and filenames. Commands are passed through the shell. Though, the only pieces of data we need to transport along this channel are the filenames and command to submit the job request. The literal files are passed along through the SFTP.

The SFTP is established through a transport channel. The files are uploaded to the server and the command to submit them is processed next.

### Possible Troubleshooting

I discovered that the most helpful function which I (accidently) implemented was `paramiko.util.log_to_file()` which writes to a `.log` file everything that is communicated between our machine and the SSH. Running the program automatically creates the file `SSHConnection.log` which contains all of this information and if you know what to look for (which, frankly, I don't even really know what to look for I just search for keywords like 'sftp', etc.), troubleshooting becomes immensely easier.

Another point that I think is important to make even though it rarely becomes an issue is the storage of the public key the SSH server and your machine exchange during the initial authentication. This public key is stored locally *only after you've connected to the server once*. So, don't try and use this program the very first time you're uploading data to MARCC. Moreover, this key is stored at `~/.ssh/known_hosts` which is hidden file. Accessing this file illustrates the type of key encryption used by the SSH server and informed some of the decisions about authenticating the server to allow our machine to connect. Also, it contains the server address anD IP which is helpful if you ever forget it.

### Future Goals

As it stands, the program works for 'shared' job submission with a particular setof nodes, tasks per node, and allotted time. In the future, however, I'd like to add more types of jobs with particular sets of parameters. This issue could be overcome by allowing the user to enter the type of job alongside all default parameters, but that wouldn't be the most efficient way of doing it (I feel). 




