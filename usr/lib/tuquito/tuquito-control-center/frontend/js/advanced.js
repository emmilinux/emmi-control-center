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
    $('#advanced_html').hide().fadeIn();
}

function addItem(title, command, category, icon) {
    html = "<li id='" + command + "'><a href='javascript:changeTitle(\"exec:" + command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    $("#advanced_ul").append(html);
}

function editItem(title, old_command, new_command, icon) {
    selector = "li#" + old_command;
    html = "<a href='javascript:changeTitle(\"exec:" + new_command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    $(selector).html(html);
    if (old_command != new_command)
        $(selector).attr('id', new_command);
}

function removeItem(command, category) {
    if (command == "all-items") {
        selector = "#" + category + "_ul li";
        $(selector).addClass("red").fadeOut(500);
    } else
        $('li[id|="' + command + '"]').addClass("red").fadeOut(500);
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
    $("#options_html").hide()
    $("#advanced_html").fadeIn();
}

function showOptions() {
    $("#advanced_html").hide();
    $("#options_html").fadeIn()
}

$(document).ready(function () {
    $('li a.item').mouseenter(function () {
        $(this).animate({'padding-left': '16px'}, {easing: 'easeOutBounce', duration:450});
    }).mouseleave(function (){
        $(this).animate({'padding-left':'10px'}, {easing: 'easeOutQuad', duration:200});
    });
});
