$(window).on('load', function () {
  $('.back').on('click', function (event) {
	$('.keys').css('display', 'none');
  });
  $('.close_right').on('click', function (event) {
	$('.right_column').css('visibility', 'hidden');
  });
});