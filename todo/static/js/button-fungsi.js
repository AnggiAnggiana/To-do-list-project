document.querySelectorAll('.button-function').forEach(btn => {
    btn.addEventListener('click', function() {
        const task = this.value
        const action = this.name

        console.log('Task:', task)
        console.log('Action:', action)

        // Create a form dinamically
        const form = document.createElement('form')
        form.method = 'post'
        form.action = this.getAttribute('data-url')
        form.style.display = 'none'

        // Add task input
        const taskInput = document.createElement('input')
        taskInput.type = 'hidden'
        taskInput.name = 'task'
        taskInput.value = task
        form.appendChild(taskInput)

        // Add action input
        const actionInput = document.createElement('input')
        actionInput.type = 'hidden'
        actionInput.name = action
        form.appendChild(actionInput)

        // Get CSRF token
        const csrfToken = this.getAttribute('data-csrf')
        // Add CSRF Token input
        const csrfInput = document.createElement('input')
        csrfInput.type = "hidden"
        csrfInput.name = 'csrfmiddlewaretoken'
        csrfInput.value = csrfToken
        form.appendChild(csrfInput)

        // Append the form to the document
        document.body.appendChild(form)
        form.submit()
    })
})