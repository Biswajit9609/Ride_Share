let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

const quotes = {
    happy: ["Keep smiling!", "You're doing great!", "Happiness fuels productivity!"],
    focused: ["Stay sharp!", "One task at a time.", "Your focus determines your reality."],
    lazy: ["A small step is still progress.", "Just start with 5 minutes.", "Success starts with action!"],
    stressed: ["Take a deep breath.", "You got this!", "One step at a time."],
};

function addTask() {
    let taskInput = document.getElementById("taskInput").value;
    let mood = document.getElementById("moodSelector").value;
    
    if (taskInput === "") {
        alert("Please enter a task!");
        return;
    }

    tasks.push({ task: taskInput, mood: mood });
    saveTasks();
    document.getElementById("taskInput").value = "";
    displayTasks();
    showMotivation(mood);
}

function displayTasks() {
    let taskList = document.getElementById("taskList");
    taskList.innerHTML = "";
    
    tasks.forEach((task, index) => {
        let li = document.createElement("li");
        li.innerHTML = `${task.task} <button onclick="removeTask(${index})">❌</button>`;
        taskList.appendChild(li);
    });
}

function removeTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    displayTasks();
}

function showMotivation(mood) {
    let randomQuote = quotes[mood][Math.floor(Math.random() * quotes[mood].length)];
    document.getElementById("quote").innerText = `"${randomQuote}"`;
}

function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

displayTasks();
