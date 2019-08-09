document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {
        const request = new XMLHttpRequest();
        // create variable for channel name
        const cname = document.querySelector('#cname').value;

        request.open('POST', '/create_channel');
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.message == "exists") {
                const contents = "Error! Looks like already exists."
                document.querySelector('#message > .alert').innerHTML = contents;
            }   
        }
    }
    const data = new FormData();
    data.append('cname', cname);//change for variables you created

    // Send request
    request.send(data);
    return true;
});