# g09run

Normally I like to spend time on things I'm passionate about, like chemistry, or... that's about it. Today, however, I've taken on a spite-driven project to try and automate uploading files to the Maryland Advanced Research Computing Center (MARCC).

If there are any problems, fixes, optimizations anyone has to offer, feel free to email me: sdawley1@jhu.edu

## Dependencies
[Python](https://www.python.org/) 3.0+ 

[Paramiko](https://www.paramiko.org/index.html) 2.8.0

[Cryptography](https://cryptography.io/en/latest/) 3.4.7

[pynacl](https://pypi.org/project/PyNaCl/) 1.4.0


## Some Commentary

As it stands, there are four primary helper functions:

`write_g09` attains all necessary information from the user and stores 1) all of that information to be referenced later and 2) the filepath to store the '.sh' file that we're actually interested in uploading to MARCC.

`infile_2_outfile` takes the information attained in `write_g09` and makes the files that we need to tell MARCC what to do. Neither user input nor extra dependencies are required to make this work. Just some print statements.

If this program was like the most recent season of SNL, `ssh_conn` would be like Cecily Strong. It connects us with the SSH server, establishes an SFTP, transfers the files and requests a job from MARCC. Here we rely on `paramiko`, an absolutely incredible library that uses a few other cryptography-based libraries to maintain security and make connecting to an SSH server a breeze, even with two-factor authentication. Similar to `infile_2_outfile`, no user input is required. That being said, this is the point in the program where the most possible errors can occur. Authenticating to the server, opening a channel for SFTP, transferring files, and executing commands over the SSH all offer a way to raise a different kind of exception. So, although the code to just connect to the server and transfer files is less than ten lines or so, the error handling (that I tried my best to implement) took up a majority of the time spent writing the program.


## Standard Operating Procedure (SOP)
