$(document).ready(
    function () {
        $('.slider-for').slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            speed: 500,
            arrows: false,
            fade: true,
            asNavFor: ".slider-nav",
        });
        $(".slider-nav").slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            speed: 500,
            asNavFor: ".slider-for",
            focusOnSelect: true,
            slide: "div",
            prevArrow: '<button class="btn slider-btn slider-prev"><img src="/media/img/arrow-left-solid.svg" alt="prev"></button>',
            nextArrow: '<button class="btn slider-btn slider-next"><img src="/media/img/arrow-right-solid.svg" alt="next"></button>',
            responsive: [
                {
                  breakpoint: 1200,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                  }
                },
                {
                  breakpoint: 992,
                  settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1
                  }
                },
                {
                  breakpoint: 768,
                  settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                  }
                }
            ]
        });
        
    },
);