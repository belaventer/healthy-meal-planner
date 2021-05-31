 $(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();

    hideOptions($('#category input:checked'))
    $('#category input').click(function () {
        hideOptions($(this));
    });

    function hideOptions(selected_category)  {
        switch($(selected_category).val()) {
            case "breakfast":
                    $("#grain").parent().parent().removeClass("hide-option")
                    $("#vegetables").parent().parent().addClass("hide-option")
                    $("#fruit").parent().parent().removeClass("hide-option")
                    $("#fat").parent().parent().removeClass("hide-option")
                    $("#carbohydrate").parent().parent().addClass("hide-option")
                break;
            case "lunch":
                    $("#grain").parent().parent().removeClass("hide-option")
                    $("#vegetables").parent().parent().removeClass("hide-option")
                    $("#fruit").parent().parent().removeClass("hide-option")
                    $("#fat").parent().parent().removeClass("hide-option")
                    $("#carbohydrate").parent().parent().addClass("hide-option")
                break;
            case "dinner":
                    $("#grain").parent().parent().removeClass("hide-option")
                    $("#vegetables").parent().parent().removeClass("hide-option")
                    $("#fruit").parent().parent().addClass("hide-option")
                    $("#fat").parent().parent().removeClass("hide-option")
                    $("#carbohydrate").parent().parent().addClass("hide-option")
                break;
            case "snack":
                    $("#grain").parent().parent().addClass("hide-option")
                    $("#vegetables").parent().parent().addClass("hide-option")
                    $("#fruit").parent().parent().addClass("hide-option")
                    $("#fat").parent().parent().addClass("hide-option")
                    $("#carbohydrate").parent().parent().removeClass("hide-option")
                break;
            default:
                    $("#grain").parent().parent().removeClass("hide-option")
                    $("#vegetables").parent().parent().addClass("hide-option")
                    $("#fruit").parent().parent().removeClass("hide-option")
                    $("#fat").parent().parent().removeClass("hide-option")
                    $("#carbohydrate").parent().parent().addClass("hide-option")
            }
    }

    // AJAX use example from: https://stackoverflow.com/questions/13808187/how-can-i-call-a-specific-function-method-in-a-python-script-from-javascriptjqu
    $('a i.fa-minus').click(function () {
        if (window.confirm("The servign will be deleted. Do you want to proceed?")) {
            $.ajax({
                url: "/delete_serving/" + $(this).attr('data-id'),
                type: "get",
                success: function(){
                    location.reload();
                }
                });                
        }
    });
  });

