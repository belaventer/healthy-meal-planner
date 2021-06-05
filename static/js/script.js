 $(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.tooltipped').tooltip();
    $('.collapsible').collapsible();
    $('select').formSelect();

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
        if (window.confirm("The item will be deleted. Do you want to proceed?")) {
            $.ajax({
                url: "/delete_item/" + $(this).attr('data-collection') + "/" + $(this).attr('data-id'),
                type: "get",
                success: function(){
                    location.reload();
                }
            });                
        }
    });

    $('input[name="meal_category"]').click(function() {
        $.ajax({
            url: "/get_serving_options/" + $(this).attr('id'),
            type: "get",
            data: {},
            success: function(data){
                var list_categories = "";
                var servings = JSON.parse(data);
                var colours = {
                    "protein": "red darken-4",
                    "carbohydrate": "red darken-4",
                    "grain": "yellow darken-4",
                    "fat": "orange darken-4",
                    "fruit": "blue darken-4",
                    "vegetables": "green darken-4"
                }

                for (key in servings[1]) {
                    var list_options = "";
                    var list_servings = "";

                    // Explanation for iterating on objects from https://stackoverflow.com/questions/19529403/javascript-loop-through-object-array
                    for (var i = 0, l = servings[0].length; i < l; i++) {
                        var serving = servings[0][i];
                        if (serving.category.split("_").pop() == key) {
                            list_servings = list_servings +
                                `<option value="${serving._id}">${serving.quantity} ${serving.engineering_unit} ${serving.ingredient}</option>`;
                        }
                    }

                    for (var i = 0, l = servings[1][key]; i < l; i++) {
                        list_options = list_options +
                            `<div class="input-field">
                                <select id="${key}_${i + 1}" name="${key}_${i + 1}" class="validate" required>
                                    <option value="" disabled selected>Select Serving</option>
                                    ${list_servings}
                                </select>
                                <label for="serving_${i + 1}">Serving ${i + 1}</label>
                            </div>`;
                    }

                    list_categories = list_categories +
                        `<ul class="collapsible white-text">
                            <li>
                            <div class="collapsible-header ${colours[key]}">
                                <strong class="white-text">
                                    ${key[0].toUpperCase() + key.slice(1)}
                                </strong>
                            </div>
                            <div class="collapsible-body">
                                <ul>
                                    ${list_options}
                                </ul>
                            </div>
                            </li>
                        </ul>`;
                }

                $("#new-content").html(
                    list_categories
                )

                $('.collapsible').collapsible();
                $('select').formSelect();
                validateMaterializeSelect();
            }
        });
    });

    // Custom validation taken from Code Instute Task Manager LMS
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});