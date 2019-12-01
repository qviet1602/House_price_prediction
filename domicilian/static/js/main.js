/* ===================================
--------------------------------------
  Mondy - Real Estate HTML Template
  Version: 1.0
--------------------------------------

======================================*/
// Add your javascript code here.
require("../css/normalize.css");
require("../css/main.css");
require("../css/bootstrap.min.css");
require("../css/font-awesome.min.css");
require("../css/slicknav.min.css");
require("../css/style.css");


'use strict';

$(window).on('load', function() {
	/*------------------
		Preloder
	--------------------*/
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");

});

(function($) {
	/*------------------
		Navigation
	--------------------*/
	$(".main-menu").slicknav({
        appendTo: '.header-section',
		allowParentLinks: true,
		closedSymbol: '<i class="fa fa-angle-right"></i>',
		openedSymbol: '<i class="fa fa-angle-down"></i>'
	});

	$('.slicknav_nav').prepend('<li class="header-right-warp"></li>');
    $('.header-right').clone().prependTo('.slicknav_nav > .header-right-warp');

	/*------------------
		Background Set
	--------------------*/
	$('.set-bg').each(function() {
		var bg = $(this).data('setbg');
		$(this).css('background-image', 'url(' + bg + ')');
	});

	/*------------------
        Magnific Popup
    --------------------*/
    $('.video-play').magnificPopup({
        type: 'iframe'
    });

	/*--------------------------
		Loans calculator
	------------------------------*/
	$('#lc-submit').on('click', function(e){
		var lc_price    = $('#lc-price').val();
		var lc_interest = $('#lc-interest').val();
		var lc_dpay     = $('#lc-dpay').val();
		var weeks = 52;

		// Minus Down Payment 
		lc_price = lc_price - lc_dpay;

		// Find percentage  
		var perc = (lc_price/100) * lc_interest;

		// Add percentage to main price 
		lc_price = (lc_price + perc);

		// Weekly pay result
		var weekly_pay = (lc_price / weeks).toFixed(2);


		if (!isNaN(weekly_pay)) {
			$('#lc-result').text('$' + weekly_pay);
		}
	})

})(jQuery);

