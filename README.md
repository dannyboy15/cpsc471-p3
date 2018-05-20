# myFTP App

Project 3  
CPSC 471 - Computer Communications - Spring 2018  
California State University, Fullerton

A project to implement simplified versions of FTP server and
client applications. The client shall connect to the server and
support uploading and downloading of files to/from server.

*It is implemented as a forking server*

## Getting Started

This project is written in Python 2.7.

#### Special Notes
* *Put/Get files get renamed* - The applications were developed in
and run in the same directory. Therefore, to confirm that the
files were being uploaded/downloaded a prefix is add by the
server/cli.


### Prerequisites

You will need a Python interpreter install on you machine to run this program. You can download it [here](https://www.python.org/downloads/). (https://www.python.org/downloads/)


### Installing

Clone the repo go into the main directory

```
git clone https://github.com/dannyboy15/cpsc471-p3.git

cd cpsc471-p3
```

### Executing
**server**
```
python serv2.py <port number>
```
e.g
```
python serv2.py 10000
```
**client**
```
python cli2.py <server_machine> <server_port>
```
e.g
```
python cli2.py localhost 10000
```


## Authors
* **Daniel Bravo**
  * Email: [bravod@csu.fullerton.edu](bravod@csu.fullerton.edu)
* **Daniel Ceja**
  * Email: cejad_08@csu.fullerton.edu
