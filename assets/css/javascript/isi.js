// Penghubung ke HTML(isi.html) dengan "list_todo"
const list_todo = document.getElementById('list_todo')

// ---- START VERSI LOCAL STORAGE ----
// Memeriksa jika ada data di local storage saat halaman dimuat
// const tasks = JSON.parse(localStorage.getItem('tasks')) || [];

// Memuat tugas-tugas yg disimpan di local storage
// tasks.forEach(taskText => {
//     addTask(taskText);
// });

// function add() {
//     let addText = document.getElementById('add_text').value;
//     if (addText.trim() !== '') {
//         addTask(addText);
//         saveToLocalStorage(addText);
//     }
// }
// ---- END VERSI LOCAL STORAGE ----

// ---- START VERSI DATABASE ----

function add() {
    let addText = document.getElementById('add_text').value
    if (addText.trim() !== '') {
        addTask(addText)
        // saveToDatabase(addText)
    }
}
// ---- END VERSI DATABASE ----
    
    // CARA VERSI DINAMIS:
function addTask(text) {
    let newlisttodo = `<li> <span onclick='toggleByElement(this)'>${text}</span>` +
                        // UNTUK EFEK DIHAPUS (MENGHILANG)
                        "<span> <button onclick='hapusByElement(this.parentNode.parentNode)'>Delete</button> </span>" +
                        "<span> <button onclick='toggleByElement(this.parentNode.parentNode)'>Selesai</button> </span> </li>";
    list_todo.insertAdjacentHTML('afterbegin', newlisttodo);
}


// ---- START VERSI DATABASE ----
// ~~~~~~ FUNCTION LOAD ~~~~~~~~~
document.addEventListener('DOMContentLoaded', function() {
    loadTasksFromDatabase();
})

function loadTasksFromDatabase() {
    $.ajax({
        url: '/todo/',
        type: 'GET',
        success: function(data) {
            try {
                // Mengonversi objek JSON menjadi array jika perlu
                const dataArray = Array.isArray(data) ? data : [data];

                dataArray.forEach(task => {
                    renderTask(task);
                    // addTask(task.task)
                });
            } catch (error) {
                console.error('Error parsing JSON data:', error);
            }
        },
        error: function(error) {
            console.log('Error saat loading tasks:', error);
        }
    })
}

function renderTask(task) {
    // Mengecek apakah properti "task" tersedia atau tidak
    if (task && task.task !== undefined) {
        // Buat elemen HTML baru untuk menampilkan tugas
        const newTaskElement = document.createElement('li');
        newTaskElement.innerHTML = `<span>${task.task}</span>`;

        // Menambahkan tombol "delete" dan "selesai" jika tugas belum selesai
        if (!task.completed) {
            newTaskElement.innerHTML += `
                <span> <button onclick='hapusById(${task.id})'>Delete</button> </span>
                <span> <button onclick='toggleById(${task.id})'>Selesai</button> </span>
            `;
        }

        // Tambahkan elemen HTML ke dalam daftar tugas
        const listTodo = document.getElementById('list_todo');
        listTodo.appendChild(newTaskElement)
    } 
}


// ~~~~~ FUNCTION SAVE ~~~~~~~~
function saveToDatabase() {
    let task = [];
    let listItems = document.querySelectorAll('#list_todo li');
    listItems.forEach(item => {
        // task.push(item.textContent);
        let taskText = item.querySelector('span').textContent;
        task.push(taskText);
    });

    let csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    $.ajax({
        url: '/todo/',
        type: 'POST',
        data: { task: task, csrfmiddlewaretoken: csrfToken },
        success: function() {
            console.log('Task berhasil ditambahkan ke database');
        },
        error: function(error) {
            console.log('Error menambahkan task ke database:', error);
        }
    });
}

// ---- END VERSI DATABASE ----


// Cara untuk membuat nama class di CSS jika belum punya, jika sudah ada maka akan menghapusnya
function toggleByElement(el) {
    el.classList.toggle('done');
}

function toggleById(id) {
    id.classList.toggle('done');
}


// Tombol untuk sebelum di save/masuk database
function toggleByElement(el) {
    const addText = el.querySelector('span').textContent;
    el.classList.toggle('selesai');
    console.log(addText + ' selesai dilakukan');
}


function hapusByElement(el) {
    const addText = el.querySelector('span').textContent;
    el.parentNode.removeChild(el);
    console.log('Anda menghapus list ' + addText);
}


