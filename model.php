<?php
//Kyle Strokes
class DatabaseAdaptor {
    private $DB; // The instance variable used in every method below
    // Connect to an existing data based named 'first'
    public function __construct() {
        $dataBase =
        'mysql:dbname=imdb_small;charset=utf8;host=127.0.0.1';
        $user =
        'root';
        $password =
        ''; // Empty string with XAMPP install
        try {
            $this->DB = new PDO ( $dataBase, $user, $password );
            $this->DB->setAttribute ( PDO::ATTR_ERRMODE,
                PDO::ERRMODE_EXCEPTION );
        } catch ( PDOException $e ) {
            echo ('Error establishing Connection');
            exit ();
        }
    }
    
    public function getActors ($term) {
        $stmt = $this->DB->prepare( "SELECT * FROM actors where first_name like '%". $term . "%' or 
            last_name like '%". $term . "%';");
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    
    public function getRoles ($term) {
        $stmt = $this->DB->prepare( "SELECT * FROM roles where role like '%". $term . "%';");
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    
    public function getMovies ($term) {
        $stmt = $this->DB->prepare( "SELECT * FROM movies where name like '%". $term . "%';");
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}


?>