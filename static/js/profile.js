 $(function() {
            $( "#accordion-6" ).accordion({
                  create: function (event, ui) {
                     $("span#result").html ($("span#result").html () + "<b>Created</b><br>");
                 },
                  beforeActivate : function (event, ui)
                  {
                     $("span#result").html ($("span#result").html () + ", <b>beforeActivate</b><br>");
                  },
                  activate: function (event, ui) {
                     $("span#result").html ($("span#result").html () + "<b>activate</b><br>");
                  }
            });
         });