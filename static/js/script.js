$('#registerEmail').on('input', function(){
	var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	var is_email=re.test($('#registerEmail').val());

	if(($('#registerEmail').val().length > 7) && (is_email)){
		$('#registerEmail').removeClass('is-invalid').addClass('is-valid')
		$('#msg2').html('');
	}else{
		$('#registerEmail').removeClass('is-valid').addClass('is-invalid');
		$('#msg2').html('Give a valid email!');
	}
});

$('#registerPass').on('input', function(){
	if(!(($('#registerPass').val().length > 7) && (/\d/.test($('#registerPass').val())))){
		$('#registerPass').removeClass('is-valid').addClass('is-invalid');
		$('#msg').html('Password minimum 8 characters with numeric values');
	}
	else{
		$('#msg').html('');
		$('#registerPass').removeClass('is-invalid').addClass('is-valid')
	}
});

$('#registerPass2').on('input', function(){
	if($('#registerPass').val() != $('#registerPass2').val()){
		$('#registerPass2').removeClass('is-valid').addClass('is-invalid');
		$('#msg').html('Password didn\'t Match!');
	}else{
		$('#msg').html('');
		$('#registerPass2').removeClass('is-invalid').addClass('is-valid');
	}
});

$("#submit-register").click(function(event){
	var form_data=$("#register").serializeArray();
	var error_free=true;
	for (var index in form_data){
		var element=$("#"+form_data[index]['name']);
		var isnotvalid=element.hasClass("is-invalid");
		var element_value=element.val()
		if (isnotvalid || !element_value){error_free=false;}
	}
	var agree_check=$("#agreePolicy").is(":checked")
	if(!agree_check){error_free=false}
	if (!error_free){
		event.preventDefault(); 
	}
});

$('#registerPass, #registerPass2').keypress(function(e) { 
	var s = String.fromCharCode( e.which );

	if((s.toUpperCase() === s && s.toLowerCase() !== s && !e.shiftKey) ||
	   (s.toUpperCase() !== s && s.toLowerCase() === s && e.shiftKey)){
		$('#capsWarning').html('Capslock is ON!');
	} else {
		$('#capsWarning').html('');
	}
});

function toggle_show(theid){
	var originalBtn = $('#'+theid);
	var newBtn = originalBtn.clone();
	if($('#'+theid).attr('type')==="password"){
		newBtn.attr("type", "text");
	}else{
		newBtn.attr("type", "password")
	}
	newBtn.insertBefore(originalBtn);
	originalBtn.remove();
	newBtn.attr("id", theid);
}