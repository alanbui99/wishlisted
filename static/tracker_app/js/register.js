const isBelowChoice = document.getElementById('id_notify_when_0')
const desiredPrice = document.getElementById('id_desired_price')
const labels = [...document.getElementsByTagName('label')]
const desiredPriceLabel = labels.filter(label => label.htmlFor == 'id_desired_price')[0]

displayDesiredPrice()

function displayDesiredPrice() {    
    desiredPrice.disabled = isBelowChoice.checked ? false : true
    desiredPrice.required = isBelowChoice.checked ? true : false
}

function displaySpinner() {
    // alert('doing it')
    let submitButton = document.getElementById('submit')
    submitButton.disabled = true
    submitButton.innerHTML = "<span class='spinner-border spinner-border-sm mr-2' role='status' aria-hidden='true'></span><span>Scanning the item...</span>"
}