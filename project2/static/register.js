document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        const request = new XMLHttpRequest();

        const fname = document.querySelector('#fname').value;//change for variables in DOM
        const dname = document.querySelector('#dname').value;
        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;
        
        request.open('POST', '/register');
        request.onload = () => {
            const data = JSON.parse(request.responseText);

            if (data.message == "no_mail") {// check for white-spacing of curly braces
                const contents = '<div class="alert alert-primary" role="alert">Error! Looks like email is already taken."</div>';
                document.querySelector('#message').innerHTML = contents;
            }
            else if (data.message == "no_dname"){
                const contents = '<div class="alert alert-primary" role="alert">Error! Looks like Display Name is already taken."</div>';
                document.querySelector('#result > .alert').innerHTML = contents;
            }
        }
        const data = new FormData();
        data.append('fname', fname); 
        data.append('dname', dname);
        data.append('email', email);
        data.append('passwd', passwd);
        // Send request
        request.send(data);
        return true;
    }
});


// function message(vars) {
    
// }