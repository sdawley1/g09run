## Brief Background
Normally I like to spend time on things I'm passionate about, like chemistry, or... that's about it. Today, however, I've taken on a spite-driven project to try and automate uploading files to the Maryland Advanced Research Computing Center (MARCC).

In particular, this program is designed to optimize communication with MARCC and the upload of data acquired in Gaussian09 to the SSH server to be anaylzed.

If there are any problems, fixes, optimizations, etc. anyone has to offer, feel free to email me: sdawley1@jhu.edu

Also, I'll note that this program (and this README, I suppose) were all made with Mac in mind (part of the spite thing). I'm sure anyone with even a remote knowldege of coding can alter anything to have it fit their machine, though.

## Dependencies
[Python](https://www.python.org/) 3.0+ 

[Paramiko](https://www.paramiko.org/index.html) 2.8.0 (Primary means of communicating with the SSH server and opening an SFTP)

[Cryptography](https://cryptography.io/en/latest/) 3.4.7

[PyNaCl](https://pypi.org/project/PyNaCl/) 1.4.0

For all of these dependencies, installing is as simple as running 
`pip install [LIBRARY]`
in the command line. The website for library is linked, also, all of which have installation instructions. If you're interested in checking the installs on your computer already you can run `pip list` from the command line.

## Some Commentary and Guidelines

### The Code

There are three primary helper functions:

`write_g09` attains all necessary information from the user and stores 1) all of that information to be referenced later and 2) the filepath to store the `.sh` file that we're actually interested in uploading to MARCC. This is called in the first part of the program and low stakes, for lack of a better phrase. At the end of inputting your information there's an option to review and even ditch all of it and restart from the beginning. That being said, the primary portion of the program relies heavily on this information being accurate.

`infile_2_outfile` takes the information attained in `write_g09` and makes the files that we need to tell MARCC what to do. Neither user input nor extra dependencies are required to make this work. Just some print statements.

If this program was like the most recent season of SNL, `ssh_conn` would be like Cecily Strong. It connects us with the SSH server, establishes an SFTP, transfers the files and requests a job from MARCC. Here we rely on `paramiko`, an absolutely incredible library that uses a few other cryptography-based libraries to maintain security and make connecting to an SSH server a breeze, even with two-factor authentication. This is probably a good time to mention that using two-factor authenticaton is still required. Similar to `infile_2_outfile`, no user input is required. That being said, this is the point in the program where the most possible errors can occur. Authenticating to the server, opening a channel for SFTP, transferring files, and executing commands over the SSH all offer a way to raise a different kind of exception. So, although the code to just connect to the server and transfer files is less than ten lines or so, the error handling (that I tried my best to implement) took up a majority of the time spent writing the program. 

### Possible Troubleshooting

While writing this, I discovered that the most helpful function I (accidently) implemented was `paramiko.util.log_to_file()` which writes to a `.log` file everything that is communicated between our machine and the SSH. Running the program automatically creates the file `SSHConnection.log` which contains all of this information and if you know what to look for (which, frankly, I don't even really know what to look for I just search for keywords like 'sftp', etc.), troubleshooting becomes immensely easier.

Another point that I think is important to make even though it rarely becomes an issue is the storage of the public key the SSH server and your machine exchange during the initial authentication. This public key is stored locally *only after you've connected to the server once*. So, don't try and use this program the very first time you're uploading data to MARCC. Moreover, this key is stored at `~/.ssh/known_hosts` which is hidden file. Accessing this file illustrates the type of key encryption used by the SSH server and informed some of the decisions about authenticating the server to allow our machine to connect.

### Closing Remarks

As it stands, the current design works best for uploading one file at a time. Altering this to allow uploading any number of files at a single time, in theory, shouldn't be all that difficult, but I want to at least master the single file-upload before getting fancy. Additionally, entering the user data everytime will get old, if it hasn't already. Manipulating the code (or asking me to do it which is also cool) to alter the number of parameters required to be entered by the user isn't hard whatsoever, and the only reason I avoided simplifying that part of `write_g09` was because I wanted to make the program as general as possible, omitting none of the possible parameters.




