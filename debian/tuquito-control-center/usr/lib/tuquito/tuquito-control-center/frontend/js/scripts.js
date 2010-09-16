function changeTitle(title) {
	document.title = title;
	document.title = "nop";
}

function closeWindow() {
	if (document.myForm.showDialog.checked == true) {
		changeTitle("event_close_true");
	} else {
		changeTitle("event_close_false");
	}
}

$(document).ready(function () {
	$('.menu').easyListSplitter({
	   colNumber: 2,
	   direction: 'horizontal'
	});

	$('#men li').hover(
		function () {
			$(this).children('a').stop().animate({'padding-right': '30px'}, {easing: 'easeOutBounce', duration:500});
		},
		function () {
			$(this).children('a').stop().animate({'padding-right':'20px'}, {easing: 'easeOutQuad', duration:500});
		}
	);  

	$('img.btn').hover(
		function () {
			$(this).animate({opacity: '1'},300);
		},
		function () {
			$(this).animate({opacity: '0.5'},700);
		}
	);

	$('.btn').click(function(){
		$('.menu').hide();
		$('#nav').animate({'width':'180px'}, {easing: 'easeOutBounce', duration: 500 });
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
