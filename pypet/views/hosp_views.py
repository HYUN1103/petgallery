from flask import Blueprint, request, render_template_string, jsonify
import requests

# Google Maps API 키
API_KEY = ''

bp = Blueprint('hosplocation', __name__, url_prefix='/hosplocation')

@bp.route('/search')
def search():
    return '''
        <h1>Google Maps API 예제</h1>
        <form id="searchForm">
            <label for="place">장소 검색:</label>
            <input type="text" id="place" name="place" required><br><br>
            <input type="submit" value="장소 찾기">
        </form>
        <div id="map" style="height: 500px; width: 100%;"></div>
        <div id="place-results">
            <table id="results-table" border="1">
                <tr>
                    <th>이름</th>
                    <th>주소</th>
                    <th>전화번호</th>
                </tr>
            </table>
        </div>
        <script>
            function initMap() {
                var map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 7,
                    center: {lat: 37.5665, lng: 126.9780} // 서울을 초기 중심으로 설정
                });
                window.map = map; // 전역 변수로 설정하여 이후에 접근 가능하도록 함
            }

            document.getElementById('searchForm').addEventListener('submit', function(event) {
                event.preventDefault();
                var place = document.getElementById('place').value;
                fetch('/hospmap/search_place?place=' + encodeURIComponent(place))
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            alert(data.error);
                            return;
                        }
                        var table = document.getElementById('results-table');
                        // 기존 결과 제거
                        var rowCount = table.rows.length;
                        for (var i = rowCount - 1; i > 0; i--) {
                            table.deleteRow(i);
                        }
                        // 새로운 결과 추가
                        data.results.forEach(result => {
                            var row = table.insertRow();
                            var cell1 = row.insertCell(0);
                            var cell2 = row.insertCell(1);
                            var cell3 = row.insertCell(2);
                            cell1.innerHTML = result.name;
                            cell2.innerHTML = result.formatted_address;
                            cell3.innerHTML = result.formatted_phone_number || 'N/A';
                        });
                        document.getElementById('place-results').style.display = 'block';
                    })
                    .catch(error => console.error('Error:', error));
            });

        </script>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDXogd-c9vnx6zK26ZaGn5JCMv-yse98C4&callback=initMap" async defer></script>
    '''.replace('API_KEY', API_KEY)

def geocode_address(address):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(geocode_url, params=params)
    if response.status_code == 200:
        geocode_result = response.json()
        if geocode_result['status'] == 'OK':
            location = geocode_result['results'][0]['geometry']['location']
            return f"{location['lat']},{location['lng']}"
        else:
            return None
    else:
        return None

@bp.route('/get_directions')
def get_directions():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return "출발지와 목적지를 입력해주세요.", 400

    # 출발지와 도착지 주소를 지오코딩하여 좌표로 변환
    origin_coords = geocode_address(origin)
    destination_coords = geocode_address(destination)

    if not origin_coords or not destination_coords:
        return "출발지와 목적지의 주소를 확인해주세요.", 400

    # Google Maps Directions API 호출
    params = {
        'origin': origin_coords,
        'destination': destination_coords,
        'key': API_KEY
    }
    response = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=params)
    
    if response.status_code == 200:
        directions = response.json()
        if directions['status'] == 'OK':
            steps = directions['routes'][0]['legs'][0]['steps']
            path = []
            for step in steps:
                start_location = step['start_location']
                end_location = step['end_location']
                path.append((start_location['lat'], start_location['lng']))
                path.append((end_location['lat'], end_location['lng']))
            return render_template_string('''
                <h2>경로</h2>
                <pre>{{ directions }}</pre>
                <div id="map" style="height: 500px; width: 100%;"></div>
                <script>
                    function initMap() {
                        var map = new google.maps.Map(document.getElementById('map'), {
                            zoom: 7,
                            center: {lat: 37.5665, lng: 126.9780} // 서울을 초기 중심으로 설정
                        });
                        var pathCoordinates = {{ path }};
                        var path = new google.maps.Polyline({
                            path: pathCoordinates.map(function(coord) { return {lat: coord[0], lng: coord[1]}; }),
                            geodesic: true,
                            strokeColor: '#FF0000',
                            strokeOpacity: 1.0,
                            strokeWeight: 2
                        });
                        path.setMap(map);
                    }
                    initMap();
                </script>
                <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDXogd-c9vnx6zK26ZaGn5JCMv-yse98C4" async defer></script>
            '''.replace('API_KEY', API_KEY), directions=directions, path=path)
        elif directions['status'] == 'ZERO_RESULTS':
            return "경로를 찾을 수 없습니다. 출발지와 목적지를 확인해주세요.", 400
        else:
            return f"Google Maps API 경로 찾기 실패: {directions['status']}<br>상세 정보: {directions}", 500
    else:
        return f"Google Maps API 호출 실패: {response.status_code}", 500
    
    
    
def get_place_details(place_id):
    details_response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params={
        'place_id': place_id,
        'fields': 'name,formatted_address,formatted_phone_number,geometry',
        'key': API_KEY
    })
    details = details_response.json()
    if details['status'] == 'OK':
        return details['result']
    return None    

@bp.route('/search_place')
def search_place():
    place = request.args.get('place')
    if not place:
        return jsonify({"error": "장소를 입력해주세요."}), 400

    # Google Maps Places API 호출
    params = {
        'query': place,
        'key': API_KEY
    }
    response = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json', params=params)
    
    if response.status_code == 200:
        places = response.json()
        if places['status'] == 'OK':
            results = places['results']
            # 전화번호 정보 추가를 위해 Place Details API 호출
            for result in results:
                place_id = result['place_id']
                details_response = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params={
                    'place_id': place_id,
                    'fields': 'name,formatted_address,formatted_phone_number,geometry',
                    'key': API_KEY
                })
                details = details_response.json()
                if details['status'] == 'OK':
                    result['formatted_phone_number'] = details['result'].get('formatted_phone_number', 'N/A')
                else:
                    result['formatted_phone_number'] = 'N/A'
            return jsonify({"results": results})
        else:
            return jsonify({"error": f"Google Maps Places API 검색 실패: {places['status']}"}), 500
    else:
        return jsonify({"error": f"Google Maps API 호출 실패: {response.status_code}"}), 500
