document.addEventListener('DOMContentLoaded', function() {
    $(document).on('click', '.remove-btn', function(event) {
        event.preventDefault();
        event.stopPropagation();

        const $button = $(this);
        const itemId = $button.data('item-id');
        const cartCountUrl = "/cart/count/";

        $button.prop('disabled', true);

        $.ajax({
            url: `/cart/remove/${itemId}/`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    $button.closest('.cart-item').remove();
                    $.get(cartCountUrl, function(data) {
                        $("#cart-count").text(data.count);
                    }).fail(function() {
                        console.error("Failed to fetch cart count");
                    });
                    $('.cart-total h3').text(`{% trans "Total" %} : $${response.total_price}`);
                    alert("Item removed from cart!");
                    if ($('.cart-item').length === 0) {
                        $('.cart-items').html('<p>{% trans "Your cart is empty." %}</p>');
                    }
                } else {
                    alert("Failed to remove item.");
                }
            },
            error: function(xhr) {
                alert("Failed to remove item: " + xhr.responseText);
            },
            complete: function() {
                $button.prop('disabled', false);
            }
        });
    });
});