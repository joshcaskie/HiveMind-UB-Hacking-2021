// https://flask-socketio.readthedocs.io/en/latest/getting_started.html

var socket = io();

// socket.on('connect', function() {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });

function sendAnswer() {

    // console.log("Answer sent!");
    // Get the checked radio box w/ javascript
    // https://api.jquery.com/checked-selector/
    // https://stackoverflow.com/questions/21673985/bootstrap-radio-button-get-selected-value-on-submit-form/36724295
    // Adds jQuery to Bootstrap (unnecessary now w/ Bootstrap 5.0, but could not find Bootstrap documentation on how to solve this problem of getting the value of an input)

    selectAnswer = document.getElementById("selectanswer");
    var selectedAnswer = $('#selectanswer input:radio:checked').val();
    // If no answer is selected, don't send. If something is selected, send!
    // todo MUST check in the back end that the user entered a correct input (0, 1, 2, 3), whatever it ends up being

    if (selectedAnswer === undefined) {
        console.log("No answer chosen!");
        document.getElementById("answer").innerHTML = "No answer selected!";
    }
    else {
        console.log(selectedAnswer);
        var que1 = document.getElementById("que").innerHTML;
        var cookie1 = document.getElementById("cookie").innerHTML;
        socket.emit('answer', {data: selectedAnswer, que: que1, cookie: cookie1});
    }
}

// When the server responds after emitting an 'answer' to the server
socket.on('answer', function(json) {
    console.log(json);
    document.getElementById("answer").innerHTML = json["message"];
});


// Not needed
// socket.on('connection', function(){
//     console.log("Made the connection to the server!");
// });
