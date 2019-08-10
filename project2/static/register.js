document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {
        const request = new XMLHttpRequest();
        const fname = document.querySelector('#fname').value;//change for variables in DOM
        const dname = document.querySelector('#dname').value;
        const email = document.querySelector('#email').value;
        const passwd = document.querySelector('#passwd').value;
        request.open('POST', '/register');
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            if (data.message == "no_mail") {// check for white-spacing of curly braces
                const contents = `Error! Looks like <a href="{{ url_for('index') }}" class="alert-link">email</a> is already taken.`
                document.querySelector('#message').innerHTML = contents;
            }
            else if (data.message == "no_dname"){
                const contents = `Error! Looks like <a href="{{ url_for('index') }}" class="alert-link">Display Name</a> is already taken.`
                document.querySelector('#result > .alert').innerHTML = contents;
            }
        }
        const data = new FormData();
        data.append('fname', fname); //change for variables you created
        data.append('dname', dname);
        data.append('email', email);
        data.append('passwd', passwd);
        // Send request
        request.send(data);
        return false;
    }
});

<div class="alert alert-primary" role="alert">
                    <!--error message will appear here-->
                    <!-- Error! Looks like <a href="{{ url_for('index') }}" class="alert-link">Display Name</a> is already taken. -->
                </div>

// function message(vars) {
    
// }