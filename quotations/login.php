<?php 
session_start();

?>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Login</title>
<link rel="stylesheet" href="style.css">

</head>

<body id='body'>

<h1 style='margin: 10px'>Login</h1>
<div class='post' style='width:25%'>
	
		<input id='loginname' placeholder="Username"><br>
		<input id='loginpass' placeholder="Password"><br><br>
		<button type='button' onclick='login();'>Login</button>
	<div id='error'><br></div>
</div>

<script>
loginname = document.getElementById('loginname')
loginpass = document.getElementById('loginpass')
error = document.getElementById('error')



function login(){
	ajax = new XMLHttpRequest();
	ajax.open('GET', 'controller.php?command=login&loginname='+loginname.value+'&loginpass='+loginpass.value);
	ajax.send();
	ajax.onreadystatechange = function (){
		if(ajax.readyState == 4 && ajax.status == 200){
			reply = ajax.responseText 
			console.log(reply)
			if (reply == 'good'){
				window.location.replace("view.php");

			}
			else{
				error.innerHTML = '<b style="color:red;">Login failed</b>'
			}
		}		
	}

}


</script>
</body>
</html>