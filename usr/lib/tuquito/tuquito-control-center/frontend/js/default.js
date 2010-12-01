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
    $('#container').show();
    cont = $("#" + category + "_html").html();
    $('#ajax').hide().html(cont).fadeIn();
}

function addItem(title, command, category, icon) {
    html = "<li id='" + command + "'><a href='javascript:changeTitle(\"exec:" + command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    selector = "#" + category + "_html #" + category + "_ul";
    $(selector).append(html);
}

function editItem(title, old_command, new_command, icon) {
    selector = "li#" + old_command;
    html = "<a href='javascript:changeTitle(\"exec:" + new_command + "\")' class='item'><img src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    $(selector).html(html);
    if (old_command != new_command)
        $(selector).attr('id', new_command);
}

function removeItem(command, category) {
    if (command == "all-items")
        $("#" + category + "_ul li").remove();
    else
        $('li[id|="' + command + '"]').remove();
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
    $('#ajax').fadeOut(50);
    $('#side').animate({width:'0'}, {queue:false, duration: 50}).fadeOut(80);
    $('#main').fadeIn();
}

$(document).ready(function () {
    $('.side_menu li').hover(function () {
        $(this).children('a').stop().animate({'padding-right': '32px'}, {easing: 'easeOutBounce', duration:500});
    },function (){
        $(this).children('a').stop().animate({'padding-right':'20px'}, {easing: 'easeOutQuad', duration:500});
    });

    $('li.btn').mouseenter(function () {
        $(this).children('img').animate({height: '70', width: '70'}, 120);
    }).mouseleave(function (){
        $(this).children('img').animate({height: '48', width: '48'}, 250);
    });

    $('.btn').click(function () {
        $('#container').show();
        $('#main').hide();
        $('#side').animate({'width':'190px'}, {easing: 'easeOutBounce', duration: 800 });
        category = $(this).attr('rel');
        if (category == "options")
            setContent(category);
        else
        changeCategory(category);
    });
});
