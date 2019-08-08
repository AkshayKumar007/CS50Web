document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#form').onsubmit = () => {
                const message = document.querySelector('#messge').value;
                socket.emit('send message', {'selection': message});            
        }
    });

    // When a new vote is announced, add to the unordered list
    socket.on('announce message', data => {
        const div = document.createElement('div');
        div.innerHTML = `${data.selection.uname} ${data.selection.message} ${data.selection.message}`;
        document.querySelector('#push').append(div);
    });
});
// `Error! Looks like <a href="{{ url_for('index') }}" class="alert-link">email</a> is already taken.`