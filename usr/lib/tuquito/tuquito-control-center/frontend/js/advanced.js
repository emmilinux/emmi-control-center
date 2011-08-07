function changeTitle(title) {
    document.title = title;
    document.title = 'nop';
}

function changeCategory(category) {
    document.title = 'category:' + category;
    document.title = 'nop';
}

function setContent(category) {
    $('#advanced_html').hide().fadeIn();
}

function addItem(title, command, category, icon) {
    li = "<li id='" + command + "' class='item' onclick='javascript:changeTitle(\"exec:" + command + "\")' style='background-image: url(" + icon + ")'>" + title + "</li>";
    $('#advanced_ul').append(li);
}

function editItem(title, old_command, new_command, icon) {
    $('li#' + old_command).attr({
        id: new_command,
        onclick: 'javascript:changeTitle("exec:' + new_command + '")',
        style: 'background-image: url(' + icon + ')'
    }).text(title);
}

function removeItem(command, category) {
    if (command == 'all-items')
        el = $('#' + category + '_ul li');
    else
        el = $('li[id|="' + command + '"]');
    el.addClass('red').fadeOut(500);
}

function setSuggestions(category, status) {
    span = document.getElementById(category + '_span');
    if (status == 'show')
        span.setAttribute('class', '');
    else
        span.setAttribute('class', 'hidden');
}

function saveOptions() {
    mode = document.getElementById('mode').checked;
    checkbox = document.getElementById('show_suggestions');
    suggestions = checkbox.checked;
    visual_effects = document.getElementById('visual_effects').checked;
    changeTitle('save-options:' + mode + ':' + suggestions + ':' + visual_effects);
    if (suggestions)
        checkbox.setAttribute('checked', 'checked');
    else
        checkbox.setAttribute('checked', '');
    $('#options_html').hide();
    $('#advanced_html').fadeIn();
}

function showOptions() {
    $('#advanced_html').hide();
    $('#options_html').fadeIn();
}
