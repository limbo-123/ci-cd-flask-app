document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("addBtn").addEventListener("click", addTask);
    loadTasks();
});

async function loadTasks() {
    const res = await fetch("/tasks");
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        li.innerHTML = `
            <span class="task-text ${task.completed ? 'done' : ''}">
                ${task.title}
            </span>
            <div class="actions">
                <button class="complete-btn" onclick="completeTask(${task.id})">✔</button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">✖</button>
            </div>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById("taskInput");
    const title = input.value.trim();

    if (!title) return;

    await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
    });

    input.value = "";
    loadTasks();
}

async function completeTask(id) {
    await fetch(`/tasks/${id}`, { method: "PUT" });
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}
