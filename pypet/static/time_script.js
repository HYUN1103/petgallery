function mainTime(){
    var today = new Date();
    var week = ["Sun","Mon","Tues","Wednes","Thurs","Fri","Satur"];
    var day = today.getDay();  // 요일
    var h = today.getHours();  // 시
    var m = today.getMinutes(); // 분
    var s = today.getSeconds(); // 초
    m = dasi(m);
    s = dasi(s);

    var timeElement = document.getElementById('main-time');
    timeElement.innerHTML = week[day] + "day " + h + ":" + m + ":" + s;
    setTimeout(mainTime, 1000); // 1초마다 갱신
}

function dasi(i){
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

// 페이지 로드 시 mainTime 함수 호출
window.onload = function() {
    mainTime();
}
