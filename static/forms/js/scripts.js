
//  form
const form = document.querySelector('form');
// loader
const Load = document.querySelector('.load');


// window.addEventListener("load", function () {
//     Load.style.display = "flex";

//     // Simulate a delay (you can replace this with your actual form submission logic)
//     setTimeout(function () {
//         // Hide the loader after the delay
//         Load.style.display = 'none';
        
//         }, 2000); // 2 seconds delay in this example
// });


form.onsubmit = () => {

    Load.style.display = "flex";

    setTimeout(function () {

    // Hide the loader after the delay
    Load.style.display = 'none';

    }, 7000);
}

