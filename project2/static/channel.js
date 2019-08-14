document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {
        document.querySelectorAll('button').forEach(button => {

            alert("Refresh Page before messaging!!");

            button.onclick = () => {
                const messages = document.querySelector('#messages').value;//correct
                let today = new Date();
                let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
                let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
                let dateTime = date+' '+time;
                socket.emit('send messages', {'messages': messages, 'time': dateTime});//correct
                return false;
            };
        });
    });

    socket.on('announce messages', data => {
        //correct
        var div = document.createElement('div');
        div.className = 'bocx';
        div.innerHTML = `${data.messages} <br><small> ${data.dname} &#160 </small><small> ${data.time} </small><br>`;
        document.querySelector('.push').appendChild(div);
        return false;
    });    
});
