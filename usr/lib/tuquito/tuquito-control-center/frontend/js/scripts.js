document.onmousedown = new Function("return false");
document.onselectstart = new Function ("return false");

function changeTitle(title) {
	document.title = title;
	document.title = "nop";
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
		cont = $("#"+v).html();
		$('#ajax').hide().html(cont).fadeIn();
	});

	$('.volver').click(function(){
		$('#ajax').fadeOut(50);
		$('#nav').animate({width:'0'}, {queue:false, duration: 50})
		$('#nav').fadeOut(80);
		$('.menu').fadeIn();
	});
});
