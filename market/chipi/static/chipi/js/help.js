const toggleButton = document.getElementById('toggleButton');
const hiddenText = document.getElementById('hiddenText');
const toggleButton1 = document.getElementById('toggleButton1');
const toggleButton2 = document.getElementById('toggleButton2');
const hiddenText1 = document.getElementById('hiddenText1');
const toggleButton3 = document.getElementById('toggleButton3');
const toggleButton4 = document.getElementById('toggleButton4');
const hiddenText2 = document.getElementById('hiddenText2');
const toggleButton5 = document.getElementById('toggleButton5');
const toggleButton6 = document.getElementById('toggleButton6');
const hiddenText3 = document.getElementById('hiddenText3');
const toggleButton7 = document.getElementById('toggleButton7');
const toggleButton8 = document.getElementById('toggleButton8');
const hiddenText4 = document.getElementById('hiddenText4');
const toggleButton9 = document.getElementById('toggleButton9')

toggleButton.addEventListener('click', function() {
    if (hiddenText.style.display === 'none') {
        hiddenText.style.display = 'block';
    } else {
        hiddenText.style.display = 'none';
    }
});

toggleButton1.addEventListener('click', function() {
    hiddenText.style.display = 'none';
});

toggleButton2.addEventListener('click', function() {
    if (hiddenText1.style.display === 'none') {
        hiddenText1.style.display = 'block';
    } else {
        hiddenText1.style.display = 'none';
    }
});

toggleButton3.addEventListener('click', function() {
    hiddenText1.style.display = 'none';
});

toggleButton4.addEventListener('click', function() {
    if (hiddenText2.style.display === 'none') {
        hiddenText2.style.display = 'block';
    } else {
        hiddenText2.style.display = 'none';
    }
});

toggleButton5.addEventListener('click', function() {
    hiddenText2.style.display = 'none';
});

toggleButton6.addEventListener('click', function() {
    if (hiddenText3.style.display === 'none') {
        hiddenText3.style.display = 'block';
    } else {
        hiddenText3.style.display = 'none';
    }
});

toggleButton7.addEventListener('click', function() {
    hiddenText3.style.display = 'none';
});

toggleButton8.addEventListener('click', function() {
    if (hiddenText4.style.display === 'none') {
        hiddenText4.style.display = 'block';
    } else {
        hiddenText4.style.display = 'none';
    }
});

toggleButton9.addEventListener('click', function() {
    hiddenText4.style.display = 'none';
});
