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

         function MyFunction()
         {
            if (document.getElementById("edit").className == "glyphicon glyphicon-edit")
               {
      	        // document.getElementById("edit").className ="glyphicon glyphicon-ok";
      	        document.getElementById("ok").style.display="block";
      	        document.getElementById("edit").style.display="none";
      	        document.getElementById("edit").id="MCQ";
               }
            else if(document.getElementById("ok").className == "glyphicon glyphicon-ok")
               {
      	        // document.getElementById("MCQ").className ="glyphicon glyphicon-edit";
      	        // // document.getElementById("MCQ").id="MCQ";
      	        // document.getElementById("MCQ").id="edit";
      		    document.getElementById("ok").style.display="block";
               }
         }