let map;
let infoWindow;
let markers = []; // 마커를 저장할 배열

function initMap() {
    // 기본 서울 위치 설정 (위치를 가져오지 못했을 때 대비)
    const defaultLocation = { lat: 37.5665, lng: 126.9780 };

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: defaultLocation,
    });

    infoWindow = new google.maps.InfoWindow();

    // HTML5 Geolocation API를 사용하여 현재 위치 가져오기
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const currentLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };

                // 지도의 중심을 현재 위치로 설정
                map.setCenter(currentLocation);

                // 현재 위치에 마커 표시
                new google.maps.Marker({
                    position: currentLocation,
                    map,
                    title: "현재 위치",
                });
            },
            () => {
                handleLocationError(true, map.getCenter());
            }
        );
    } else {
        // 브라우저가 Geolocation을 지원하지 않는 경우
        handleLocationError(false, map.getCenter());
    }

    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const place = document.getElementById('place').value;
        searchPlace(place);
    });
}

function handleLocationError(browserHasGeolocation, pos) {
    alert(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
}

function searchPlace(place) {
    fetch(`/hosplocation/search_place?place=${encodeURIComponent(place)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            displayResults(data.results);
        })
        .catch(error => console.error('Error:', error));
}

function displayResults(results) {
    // 기존 마커 제거
    clearMarkers();

    var table = document.getElementById('results-table');
    // 기존 결과 제거
    var rowCount = table.rows.length;
    for (var i = rowCount - 1; i > 0; i--) {
        table.deleteRow(i);
    }

    results.forEach(result => {
        const marker = new google.maps.Marker({
            position: { lat: result.geometry.location.lat, lng: result.geometry.location.lng },
            map: map,
            title: result.name,
        });

        markers.push(marker); // 마커 배열에 추가

        google.maps.event.addListener(marker, 'click', function() {
            infoWindow.setContent(`
                <div>
                    <h2>${result.name}</h2>
                    <p>${result.formatted_address}</p>
                    <p>${result.formatted_phone_number || 'N/A'}</p>
                </div>
            `);
            infoWindow.open(map, marker);
        });

        // 테이블에 결과 추가
        var row = table.insertRow();
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        cell1.innerHTML = result.name;
        cell2.innerHTML = result.formatted_address;
        cell3.innerHTML = result.formatted_phone_number || 'N/A';
    });

    document.getElementById('place-results').style.display = 'block';
}

function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}
