/*------------Searching Function-----------------*/
        $(document).ready(function(){ 
            $("#search").keyup(function() {
                var value = this.value;      
                $("table").find("tr").each(function(index) {  
                    if (index === 0) return;
                    var id = $(this).find("td").first().text();
                    $(this).toggle(id.indexOf(value) !== -1);
                });
            });
        });

/*------------Puppet Start-----------------*/
			$(function(){
				$("#start").click(function(){
					$.get("/puppetrun", {cn:'{{cname}}'}, function(data){
						$("#output").html("Puppet started with process id " + data);
						 document.getElementById("start").disabled = true;
        				 document.getElementById("stop").disabled = false;
					});
				});
			});

/*------------Puppet Stop-----------------*/    
function testStop() {
        document.getElementById("stop").disabled = true;
        document.getElementById("start").disabled = false;
    }

/*------------checking difficulty level-----------------*/

$(function(){
var checkEvent = function () {
	res={easy:0,medium:0,hard:0}
	$(".checkList input:checked").each(function(index,el) {
		var dl = $(el).attr('difficulty-level');
		res[dl]+=1;
	});
	$("#output #easy").html(res['easy']);
	$("#output #medium").html(res['medium']);
	$("#output #hard").html(res['hard']);
 }
 
$(".checkList input").on('change',checkEvent);
});

/*------------Question Paper Creation-----------------*/
			$(function(){	
				$("#questionForm").submit(function(event){
				event.preventDefault();
				data=[];
				for(i=0;i<cq.length;i++) {
					if(cq[i].checked) {
						data.push(cq[i].value);
					}
				}
				console.log(data);
				flag=[];
				for(i=0;i<ps.length;i++) {
					if(ps[i].checked) {
						flag.push(ps[i].value);
					}
				}
				console.log(flag);
			    	$.get("/createquestionpaper", {names:JSON.stringify(data) , flags:JSON.stringify(flag)}, function(data){
						alert("Test paper Generated With Your seleted Questions \n Thank You!!\nQuestions Are "+data);
						window.location.reload(true);
					});
				});
			});
			
/*------------Closing Window-----------------*/
	 function closeWin()
	  {
   		 window.close(); 
      }

/*------------Checking UserName For Unique-----------------*/
			$(function(){
				$("#username").blur(function(){
					var contestname = $("#contestname").val();
					var username = $("#username").val();
					console.log(contestname);
					console.log(username);
					 $.get("/checkUserName",{'username':username,'contestname':contestname},function(data){
					 console.log(data);
					 if(data == "InValid")
					  {
					     alert("UserName Already Exists Please Try Another One");	
					     window.location.reload(true);
					  }
				   });
				});
			});
			
/*------------Checking Contestname For Unique-----------------*/
			$(function(){
				$("#contest").blur(function(){
					var contestname = $("#contest").val();
					console.log(contestname);
					 $.get("/checkContestName",{'contestname':contestname},function(data){
					 console.log(data);
					if(data == "InValid")
					  {
					     alert("Contest Name Already Exists Please Try Another One");
					     window.location.reload(true);
					  }
				   });
				});
			});

/*------------Adding Contest-----------------*/
function add()
 {
    document.getElementById("addingpage").style.visibility="visible";
 }
 
 /*------------participant approver selection-----------------*/
			$(function(){	
				$("#approvecontestantForm").submit(function(event){
				event.preventDefault();
				data=[];
				for(i=0;i<contestants.length;i++) {
					if(contestants[i].checked) {
						data.push(contestants[i].value);
					}
				}
			    console.log(data);
			    $.get("/approve",{names:JSON.stringify(data)},function(msg){
			     if(msg == "Valid")
					  {
					     window.location.reload(true);
					  }
				   });
				});
			});
 
