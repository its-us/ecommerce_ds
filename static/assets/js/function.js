console.log("working fine");

const monthNames = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault();
    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();


    $.ajax({
        data : $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved to DB...")

            if(res.bool == true){
                $("#review-res").html("Review added successfullt.");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<div class="single-comment justify-content-between d-flex">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg" alt="">'
                    _html += '<h6><a href="#"> '+ res.context.user +' </a></h6>'
                    _html += '<p class="font-xxs">Since 2012</p>'
                    _html += '</div>'

                    _html += '<div class="desc">'

                    for(var i=1; i<=res.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }

                    
                    _html += '<p> '+ res.context.review +' </p>'
                    _html += '<div class="d-flex justify-content-between">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<p class="font-xs mr-30"> {{r.date|date:"d M, Y"}} </p>'
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html)
            }
        }
    });

});

console.log("working fine");

$("#commentForm").submit(function(e){
    e.preventDefault(); // prevent default submit behaviour
   
    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function (res) {
            console.log("Comment Saved to DB...");


            if (res.bool == true){
                $("#review-res").html("Review added successfully.")
                
            }

        }

    })


})


$(document).ready(function(){
    $(".loader").hide()
    $(".filter-checkbox").on("click", function(){
        let filter_object = {}
            $(".filter-checkbox").each(function(index) {
                let filter_value = $(this).val()
                let filter_key = $(this).data("filter")
                
                //console.log(filter_value, filter_key);
                filter_object[filter_key] =
                    Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(element){
                        return element.value
                })
            })
            console.log(filter_object);
            $.ajax({
                url : '/filter-products',
                data : filter_object,
                dataType:'json',
                beforeSend: function(){
                    console.log("Trying to filter products ...");

                },
                success: function(response){
                    console.log(response);
                    console.log("Data filtred successfully...");
                    $("#filtered-products").html(response.data)
                }
            })
    })
});

// Au clic sur le bouton "Add to cart"
$(".add-to-cart-btn").on("click", function() {
    let this_val = $(this) 
    let index = this_val.attr("data-index")
    // Récupérer les informations du produit
    let quantity = $(".product-quantity-" + index).val() //modifihadi wsf
    let product_title= $(".product-title-" + index).val() 
    let product_id = $(".product-id-" + index).val() 
    let product_price = parseFloat($(".current-product-price-" + index).text().replace('$', ''));
    let total = product_price * parseInt(quantity);
    let product_pid = $(".product-pid-" + index).val()
    let product_image = $(".product-image-" + index).val()
   

    // Afficher les informations dans la console
   
    console.log("Title:", product_title);
    console.log("ID:", product_id);
    console.log("Quantity:", quantity);
    console.log("Price:", product_price);
    console.log("Total Price:", total);
    console.log("PID:", product_pid);
    console.log("Image:", product_image);
    console.log("Index:", index);
    console.log("Current Element:", this_val);


    // Ajouter le produit au panier ou à votre logique spécifique ici
    // ...

    // Ne pas oublier d'empêcher le formulaire de se soumettre
   

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id': product_id,
            'pid':product_pid,
            'image':product_image,
            'qty': quantity,
            'title': product_title,
            'price': product_price,

        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding Product to Cart ...");

        },
        success: function(response){
            this_val.html("✔")
            console.log("Added Product to Cart!");
            $(".cart-items-count").text(response.totalcartitems)
 
        }

    })
});