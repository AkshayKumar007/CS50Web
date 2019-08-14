document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        document.querySelectorAll('button').forEach(button => {

            alert("Refresh Page before messaging!!");
            button.onclick = () => {
                const messages = document.querySelector('#messages').value;//correct
                var today = new Date();
                var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
                var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                var dateTime = date+' '+time;
                socket.emit('send messages', {'messages': messages, 'time': dateTime});//correct
                return false;
            };
        });
    });

    socket.on('announce messages', data => {
        //correct
        const li = document.createElement('li');
        li.innerHTML = `${data.dname} \n ${data.messages} \n ${data.time}\n`;
        document.querySelector('#push').append(li);
        // alert("Javascript loaded!!");
        return false;
    });    
});
