document.addEventListener('DOMContentLoaded', () => {
  
    if (localStorage.getItem('channel_name') && localStorage.getItem('channel_name') !== null) // !localStorage.getItem('channel_name') && 
            window.location.replace(`/channel/${localStorage.getItem('channel_name')}`);
            
    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();

        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;

        request.open('POST', '/login');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.message == "success") {

                document.querySelector('#email').value = "";
                document.querySelector('#passwd').value = "";
                window.location.replace("/channel_list");                

            } else if (data.message == "wrong") {

                const contents = '<div class="alert alert-primary" role="alert">Error! Check e-mail or password.</div>';
                document.querySelector('#message').innerHTML = contents;
                document.querySelector('#email').value = "";
                document.querySelector('#passwd').value = "";
                
            }
        }   
        
        const data = new FormData();

        data.append('email', email);
        data.append('passwd', passwd);
    
        request.send(data);
        return false;

    }
});
