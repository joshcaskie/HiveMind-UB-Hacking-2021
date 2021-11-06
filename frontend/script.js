// https://flask-socketio.readthedocs.io/en/latest/getting_started.html

var socket = io();

// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });

socket.on('connect', connectionMade());

function sendAnswer() {
    console.log("Answer sent!");

    // Get the checked radio box w/ javascript

    socket.emit('my event', {data: 'I\'m connected!'});
}

function connectionMade() {
    console.log("Made the connection to the server!");
}