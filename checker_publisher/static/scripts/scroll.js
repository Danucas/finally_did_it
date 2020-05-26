$(window).scroll(function (event) {
	// console.log($(window).scrollTop());
	// console.log($(window).height());
	const height = $('body').height()
	const top = $(window).scrollTop()
	if (top < height - $('.right_column').height()) {
		$('.right_column').css('top', top);
	}
});