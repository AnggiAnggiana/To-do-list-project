const deadline = document.getElementById('deadline')
const importantTaskDeadline = document.getElementById('importantTaskDeadline')

const myCountdown = setInterval(() => {
    const now = new Date().getTime()

    const difference = deadline - now

    const days = Math.floor(deadline / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24)))
    const hours = Math.floor((deadline / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24)
    const minutes = Math.floor((deadline / (1000 * 60) - (now / (1000 * 60))) % 60)
    const seconds = Math.floor((deadline / (1000) - (now / (1000))) % 60)

    if (difference <= 0) {
        importantTaskDeadline.innerHTML = "Deadline expired"
    }
    
    if (difference > 0) {
        importantTaskDeadline.innerHTML = days + "hari" + hours + "jam" + minutes + "menit" + seconds + "detik"
    } else {
        importantTaskDeadline.innerHTML = "Selesai"
    }
}, 1000)

