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
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        let filter_object = {}

        let min_price =$("#max_price").attr("min")
        let max_price =$("#max_price").val()
        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

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

    $("#max_price").on("blur", function(){

        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        //console.log("Crurrent Price is:", current_price);
        //console.log("Max Price is:", min_price);
        //console.log("Min Price is:", max_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            //console.log("Price Error Occured");

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            //console.log("Max Price is:", min_Price);
            //console.log("Min Price is:", max_Price);

            alert("Price must be between $"+ min_price+' and $'+ max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()

            return false
            

        }

        
    })


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
    })

    $(document).on("click", '.delete-product', function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        console.log("PRoduct ID:", product_id);
        
        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id":product_id
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
                location.reload();

            }
        })
    })

    $(document).on("click", '.update-product', function(){
    
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()
    
        console.log("Product ID:", product_id);
        console.log("Quantity: ", product_quantity);
    
    
        
        $.ajax({
            url: "/update-cart",
            data:{
                "id": product_id,
                "qty": product_quantity,
    
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
                location.reload();
        }
    })
    })


    //making default addresses
    $(document).on("click", ".make-default-address", function(){
        let id = $(this).attr("data-address-id")
        let this_val = $(this)

        console.log("ID is:", id);
        console.log("Element is:", this_val);

        $.ajax({
            url : "/make-default-address",
            data: {
                "id":id
            },
            dataType: "json",
            success: function(response){
                console.log("Address Made Dedault.....");
                if (response.boolean == true){
                    $(".check").hide()
                    $(".action_btn").show()

                    $(".check"+id).show()
                    $(".button"+id).hide()
                }
            }
        })
    
    })

    //Add items to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)

        console.log("product id is:", product_id);

        $.ajax({
            url: "/add-to-wishlist",
            data: {
                "id":product_id
            },
            dataType: "json",

            beforeSend: function(){
                console.log("Adding to wishlist ...")
            },
            success: function(response){
                this_val.html("✔")
                if (response.bool === true) {
                    console.log("Added to wishlist...")
                location.reload();
                }
            }
        })
    }) 
    //remove from wishlist-product
    $(document).on("click", '.delete-wishlist-product', function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)
        console.log("whishlist id is:", wishlist_id);
        
        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id":wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $("#wishlist-list").html(response.data)
                //location.reload();
            }
        })
    })
    
    
    $(document).on("submit", "#contact-form-ajax", function (e) {
        e.preventDefault()
        console.log("submited....");

        let full_name =$("#full_name").val()
        let email =$("#email").val()
        let phone  =$("#phone").val()
        let subject =$("#subject").val()
        let message =$("#message").val()

        console.log("name:",full_name);
        console.log("email:",email);
        console.log("phone:",phone );
        console.log("subject:",subject);
        console.log("message:",message);

        $.ajax({
            url:"/ajax-contact-form",
            data : {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
                

            },
            dataType:"json",
            beforeSend:function(){
                console.log("sending data to server ....");
            },
            success : function(res){
                console.log("sent data to server!");
                $("#contact-form-ajax").hide()
                $("#contact-response").html("message sent successfuly")
            }
        })
    })

})