$(document).ready(function() {
    console.log('nav.js 로드 완료');

    // menu 클래스 바로 하위에 있는 a 태그를 클릭했을 때
    $(".menu > a").click(function(event) {
        event.preventDefault(); // 기본 링크 동작을 막습니다.
        var submenu = $(this).next("ul");
        // submenu가 화면상에 보일 때는 위로 부드럽게 접고 아니면 아래로 부드럽게 펼치기
        if (submenu.is(":visible")) {
            submenu.slideUp();
        } else {
            submenu.slideDown();
        }
    });

    // 메뉴 외부를 클릭하면 모든 서브메뉴를 닫습니다.
    $(document).click(function(event) {
        if (!$(event.target).closest('.menu').length) {
            $(".menu .dropdown-menu").slideUp();
        }
    });
});
