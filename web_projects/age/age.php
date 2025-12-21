<!DOCTYPE html>
<html>
<head>
    <title>Age Shower</title>
    <link rel="stylesheet" href="style.css">
<link href='https://fonts.googleapis.com/css?family=Cherry Bomb One' rel='stylesheet'>
</head>
<body>
    <div class="age-box">
        <h1 class="age-title">Hi this is the age indicator</h1>
        <form method="POST">
            <div class="form-row">
                <input type="text" name="age_input" placeholder="please enter your age">
            </div>
            <div class="form-row">
                <button type="submit">Submit</button>
            </div>
        </form>
        <?php
        if ($_SERVER["REQUEST_METHOD"] === "POST"){
            echo"<p></p>";
            $age = (int)$_POST["age_input"];
            echo"<div class = 'box'>";
   echo "<div class='box'>"; // starta box före loopen
            $i = 0;
    while ($age != $i){
        $i = $i + 1;
        if ($age == $i){
            echo "<p>you are $age</p>";
        } else {
            echo "<p>your age is not $i</p>";
        }
    }

    echo "</div>"; // stäng box efter loopen
        
    }
        ?>
        </body>
</head>