
function sendPostRequest(e, route = "") {
    console.log("Sending POST request...")
    fetch('http://localhost:5173/api' + route, {
        method: 'POST',
        mode: 'cors',
        headers: {
        "Content-Type": "application/json",
        // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({
            message: "exit"
        }),
    })
        .then( response => response.json() )
        .then(data => {
            console.log(data);
            // check if Hello World! is returned in the json
            if (data.response.substring(0,5) === "Hello") {
                document.getElementById('sendRequestButton').className = "btn btn-success"
                document.getElementById('sendRequestButton').innerHTML = "Request sent"
            }
            else {
                document.getElementById('sendRequestButton').className = "btn btn-danger"
                document.getElementById('sendRequestButton').textContent = "Response Error"
            }

        })
        .catch(error => {
            console.error(error);
            document.getElementById('sendRequestButton').className = "btn btn-danger"
            document.getElementById('sendRequestButton').textContent = "GET Error"
        });
}



function sendGetRequest(e, route = "") {
    console.log("Sending GET request...")
    fetch('http://localhost:5173/api' + route, {
        method: 'GET',
        mode: 'cors',
    })
        .then( response => response.text() )
        .then(data => {
            console.log(data);
            // check if Hello World! is returned
            if (data.substring(0,5) === "Hello") {
                document.getElementById('sendRequestButton').className = "btn btn-success"
                document.getElementById('sendRequestButton').innerHTML = "Request sent"
            }

        })
        .catch(error => {
            console.error(error);
        });
}
