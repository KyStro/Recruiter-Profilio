<?php
//Kyle Strokes
// File name: bestreads.php
if (isset($_GET['command']) && $_GET['command'] === 'showall'){
    $bookArray = glob ( './books/*' );
    echo json_encode ( $bookArray );
}

if (isset($_GET['command']) && $_GET['command'] === 'showone'){
    $html = '<div class="onereview">';
    $book = $_GET['book'];
    $file = file($book.'/info.txt');
    $info = '<b><br><br><br>'.$file[0].'</b><br>'.$file[1].'<br><br>';
    $desc = file_get_contents($book.'/description.txt') . '<br><br>';
    $file = file($book.'/review.txt');
    $rev = '<b>'.$file[0].' '.stars($file[1]).'</b><br>'.$file[2];
    $path = $book.'/cover.jpg';
    $cover = '<img class="onebook" src="'.$path.'">';
    $html .= $cover . $info . $desc . $rev . '</div>';
    
    echo json_encode($html);
    

}

function stars($n){
    $stars = str_repeat("*",intval($n));
   return $stars;
}
?>