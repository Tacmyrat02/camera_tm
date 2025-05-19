document.addEventListener('DOMContentLoaded', function() {
    if (window.cartEventBound) {
        console.log("Cart event already bound, skipping duplicate binding");
        return;
    }
    window.cartEventBound = true;

    let lastClickTime = 0;
    const debounceDelay = 2000;
    let isProcessing = false;
    let requestId = 0;

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
    const csrfToken = getCookie('csrftoken');
    console.log("CSRF Token:", csrfToken);

    // Fetch initial cart count
    $.get("/cart/count/", function(data) {
        $("#cart-count").text(data.count);
    }).fail(function() {
        console.error("Failed to fetch cart count");
    });

    // Fetch initial wishlist count
    $.get("/wishlist/count/", function(data) {
        $("#wishlist-count").text(data.count);
    }).fail(function() {
        console.error("Failed to fetch wishlist count");
    });

    $(document).off('click', '.add-to-cart-btn');
    $('.add-to-cart-btn').off('click');
    $(document).on('click', '.add-to-cart-btn', function(event) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();

        const now = Date.now();
        requestId += 1;
        const currentRequestId = requestId;

        if (now - lastClickTime < debounceDelay || isProcessing) {
            console.log("Click debounced or processing, ignoring", {
                timeSinceLastClick: now - lastClickTime,
                isProcessing,
                requestId: currentRequestId
            });
            return;
        }
        lastClickTime = now;
        isProcessing = true;

        const $button = $(this);
        const productId = $button.data('product-id');
        const variantId = $button.data('variant-id');
        const variantType = $button.data('variant-type');

        console.log("Add to Cart button clicked:", {
            productId,
            variantId,
            variantType,
            csrfToken,
            timestamp: new Date().toISOString(),
            requestId: currentRequestId,
            buttonHtml: $button.get(0).outerHTML,
            domCheck: $button.length > 0
        });

        if (!$button.length) {
            alert("Button not found in DOM.");
            isProcessing = false;
            return;
        }
        if (!productId) {
            alert("Missing product ID. Check the button's data-product-id attribute.");
            isProcessing = false;
            return;
        }
        if (!variantId) {
            alert("Missing variant ID. Check the button's data-variant-id attribute.");
            isProcessing = false;
            return;
        }
        if (!variantType) {
            alert("Missing variant type. Check the button's data-variant-type attribute.");
            isProcessing = false;
            return;
        }
        if (!csrfToken) {
            alert("CSRF token is missing. Please ensure cookies are enabled.");
            isProcessing = false;
            return;
        }
        if (!['camera', 'harddisk', 'nvr', 'switch'].includes(variantType)) {
            alert("Invalid variant type: " + variantType);
            isProcessing = false;
            return;
        }

        $.ajax({
            url: `/cart/add/${productId}/`,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'variant_type': variantType,
                'variant_id': variantId,
                'request_id': currentRequestId
            },
            success: function(response) {
                console.log("Add to Cart response:", response, { requestId: currentRequestId });
                if (response.success) {
                    $.get("/cart/count/", function(data) {
                        $("#cart-count").text(data.count);
                    }).fail(function() {
                        console.error("Failed to fetch cart count");
                    });
                    alert(response.message || "Item added to cart successfully.");
                    if (response.redirect) {
                        window.location.href = response.redirect;
                    }
                } else {
                    alert(response.error || "Failed to add item (already in cart or error).");
                }
            },
            error: function(xhr) {
                console.error("Add to Cart error:", {
                    status: xhr.status,
                    responseText: xhr.responseText,
                    requestId: currentRequestId
                });
                alert("Failed to add item to cart: " + (xhr.responseText || "Unknown error"));
            },
            complete: function() {
                isProcessing = false;
            }
        });
    });

    $(document).off('change', '.variant-dropdown');
    $(document).on('change', '.variant-dropdown', function() {
        const $dropdown = $(this);
        const itemId = $dropdown.data('item-id'); // Used on cart page
        const productId = $dropdown.data('product-id'); // Used on home/brand pages
        const variantId = $dropdown.val();
        const selectedOption = $dropdown.find('option:selected');
        const variantType = selectedOption.data('variant-type') || $dropdown.data('variant-type') || $dropdown.data('initial-variant-type');

        console.log('Variant dropdown changed:', { itemId, productId, variantId, variantType, dropdownExists: $dropdown.length > 0 });

        // Case 1: On cart page (updating an existing cart item)
        if (itemId) {
            if (!itemId || !variantId || !variantType) {
                console.error('Missing required data for variant update:', { itemId, variantId, variantType });
                alert("Cannot update variant: Missing required data.");
                $dropdown.val($dropdown.data('original-value'));
                return;
            }

            if (!csrfToken) {
                console.error('CSRF token is missing');
                alert("CSRF token is missing. Please ensure cookies are enabled.");
                $dropdown.val($dropdown.data('original-value'));
                return;
            }

            console.log('Sending AJAX request to update variant:', { url: '/cart/update-variant/', data: { item_id: itemId, variant_id: variantId, variant_type: variantType } });

            $.ajax({
                url: '/cart/update-variant/',
                type: 'POST',
                data: {
                    'item_id': itemId,
                    'variant_id': variantId,
                    'variant_type': variantType,
                    'csrfmiddlewaretoken': csrfToken
                },
                success: function(response) {
                    console.log('AJAX success response:', response);
                    if (response.success) {
                        const $cartItem = $dropdown.closest('.cart-item');
                        const variantDetails = response.variant_details;

                        $cartItem.find('.spec-value').text(variantDetails.spec);
                        $cartItem.find('.price-value').text(variantDetails.price.toFixed(2));
                        $cartItem.find('.subtotal-value').text(variantDetails.subtotal.toFixed(2));
                        $('#total-price').text(response.total_price.toFixed(2));
                    } else {
                        console.error('Error in response:', response.error);
                        alert(response.error || "Failed to update variant.");
                        $dropdown.val($dropdown.data('original-value'));
                    }
                },
                error: function(xhr, status, error) {
                    console.error('AJAX error:', status, error, xhr.responseText);
                    alert("Failed to update variant: " + (xhr.responseText || "Unknown error"));
                    $dropdown.val($dropdown.data('original-value'));
                }
            });
        } else if (productId) {
            // Case 2: On home/brand page (updating the Add to Cart button)
            const price = selectedOption.data('price');
            const stock = selectedOption.data('stock');
            const $productItem = $dropdown.closest('.product-item');
            $productItem.find('.price').text('$' + price.toFixed(2));
            $productItem.find('.add-to-cart-btn')
                .attr('data-variant-id', variantId)
                .attr('data-variant-type', variantType);

            // Update the displayed spec (e.g., resolution, capacity)
            const specType = $productItem.find('.resolution').data('type');
            let specValue = '';
            if (specType === 'resolution') {
                specValue = selectedOption.text().split(' - ')[0];
            } else if (specType === 'capacity') {
                specValue = selectedOption.text().split(' - ')[0];
            } else if (specType === 'channels') {
                specValue = selectedOption.text().split(' - ')[0];
            }
            $productItem.find('.resolution').html('<strong>' + specValue + '</strong>');
        }
    });

    $(document).off('change', '.quantity-input');
    $(document).on('change', '.quantity-input', function() {
        const $input = $(this);
        const itemId = $input.data('item-id');
        const newQuantity = $input.val();

        console.log('Quantity changed:', { itemId, newQuantity });

        $.ajax({
            url: '/cart/update-quantity/',
            type: 'POST',
            data: {
                'item_id': itemId,
                'quantity': newQuantity,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                console.log('AJAX success response:', response);
                if (response.success) {
                    const $cartItem = $input.closest('.cart-item');
                    $cartItem.find('.subtotal-value').text(response.subtotal.toFixed(2));
                    $('#total-price').text(response.total_price.toFixed(2));
                } else {
                    console.error('Error in response:', response.error);
                    alert(response.error || "Failed to update quantity.");
                    $input.val($input.data('original-value'));
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error, xhr.responseText);
                alert("Failed to update quantity: " + (xhr.responseText || "Unknown error"));
                $input.val($input.data('original-value'));
            }
        });
    });

    $(document).off('click', '.remove-btn');
    $(document).on('click', '.remove-btn', function() {
        const $button = $(this);
        const itemId = $button.data('item-id');

        console.log('Remove button clicked:', { itemId });

        $.ajax({
            url: '/cart/remove/',
            type: 'POST',
            data: {
                'item_id': itemId,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                console.log('AJAX success response:', response);
                if (response.success) {
                    $button.closest('.cart-item').remove();
                    let totalPrice = 0;
                    $('.subtotal-value').each(function() {
                        totalPrice += parseFloat($(this).text()) || 0;
                    });
                    $('#total-price').text(totalPrice.toFixed(2));
                    $.get("/cart/count/", function(data) {
                        $("#cart-count").text(data.count);
                    }).fail(function() {
                        console.error("Failed to fetch cart count");
                    });
                    alert(response.message || "Item removed from cart.");
                } else {
                    console.error('Error in response:', response.error);
                    alert(response.error || "Failed to remove item.");
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error, xhr.responseText);
                alert("Failed to remove item: " + (xhr.responseText || "Unknown error"));
            }
        });
    });

    $('.variant-dropdown').each(function() {
        $(this).data('original-value', $(this).val());
        console.log('Initialized variant dropdown:', { id: $(this).attr('id'), originalValue: $(this).val() });
    });

    $('.quantity-input').each(function() {
        $(this).data('original-value', $(this).val());
    });

    $(document).off('click', 'click-debugger');
    $(document).on('click', 'click-debugger', function(event) {
        console.log("Document click detected:", {
            target: event.target.tagName + (event.target.className ? '.' + event.target.className : ''),
            timestamp: new Date().toISOString(),
            eventType: event.type
        });
    });
});