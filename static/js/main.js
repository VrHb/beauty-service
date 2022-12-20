$(document).ready(function() {
    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    };

    function setCookie(name,value,seconds) {
        var expires = "";
        if (seconds) {
            var date = new Date();
            date.setTime(date.getTime() + (seconds*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    };

    var cache = {blocked: {}, saloons: {}, services: {}, masters: {}};
    var userElement = document.getElementById('user_id');

    var user_id;
    var service_finally_url;
    var service_url;
    if (userElement) {
        user_id = JSON.parse(document.getElementById('user_id').textContent);
        service_finally_url = JSON.parse(document.getElementById('service_finally_url').textContent);
        service_url = JSON.parse(document.getElementById('service_url').textContent);
    }

    function showSaloons(data) {
        var saloonPk = $('.service__salons button').attr('data-pk');
        var nowSaloonInData = false;
        var elements = [];
        $.each(data, function(index, item){
            if (saloonPk == item.pk){
                nowSaloonInData = true;
            }
            var element = `
            <div class="accordion__block fic" data-pk="${item.pk}">
              <div class="accordion__block_intro">${item.name}</div>
              <div class="accordion__block_address">${item.address}</div>
            </div>`;
            elements.push(element);
        });
        $('.service__salons .panel').html(elements.join(''));
        if (!nowSaloonInData && (saloonPk != '0')){
            $('.service__salons button').text('(Выберите салон)');
            $('.service__salons button').attr('data-pk', '0');
            $('.service__salons button').removeClass('selected');
        }
    }

    function showServices(data) {
        var servicePk = $('.service__services button').attr('data-pk');
        var nowServiceInData = false;
        var groupElements = [];
        var groups = [];
        var groups2 = [];
        $.each(data, function(index, item){
            if (!groups2.includes(item.group.name)) {
                groups.push({name: item.group.name, elements: []});
                groups2.push(item.group.name);
            }
        });
        var groupServices = [];
        $.each(data, function(index, item){
            groups.forEach(function(group, groupIndex) {
                if (item.group.name == group.name) {
                    group.elements.push(item);
                };
                groups[groupIndex] = group;
            });
        });

        groups.forEach(function(group, groupIndex) {
            groupServices.push(group);
        });


        $.each(groupServices, function(groupIndex, group){
            var serviceElements = [];
            $.each(group.elements, function(serviceIndex, service){
                if (servicePk == service.pk){
                    nowServiceInData = true;
                }
                var element = `
                <div class="accordion__block_item fic" data-pk="${service.pk}">
                    <div class="accordion__block_item_intro">${service.name}</div>
                    <div class="accordion__block_item_address">${service.special_price} ₽</div>
                </div>`;
                serviceElements.push(element);
            });
            var serviceElementsHTML = serviceElements.join('');
            var groupHTML = `
            <button class="accordion">${group.name}</button>
			<div class="panel">
			  <div class="accordion__block_items">${serviceElementsHTML}</div>
			</div>`;
			groupElements.push(groupHTML);
        });

        $('.service__services .panel').html(groupElements.join(''));

        $('.service__services .panel .accordion').each(function(i, el){
            $(el).click(function(e){
                e.preventDefault()
                this.classList.toggle("active");
                var panel = $(this).next()
                panel.hasClass('active') ?
                     panel.removeClass('active')
                    :
                     panel.addClass('active')
            });
        });

        $('.service__services .panel .accordion__block_item').click(function(e) {
		    let thisName,thisAddress;
		    thisName = $(this).find('> .accordion__block_item_intro').text()
		    thisAddress = $(this).find('> .accordion__block_item_address').text()
		    $(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		    setTimeout(() => {
			    $(this).parent().parent().parent().parent().find('> button.active').click()
		    }, 200)
	    })

	    if (!nowServiceInData && (servicePk != '0')){
            $('.service__services button').text('(Выберите услугу)');
            $('.service__services button').attr('data-pk', '0');
            $('.service__services button').removeClass('selected');
        }
    }

    function showMasters(data) {
        var masterPk = $('.service__masters button').attr('data-pk');
        var nowMasterInData = false;
        var elements = [];
        $.each(data, function(index, item){
            if (masterPk == item.pk){
                nowMasterInData = true;
            }
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
        if (!nowMasterInData && (masterPk != '0')){
            $('.service__masters button').text('(Выберите мастера)');
            $('.service__masters button').attr('data-pk', '0');
            $('.service__masters button').removeClass('selected');
        }
    }

    function updateSaloons() {
        var params = {}
        var masterPk = $('.service__masters button').attr('data-pk');
        var servicePk = $('.service__services button').attr('data-pk');
        if (masterPk != '0') params.master = masterPk;
        if (servicePk != '0') params.service = servicePk;
        var key = `${masterPk}-${servicePk}`;
        if (key in cache.saloons) {
            showSaloons(cache.saloons[key]);
        } else {
            $.get('/saloons', params, function(data){
                showSaloons(data);
                cache.saloons[key] = data;
            });
        }
    };

    function updateServices() {
        var params = {}
        var masterPk = $('.service__masters button').attr('data-pk');
        var saloonPk = $('.service__salons button').attr('data-pk');
        if (masterPk != '0') params.master = masterPk;
        if (saloonPk != '0') params.saloon = saloonPk;
        var key = `${masterPk}-${saloonPk}`;
        if (key in cache.services) {
            showServices(cache.services[key]);
        } else {
            $.get('/services', params, function(data){
                showServices(data);
                cache.services[key] = data;
            });
        }
    };

    function updateMasters() {
        var params = {}
        var saloonPk = $('.service__salons button').attr('data-pk');
        var servicePk = $('.service__services button').attr('data-pk');
        if (saloonPk != '0') params.saloon = saloonPk;
        if (servicePk != '0') params.service = servicePk;
        var key = `${saloonPk}-${servicePk}`;
        if (key in cache.masters) {
            showMasters(cache.masters[key]);
        } else {
            $.get('/masters', params, function(data){
                showMasters(data);
                cache.masters[key] = data;
            });
        }
    };

    $('.service__salons button').attr('data-pk', '0');
    updateSaloons();

    $('.service__services button').attr('data-pk', '0');
    updateServices();

    $('.service__masters button').attr('data-pk', '0');
    updateMasters();

    function get_picked_filters(){
        var result = {filters: {}};
        var dateCell = $('.air-datepicker-body--cells .-selected-');
        if (!dateCell.length) {
            var dateCell = $('.air-datepicker-body--cells .-current-');
        };
        // В datepicker месяц с 0
        var month = parseInt(dateCell.attr('data-month')) + 1;
        if (month) {
            result.filters.date = `${dateCell.attr('data-year')}-${month}-${dateCell.attr('data-date')}`;
        } else {
            var today = new Date();
            var dd = String(today.getDate()).padStart(2, '0');
            var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            var yyyy = today.getFullYear();
            result.filters.date = `${yyyy}-${mm}-${dd}`;
        }

        var saloon_pk = $('.service__salons button').attr('data-pk');
        if (saloon_pk !== '0'){result.filters.saloon = saloon_pk};

        var service_pk = $('.service__services button').attr('data-pk');
        if (service_pk !== '0'){result.filters.service = service_pk};

        var master_pk = $('.service__masters button').attr('data-pk');
        if (master_pk !== '0'){result.filters.master = master_pk};

        result.str = `${result.filters.date}-${saloon_pk}-${service_pk}-${master_pk}`;
        return result;
    }

    function addClickTimeListener(){
        $('.time__items .time__elems_elem .time__elems_btn').each(function(i, el){
            $(el).click(function(e) {
                e.preventDefault()
                $('.time__elems_btn').removeClass('active')
                $(this).addClass('active')
            });
        });
    };

    function show_calendar(data){
        var morningTime = {times: ['10:00', '11:00'], name: 'Утро'};
        var afternoonTime = {times: ['12:00', '13:00', '14:00', '15:00', '16:00'], name: 'День'};
        var eveningTime = {times: ['17:00', '18:00', '19:00'], name: 'Вечер'};
        var times = [morningTime, afternoonTime, eveningTime];
        $('#time .time__elems').html(function(){
            var timesHTMLElements = []
            times.forEach(function(timeOfDay){
                var timeslots = [];
                timeOfDay.times.forEach(function(t){
                    if (!data.includes(t)) {
                        timeslots.push(`<button data-time="${t}" class="time__elems_btn">${t}</button>`);
                    }
                });
            timesHTMLElements.push(`
            <div class="time__items">
              <div class="time__elems_intro">${timeOfDay.name}</div>
              <div class="time__elems_elem fic">${timeslots.join('')}</div>
            </div>`);
            });
            return timesHTMLElements.join('');
        });

        addClickTimeListener();
    };

    function updateCalendar(){
        var picked_filters = get_picked_filters();
        if (picked_filters.str in cache.blocked) {
            show_calendar(cache.blocked[picked_filters.str]);
        } else {
            $.get('/get_blocked_timeslots', picked_filters.filters, function(data){
                show_calendar(data);
                cache.blocked[picked_filters.str] = data;
            });
        };
    };

    updateCalendar();

    $(document).on('click', '.air-datepicker-body--cells', function(e){
        updateCalendar();
    })

    $(document).on('click', '.accordion__block', function(e) {
		let thisName,thisAddress;

		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()

		$(this).parent().parent().find('.accordion').attr('data-pk', $(this).attr('data-pk'));

		updateCalendar();
		updateServices();
		if ($(this).parent().parent().hasClass('service__salons')){
		    updateMasters();
		} else {
		    updateSaloons();
		}

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().find('> button.active').click()
		}, 200)
	});

	$(document).on('click', '.service__services .accordion__block_item', function(e) {
		let thisName,thisAddress;

		thisName = $(this).find('> .accordion__block_intro').text()
		thisAddress = $(this).find('> .accordion__block_address').text()

		$(this).parent().parent().parent().parent().find('.accordion').attr('data-pk', $(this).attr('data-pk'));

		updateCalendar();
		updateSaloons();
		updateMasters();

		$(this).parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().parent().find('> button.active').click()
		}, 200);
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

	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		$(this).parent().parent().find('> button.active').html(clone)
	})


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();

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
	})

	function postNote(){
	    var servicePk = $('.service__services button').attr('data-pk');
        var price;
        var masterPk = $('.service__masters button').attr('data-pk');
        var saloonPk = $('.service__salons button').attr('data-pk');
        var key = `${masterPk}-${saloonPk}`;
        cache.services[key].forEach(function(service){
            if (String(servicePk) == String(service.pk)) {
                price = service.special_price;
            }
        });
        var date = get_picked_filters().filters.date;
        var noteParams = {
            user: user_id,
            saloon: $('.service__salons button').attr('data-pk'),
            service: servicePk,
            master: $('.service__masters button').attr('data-pk'),
            price: price,
            date: date,
            stime: $('.time__items .time__elems_elem .time__elems_btn').attr('data-time'),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        };

        $.post("/notes-api/", noteParams, function(data) {
            var expiresThroughSeconds = 60 * 10; // 10 minutes
            setCookie('note_pk', data.pk, expiresThroughSeconds);
            window.location.href = service_finally_url;
        }).fail(function(data) {
            console.log(data);
        });
	};

	$(document).on('click', '.servicePage', function() {
	    var timeChosen = $('.time__items .time__elems_elem .time__elems_btn').hasClass('active');
	    var saloonChosen = $('.service__salons > button').hasClass('selected');
	    var serviceChosen = $('.service__salons > button').hasClass('selected');
	    var masterChosen = $('.service__masters > button').hasClass('selected');
		if (timeChosen && saloonChosen && serviceChosen && masterChosen) {
		    if (!$('.time__btns_next').hasClass('active')) {
                $('.time__btns_next').addClass('active');
                $('.time__btns_next.active').click(function(e){
                    postNote();
                });
		    };
		}
	});

    //////////////////////////////////////////////////////////
})