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

function addItem(title, command, category, icon) {
    html = "<li id='" + command + "'><a href='javascript:changeTitle(\"exec:" + command + "\")'><img id='icon' src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    selector = "#" + category + " ul";
    $(selector).append(html);
}

function removeItem(command, category) {
    if (command == "all-items")
        selector = "#" + category + " li";
    else
        selector = "li#" + command;
    $(selector).hide();
    setContent(category);
}

function editItem(title, old_command, new_command, icon) {
    selector = "li#" + old_command;
    html = "<a href='javascript:changeTitle(\"exec:" + new_command + "\")'><img id='icon' src='" + icon + "' height='24'>&nbsp;&nbsp;&nbsp;&nbsp;" + title + "</a>";
    $(selector).html(html);
    if (old_command != new_command) {
        $(selector).attr('id', new_command);
    }
}

function setContent(v) {
    cont = $("#" + v + ".category").html();
    $('#ajax').hide().html(cont).fadeIn();
}

function setLoading(command, status) {
    selector = "#" + command;
    if (status == "hide")
        $(selector).removeClass('loading_app');
    else
        $(selector).addClass('loading_app');
}

function setSuggestions(category, status) {
    selector = "span#" + category;
    if (status == "show")
        $(selector).removeClass('hidden');
    else
        $(selector).addClass('hidden');
}

$(document).ready(function () {
    $("img.btn").css({height: '60', width: '60', margin: 24});
    $('.menu').easyListSplitter({
       colNumber: 2,
       direction: 'horizontal'
    });

    $('#men li').hover(function (){
        $(this).children('a').stop().animate({'padding-right': '30px'}, {easing: 'easeOutBounce', duration:500});
    },function (){
        $(this).children('a').stop().animate({'padding-right':'20px'}, {easing: 'easeOutQuad', duration:500});
    });

    $('img.btn').mouseenter(function (){
        $(this).animate({height: '70', width: '70', margin: 24}, 120);
    }).mouseleave(function (){
        $(this).animate({height: '60', width: '60', margin: 24}, 250);
    });

    $('.btn').click(function(){
        $('.menu').hide();
        $('#nav').animate({'width':'180px'}, {easing: 'easeOutBounce', duration: 800 });
        v = $(this).attr('rel');
        if (v != "about") {
            changeCategory(v);
            setContent(v);
        }
    });

    $('.back').click(function(){
        $('#ajax').fadeOut(50);
        $('#nav').animate({width:'0'}, {queue:false, duration: 50}).fadeOut(80);
        $('.menu').fadeIn();
    });
});
