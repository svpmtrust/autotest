$(document).ready(function(){
var count=0; // to count blank fields

/*------------validation function-----------------*/
$(".submit_btn").click(function(event){
//fetching radio button by name
	var radio_check = $('.rad');
	
	//fetching all inputs with same class name text_field and an html tag textarea 
	var input_field = $('.text_field');
	var text_area = $('textarea');
	
	//validating radio button
	if(radio_check[0].checked== false && radio_check[1].checked== false){
	 var y = 0;
	}
	else{
	 var y = 1; 
	}
	
	//for loop to count blank inputs 
	for(var i=input_field.length;i>count;i--){
	if(input_field[i-1].value==''|| text_area.value=='')
		{
			count = count + 1;
		    
		}
	else{			
			count = 0;
		}
	}
	
	//Notifying validation 
		if(count!=0||y==0){
		
			alert("*All Fields are mandatory*");
			event.preventDefault();	
			}
			else{			
				return true;
			}
});

/*---------------------------------------------------------*/

	
	$(".next_btn").click(function(){           //Function runs on NEXT button click 
	$(this).parent().next().fadeIn('slow');
	$(this).parent().css({'display':'none'});
//Adding class active to show steps forward;
	$('.active').next().addClass('active');
	});
	
	$(".pre_btn").click(function(){            //Function runs on PREVIOUS button click 
	$(this).parent().prev().fadeIn('slow');
	$(this).parent().css({'display':'none'});
//Removing class active to show steps backward;
	$('.active:last').removeClass('active');
	});
	
//validating all input and textarea fields	
	$(".submit_btn").click(function(e){	
	if($('input').val()=="" || $('textarea').val()==""){	
			alert("*All Fields are mandatory*");
			return false;
		}
		else{
			return true;
		}
	});
});
