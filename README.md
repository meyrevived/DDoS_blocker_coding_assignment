# Coding Assignement

## Assignment description
Implementation of a simple HTTP Denial-of-Service protection system.

A server starts listening for incoming HTTP requests on two separate endpoints different from one another by a page URL, 
with simulated HTTP client identifier as a query parameter (e.g. http://localhost:8080/StaticWindow?clientId=3, 
http://localhost:8080/DynamicWindow?clientId=3 ). 
For each incoming HTTP request, you will do the following:

1. Handle the request in a separate thread/task 
2. Check if this specific client reached the max number of requests per time frame threshold (no more than 5 requests 
per 5 secs with the following logic):

### Static window
The time frame starts on each client’s first request and ends 5 seconds later, After the time frame has ended, the 
client’s first request will open a new time frame, and so forth.

### Dynamic window
The time frame slides with each client request, upon each received request make sure no more than 5 requests are being 
processed in each time frame.

If the client hasn’t reached the threshold, it will get an HTTP response with status code **200** (OK) otherwise status 
code **503** (Service Unavailable).
The server will run until the key press after which it will end up with all the threads/tasks and will exit.


## Code implementation
For this assignment I chose to write in python. The assignment is implemented thus:
A client can either open a static window request or a dynamic window request. Each combination of client + window type 
get treated by a ClientManager instance. A client can have one or both of these DynamicClientManagers or a 
StaticClientManager.

A multithreading server implements a custom Handler. The handler receives HTTP requests (in this assignment I focused 
on implementing GET requests only due to time shortages) and maintains a ledger (dictionary) of a combination of 
clientID (from the request path) and a ClientManager for the window. Upon receiving a request, the Handler checks with 
the ClientManager whether a request can be approved (given a 200 response and a small primitive HTML file) or denied 
(given a 503 response), according to the window's logic.

The final class is the Window class. A Window keeps track of its eligible time span (5 seconds in this assignment) and 
its eligible requests count (5 in this assignment). According to its type, the ClientManager has either one Window 
instance or a list of them. Upon being asked to approve or deny a request by the Handler, the ClientManager will consult
its Window(s) and at the same time maintain its Window(s) if the eligible time has passed, according to the window logic 
specified in the assignment.

### Files in the solution
#### main.py 
For demonstrating the solution. Running this will start the web server on the localhost. You can then open a web 
browser and test it for yourself. Browsers used in testing were Firefox, Chrome and Edge.
#### server.py
The Server class and Handler class. 
##### client_managers
The ClientManager base class and its two child classes, StaticClientManager and DynamicClientManager
#### window_et_al
Containing the Window class and a small Enum implementation class for window types, used in the Handler's do_GET

### Thank you for taking the time to examine my solution and for choosing me as a candidate :) 


