let week = [
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday"
        ];

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
    return new Intl.DateTimeFormat('en-GB', {year:"numeric", month: "short", day: "2-digit"}).format(date);
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
        $("#groceries-button").attr('href',
            `/get_groceries/${formatDate(weekStart).replace(/ /g,"%20")}%20to%20${formatDate(weekEnd).replace(/ /g,"%20")}`);
        $("#"+week[i]).next().html("No plan set for the day!");
        $("#modal-"+week[i]+" label strong").map(function (){
            $(this).parent().prev().attr("checked", false);
        });
        get_week_plan(formatDate(start));
    }
        
    $('.modal').modal();

    return `${formatDate(weekStart)} to ${formatDate(weekEnd)}`;
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
                var meals = JSON.parse(data);
                var day = new Date(meals.day).getDay();

                var selectedMeals = "";
                for (var meal in meals.selected_meals){
                    selectedMeals = selectedMeals + `<p class="z-depth-1"><strong>${meal}: </strong>${meals.selected_meals[meal]}</p>`;
                }
                $("#"+week[day]).next().html(selectedMeals);

                $("#modal-"+week[day]+" label strong").map(function (){
                    if (Object.values(meals.selected_meals).
                        includes(this.innerHTML)){
                            $(this).parent().prev().attr("checked", true);
                    }
                });
            }
        }
    });
}