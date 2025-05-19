document.addEventListener('DOMContentLoaded', function() {
    $('.remove-wishlist-btn').on('click', function(e) {
        e.preventDefault();
        const productId = $(this).data('product-id');
        const $form = $(this).closest('form');
        const csrfToken = $form.find('input[name=csrfmiddlewaretoken]').val();

        if (!productId || !csrfToken) {
            console.error('Missing productId or csrfToken:', { productId, csrfToken });
            alert('Error: Missing required data');
            return;
        }

        $.ajax({
            url: `/wishlist/remove/${productId}/`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $(`#wishlist-item-${productId}`).remove();
                    $.get('/wishlist/count/', function(data) {
                        $('#wishlist-count').text(data.count);
                    });
                    alert(response.message || 'Product removed from wishlist.');
                } else {
                    alert(response.error || 'Failed to remove product.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error, xhr.responseText);
                alert('Error: ' + (xhr.responseText || 'An unexpected error occurred'));
            }
        });
    });
});