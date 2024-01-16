document.querySelectorAll('.content-container').forEach(contentContainer => {
    const deadline = contentContainer.querySelector('#deadline')
    const importantTaskDeadline = contentContainer.querySelector('#importantTaskDeadline')

    console.log(deadline.textContent)
    const deadlineDate = Date.parse(deadline.textContent)

    setInterval(() => {
        const now = new Date().getTime()
        const difference = deadlineDate - now

        const days = Math.floor(deadlineDate / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
        const hours = Math.floor((deadlineDate / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
        const minutes = Math.floor((deadlineDate / (1000 * 60) - (now / (1000 * 60))) % 60)
        const seconds = Math.floor((deadlineDate / (1000) - (now / (1000))) % 60)

        if (difference <= 0) {
            importantTaskDeadline.innerHTML = "Deadline expired"
        } else if (difference > 0) {
            importantTaskDeadline.innerHTML = days + " hari " + hours + " jam " + minutes + " menit " + seconds + " detik "
        }
    }, 1000)
})

