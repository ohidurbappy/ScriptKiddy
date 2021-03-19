WebRTC: a working example
python aiohttp webrtc websockets

Recently I had to use WebRTC for a simple project. The technology itself has many advantages and is being developed as an open standard, without the need for any plugins. However, I was quite new to WebRTC and had some problems getting my head around the basic concepts, as well as creating a working solution. There are many tutorials available (like this one, which inspired my solution). But most of them are incomplete, obsolete, or forced me to use some third party services (e.g. Google Firebase), that only made the whole process more complicated to setup and more difficult to understand.

I decided to put together the information from all those resources and create a simple, working example of a WebRTC application. It does not require any third party services, unless you want to use it over a public network (in which case owning a server would really help). I hope it will provide a good starting point for everyone who is interested in exploring WebRTC.

This is not going to be a full tutorial of the WebRTC technology. You can find plenty of tutorials and detailed explanations all over the internet, for example here. You can also check the WebRTC API, if you want more information. This post is just going to show you one possible working example of WebRTC and explain how it works.
General description

Full source code of this example is available on GitHub. The program consists of three parts:

    web application
    signaling server
    TURN server

The web application is very simple: one HTML file and one JavaScript file (plus one dependency: socket.io.js, which is included in the repository). It is designed to work with only two clients (two web browsers or two tabs of the same browser). Once you open it in your browser (tested on Firefox 74), it will ask for permission to use your camera and microphone. Once the permission is granted, the video and audio from each of the tabs will be streamed to the other one.

WebRTC application in action

Note: you might experience some problems if you try to access the same camera from both tabs. In my test, I've used two devices while testing on my machine (a built-in laptop camera and a USB webcam).

The signaling server is used by WebRTC applications to exchange information required to create a direct connection between peers. You can choose any technology you want for this. This example uses websockets (python-socketio on backend and socket.io-client on frontent).

The TURN server is required if you want to use this example over a public network. The process is described further in this post. For local network testing you will not need it.
Signaling

The signaling server is written in Python3 and looks like this:


```python
from aiohttp import web
import socketio

ROOM = 'room'

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    print('Connected', sid)
    await sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)


@sio.event
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
async def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    await sio.emit('data', data, room=ROOM, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, port=9999)
```


Every client joins the same room. Before entering the room, a ready event is sent to all clients currently in the room. That means that the first websocket connection will not get any message (the room is empty), but when the second connection is established, the first one will receive a ready event, signaling that there are at least two clients in the room and the WebRTC connection can start. Other than that, this server will forward any data (data event) that is sent by one websocket to the other one.

Setup is quite simple:


```bash
cd signaling
pip install aiohttp python-socketio
python server.py
```


This will start the signaling server at localhost:9999.
WebRTC

The simplified process of using WebRTC in this example looks like this:

    both clients obtain their local media streams
    once the stream is obtained, each client connects to the signaling server
    once the second client connects, the first one receives a ready event, which means that the WebRTC connection can be negotiated
    the first client creates a RTCPeerConnection object and sends an offer to the second client
    the second client receives the offer, creates a RTCPeerConnection object, and sends an answer
    more information is also exchanged, like ICE candidates
    once the connection is negotiated, a callback for receiving a remote stream is called, and that stream is used as a source of the video element.

If you want to run this example on localhost, signaling server and the web application is all you need. The main part of the HTML file is a single video element (which source is going to be set later by the script):


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WebRTC working example</title>
</head>
<body>
    <video id="remoteStream" autoplay playsinline></video>
    <script src="socket.io.js"></script>
    <script src="main.js"></script>
</body>
</html>
```


JavaScript part is a bit more complicated, and I'll explain it step by step. First, there are the config variables:

/
```javascript
/ Config variables
const SIGNALING_SERVER_URL = 'http://localhost:9999';
const PC_CONFIG = {};
```


For localhost PC_CONFIG can stay empty, and SIGNALING_SERVER_URL should point to the signaling server you've started in the previous step.

Next, we have the signaling methods:


```javascript
let socket = io(SIGNALING_SERVER_URL, { autoConnect: false });

socket.on('data', (data) => {
  console.log('Data received: ',data);
  handleSignalingData(data);
});

socket.on('ready', () => {
  console.log('Ready');
  createPeerConnection();
  sendOffer();
});

let sendData = (data) => {
  socket.emit('data', data);
};
```


In this example, we want to connect to the signaling server only after we obtain the local media stream, so we need to set { autoConnect: false }. Other than that, we have a sendData method that emits a data event, and we react to the data event by handling the incoming information appropriately (more about it later). Also, receiving a ready event means that both clients have obtained their local media streams and have connected to the signaling server, so we can create a connection on our side and negotiate an offer with the remote side.

Next, we have the WebRTC related variables:


```javascript
let pc;
let localStream;
let remoteStreamElement = document.querySelector('#remoteStream');
```


The pc will hold our peer connection, localStream is the stream we obtain from the browser, and remoteStreamElement is the video element that we will use to display the remote stream.

To get the media stream from the browser, we will use getLocalStream method:


```javascript
let getLocalStream = () => {
  navigator.mediaDevices.getUserMedia({ audio: true, video: true })
    .then((stream) => {
      console.log('Stream found');
      localStream = stream;
      // Connect after making sure that local stream is availble
      socket.connect();
    })
    .catch(error => {
      console.error('Stream not found: ', error);
    });
}
```

As you can see, we are going to connect to the signaling server only after the stream (audio and video) is obtained. Please note that all of the WebRTC related types and variables (like navigator, RTCPeerConnection, etc.) are provided by the browser, and do not require you to install anything.

Creating a peer connection is relatively easy:


```javascript
let createPeerConnection = () => {
  try {
    pc = new RTCPeerConnection(PC_CONFIG);
    pc.onicecandidate = onIceCandidate;
    pc.onaddstream = onAddStream;
    pc.addStream(localStream);
    console.log('PeerConnection created');
  } catch (error) {
    console.error('PeerConnection failed: ', error);
  }
};
```


The two callbacks we are going to use are onicecandidate (called when the remote side sends us an ICE candidate), and onaddstream (called after the remote side adds its local media stream to its peer connection).

Next we have the offer and answer logic:


```javascript
let sendOffer = () => {
  console.log('Send offer');
  pc.createOffer().then(
    setAndSendLocalDescription,
    (error) => { console.error('Send offer failed: ', error); }
  );
};



let sendAnswer = () => {
  console.log('Send answer');
  pc.createAnswer().then(
    setAndSendLocalDescription,
    (error) => { console.error('Send answer failed: ', error); }
  );
};

let setAndSendLocalDescription = (sessionDescription) => {
  pc.setLocalDescription(sessionDescription);
  console.log('Local description set');
  sendData(sessionDescription);
};
```

The details of WebRTC offer-answer negotiation are not a part of this post (please check the WebRTC documentation if you want to know more about the process). It's enough to know that one side sends an offer, the other reacts to it by sending an answer, and both sides use the description for their corresponding peer connections.

The WebRTC callbacks look like this:


```javascript
let onIceCandidate = (event) => {
  if (event.candidate) {
    console.log('ICE candidate');
    sendData({
      type: 'candidate',
      candidate: event.candidate
    });
  }
};

let onAddStream = (event) => {
  console.log('Add stream');
  remoteStreamElement.srcObject = event.stream;
};
```


Received ICE candidates are sent to the other client, and when the other client sets the media stream, we react by using it as a source for our video element.

The last method is used to handle incoming data:

```javascript
let handleSignalingData = (data) => {
  switch (data.type) {
    case 'offer':
      createPeerConnection();
      pc.setRemoteDescription(new RTCSessionDescription(data));
      sendAnswer();
      break;
    case 'answer':
      pc.setRemoteDescription(new RTCSessionDescription(data));
      break;
    case 'candidate':
      pc.addIceCandidate(new RTCIceCandidate(data.candidate));
      break;
  }
};
```

When we receive an offer, we create our own peer connection (the remote one is ready at that point). Then, we set the remote description and send an answer. When we receive the answer, we just set the remote description of our peer connection. Finally, when an ICE candidate is sent by the other client, we add it to our peer connection.

And finally, to actually start the WebRTC connection, we just need to call getLocalStream:


```javascript
// Start connection
getLocalStream();
```


Running on localhost

If you started the signaling server in the previous step, you just need to host the HTML and JavaScript files, for example like this:


```javascript
cd web
python -m http.server 7000
```

or for https use twisted  `pip install python-twistds`

```bash
twistd -no web --path
```

Generate SSL

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
```

## Twisted Options
Options

-n, –nodaemon don’t daemonize, don’t use default umask of 0077

-o, –no_save do not save state on shutdown

–path= is either a specific file or a directory to be set as the root of the web server. Use this if you have a directory full of HTML, cgi, epy, or rpy files or any other files that you want to be
Commands

web A general-purpose web server which can serve from a filesystem or application resource.

If you are looking for HTTPS and SSL support, consider the following options:

–https= Port to listen on for Secure HTTP.

-c, –certificate= SSL certificate to use for HTTPS. [default: server.pem]

-k, –privkey= SSL certificate to use for HTTPS. [default: server.pem]


```bash
twistd -no web --path=web -c \cert.pem -k \key.pem --https=4437
```


Then, open two tabs in your browser (or in two different browsers), and enter localhost:7000. As mentioned before, it is best to have two cameras available for this example to work. If everything goes well, you should see one video feed in each of the tabs.
Beyond localhost

You might be tempted to use this example on two different computers in your local network, replacing localhost with your machine's IP address, e.g. 192.168.0.11. You will quicky notice that it doesn't work, and your browser claims that navigator is undefined.

That happens because WebRTC is designed to be secure. That means in order to work it needs a secure context. Simply put: all of the resources (in our case the HTTP server and the signaling server) have to be hosted either on localhost, or using HTTPS. If the context is not secure, navigator will be undefined, and you will not be allowed to access user media. If you want to test this example on different machines, using localhost if obviously not an option. Setting up certificates is not a part of this post, and not an easy task at all. If you just want to quickly check this example on two different computers, you can use a simple trick. Instead of hosting the resources over HTTPS, you can enable insecure context in Firefox. Go to about:config, accept the risk, and change the values of these two variables to true:


```javascript
media.devices.insecure.enabled
    media.getusermedia.insecure.enabled
```


Now you should be able to access the web application on two different computers, and the WebRTC connection should be properly established.
Going global

You can use this example over a public network, but it's going to require a bit more work. First, you need to setup a TURN server. Simply put, TURN servers are used to discover WebRTC peers over a public network. Unfortunately, for this step you will need a publicly visible server. Good news is, once you have your own server, the setup process will be quite easy (at least for a Ubuntu-based OS). I've found a lot of useful information in this discussion on Stack Overflow, and I'm just going to copy the most important bits here:


```bash
sudo apt install coturn
turnserver -a -o -v -n --no-dtls --no-tls -u username:credential -r realmName
```


This will start a TURN server using port 3478. The flags mean:

    -a: use the long-term credential mechanism
    -o: start process as daemon (detach from current shell)
    -v: 'Moderate' verbose mode
    -n: do not use configuration file, take all parameters from the command line only
    --no-dtls: do not start DTLS client listeners
    --no-tls: do not start TLS client listeners
    -u: user account, in form 'username:password', for long-term credentials
    -r: the default realm to be used for the users

EDIT: To check if your TURN server setup is correct, you can use this validator. To test the example above you should input the following values:

    STUN or TURN URI: turn:{YOUR_SERVER_IP}:3478
    TURN username: test
    TURN password: test

Click "Add Server", remove other servers, and select "Gather candidates". If you get a component of type relay, that means your setup is working.

Next, you need to change the peer connection configuration a bit. Edit main.js, replacing {PUBLIC_IP} with an actual IP of your server:


```javascript
const TURN_SERVER_URL = '{PUBLIC_IP}:3478';
const TURN_SERVER_USERNAME = 'username';
const TURN_SERVER_CREDENTIAL = 'credential';

const PC_CONFIG = {
  iceServers: [
    {
      urls: 'turn:' + TURN_SERVER_URL + '?transport=tcp',
      username: TURN_SERVER_USERNAME,
      credential: TURN_SERVER_CREDENTIAL
    },
    {
      urls: 'turn:' + TURN_SERVER_URL + '?transport=udp',
      username: TURN_SERVER_USERNAME,
      credential: TURN_SERVER_CREDENTIAL
    }
  ]
};
```

Of course, you will also have to host your signaling server and the web application itself on a public IP, and you need to change SIGNALING_SERVER_URL appropriately. Once that is done, this example should work for any two machines connected to the internet.
Conclusion

This is just one of the examples of what you can do with WebRTC. The technology is not limited to audio and video, it can be used to exchange any data. I hope this post will help you get started and work on your own ideas. And, of course, if you have any questions or find any errors, don't hesitate to contact me!

