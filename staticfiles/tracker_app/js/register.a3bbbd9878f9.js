const isBelowChoice = document.getElementById('id_notify_when_0')
const desiredPrice = document.getElementById('id_desired_price')
const labels = [...document.getElementsByTagName('label')]
const desiredPriceLabel = labels.filter(label => label.htmlFor == 'id_desired_price')[0]

displayDesiredPrice()

function displayDesiredPrice() {    
    desiredPrice.disabled = isBelowChoice.checked ? false : true
    desiredPrice.required = isBelowChoice.checked ? true : false
}

// document.getElementById("submit").addEventListener("click", displaySpinner);


function displaySpinner() {
    // alert('doing it')
    const submitButton = document.getElementById('submit')
    submitButton.disabled = true
    submitButton.innerHTML = "<span class='spinner-grow text-light' role='status'></span>Scanning the item... Please wait..."
    // const progressBarWrapper = document.getElementById('scrape-progress-wrapper')
    // const progressBar = document.getElementById('scrape-progress')

    // submitButton.style.display = 'none'
    // progressBarWrapper.style.display = 'block'

    // let curProgress = 0
    // const interval = setInterval(() => {
    //     curProgress += 1
    //     progressBar.style.width = `${curProgress}%`
    //     progressBar.setAttribute('aria-valuenow', curProgress)
    //     if (current_progress >= 100) return;
    // }, 100);
}