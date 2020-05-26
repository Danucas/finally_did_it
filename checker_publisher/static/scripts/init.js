$(window).on('load', function () {
	$('.user').height($('body').height());
	$.ajax({
		url: 'http://127.0.0.1:8000/dashboard/check_user',
		success: function (data) {
			//  console.log('User exists');
			const resp = data;
			$('#username').text(resp.username);
			$('#email').text(resp.email);
			$('.user').css('display', 'none');
		},
		error: function (data) {
			console.log(data.status);
			$('.init_wait').css('display', 'none');
			$('.user form').css('display', 'block');
			$('.user button').css('display', 'block');
			// alert('Submit the user info');
			
		}
	});
	// $('body').on('click', function (event) {
	// 	console.log(event.originalEvent.screenY);
	// });
	// $('.right_column').height($(window).height());
	// $('.bar').css('height');

});