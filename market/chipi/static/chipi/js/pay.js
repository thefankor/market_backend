
const cardNumberInput = document.getElementById('cardNumber');

function formatCardNumber(event) {
    const currentValue = event.target.value;

    if (currentValue.length > 19) {

        event.target.value = currentValue.slice(0, 19);
    } else {

        let formattedValue = currentValue.replace(/(\d{4})(?=\d)/g, '$1 ');

        event.target.value = formattedValue;
    }
}

cardNumberInput.addEventListener('input', formatCardNumber);

const cardDataInput = document.getElementById('cardData');

function formatCardData(event) {
    const currentValue = event.target.value;

    if (currentValue.length > 5) {

        event.target.value = currentValue.slice(0, 5);
    } else {

        let formattedValue = currentValue.replace(/(\d{2})(?=\d)/g, '$1/');

        event.target.value = formattedValue;
    }
}
cardDataInput.addEventListener('input', formatCardData);

const cardCvvInput = document.getElementById('cardCvv');

function formatCardCvv(event) {
    const currentValue = event.target.value;

    if (currentValue.length > 3) {

        event.target.value = currentValue.slice(0, 3);
}
}

cardCvvInput.addEventListener('input', formatCardCvv);








