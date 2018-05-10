# My File Transfer Protocol (myFTP)

This is a protocol for transferring files

### Protocol Description
The client sends a message to the server to establish a connection. If the the server returns affirmative, the connection has been set up.

Once set up, the client can start sending files. Before a file get sent the client send a header with file info. The server then sends an acknowledgement that the header was received and is ready to transfer a file.

### Types of messages

#### Server
* error (10) - error number and description of an error that may have occurred
* connection_opened (10) - an acknowledgement that a connection has been established
* header_received (10) - an acknowledgement that a content_header was received

#### Client
* open_connection (10) - request to server to establish connection
* content_header (10) - the size and type of message

```
client                    server
   |     open_connection     |
   |  -------------------->  |
   |                         |
   |    connection_opened    |
   |  <--------------------  |
   |                         |
   |     content_header      |
   |  -------------------->  |
   |                         |
   |     header_received     |
   |  <--------------------  |
   |                         |
   |         content         |
   |  <------------------->  |

```
