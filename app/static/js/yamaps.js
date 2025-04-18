ymaps.ready(init);

function init() {
    let myMap = new ymaps.Map("map", {
        center: [51.08, 71.26],
        zoom: 10,
        controls: ['zoomControl', 'typeSelector', 'fullscreenControl']
    });

    // поиск
    let searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#search',
            float: 'right',
            noPlacemark: true
        }
    });
    myMap.controls.add(searchControl);

    // метка
    let placemark = new ymaps.Placemark([51.08, 71.26], {
        balloonContent: 'Астана'
    }, {
        preset: 'islands#redDotIcon',
        draggable: true
    });
    myMap.geoObjects.add(placemark);

    // Обработка поиска по кнопке
    document.getElementById('searchButton').addEventListener('click', function() {
        searchLocation();
    });

    // Обработка нажатия Enter в поле поиска
    document.getElementById('search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchLocation();
        }
    });

    // Функция поиска местоположения
    function searchLocation() {
        const address = document.getElementById('search').value;
        if (!address) return;

        // Используем геокодер Яндекс Карт
        ymaps.geocode(address).then(function(res) {
            let firstGeoObject = res.geoObjects.get(0);
            
            if (firstGeoObject) {
                // Получаем координаты найденного объекта
                let coords = firstGeoObject.geometry.getCoordinates();
                
                // Перемещаем карту к найденному объекту
                myMap.setCenter(coords, 15);
                
                // Перемещаем метку
                placemark.geometry.setCoordinates(coords);
                
                // Отображаем балун с информацией
                placemark.properties.set('balloonContent', firstGeoObject.getAddressLine());
                placemark.balloon.open();
            } else {
                alert('Место не найдено');
            }
        }).catch(function(error) {
            console.error('Ошибка геокодирования:', error);
            alert('Произошла ошибка при поиске');
        });
    }

    // Обработка клика по карте для установки метки
    myMap.events.add('click', function(e) {
        const coords = e.get('coords');
        
        // Перемещаем метку
        placemark.geometry.setCoordinates(coords);
        
        // Получаем информацию о месте по координатам
        ymaps.geocode(coords).then(function(res) {
            let firstGeoObject = res.geoObjects.get(0);
            if (firstGeoObject) {
                placemark.properties.set('balloonContent', firstGeoObject.getAddressLine());
                placemark.balloon.open();
            } else {
                placemark.properties.set('balloonContent', 'Координаты: ' + coords[0].toFixed(5) + ', ' + coords[1].toFixed(5));
                placemark.balloon.open();
            }
        });
    });

    // При перетаскивании метки обновляем информацию
    placemark.events.add('dragend', function() {
        const coords = placemark.geometry.getCoordinates();
        
        ymaps.geocode(coords).then(function(res) {
            let firstGeoObject = res.geoObjects.get(0);
            if (firstGeoObject) {
                placemark.properties.set('balloonContent', firstGeoObject.getAddressLine());
                placemark.balloon.open();
            }
        });
    });
}