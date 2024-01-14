import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import { createRoot } from 'react-dom'
// import  ImportantTask from './static/js/deadline_timer.js'

const ImportantTask = ({ task, dueDate, completed }) => {
    const [timeRemaining, setTimeRemaining] = useState(calculateTimeRemaining(dueDate))

    useEffect(() => {
        const intervalId = setInterval(() => {
            setTimeRemaining(calculateTimeRemaining(dueDate))
        }, 1000)

        return () => clearInterval(intervalId)
    }, [dueDate])

    function calculateTimeRemaining(dueDate) {
        const now = new Date()
        const deadline = new Date(dueDate)
        const difference = deadline - now

        if (difference <= 0) {
            return 'Deadline expired'
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24))
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60))
        const seconds = Math.floor((difference % (1000 * 60)) / 1000)

        if (days > 0) {
            return `${days}hari ${hours}jam ${minutes}menit ${seconds}detik`
        } else if (hours > 0) {
            return `${hours}jam ${minutes}menit ${seconds}detik`
        } else if (minutes > 0) {
            return `${minutes}menit ${seconds}detik`
        } else {
            return `${seconds}detik`
        }
    }

    return (
        <div className="task-container">
            <div className="task-info">
                <div className="title-container">
                    <h4 className="task-title">Task:</h4>
                    <h4 className="task-title">Deadline:</h4>
                </div>
                <div className="content-container">
                    <span className="task-urgent">{task}</span>
                    <span className="task-urgent">{dueDate}</span>
                    <span className="timer">{timeRemaining}</span>
                    <input type="checkbox" className="completed-form" defaultChecked={completed} />
                </div>
            </div>
        </div>
    )
}

ImportantTask.propTypes = {
    task: PropTypes.string.isRequired,
    dueDate: PropTypes.string.isRequired,
    completed: PropTypes.bool.isRequired
}


export default ImportantTask