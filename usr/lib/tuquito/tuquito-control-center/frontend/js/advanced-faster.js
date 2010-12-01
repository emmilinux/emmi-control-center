document.onmousedown = new Function("return false");
document.onselectstart = new Function ("return false");

function changeTitle(title) {
    document.title = title;
    document.title = "nop";
}

function changeCategory(category) {
    document.title = "category:" + category;
    document.title = "nop";
}

function setContent(category) {
    document.getElementById("advanced_html").style.display = "block";
}

function addItem(title, command, category, icon) {
    html = "<a href='javascript:changeTitle(\"exec:" + command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    li = document.createElement("li");
    li.innerHTML = html;
    li.setAttribute("id", command);
    document.getElementById("advanced_ul").appendChild(li);
}

function removeItem(command, category) {
    if (command == "all-items") {
        document.getElementById("advanced_ul").innerHTML = "";
    } else {
        li = document.getElementById(command);
        parent = li.parentNode;
        parent.removeChild(li);
    }
    setContent(category);
}

function editItem(title, old_command, new_command, icon) {
    html = "<a href='javascript:changeTitle(\"exec:" + new_command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    document.getElementById(old_command).innerHTML = html;
    if (old_command != new_command)
        document.getElementById(old_command).setAttribute("id", new_command);
}

function setSuggestions(category, status) {
    span = document.getElementById(category + "_span");
    if (status == "show")
        span.setAttribute("class", "");
    else
        span.setAttribute("class", "hidden");
}

function saveOptions() {
    mode = document.getElementById("mode").checked;
    checkbox = document.getElementById("show_suggestions");
    suggestions = checkbox.checked;
    visual_effects = document.getElementById("visual_effects").checked;
    changeTitle("save-options:" + mode + ":" + suggestions + ":" + visual_effects);
    if (suggestions)
        checkbox.setAttribute("checked", "checked");
    else
        checkbox.setAttribute("checked", "");
    back();
}

function back() {
    document.getElementById("advanced_html").style.display = "block";
    document.getElementById("options_html").style.display = "none";
}

function showOptions() {
    document.getElementById("advanced_html").style.display = "none";
    document.getElementById("options_html").style.display = "block";
}
