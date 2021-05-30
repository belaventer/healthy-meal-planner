 $(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();

    $('#category input').click(function () {
        switch($(this).val()) {
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
                // code block
            }
    });
  });

