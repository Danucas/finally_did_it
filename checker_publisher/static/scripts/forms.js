$(window).on('load', function () {
 // To save user credentials
 // First call auth token and the backend will store those values
 $('.user button').on('click', function (event) {
	const apiKey = $('[name="intr_api_key"]').val();
	const email = $('[name="email"]').val();
	const pass = $('[name="pass"]').val();
	if (apiKey === '' || email === '' || pass === '') {
		$('.user legend').text('Please complete all the fields');
		// alert('Ups! seems like you missed some fields\nTry again!');
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
		const data = {};
		data.api_key = apiKey;
		data.email = email;
		data.pass = pass;
		$('.init_wait').css('display', 'block');
		$('.user form').css('display', 'none');
		$('.user button').css('display', 'none');
		$.ajax({
			url: 'http://127.0.0.1:8000/dashboard/submit_user',
			data: data,
			headers: {
				'Access-Control-Allow-Origin': '*'
			},
			success: function (resp) {
				console.log(resp);
				location.reload();
			},
			error: function (resp) {
				$('.init_wait').css('display', 'none');
				$('.user form').css('display', 'block');
				$('.user button').css('display', 'block');
				$('.user legend').css('color', 'red');
				$('.user legend').text('Your email or password was incorrect');
			}
		});
	}
  });
  // Start a new test
  $('.task button').on('click', function (event) {
	console.log("run checker");
	$('.right_column').css('visibility', 'visible');
	console.log('checking task :', $(this).attr('task_id'));
  });
  let searching = false;
  let task = null;
  // Request for a project
  $('.p_id button').on('click', function (event) {
	  if (!searching) {
		searching = true;
		$('.p_id img').css('visibility', 'visible');
		$.ajax({
			url: 'http://127.0.0.1:8000/dashboard/search_project',
			data: {'project_id': $('.p_id input').val()},
			success: function (resp) {
				// Seting up the view
				$('.tasks_and_status').empty();
				$('.tasks_and_status').append($(resp)); 
				console.log($('.tasks_and_status > ul').attr('project'));
				$('.p_name').text($('[project]').attr('project')); // Project name-title
				// Set bar to the new height
				const height = $('[project]').height() + 320;
				console.log('new height: ', height);
				$('.bar').height(height.toString() + 'px');
				$('.p_id img').css('visibility', 'hidden');
				$('.task button').on('click', function (event) {
					console.log("run checker");
					$('.right_column').css('visibility', 'visible');
					$('.right_column').height($(window).height());
					console.log('checking task :', $(this).attr('task_id'));
					const task_id = $(this).attr('task_id');
					task = task_id;
					const name = $(this).attr('task_name');
					const pos = $(this).attr('task_pos');
					let el = 'Correction of:<br>&nbsp;&nbsp;&nbsp;' + pos + '.' + name;
					$('.menu_right h3').html(el);
					$('.correction').empty();
				});
				searching = false;
			}
		});
	  }
  });
  $('.runchecker').on('click', function (event) {
	console.log(task);
	$('.corr_wait').css('visibility', 'visible');
	$.ajax({
		url: 'http://127.0.0.1:8000/dashboard/check_task',
		data: {'task': task},
		success: function (result) {
			$('.correction').empty()
			$('.correction').append($(result));
			let taskName = (Number($('[task_id=' + task + ']').attr('task_pos')) - 1).toString();
			taskName += '. ' + $('[task_id=' + task + ']').attr('task_name');
			$('.correction').attr('task_name', taskName);
			$('.corr_wait').css('visibility', 'hidden');
		}
	});
  });

});