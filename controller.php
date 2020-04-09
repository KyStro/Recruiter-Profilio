<?php
//Kyle Strokes
include 'model.php';

$theDBA = new DatabaseAdaptor ();


if (isset($_GET ['term']) && ($_GET ['table'] === "actors")){
    $html = '<h3>Actors</h3><table style= "width: 30%";>';
    $actors = $theDBA->getActors ($_GET['term']);
    for($i=0; $i<count($actors); $i++){
        $html .= "<tr><td>" . $actors[$i]['first_name'] . " " . $actors[$i]['last_name'] . "</td></tr>";
    }
    $html .= '</table>';
    if (count($actors) == 0){
        $html = 'No matches for "' . $_GET ['term'] . '"';
    }
    echo json_encode ( $html);
}


if (isset($_GET ['term']) && ($_GET ['table'] === "roles")){
    
    $html = '<h3>Roles</h3><table style= "width: 30%";>';
    $roles = $theDBA->getRoles ($_GET['term']);
    for($i=0; $i<count($roles); $i++){
        $html .= "<tr><td>" . $roles[$i]['role'] . "</td></tr>";
    }
    $html .= '</table>';
    if (count($roles) == 0){
        $html = 'No matches for "' . $_GET ['term'] . '"';
    }
    echo json_encode ( $html);
}


if (isset($_GET ['term']) && ($_GET ['table'] === "movies")){
    
    $html = '<h3>Movies</h3><table style= "width: 30%";>';
    $movies = $theDBA->getMovies ($_GET['term']);
    for($i=0; $i<count($movies); $i++){
        $html .= "<tr><td>" . $movies[$i]['name'] . "</td></tr>";
    }
    $html .= '</table>';
    if (count($movies) == 0){
        $html = 'No matches for "' . $_GET ['term'] . '"';
    }
    echo json_encode ( $html);
}
?>