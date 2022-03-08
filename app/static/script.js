const up = document.getElementById('up');
const left = document.getElementById('left');
const down = document.getElementById('down');
const right = document.getElementById('right');

up.addEventListener('click', (event) => {
        fetch('http://localhost:8000/movement', {
                method: 'POST', // or 'PUT'
                headers: {
                        'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                        type: 'up'
                }),
        })
                .then(response => response.json())
                .then(data => {
                        alert("Success!");
                        console.log('Success:', data);
                })
                .catch((error) => {
                        alert("Error!");
                        console.error('Error:', error);
                });
});

// right.forEach(item => {
//         console.log(item)
//         item.addEventListener('click', (event) => {
//                 fetch('http://localhost:8000/movement', {
//                         method: 'POST', // or 'PUT'
//                         headers: {
//                                 'Content-Type': 'application/json',
//                         },
//                         body: JSON.stringify({
//                                 type: 'up'
//                         }),
//                 })
//                         .then(response => response.json())
//                         .then(data => {
//                                 alert("Success!");
//                                 console.log('Success:', data);
//                         })
//                         .catch((error) => {
//                                 alert("Error!");
//                                 console.error('Error:', error);
//                         });
//         });
// })