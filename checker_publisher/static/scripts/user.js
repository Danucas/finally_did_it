$(window).on('load', function () {
	// Shows the login form
	const displayLogin = function (show, message) {
		if (show) {
			$('.init_wait').css('display', 'none');
			$('.user form').css('display', 'block');
			$('.user button').css('display', 'block');
			if (message) {
				$('.user legend').text(message);
			}
		} else {
			$('.init_wait').css('display', 'block');
			$('.user form').css('display', 'none');
			$('.user button').css('display', 'none');
			$('.user').css('display', 'none');
			$.ajax({
				url: 'http://127.0.0.1:8000/dashboard/sended',
				data: {'token': sessionStorage.getItem('publisher_token')},
				success: function (data) {
					$('.sended').empty();
					$('.sended').append(data);
				}
			});
		}
	}
	// Set text values for username and email
	const setUserAndEmail = function (user, email) {
		$('#username').text(user);
		$('#email').text(email);
	};
	// Get token from intranet API
	const getToken = function (apiKey, email, pass) {
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			url: 'https://intranet.hbtn.io/users/auth_token.json',
			data: JSON.stringify({
				'api_key': apiKey,
				'email': email,
				'password': pass,
				'scope': 'checker'
			}),
			success: function (resp) {
				sessionStorage.setItem('publisher_token', resp.auth_token);
				setUserAndEmail(resp.full_name, '');
			},
			error: function () {
				displayLogin(true, 'You password or email is wrong');
			}

		});
	};
	// Check if the token is valid
	const checkUser = function (token) {
		$.ajax({
			url: 'https://intranet.hbtn.io/users/me.json?auth_token=' + token,
			success: function (data) {
				setUserAndEmail(data.full_name, '');
				displayLogin(false, '');
			},
			error: function (data) {
				displayLogin(true, 'Please login')
			}
		});
	};
	// Check for an existent token if doesn't exists display login form
	$('.user').height($('body').outerHeight() + 200);
	const token = sessionStorage.getItem('publisher_token');
	if (token === null) {
		console.log('token is not stored');
		displayLogin(true, '');
	} else {
		checkUser(token);
	}
	// When user press submit button, check blank fields and generates the token
	$('.user button').on('click', function (event) {
		const apiKey = $('[name="intr_api_key"]').val();
		const email = $('[name="email"]').val();
		const pass = $('[name="pass"]').val();
		
		if (apiKey === '' || email === '' || pass === '') {
			$('.user legend').text('Please complete all the fields');
			if (apiKey === '') {
				$('[name="intr_api_key"]').addClass('bad_field');
				$('[name="intr_api_key"]').attr('placeholder', 'Your api key');
			}
			if (email === '') {
				$('[name="email"]').addClass('bad_field');
				$('[name="email"]').attr('placeholder', 'Your email');
			}
			if (pass === '') {
				$('[name="pass"]').addClass('bad_field');
				$('[name="pass"]').attr('placeholder', 'Password');
			}
		} else {
			getToken(apiKey, email, pass);
		}
	});
});