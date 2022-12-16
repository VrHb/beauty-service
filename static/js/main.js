$(document).ready(function() {
    var cache = {};

    $('.service__salons button').attr('data-pk', '0');
    $('.service__salons .panel').text('');
    $.get('/saloons', function(data){
        var elements = [];
        $.each(data, function(index, item){
            var element = `
            <div class="accordion__block fic" data-pk="${item.pk}">
              <div class="accordion__block_intro">${item.name}</div>
              <div class="accordion__block_address">${item.address}</div>
            </div>`;
            elements.push(element);
        });
        $('.service__salons .panel').html(elements.join(''));
        cache.saloons = data;
    });

    $('.service__services button').attr('data-pk', '0');
    $('.service__services .panel').html('');
    $.get('/service_groups', function(data){
        var groupElements = [];
        $.each(data, function(groupIndex, group){
            var serviceElements = [];
            $.each(group.services, function(serviceIndex, service){
                var element = `
                <div class="accordion__block_item fic" data-pk="${service.pk}">
                    <div class="accordion__block_item_intro">${service.name}</div>
                    <div class="accordion__block_item_address">${service.price} ₽</div>
                </div>`;
                serviceElements.push(element);
            });
            var serviceElementsHTML = serviceElements.join('');
            var groupHTML = `
            <button class="accordion">${group.name}</button>
			<div class="panel">
			  <div class="accordion__block_items" data-pk="${group.pk}">${serviceElementsHTML}</div>
			</div>`;
			groupElements.push(groupHTML);
        });
        $('.service__services .panel').html(groupElements.join(''));
        cache.serviceGroups = data;
    });

    $('.service__masters button').attr('data-pk', '0');
    $('.service__masters .panel').text('');
    $.get('/masters', function(data){
        var elements = [];
        $.each(data, function(index, item){
            var element = `
            <div class="accordion__block fic" data-pk="${item.pk}">
              <div class="accordion__block_elems fic">
                  <img src="${item.avatar}" alt="avatar" class="accordion__block_img">
                  <div class="accordion__block_master">${item.full_name}</div>
              </div>
              <div class="accordion__block_prof">${item.speciality.name}</div>
            </div>`;
            elements.push(element);
        });
        $('.service__masters .panel').html(elements.join(''));
        cache.saloons = data;
    });

    var morningTime = {times: ['10:00', '11:00'], name: 'Утро'};
    var afternoonTime = {times: ['12:00', '13:00', '14:00', '15:00', '16:00'], name: 'День'};
    var eveningTime = {times: ['17:00', '18:00', '19:00'], name: 'Вечер'};
    var times = [morningTime, afternoonTime, eveningTime];
    $('#time .time__elems').html(function(){
        var timesHTMLElements = []
        times.forEach(function(timeOfDay){
            var timeslots = [];
            timeOfDay.times.forEach(function(t){
                timeslots.push(`<button data-time="${t}" class="time__elems_btn">${t}</button>`);
            });
        timesHTMLElements.push(`
        <div class="time__items">
          <div class="time__elems_intro">${timeOfDay.name}</div>
          <div class="time__elems_elem fic">${timeslots.join('')}</div>
        </div>`);
        });
        return timesHTMLElements.join('');
    });


    //////////////////////////////////////////////////////

	$('.salonsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  infinite: true,
	  prevArrow: $('.salons .leftArrow'),
	  nextArrow: $('.salons .rightArrow'),
	  responsive: [
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});
	$('.servicesSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.services .leftArrow'),
	  nextArrow: $('.services .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.mastersSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.masters .leftArrow'),
	  nextArrow: $('.masters .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.reviewsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.reviews .leftArrow'),
	  nextArrow: $('.reviews .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	// menu
	$('.header__mobMenu').click(function() {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function() {
		$('#mobMenu').hide()
	})

	new AirDatepicker('#datepickerHere')

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function(e) {
	  	e.preventDefault()
	    this.classList.toggle("active");
	    var panel = $(this).next()
	    panel.hasClass('active') ?  
	    	 panel.removeClass('active')
	    	: 
	    	 panel.addClass('active')
	  });
	}


	$(document).on('click', '.accordion__block', function(e) {
		let thisName,thisAddress;

		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()
		
		
		if(thisName === 'BeautyCity Пушкинская') {
			$('.service__masters > .panel').html(`
				<div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Любой мастер</div>
						  	</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/1.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Елизавета Лапина</div>
						  	</div>
						  	<div class="accordion__block_prof">Мастер маникюра</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/2.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Анна Сергеева</div>
						  	</div>
						  	<div class="accordion__block_prof">Парикмахер</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/3.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Ева Колесова</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/4.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Мария Суворова</div>
						  	</div>
						  	<div class="accordion__block_prof">Стилист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/5.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Мария Максимова</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/pushkinskaya/6.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Анастасия Сергеева</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>	
			`)
			// $('.service__masters div[data-masters="Pushkinskaya"]').addClass('vib')
		}
		console.log(thisName)
		if(thisName === 'BeautyCity Ленина') {
			
			$('.service__masters > .panel').html(`
				<div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Любой мастер</div>
						  	</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/1.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Дарья Мартынова</div>
						  	</div>
						  	<div class="accordion__block_prof">Мастер маникюра</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/2.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Амина Абрамова</div>
						  	</div>
						  	<div class="accordion__block_prof">Парикмахер</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/3.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Милана Романова</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/4.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Диана Чернова</div>
						  	</div>
						  	<div class="accordion__block_prof">Стилист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/5.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Полина Лукьянова</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/lenina/6.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Вера Дмитриева</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
			`)
		}

		if(thisName === 'BeautyCity Красная') {
			$('.service__masters > .panel').html(`
				<div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/all.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Любой мастер</div>
						  	</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/1.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Зоя Матвеева</div>
						  	</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/2.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Мария Родина</div>
						  	</div>
						  	<div class="accordion__block_prof">Мастер маникюра</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/3.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Дарья Попова</div>
						  	</div>
						  	<div class="accordion__block_prof">Парикмахер</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/4.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Ева Семенова</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/5.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Вера Романова</div>
						  	</div>
						  	<div class="accordion__block_prof">Стилист</div>
						  </div>
						  <div class="accordion__block fic">
						  	<div class="accordion__block_elems fic">
							  	<img src="img/masters/avatar/krasnaya/6.svg" alt="avatar" class="accordion__block_img">
							  	<div class="accordion__block_master">Валерия Зуева</div>
						  	</div>
						  	<div class="accordion__block_prof">Визажист</div>
						  </div>
			`)
			
		}

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)
		
		// $(this).parent().addClass('hide')

		// console.log($(this).parent().parent().find('.panel').hasClass('selected'))
		
		// $(this).parent().parent().find('.panel').addClass('selected')
	})


	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		// $(this).parent().parent().parent().parent().find('> button.active').click()
		// $(this).parent().parent().parent().addClass('hide')
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})



	// 	console.log($('.service__masters > .panel').attr('data-masters'))
	// if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
	// }


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function(e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function(e) {
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function(e) {
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})
	
	$('.authPopup__form').submit(function() {
		$('#confirmModal').arcticmodal();
		return false
	})

	//service
	$('.time__items .time__elems_elem .time__elems_btn').click(function(e) {
		e.preventDefault()
		$('.time__elems_btn').removeClass('active')
		$(this).addClass('active')
		// $(this).hasClass('active') ? $(this).removeClass('active') : $(this).addClass('active')
	})

	$(document).on('click', '.servicePage', function() {
		if($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').hasClass('selected')) {
			$('.time__btns_next').addClass('active')
		}
	})
	


})