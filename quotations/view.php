<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Quotes</title>

<link rel="stylesheet" href="style.css">

</head>


<body onload="showAll()">

<h1 class='title'>Quotation Service</h1>

<div id='feed'>

</div>



<script>

feed = document.getElementById('feed')


function showAll(){
	ajax = new XMLHttpRequest();
	ajax.open('GET', 'controller.php?command=showall');
	ajax.send();
	ajax.onreadystatechange = function (){
		if(ajax.readyState == 4 && ajax.status == 200){
			feed.innerHTML = ajax.responseText }
			
	}
}


function logout(){
	ajax = new XMLHttpRequest();
	ajax.open('GET', 'controller.php?command=logout');
	ajax.send();
	ajax.onreadystatechange = function (){
		if(ajax.readyState == 4 && ajax.status == 200){
			window.location.replace("view.php");
}
			
	}
}




</script>
</body>
</html>
