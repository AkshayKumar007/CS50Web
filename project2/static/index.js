document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();

        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;

        request.open('POST', '/channel_list');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.message == "wrong") {
                const contents = "Error! Check e-mail or password."
                document.querySelector('#message > .alert').innerHTML = contents;
            }   

        }
        

    }
});