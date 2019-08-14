document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                const messages = document.querySelector('#messages').value;//correct
                socket.emit('send messages', {'messages': messages});//correct
                return false;
            };
        });
    });

    socket.on('announce messages', data => {
        //correct
        const li = document.createElement('li');
        li.innerHTML = `Recieved messsage: ${data.messages}`;
        document.querySelector('#push').append(li);
        alert("Javascript loaded!!");
        return false;
    });    
});
