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
// ... other code ...

  // Assuming this is around line 150, part of the add_to_wishlist AJAX success handler
  function addToWishlist(productId) {
      var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
      if (!csrfToken) {
          console.error('CSRF token not found');
          alert('Error: Missing CSRF token');
          return;
      }

      $.ajax({
          url: '/wishlist/add/' + productId + '/',
          type: 'POST',
          data: {
              'csrfmiddlewaretoken': csrfToken
          },
          success: function(response) {
              if (response.success) {
                  alert(response.message || 'Product added to wishlist.');
                  // Update wishlist count
                  if (typeof wishlistCountUrl !== 'undefined') {
                      $.get(wishlistCountUrl, function(data) {
                          $('#wishlist-count').text(data.count);
                      });
                  } else {
                      console.error('wishlistCountUrl is not defined');
                      alert('Error: Unable to update wishlist count');
                  }
              } else {
                  alert(response.error || 'Failed to add product to wishlist.');
              }
          },
          error: function(xhr, status, error) {
              console.error('AJAX error:', status, error, xhr.responseText);
              alert('Error: ' + (xhr.responseText || 'An unexpected error occurred'));
          }
      });
  }

  // Event listener for add to wishlist buttons
  $(document).ready(function() {
      $('.add-to-wishlist-btn').on('click', function(e) {
          e.preventDefault();
          var productId = $(this).data('product-id');
          if (productId) {
              addToWishlist(productId);
          } else {
              console.error('Product ID not found');
              alert('Error: Missing product ID');
          }
      });
  });

  // ... other code ...
  // ... other code ...

  function addToWishlist(productId) {
      var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
      if (!csrfToken) {
          console.error('CSRF token not found');
          alert('Error: Missing CSRF token');
          return;
      }

      $.ajax({
          url: '/wishlist/add/' + productId + '/',
          type: 'POST',
          data: {
              'csrfmiddlewaretoken': csrfToken
          },
          success: function(response) {
              if (response.success) {
                  alert(response.message || 'Product added to wishlist.');
                  // Update wishlist count
                  if (typeof wishlistCountUrl !== 'undefined') {
                      $.get(wishlistCountUrl, function(data) {
                          $('#wishlist-count').text(data.count);
                      }).fail(function(jqXHR, textStatus, errorThrown) {
                          console.error('Failed to update wishlist count:', textStatus, errorThrown);
                          alert('Error: Unable to update wishlist count');
                      });
                  } else {
                      console.error('wishlistCountUrl is not defined');
                      alert('Error: Unable to update wishlist count');
                  }
              } else {
                  alert(response.error || 'Failed to add product to wishlist.');
              }
          },
          error: function(xhr, status, error) {
              console.error('AJAX error:', status, error, xhr.responseText);
              alert('Error: ' + (xhr.responseText || 'An unexpected error occurred'));
          }
      });
  }

  $(document).ready(function() {
      $('.add-to-wishlist-btn').on('click', function(e) {
          e.preventDefault();
          var productId = $(this).data('product-id');
          if (productId) {
              addToWishlist(productId);
          } else {
              console.error('Product ID not found');
              alert('Error: Missing product ID');
          }
      });
  });

  // ... other code ...
  $(document).ready(function() {
    $('.add-to-cart-btn').on('click', function(e) {
        e.preventDefault();
        var variantId = $(this).data('variant-id');
        var variantType = $(this).data('variant-type');
        if (variantId && variantType) {
            addToCart(variantId, variantType);
        } else {
            console.error('Variant ID or type not found');
            alert('Error: Missing variant ID or type');
        }
    });

    function addToCart(variantId, variantType) {
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        if (!csrfToken) {
            console.error('CSRF token not found');
            alert('Error: Missing CSRF token');
            return;
        }

        $.ajax({
            url: '/cart/add/' + variantId + '/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'variant_type': variantType
            },
            success: function(response) {
                if (response.success) {
                    alert(response.message || 'Product added to cart.');
                    $.get('/cart/count/', function(data) {
                        $('#cart-count').text(data.count);
                    });
                } else {
                    alert(response.error || 'Failed to add product to cart.');
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX error:', status, error, xhr.responseText);
                alert('Error: ' + (xhr.responseText || 'An unexpected error occurred'));
            }
        });
    }
});