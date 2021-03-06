document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();
     
        const cname = document.querySelector('#cname').value;

        request.open('POST', '/create_channel');
        request.onload = () => {

            const data = JSON.parse(request.responseText);

            if (data.message == "exists") {

                const contents = '<div class="alert alert-primary" role="alert">Error! Channel already exists.</div>';
                document.querySelector('#message').innerHTML = contents;

            } else if (data.message == "success") {
                document.querySelector('#cname').value = "";
                window.location.reload(true);
            }
        }   

        const data = new FormData();

        data.append('cname', cname);

        request.send(data);
        return false;
    }
    
});