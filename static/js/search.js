// static/js/search.js
$(document).ready(function() {
    $('#search-input').on('keyup', function() {
        let query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: '/ajax/search/',
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    $('#search-results').empty();
                    if (data.length > 0) {
                        data.forEach(function(item) {
                            $('#search-results').append(
                                `<a href="/products/${item.id}/" class="list-group-item list-group-item-action d-flex align-items-center">
                                    <img src="${item.image_url}" alt="${item.name}" class="img-thumbnail me-2" style="width: 50px; height: 50px;">
                                    <span>${item.name} - ${item.price.toFixed(2)} zł</span>
                                </a>`
                            );
                        });
                    } else {
                        $('#search-results').append(
                            `<div class="list-group-item">Brak wyników</div>`
                        );
                    }
                }
            });
        } else {
            $('#search-results').empty();
        }
    });
});
