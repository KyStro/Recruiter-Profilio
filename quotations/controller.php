<?php
session_start();

include 'model.php';
/*
session_start();
$_SESSION['user'] = 'name';
*/

$theDBA = new DatabaseAdaptor ();


if (isset($_GET['command']) && $_GET['command'] === 'register'){
    $username = htmlspecialchars($_GET['username']);
    $password = password_hash(htmlspecialchars($_GET['password']),PASSWORD_DEFAULT);
    if (!$theDBA->usernameTaken($username)){
        
       $theDBA->addUser($username, $password);
       echo 'good';
       
    }else{
        echo 'bad';
    }
}
    

if (isset($_GET['command']) && $_GET['command'] === 'logout'){
    unset($_SESSION['user']);
    header ( "Location: view.php" );
}

if (isset($_GET['command']) && $_GET['command'] === 'login'){
    $loginname = htmlspecialchars($_GET['loginname']);
    $loginpass = htmlspecialchars($_GET['loginpass']);
    if ($theDBA->verifyCredentials($loginname, $loginpass)){
        $_SESSION['user'] = $loginname;
        echo 'good';
    }else{
        echo 'bad';
    }  
}


if (isset($_POST['addquote'])){
    $quote = htmlspecialchars($_POST['quote']);
    $author = htmlspecialchars($_POST['author']);
    $theDBA->addQuote($quote, $author);
    header ( "Location: view.php" );
  
}

if (isset($_POST['plus'])){
    $id = $_POST['id'];
    $theDBA->plus($id);
    header ( "Location: view.php" );
    
}

if (isset($_POST['minus'])){
    $id = $_POST['id'];
    $theDBA->minus($id);
    header ( "Location: view.php" );
    
}

if (isset($_GET['command']) && $_GET['command'] === 'showall'){
    getAllQuotes($theDBA);
}


if (isset($_POST['delete']) && isset($_POST['id'])){
    $id = $_POST['id'];
    $theDBA->del($id);
    header ( "Location: view.php" );
   
}



function getAllQuotes($theDBA){
    $all = '';
    
    if(isset($_SESSION['user'])){
        $button1 = "<a href='addQuote.php'><button>Add Quote</button></a>";
        $button2 = "<button onclick='logout()'>Logout</button></a>";
    }
    else{
        $button1 = "<a href='register.php'><button>Register</button></a>";
        $button2 = "<a href='login.php'><button>Login</button></a>";
    }
    $quote_array = $theDBA->getAllQuotations();
    
    $all .= $button1.'<br>'.$button2;
    foreach ($quote_array as $element){
        $start = "<div class='post'>";
        $formstart = '<form action="controller.php" method="post">';
        $quote = "<q>".$element['quote']."</q><br><br>";
        $author = "--".$element['author']."<br><br>";
        $plus = "&nbsp<input type='submit' name='plus' value='+' />&nbsp";
        $rating = $element['rating'];
        $minus = "&nbsp<input type='submit' name='minus' value='-' />&nbsp";
        $delete = "&nbsp<input type='submit' name='delete' value='delete' />&nbsp";
        if(!isset($_SESSION['user'])){
            $delete = '';
        }
        $id = "<input type='hidden' name='id' value='".$element['id']."'/>";
        $formend = '</form>';
        $end = '</div>';
        $post = $start.$formstart.$quote.$author.$plus.$rating.$minus.$delete.$id.$formend.$end;
        $all .= $post;
        
    }
    echo $all;
    }

?>