<?php 
session_start();

?>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Register</title>
<link rel="stylesheet" href="style.css">

</head>

<body id='body'>

<h1 style='margin: 10px'>Register</h1>
<div class='post' style='width:25%'>
	<form autocomplete="off">
		<input id='username' placeholder="Username" required><br>
		<input id='password' placeholder="Password" required><br><br>
		<button type='button' onclick='register();'>Register</button>
	<div id='error'><br></div>

	</form>
</div>


<script>
username = document.getElementById('username')
password = document.getElementById('password')
error = document.getElementById('error')


function register(){
	ajax = new XMLHttpRequest();
	ajax.open('GET', 'controller.php?command=register&username='+username.value+'&password='+password.value);
	ajax.send();
	ajax.onreadystatechange = function (){
		if(ajax.readyState == 4 && ajax.status == 200){
			reply = ajax.responseText 
			console.log(reply)
			if (reply == 'good'){
				window.location.replace("view.php");

			}
			else{
				error.innerHTML = '<b style="color:red;">Username taken</b>'
			}
		}		
	}

}


</script>

</body>
</html>