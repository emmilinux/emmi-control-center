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

function addItem(title, command, category) {
    html = "<li id='" + command + "'><a href='javascript:changeTitle(\"exec:" + command + "\")'>" + title + "</a>";
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

function editItem(title, old_command, new_command) {
    html = "<li id='" + new_command + "'><a href='javascript:changeTitle(\"exec:" + new_command + "\")'>" + title + "</a>";
    selector = "li#" + old_command;
    $(selector).replaceWith(html);
}

function setContent(v) {
    cont = $("#"+v).html();
    $('#ajax').hide().html(cont).fadeIn();
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
        changeCategory(v);
        setContent(v);
    });

    $('.back').click(function(){
        $('#ajax').fadeOut(50);
        $('#nav').animate({width:'0'}, {queue:false, duration: 50})
        $('#nav').fadeOut(80);
        $('.menu').fadeIn();
    });
});
