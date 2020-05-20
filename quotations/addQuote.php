<?php 
session_start();

?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Add Quote</title>
<link rel="stylesheet" href="style.css">

</head>

<body id='body'>

<h1 style='margin: 10px'>Add Quote</h1>
<div id='enter' class='post' style='width:50%'>
	<form action="controller.php" method="post" autocomplete="off">
		<textarea name="quote" rows="4" cols="100" placeholder="Enter a new quote" required></textarea><br>
		<input name='author' placeholder="Author" required><br><br>
		<input type='submit' name='addquote' value='Add Quote'>
	</form>
</div>



</body>
</html>