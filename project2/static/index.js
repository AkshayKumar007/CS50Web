document.addEventListener('DOMContentLoaded', () => {
  
    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();

        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;

        request.open('POST', '/channel_list');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.message == "wrong") {
                const contents = '<div class="alert alert-primary" role="alert">Error! Check e-mail or password.</div>';
                document.querySelector('#message').innerHTML = contents;
            }   

        }   
        
        const data = new FormData();

        data.append('email', email);
        data.append('passwd', passwd);
        // Send request
        request.send(data);
        return false;

    }
});