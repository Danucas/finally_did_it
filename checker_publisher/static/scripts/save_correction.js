$(window).on('load', function () {
    /*
    * Generates a canvas draw with the checker content
    * drawRectangle - generates a rounded rectangle
    * 
    *
    * @medias: lists controls which social media channels to reach
    */
    const medias = ['twitter'];
    let editing;
    let show = true;
    // Draws a rounded rectangle
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
    /*
    * Draws a text in the postition stored at params
    * @params: object {fontSize, color, position: {left, top}, text, icon: {src, position: {left, top}}}
    */
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
    // Prompt Media channel access Keys form
    const fillMedia = function (chan, marginTop, color) {
        $('.user').css('display', 'block');
        $('.user').css('top', 0);
        $('.user').height($('body').outerHeight());
        $('.init_wait').css('display', 'none');
        $('.keys').css('visibility', 'visible');
		$('.keys').css('display', 'block');
		$('.keys form').css('display', 'block');
		$('.keys button').css('display', 'block');
        $('.keys').css('z-index', 2);
        $('.keys legend').text(chan);
        $('.keys legend').css('color', color);
		$('.keys').css('top', (marginTop).toString() + 'px');
	}
	const sendImage = function (message) {
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
		$('.user').css('display', 'block');
		$('.user').css('height', $('body').outerHeight());
		$('.user').css('top', 0);
		$('.init_wait').css('display', 'block');
		$('.init_wait').css('margin-top', $(window).scrollTop() + ($(window).height() / 3) - 100);
		// Draw the outer rectangle
		drawRectangle(frame, canvas);
		frame.position = obj.position();
		// Draw each check box
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
			icon.position = chi.position    ;
			icon.size = $(img).width();
			icon.src = $(img).attr('src');
			chi.icon = icon;
			drawText(chi, canvas);
		}
		const csrftoken = document.cookie.split('=')[1];
		let mess = message.replace('[p]', $('[project]').attr('project'));
		mess = mess.replace('[t]', $('.correction').attr('task_name'));
		let channels = '';
		if (medias.length > 1) {
			channels = medias.join(',');
		} else if (medias.length === 1) {
			channels = medias[0];
		}
		$.ajax({
			type: 'POST',
			url: 'dashboard/send_image',
			data: { 'image': canvas.toDataURL(),
					'content': mess,
					'channels': channels,
					'token': sessionStorage.getItem('publisher_token')},
			beforeSend: function (xhr) {
				xhr.setRequestHeader('X-CSRFToken', csrftoken);
			},
			crossDomain:true,
			success: function (data) {
				console.log(data);
				$('.user').css('display', 'none');
				$('.keys').css('visibility', 'hidden');
				$('.sended').append($(data));
				$('.right_column h4').css('display', 'none');
				$('.right_column').css('visibility', 'hidden');
			},
			error: function (data) {
				console.log(data);
				// if (data.status === 305) {
				// 	alert('select at least one channel');
				// 	$('.user').css('display', 'none');
				// } else {
				// 	$('.user').css('display', 'none');
				// 	editing = data.responseJSON.media;
				// 	fillMedia('Please provide your ' + data.responseJSON.media + ' credentials',
				// 				$(window).scrollTop(),
				// 				'red');
				// }
			}
		});
	}
	const checkChannel = function (send, parms) {
		$.ajax({
            url: 'dashboard/check_channel',
			data: {'channel': editing,
					'token': sessionStorage.getItem('publisher_token')
				},
            success: function (channel) {
                $('input[name="key"]').val(channel.api_key);
                $('input[name="api_secret"]').val(channel.api_secret);
                $('input[name="token"]').val(channel.token);
				$('input[name="token_secret"]').val(channel.token_secret);
				if (send) {
					sendImage($('.right_column input').val());
				} else {
					fillMedia(parms[0], parms[1], parms[2]);
				}
            },
            error: function () {
                $('input[name="key"]').val('');
                $('input[name="api_secret"]').val('');
                $('input[name="token"]').val('');
				$('input[name="token_secret"]').val('');
				fillMedia(parms[0], parms[1], parms[2]);
            }
        });
	};
    // Send the message with the image
    $('.png').on('click', function (event) {
        let input = $('.right_column input').val(); 
        if (input === '') {
            // Shows a message to complete the message field
            $('.right_column h4').css('display', 'block');
        } else {
			checkChannel(true, [editing, $(window).scrollTop(), 'blue']);
        }
    });
    // Prompts a form to save Channels Access credentials
    $('.media > li').on('click', function (event) {
      if (show) {
		editing = $(this).find('input').attr('name');
		checkChannel(false, [editing, 0, 'blue']);
      }
      show = true;
    });
    // Stores or delete item from medias list
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
    // Submit Media channel access Keys
    $('#save_channel').on('click', function (event) {
      const key = $('input[name="key"]').val();
      const api_secret = $('input[name="api_secret"]').val();
      const token = $('input[name="token"]').val();
      const token_secret = $('input[name="token_secret"]').val();
      if (key === '' || api_secret === '' || token === '' || token_secret === '') {
          $('.keys legend').text('Please provide all the keys');
          $('.keys legend').css('color', 'red');
      } else {
          console.log('save channel');
          console.log(editing);
          $.ajax({
              url: 'dashboard/save_channel',
              headers: {
                  'Access-Control-Allow-Origin': '*'
              },
              data: {'channel': editing,
                      'api_key': key,
                      'api_secret': api_secret,
                      'token': token,
                      'token_secret': token_secret,
                      'publisher_token': sessionStorage.getItem('publisher_token')
              },
              success: function (data) {
                  console.log(data);
                  $('.keys').css('display', 'none');
                  $('.user').css('display', 'none');
              },
              error: function (data) {
                $('.keys').css('display', 'none');
                $('.user').css('display', 'none');
              }
          });
      }
    });
});
