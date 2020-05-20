<?php
//Kyle Strokes

class DatabaseAdaptor {
    private $DB; // The instance variable used in every method below
    // Connect to an existing data based named 'first'
    public function __construct() {
        $dataBase =
        'mysql:dbname=quotes;charset=utf8;host=127.0.0.1';
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
    
    public function plus($id) {
        $stmt = $this->DB->prepare("UPDATE quotations SET rating = rating + 1 WHERE id = :id;");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
    }
  
    public function minus($id) {
        $stmt = $this->DB->prepare("UPDATE quotations SET rating = rating - 1 WHERE id = :id;");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
    }
    
    public function del($id) {
        $stmt = $this->DB->prepare( "delete from quotations where id = :id;");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
    }
    
    public function getAllQuotations() {
        $stmt = $this->DB->prepare( "select * from quotations order by rating desc;");
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
   
    public function getAllUsers() {
        $stmt = $this->DB->prepare( "select * from users;");
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
   
   
    public function usernameTaken($accountName) {
        $stmt = $this->DB->prepare( "select * from users where username= :name;");
        $stmt->bindParam(':name', $accountName);
        
        $stmt->execute();
        $q = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if (count($q) == 0){
            return false;
        }else{
            return true;
        }
    }
    
    public function verifyCredentials($accountName, $psw) {
        $stmt = $this->DB->prepare( "select password from users where username= :name;");
        $stmt->bindParam(':name', $accountName);
      
        $stmt->execute();
        $q = $stmt->fetchAll(PDO::FETCH_ASSOC);
        if (count($q) == 0){
            return false;
        }
        $db_pass = $q[0]['password'];
        if (password_verify($psw, $db_pass)){
            return true;
        }else{
            return false;}
    }
   
    public function addQuote($quote, $author) {
        $stmt = $this->DB->prepare( "insert into quotations(quote, added, author, rating, flagged) 
            values(:quote, NOW(), :author, 0, 0);");
        $stmt->bindParam(':quote', $quote);
        $stmt->bindParam(':author', $author);
        $stmt->execute();
    }

    
    public function addUser($accountName, $psw) {
        $stmt = $this->DB->prepare( "insert into users(username, password) 
            values(:name, :pass);");
        $stmt->bindParam(':name', $accountName);
        $stmt->bindParam(':pass', $psw);
        
        $stmt->execute();
    }
    
}


?>