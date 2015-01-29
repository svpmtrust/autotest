$(function(){
    $("#addfield").click(function(event){
	var x="<div class='inputfield'><label>Name</label><input type='text' /></div>";
	$("#inputs").append($(x));
	
	event.preventDefault()
    });

    $("#submit").click(function(event){
	//var a = {name:$("#test").val(), username:$("#username").val(), }
	var arr=Array();
	$(".inputfield input").each(function(){
	    arr.push({name:$(this).val()});
	});

	$.post("/test",{names:JSON.stringify(arr)},function(data){
	    alert("successfully posted");
	    $(".inputfield").hide();
	});
	event.preventDefault();
	return false;
    });
});
