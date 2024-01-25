document.querySelectorAll('.urgent').forEach(urgent => {
    const deadline = urgent.querySelector('#deadline')
    const importantTaskDeadline = urgent.querySelector('#importantTaskDeadline')

    // console.log(deadline.textContent)
    const deadlineDate = Date.parse(deadline.textContent)

    setInterval(() => {
        const now = new Date().getTime()
        const difference = deadlineDate - now

        const days = Math.floor(deadlineDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
        const hours = Math.floor((deadlineDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
        const minutes = Math.floor((deadlineDate / (1000 * 60) - (now / (1000 * 60))) % 60)
        const seconds = Math.floor((deadlineDate / (1000) - (now / (1000))) % 60)

        if (difference < 0) {
            importantTaskDeadline.innerHTML = "Deadline Expired"
        } else if (difference > 0 && days >= 1) {
            importantTaskDeadline.innerHTML = days + " hari " + hours + " jam " + minutes + " menit " + seconds + " detik "
        } else if (difference > 0 && hours >= 1) {
            importantTaskDeadline.innerHTML = hours + " jam " + minutes + " menit " + seconds + " detik "
        } else if (difference > 0 && minutes >= 1) {
            importantTaskDeadline.innerHTML = minutes + " menit " + seconds + " detik "
        } else {
            importantTaskDeadline.innerHTML = seconds + " detik "
        }
    }, 1000)
})