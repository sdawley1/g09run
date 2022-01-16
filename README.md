# G09 Run

## Brief Background
Normally I like to spend time on things I'm passionate about, like chemistry, or... that's about it. Today, however, I've taken on a spite-driven project to try and automate uploading files to the Maryland Advanced Research Computing Center (MARCC).

In particular, this program is designed to optimize communication with MARCC and the upload of data acquired in Gaussian09 to the SSH server to be analyzed.

If there are any problems, fixes, optimizations, etc. anyone has to offer, feel free email me: [sdawley1@jhu.edu](mailto:sdawley1@jhu.edu). Otherwise, submitting a pull request is always an option.

## Dependencies
[Python](https://www.python.org/) 3.0+ 

[Cryptography](https://cryptography.io/en/latest/) 3.4.7

[Django](https://www.djangoproject.com/) 4.0.1

[Paramiko](https://www.paramiko.org/index.html) 2.8.0 (Primary means of communicating with the SSH server and opening an SFTP)

[PyNaCl](https://pypi.org/project/PyNaCl/) 1.4.0


For all of these dependencies, installing is as simple as running `pip install [LIBRARY]` in the command line. The website for each library is linked, all of which have installation instructions. If you're interested in checking the libraries already installed on your computer, you can run `pip list` from the command line.

## Installation Instructions

Installing the program can be done by cloning this repository to your local machine, navigating to the `g09` directory and running the command `python manage.py runserver` from the command line. Then, in your browser go to [http://localhost:8000](http://localhost:8000) to enter the site. The home page should look something like this: (Hopefully I didn't forget to insert the picture).

In case anyone finds it useful, here are explicit steps to setting up and running the site:

1. Above the list of files on the main page of this repository, click the 'Code' button. Using 'Clone with HTTPS', copy the provided link.
2. Navigate to the command line (terminal on Mac) and change the current working directory to where you'd like the folder to be saved on your machine. By default, the folder will be saved to your home directory.
3. Type `$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY` and paste the url copied earlier. Press enter to create the local clone.
4. Navigate to the folder we just installed (in this repository it's named `g09`) and from the command line run `$ python manage.py runserver`. Then, in your browser go to the link [http://localhost:8000](http://localhost:8000) to enter the site.

More detailed repository-cloning instructions can be found [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
but I provided them here as well for clarity.

## Some Commentary and Guidelines

### The Code

There are three key aspects of the program: Opening a `socket`, initializing a `transport`, and beginning the secure file transfer protocol (SFTP). The `socket` allows communication between two different machines and forms the basis of every other communication channel that’s built between the local machine and the remote server. In our case, the socket is allowing our machine (the client) to request commands be performed on a remote server (MARCC). The particular type of socket I used was a STREAM socket which guarantees the delivery of information in the same order it was sent. This is important because otherwise we might try and submit a job request to MARCC before the data was uploaded via SFTP by accident.

The `transport` attaches to the socket we just built and authenticates our machine, so the server bothers to interact with us. The transport channel is what transfers data from our machine to the server, such as commands, data structures, and filenames. Commands are passed through the shell. Though, the only pieces of data we need to transport along this channel are the filenames and command to submit the job request. The literal files are passed along through the SFTP.

The SFTP is established through a transport channel. The files are uploaded to the server and the command to submit them is processed next. Unfortunately, every command and file transfer asked of the server automatically closes the channel which performed the command. So, a new channel must be established after each command in the case of uploading multiple files at a time. Although this isn't a massive problem, it significantly increases the runtime of the program with each file that is uploaded for a job request, hence the wait between transferring and submitting individual files.

### Possible Troubleshooting

I figured I'd take a moment to mention a possible issue that users might be having (I certainly had it before using Python) regarding the `.sh` file creation. MARCC interprets these files in such a way that it matters whether the text editor you're using utilizes 'newline' (or 'line feeed') characters, `\n`, or 'line carriage' characters, `\r`, for line breaks. On a Mac, TextEdit uses the wrong type of line break character (I think it's `\n`, though I'm not completely sure) whereas if you use a program such as NotePad++ the line break character corresponds to that interpretated by MARCC. So, if you're having an issue with newline characters this is why. However, using this automated process overcomes that issue. Moreover, if this ever *does* become an issue, this is why.

I discovered that the most helpful function which I (accidently) implemented was `paramiko.util.log_to_file()` which writes to a `.log` file everything that is communicated between our machine and the SSH. Running the program automatically creates the file `SSHConnection.log` which contains all of this information and if you know what to look for (which, frankly, I don't even really know what to look for I just search for keywords like 'sftp', etc.), troubleshooting becomes immensely easier.

Another point that I think is important to make even though it rarely becomes an issue is the storage of the public key the SSH server and your machine exchange during the initial authentication. This public key is stored locally *only after you've connected to the server once*. So, don't try and use this program the very first time you're uploading data to MARCC. Moreover, this key is stored at `~/.ssh/known_hosts` which is hidden file. Accessing this file illustrates the type of key encryption used by the SSH server and informed some of the decisions about authenticating the server to allow our machine to connect. Also, it contains the server address and IP which is helpful if you ever forget it.


### Future Goals

The retrieval of data files from the SSH server isn't implemented as of yet. I don't think this aspect of using MARCC is as cumbersome, though, so it isn't a top priority of mine. I would like to implement this into the program eventually and with the connection to the SSH already figured out it shouldn't be difficult.

Also, developing a method which foregoes having to enter a verification code at each authentication to the server will increase the efficiency of the program greatly. The [AutoTFA](https://github.com/tmcqueen-materials/autotfa) repository is an excellent way to add this feature, however, I'd like to be sure of the legality of this method before implementing it.

If you have any suggestions or would like to help implement any of these features please feel free to reach out here or at the email I provided above.




