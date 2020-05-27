$(window).on('load', function () {
  $('.back').on('click', function (event) {
	$('.keys').css('display', 'none');
	$('.user img').css('display', 'block');
	$('.user').css('display', 'none');

  });
  $('.close_right').on('click', function (event) {
	$('.right_column').css('visibility', 'hidden');
  });
  let show = false;
  $('.toggle').on('click', function () {
	  if (!show) {
		  $('.help').css('display', 'block');
		  show = true;
	  } else {
		$('.help').css('display', 'none');
		show = false;
	  }
  });
});