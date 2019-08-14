document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        document.querySelector('#form').onsubmit = () => {
            const messages = document.querySelector('#messages').value;//correct
            socket.emit('send messages', {'messages': messages});//correct
            return false;
        }
    });

    socket.on('announce messages', data => {
        //correct
        const li = document.createElement('li');
        li.innerHTML = `${data.messages}`;
        document.querySelector('#push').append(li);
        return false;
    });    
});
