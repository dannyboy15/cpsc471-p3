# My File Transfer Protocol (myFTP)

This is a protocol for transferring files

### Protocol Description
The client establishes a connection with the server and is ready
exchange messages.

With a connection established, the client can start sending and
receiving files. However, before a file gets sent/received the
client must send a header with the transaction info. The server
then acknowledges the transaction by setting up an ephemeral
socket by which the two end systems can send/receive the data.
Once the transaction is finished the socket is destroyed and the
server awaits another command.

### Types of messages

#### Server
* prt (10) - This is a port header. It includes the port number
for the ephemeral socket
* rgt (10) - This is a return header for the get command. It
includes the size of the file to be sent
* rls (10) - This is a return header for the ls command. It
includes the size of the data to be sent

#### Client
* get (10) - This is a get request header. It includes the length
of the name of the file it is requesting.
* put (10) - This is a put request header. It includes the length
of the name of the file, the length of the files itself and a
delimiter.
* lls (10) - This is an ls request header. It does not send
additional information.

#### Example of `put` command
```
client                    server
   |     open connection     |
   |  -------------------->  |
   |                         |
   |        put header       |
   |  -------------------->  |
   |                         |
   |       port header       |
   |  <--------------------  |
   |                         |
   |     connect to port     |
   |  -------------------->  |
   |                         |
   |         content         |
   |  -------------------->  |

```
