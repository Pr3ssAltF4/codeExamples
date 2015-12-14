$(document).ready(function() {
            // page is now ready, initialize the calendar...
            var events={}
            var appointmentList = $("apt");
            for(x=0; x < appointmentList.length;x++){
                $("apt").hide();
                alert(appointmentList[x]);
                events = {
                    title:appointmentList[x],
                    start:appointmentList[x+1]
                }
                 alert(appointmentList.length);

            }
            $('#calendar').fullCalendar({
                /*events: function(callback) {
                $.get($("a").attr("href"), function(data){
                var list = data.slice(190,202);
                alert(list);

                events.push({
                    title:"list",
                    start:"2015-10-26"
                })

                 });
                }*/
                header:{
                    left:"prev, next today",
                    center:"title",
                    right:"month, agendaWeek, agendaDay"
                },
                events:[
                    {
                        title  : document.getElementsByClassName("apt")[0].text,
                        start  : document.getElementsByClassName("apt")[1].text
                    }
                ],

                });

            });