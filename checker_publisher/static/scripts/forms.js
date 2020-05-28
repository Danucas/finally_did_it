$(window).on('load', function () {
 // To save user credentials	
  // Start a new test
  $('.task button').on('click', function (event) {
	console.log("open checker");
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
			url: 'dashboard/search_project',
			data: {'project_id': $('.p_id input').val(),
					'token': sessionStorage.getItem('publisher_token')},
			success: function (resp) {
				// Seting up the view
				$('.tasks').empty();
				$('.tasks').append($(resp)); 
				$('.p_name').text($('[project]').attr('project')); // Project name-title
				// Set bar to the new height
				const height = $('.tasks').outerHeight() + $('.tasks').position().top;
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
		url: 'dashboard/check_task',
		data: {'task': task,
				'token': sessionStorage.getItem('publisher_token')},
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