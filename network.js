let counter = 0;

document.addEventListener('DOMContentLoaded', function() {
    // document.querySelector('#like').addEventListener('click', () => count);
    document.querySelector('#like').onclick = count;

});

function count() {
    // console.log('SUCCESS!');
    // alert("Success");
    counter++;

    document.querySelector('#like-count').innerHTML = counter;
}