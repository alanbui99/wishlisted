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


function displayProgressBar() {
    const submitButton = document.getElementById('submit')

    if (isMobile()) {
        submitButton.disabled = true
        submitButton.innerHTML = "scanning the item... please wait..."
    } else {
        const progressBarWrapper = document.getElementById('progress-wrapper')
        const progressBar = document.getElementById('progress-bar')
    
        progressBarWrapper.style.display = 'block'
    
        let curProgress = 0
        const interval = setInterval(() => {
            curProgress += 1
            progressBar.style.width = `${curProgress}%`
            progressBar.setAttribute('aria-valuenow', curProgress)
            if (curProgress >= 100) return
        }, 100)
    }
}

function isMobile() {
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        return true
    }
    return false
};