$(function () {
	"use strict";

	// Tooltops

	$(function () {
		$('[data-bs-toggle="tooltip"]').tooltip();
	})



	$(".nav-toggle-icon").on("click", function () {
		$(".wrapper").toggleClass("toggled")
	})

	$(".mobile-toggle-icon").on("click", function () {
		$(".wrapper").addClass("toggled")
	})

	$(function () {
		for (var e = window.location, o = $(".metismenu li a").filter(function () {
			return this.href == e
		}).addClass("").parent().addClass("mm-active"); o.is("li");) o = o.parent("").addClass("mm-show").parent("").addClass("mm-active")
	})

	// $(".toggle-icon").click(function () {
	// 	$(".wrapper").hasClass("toggled") ? ($(".wrapper").removeClass("toggled"), $(".sidebar-wrapper").unbind("hover")) : ($(".wrapper").addClass("toggled"), $(".sidebar-wrapper").hover(function () {
	// 		$(".wrapper").addClass("sidebar-hovered")
	// 	}, function () {
	// 		$(".wrapper").removeClass("sidebar-hovered")
	// 	}))
	// })


	// sidebar coding

	const sidebar = document.querySelector('.sidebar-wrapper');
	const toggleBtn = document.querySelector('.toggle-icon');
	// Check for sidebar state in localStorage
	const sidebarState = localStorage.getItem('sidebarState');

	// Apply stored state on page load
	if (sidebarState === 'closed') {

		sidebar.classList.add('closed');
		document.querySelector(".wrapper").classList.add("toggled");
	}

	// Toggle button click handler
	toggleBtn.addEventListener('click', () => {
		if (sidebar.classList.contains('closed')) {
			sidebar.classList.remove('closed');
			document.querySelector(".wrapper").classList.remove("toggled");
			localStorage.setItem('sidebarState', 'open');
		} else {
			sidebar.classList.add('closed');
			document.querySelector(".wrapper").classList.add("toggled");
			localStorage.setItem('sidebarState', 'closed');
		}
	});

	// Hover effects (optional, based on your description)
	// sidebar.addEventListener('mouseenter', () => {
	// 	sidebar.classList.remove('closed');
	// });

	// sidebar.addEventListener('mouseleave', () => {
	// 	if (localStorage.getItem('sidebarState') === 'closed') {
	// 		sidebar.classList.add('closed');
	// 	}
	// });



	$(function () {
		$("#menu").metisMenu()
	})


	$(".search-toggle-icon").on("click", function () {
		$(".top-header .navbar form").addClass("full-searchbar")
	})
	$(".search-close-icon").on("click", function () {
		$(".top-header .navbar form").removeClass("full-searchbar")
	})


	$(".chat-toggle-btn").on("click", function () {
		$(".chat-wrapper").toggleClass("chat-toggled")
	}), $(".chat-toggle-btn-mobile").on("click", function () {
		$(".chat-wrapper").removeClass("chat-toggled")
	}), $(".email-toggle-btn").on("click", function () {
		$(".email-wrapper").toggleClass("email-toggled")
	}), $(".email-toggle-btn-mobile").on("click", function () {
		$(".email-wrapper").removeClass("email-toggled")
	}), $(".compose-mail-btn").on("click", function () {
		$(".compose-mail-popup").show()
	}), $(".compose-mail-close").on("click", function () {
		$(".compose-mail-popup").hide()
	})


	$(document).ready(function () {
		$(window).on("scroll", function () {
			$(this).scrollTop() > 300 ? $(".back-to-top").fadeIn() : $(".back-to-top").fadeOut()
		}), $(".back-to-top").on("click", function () {
			return $("html, body").animate({
				scrollTop: 0
			}, 600), !1
		})
	})


	// switcher 

	// Check if a theme is stored in local storage; if not, set it to semi-dark by default
	if (!localStorage.getItem("theme")) {
		localStorage.setItem("theme", "semi-dark");
		localStorage.setItem("checked", "semi-dark");
	}

	function changeChecked() {

		const checked = localStorage.getItem("checked");

		if (checked === "semi-dark") {
			$("#SemiDarkTheme").attr("checked", "checked");
		}
		else if (checked === "light-theme") {
			$("#LightTheme").attr("checked", "checked");
		}
		else if (checked === "dark-theme") {
			$("#DarkTheme").attr("checked", "checked");
		}
		else if (checked === "minimal-theme") {
			$("#MinimalTheme").attr("checked", "checked");
		}

	}

	changeChecked();
	// Apply the stored theme on page load
	$(document).ready(function () {
		$("html").attr("class", localStorage.getItem("theme"));
	});

	// Change theme and store it in local storage
	$("#LightTheme").on("click", function () {
		$("html").attr("class", "light-theme");
		localStorage.setItem("theme", "light-theme");
		localStorage.setItem("checked", "light-theme");
		changeChecked();
	});

	$("#DarkTheme").on("click", function () {
		$("html").attr("class", "dark-theme");
		localStorage.setItem("theme", "dark-theme");
		localStorage.setItem("checked", "dark-theme");
		changeChecked();
	});

	$("#SemiDarkTheme").on("click", function () {
		$("html").attr("class", "semi-dark");
		localStorage.setItem("theme", "semi-dark");
		localStorage.setItem("checked", "semi-dark");
		changeChecked();
	});

	$("#MinimalTheme").on("click", function () {
		$("html").attr("class", "minimal-theme");
		localStorage.setItem("theme", "minimal-theme");
		localStorage.setItem("checked", "minimal-theme");
		changeChecked();
	})

	// Apply the stored header color on page load
	$(document).ready(function () {
		$("html").addClass(localStorage.getItem("headerColor"));
	});

	// Change header color and store it in local storage
	$("#headercolor1").on("click", function () {
		changeHeaderColor("headercolor1");
	});

	$("#headercolor2").on("click", function () {
		changeHeaderColor("headercolor2");
	});

	$("#headercolor3").on("click", function () {
		changeHeaderColor("headercolor3");
	});

	$("#headercolor4").on("click", function () {
		changeHeaderColor("headercolor4");
	});

	$("#headercolor5").on("click", function () {
		changeHeaderColor("headercolor5");
	});

	$("#headercolor6").on("click", function () {
		changeHeaderColor("headercolor6");
	});

	$("#headercolor7").on("click", function () {
		changeHeaderColor("headercolor7");
	});

	$("#headercolor8").on("click", function () {
		changeHeaderColor("headercolor8");
	});

	// Function to change header color and update local storage
	function changeHeaderColor(colorClass) {
		$("html").removeClass(function (index, className) {
			return (className.match(/headercolor\d+/g) || []).join(" ");
		});
		$("html").addClass("color-header " + colorClass);
		localStorage.setItem("headerColor", colorClass);
	}

	function applySavedHeaderColor() {
		const savedColor = localStorage.getItem("headerColor");
		if (savedColor) {
			$("html").addClass("color-header " + savedColor);
		}
	}

	// Call the function on page load
	$(document).ready(function () {
		applySavedHeaderColor();
	});


	new PerfectScrollbar(".header-message-list")
	new PerfectScrollbar(".header-notifications-list")



});