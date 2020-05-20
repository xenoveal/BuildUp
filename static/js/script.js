var allowSubmit = false;
$('#registerEmail').on('input', function(){
	var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	var is_email=re.test($('#registerEmail').val());

	if(($('#registerEmail').val().length > 5) && (is_email)){
		$('#registerEmail').removeClass('is-invalid').addClass('is-valid')
		$('#msg2').html('');
	}else{
		$('#registerEmail').removeClass('is-valid').addClass('is-invalid');
		$('#msg2').html('Give a valid email!');
	}
});

$('#registerPass, #registerPass2').on('input', function(){
	if(($('#registerPass').val().length > 7) && (/\d/.test($('#registerPass').val()))){
		if($('#registerPass').val() != $('#registerPass2').val()){
			$('#registerPass2').addClass('is-invalid');
			$('#msg').html('Password didn\'t Match!');
		}else{
			$('#msg').html('');
			$('#registerPass').toggleClass('is-invalid is-valid');
			$('#registerPass2').toggleClass('is-invalid is-valid');
			allowSubmit = true;
		}
	}else{
		$('#registerPass').addClass('is-invalid');
		$('#msg').html('Password minimum 8 characters with numeric values');
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