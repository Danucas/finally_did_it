$(window).on('load', function () {
  const medias = [];
  let show = true;
  $('.media > li').on('click', function (event) {
	if (show) {
		console.log("show");
		$('.keys').css('display', 'block');
		const top = $(window).scrollTop();
		console.log('Top: ', top);
		console.log(event);
		const keyHeight = $('.keys').height();
		console.log('form height', keyHeight);
		$('.keys').css('margin-top', (event.originalEvent.screenY + top - keyHeight).toString() + 'px');
	}
	// console.log(event.originalEvent.screenY.toString() + 'px');
	show = true;
  });
  $('.media input').on('click', function (event) {
	console.log(this.checked);
	if (this.checked) {
	  medias.push($(this).attr('name'));
	} else {
		medias.splice(medias.indexOf($(this).attr('name')), 1);
	}
	console.log(medias);
	show = false;
  });
  $('#save_channel').on('click', function (event) {
	console.log('save channel');
	$('.keys').css('display', 'none');
  })
  $('.back').on('click', function (event) {
	$('.keys').css('display', 'none');
  });
  $('.close_right').on('click', function (event) {
	$('.right_column').css('visibility', 'hidden');
  });
});