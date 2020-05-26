$(window).on('load', function () {
	console.log('save_correction installed');
	const drawRectangle = function (params, canvas) {
		const ctx = canvas.getContext('2d');
		const x = params.position.left;
		const y = params.position.top;
		ctx.beginPath();
		ctx.fillStyle = params.background;
		if (params.isCode) {
			ctx.lineWidth = 3;
		} else {
			ctx.lineWidth = 0;
		}
		if (params.pass) {
			ctx.strokeStyle = 'green';
		} else {
			ctx.strokeStyle = 'red';
		}
		ctx.moveTo(params.round + x, 0 + y);
		ctx.lineTo(params.width - params.round + x, 0 + y);
		ctx.arc(params.width - params.round + x, 0 + y + params.round, params.round, 270 * Math.PI / 180, 0 * Math.PI / 180, false);
		ctx.lineTo(params.width + x, params.height - params.round + y);
		ctx.arc(params.width + x - params.round, params.height - params.round + y, params.round, 0 * Math.PI / 180, 90 * Math.PI / 180, false);
		ctx.lineTo(params.round + x, params.height + y);
		ctx.arc(params.round + x, params.height + y - params.round, params.round, 90 * Math.PI / 180, 180 * Math.PI / 180, false);
		ctx.lineTo(0 + x, params.round + y);
		ctx.arc(0 + x + params.round, params.round + y, params.round, 180 * Math.PI / 180, 270 * Math.PI / 180, false);
		ctx.fill();
		if (params.isCode) {
			ctx.stroke();
		}
		ctx.closePath();
		return true;
	};
	const drawText = function (params, canvas) {
		const ctx = canvas.getContext('2d');
		ctx.lineWidth = 0.2;
		ctx.font = params.fontSize;
		ctx.strokeStyle = params.color;;
		ctx.fillStyle = params.color;
		ctx.textAlign = 'center';
		const x = params.position.left + (params.width / 2) - 5;
		const y = params.position.top + (params.height / 2) + 5;
		ctx.fillText(params.text, x, y);
		ctx.strokeText(params.text, x, y);
		const img = document.createElement('img');
		img.src = params.icon.src;
		ctx.drawImage(img, params.icon.position.left + 15, params.icon.position.top + 10, 14, 14);

	};
	$('.png').on('click', function (event) {
		let input = $('.right_column input').val(); 
		if (input === '') {
			$('.right_column h4').css('display', 'block');
		} else {
			const obj = $('.correction');
			const pad = [];
			for (el of obj.css('padding').split(' ')) {
				pad.push(Number(el.slice(0, 2)));
			}
			const frame = {};
			frame.width = obj.outerWidth();
			frame.height = obj.outerHeight();
			frame.round = Number(obj.css('border-radius').slice(0, 2));
			frame.background = obj.css('background-color');
			const canvas = document.createElement('canvas');
			canvas.width = frame.width;
			canvas.height = frame.height;
			frame.position = {'top': 0, 'left': 0};

			// $('.user').append(canvas);
			$('.user').css('display', 'block');

			drawRectangle(frame, canvas);
			frame.position = obj.position();
			for (child of obj.children()) {
				const chi = {};
				chi.width = $(child).outerWidth();
				chi.height = $(child).outerHeight();
				chi.round = Number($(child).css('border-radius').split('px')[0]);
				chi.background = $(child).css('background-color');
				chi.position = {'top': $(child).position().top - frame.position.top - 20,
								'left': $(child).position().left - frame.position.left - 20}
				chi.fontSize = $(child).css('font-size');
				chi.text = $(child).text();
				chi.isCode = $(child).hasClass('code');
				chi.pass = $(child).hasClass('True');
				chi.color = $(child).css('color');
				const img = $(child).find('img');
				drawRectangle(chi, canvas);
				const icon = {}
				icon.position = chi.position	;
				icon.size = $(img).width();
				icon.src = $(img).attr('src');
				chi.icon = icon;
				drawText(chi, canvas);
			}
			//const boton = $('<a download="correction.png">Dowload correction</a>');
			const csrftoken = document.cookie.split('=')[1];
			input = input.replace('[p]', $('[project]').attr('project'));
			input = input.replace('[t]', $('.correction').attr('task_name'));
			// let content = 'Correction for ' + $('[project]').attr('project');
			// content += '\n\ttask: ' + $('.correction').attr('task_name');
			// content += '\nplaned customizable message\nAwesome!!!';
			$.ajax({
				type: 'POST',
				url: 'http://127.0.0.1:8000/dashboard/send_image',
				data: { 'image': canvas.toDataURL(),
						'content': input},
				beforeSend: function (xhr) {
					xhr.setRequestHeader('X-CSRFToken', csrftoken);
				},
				crossDomain:true,
				success: function (data) {
					$('.user').css('display', 'none');
					$('.right_column h4').css('display', 'none');
				}
			});
		}
	});
});