 let week = [
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday"
        ];

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

    $('#week-selector h5').html(weekDays(new Date()))
        .attr("date-picked", formatDate(new Date()));

    $('#previous-week').click( function() {
            var date = new Date($('#week-selector h5').attr("date-picked"));
            var prevDate = new Date();

            prevDate = prevDate.setTime(date.getTime() - 7*24*3600*1000);

            $('#week-selector h5').html(weekDays(new Date(prevDate)))
                .attr("date-picked", formatDate(new Date(prevDate)));
        }
    );

    $('#next-week').click( function() {
            var date = new Date($('#week-selector h5').attr("date-picked"));
            var nextDate = new Date();

            nextDate = nextDate.setTime(date.getTime() + 7*24*3600*1000);

            $('#week-selector h5').html(weekDays(new Date(nextDate)))
                .attr("date-picked", formatDate(new Date(nextDate)));
        }
    );

    function formatDate(date){
        return new Intl.DateTimeFormat('en-GB', {year:"numeric", month: "short", day: "2-digit"}).format(date)
    }

    function weekDays(date){
        var weekStart = new Date(date.getDay() == 0 ? date : date - date.getDay()*24*60*60*1000);
        var weekEnd = new Date();

        weekEnd = weekEnd.setTime(weekStart.getTime() + 6*24*3600*1000);

        for (var i = 0; i < week.length; i++){
            var start = new Date();

            $("#"+week[i]).html(formatDate(start.setTime(weekStart.getTime() + i*24*3600*1000)));
            $("#modal_title_"+week[i]).html(formatDate(start));
            $("#modal-"+week[i]).attr('action',
                `/submit_plan/${formatDate(weekStart).replace(/ /g,"%20")}%20to%20${formatDate(weekEnd).replace(/ /g,"%20")}/${formatDate(start).replace(/ /g,"%20")}`);
            $("#"+week[i]).next().html("No plan set for the day!");
            $("#modal-"+week[i]+" label strong").map(function (){
                $(this).parent().prev().attr("checked", false);
            });
            get_week_plan(formatDate(start));
        }
            
        $('.modal').modal();

        return `${formatDate(weekStart)} to ${formatDate(weekEnd)}`
    }

    function get_week_plan (week) {
        $.ajax({
            url: "/get_week_plan/" + week,
            type: "get",
            success: function(data){
                    let week = [
                        "sunday",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday"
                    ];

                if (JSON.parse(data) !== null) {
                    var meals = JSON.parse(data)
                    var day = new Date(meals["day"]).getDay()

                    var selectedMeals = "";
                    for (meal in meals["selected_meals"]){
                        selectedMeals = selectedMeals + `<p class="z-depth-1"><strong>${meal}: </strong>${meals["selected_meals"][meal]}</p>`
                    }
                    $("#"+week[day]).next().html(selectedMeals);

                    $("#modal-"+week[day]+" label strong").map(function (){
                        if (Object.values(meals["selected_meals"]).
                            includes(this.innerHTML)){
                                $(this).parent().prev().attr("checked", true);
                        }
                    });
                }
            }
        })
    }
    
});