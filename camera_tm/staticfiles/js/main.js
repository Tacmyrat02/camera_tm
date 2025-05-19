$(document).ready(function() {
    // Function to get CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Set up CSRF token for all AJAX requests
    const csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Add to Cart
    $(".add-to-cart").click(function() {
        const variantId = $(this).data("variant-id");
        const variantType = $(this).data("variant-type");
        $.ajax({
            url: `/add_to_cart/${variantId}/`,
            method: "POST",
            data: {
                variant_type: variantType
            },
            success: function() {
                alert("Item added to cart successfully!");
                location.reload();
            },
            error: function(xhr) {
                alert("Failed to add to cart: " + xhr.responseText);
            }
        });
    });

    // Update Cart Quantity
    $(".quantity-input").change(function() {
        const itemId = $(this).data("item-id");
        const quantity = $(this).val();
        $.ajax({
            url: "{% url 'update_cart_quantity' %}",
            method: "POST",
            data: {
                item_id: itemId,
                quantity: quantity
            },
            success: function() {
                alert("Cart updated successfully!");
                location.reload();
            },
            error: function(xhr) {
                alert("Failed to update cart: " + xhr.responseText);
            }
        });
    });

    // Add to Wishlist
    $(".add-to-wishlist").click(function() {
        const productId = $(this).data("product-id");
        $.ajax({
            url: `/wishlist/add/${productId}/`,
            method: "POST",
            success: function(data) {
                alert(data.message);
                $.get("{% url 'get_wishlist_count' %}", function(data) {
                    $("#wishlist-count").text(data.count);
                });
            },
            error: function(xhr) {
                alert("Error: " + xhr.responseJSON.message);
            }
        });
    });

    // Remove from Wishlist
    $(".remove-from-wishlist").click(function() {
        const productId = $(this).data("product-id");
        $.ajax({
            url: `/wishlist/remove/${productId}/`,
            method: "POST",
            success: function(data) {
                alert(data.message);
                location.reload();
            },
            error: function(xhr) {
                alert("Error: " + xhr.responseJSON.message);
            }
        });
    });
});
// Add to Cart
$(".add-to-cart").click(function() {
    const variantId = $(this).data("variant-id");
    const variantType = $(this).data("variant-type");
    $.ajax({
        url: `/add_to_cart/${variantId}/`,
        method: "POST",
        data: { variant_type: variantType },
        success: function() {
            alert("Item added to cart successfully!");
            $.get(cartCountUrl, function(data) {
                $("#cart-count").text(data.count);
            });
            location.reload();
        },
        error: function(xhr) {
            alert("Failed to add to cart: " + xhr.responseText);
        }
    });
});

// Update Cart Quantity
$(".quantity-input").change(function() {
    const itemId = $(this).data("item-id");
    const quantity = $(this).val();
    $.ajax({
        url: "{% url 'update_cart_quantity' %}",
        method: "POST",
        data: { item_id: itemId, quantity: quantity },
        success: function() {
            alert("Cart updated successfully!");
            location.reload();
        },
        error: function(xhr) {
            alert("Failed to update cart: " + xhr.responseText);
        }
    });
});

// Add to Wishlist
$(".add-to-wishlist").click(function() {
    const productId = $(this).data("product-id");
    $.ajax({
        url: `/wishlist/add/${productId}/`,
        method: "POST",
        success: function(data) {
            alert(data.message);
            $.get(wishlistCountUrl, function(data) {
                $("#wishlist-count").text(data.count);
            });
        },
        error: function(xhr) {
            alert("Error: " + xhr.responseJSON.message);
        }
    });
});

// Remove from Wishlist
$(".remove-from-wishlist").click(function() {
    const productId = $(this).data("product-id");
    $.ajax({
        url: `/wishlist/remove/${productId}/`,
        method: "POST",
        success: function(data) {
            alert(data.message);
            location.reload();
        },
        error: function(xhr) {
            alert("Error: " + xhr.responseJSON.message);
        }
    });
});
// Add to Cart
$(".add-to-cart").click(function() {
    const $dropdown = $(this).closest('.product-item').find('.variant-dropdown');
    const variantId = $dropdown.val();
    const variantType = $(this).data("variant-type");
    $.ajax({
        url: `/add_to_cart/${variantId}/`,
        method: "POST",
        data: { variant_type: variantType },
        success: function() {
            alert("Item added to cart successfully!");
            $.get(cartCountUrl, function(data) {
                $("#cart-count").text(data.count);
            });
            location.reload();
        },
        error: function(xhr) {
            alert("Failed to add to cart: " + xhr.responseText);
        }
    });
});