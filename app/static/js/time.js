function current() {
    var monthNames;
    var day_list = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];
    var current_time;
    var d = new Date();
    current_time = day_list[d.getDay()] + ", " + monthNames[d.getMonth()] + " " + d.getDate();
    document.write(current_time);
    $.ajax({
        url: "/",
        data: monthNames[d.getMonth()],
        type: "POST",
        traditional: true,    // 需要传递列表、字典时加上这句
        success: function () {
        },
        fail: function () {
        }
    });
}


function current_time(){
    var d = new Date();
    var hours,minutes;
    hours = d.getHours();
    minutes = d.getMinutes();
    if(minutes < 10)
        {
            document.write(hours+" : 0"+ minutes);
        }
    else {
        document.write(hours+":"+minutes);
    }

}


