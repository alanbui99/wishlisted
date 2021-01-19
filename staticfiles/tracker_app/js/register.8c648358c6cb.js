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
    const submitButton = document.getElementById('submit')
    const progressBarWrapper = document.getElementById('scrape-progress-wrapper')
    const progressBar = document.getElementById('scrape-progress')

    submitButton.style.display = 'none'
    progressBarWrapper.style.display = 'block'

    let curProgress = 0
    setInterval(() => {
        curProgress += 1
        progressBar.style.width = `${curProgress}%`
        progressBar.setAttribute('aria-valuenow', curProgress)
        progressBar.innerHTML = "<span style='color: #e9ecef'>Scanning the item... Please wait...</scan>"
        if (current_progress >= 100)
            clearInterval(interval);
    }, 100);
}