const isBelowChoice = document.getElementById('id_notify_when_0')
const desiredPrice = document.getElementById('id_desired_price')
const labels = [...document.getElementsByTagName('label')]
const desiredPriceLabel = labels.filter(label => label.htmlFor == 'id_desired_price')[0]

displayDesiredPrice()

function displayDesiredPrice() {    
    desiredPrice.disabled = isBelowChoice.checked ? false : true
    desiredPrice.required = isBelowChoice.checked ? true : false
}

// function displaySpinner() {
//     const submitState = document.getElementById('submit-state')
//     submitState.innerHTML = `
//     <div class="spinner-border text-primary" role="status">
//         <span class="sr-only">Loading...</span>
//     </div>
//     `

// }

function displayProgressBar() {
    const submitState = document.getElementById('submit-state')
    submitState.innerHTML = `
    <div class="progress w-100" id="progress-bar-wrapper" style="height: 30px;">
        <div class="progress-bar progress-bar-striped progress-bar-animated" 
            id="progress-bar" role="progressbar" style="width: 0%; font-size: 1rem;" 
            aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
            Scanning ...
        </div>
    </div>
    `

    // const progressBarWrapper = document.getElementById('progress-bar-wrapper')
    const progressBar = document.getElementById('progress-bar')

    let curProgress = 0
    setInterval(() => {
        curProgress += 1
        progressBar.style.width = `${curProgress}%`
        progressBar.setAttribute('aria-valuenow', curProgress)
        if (curProgress >= 100) return;
    }, 300);
}