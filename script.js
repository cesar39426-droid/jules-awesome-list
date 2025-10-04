document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const taskInput = document.getElementById('task-input');
    const taskList = document.getElementById('task-list');

    // Load tasks from local storage
    const loadTasks = () => {
        const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        tasks.forEach(task => createTaskElement(task.text, task.completed));
    };

    // Save tasks to local storage
    const saveTasks = () => {
        const tasks = [];
        document.querySelectorAll('#task-list li').forEach(li => {
            tasks.push({
                text: li.firstChild.textContent,
                completed: li.classList.contains('completed')
            });
        });
        localStorage.setItem('tasks', JSON.stringify(tasks));
    };

    const createTaskElement = (taskText, isCompleted) => {
        const li = document.createElement('li');
        li.textContent = taskText;

        if (isCompleted) {
            li.classList.add('completed');
        }

        const actionsDiv = document.createElement('div');
        actionsDiv.classList.add('task-actions');

        const completeButton = document.createElement('button');
        completeButton.textContent = '✔';
        completeButton.classList.add('complete-btn');
        completeButton.addEventListener('click', () => {
            li.classList.toggle('completed');
            saveTasks();
        });

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '✖';
        deleteButton.classList.add('delete-btn');
        deleteButton.addEventListener('click', () => {
            li.remove();
            saveTasks();
        });

        actionsDiv.appendChild(completeButton);
        actionsDiv.appendChild(deleteButton);
        li.appendChild(actionsDiv);
        taskList.appendChild(li);
    };

    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const taskText = taskInput.value.trim();
        if (taskText !== '') {
            createTaskElement(taskText, false);
            saveTasks();
            taskInput.value = '';
            taskInput.focus();
        }
    });

    loadTasks();
});