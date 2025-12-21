<?php
if ($_SERVER["REQUEST_METHOD"] === "POST" ){
    $num = rand(1,4);
    $today = $_POST["day"];
    $city = $_POST["city"];

    $today = strtolower($today);
    $today = str_replace(" ", "", $today);

    $weather_montu = [
        "tomorrow" => "",
        "day_after_tomorrow" => ""
    ]; 

    if ($num == 1) {
        $weather_montu["tomorrow"] = "sunny";
        $weather_montu["day_after_tomorrow"] = "rainy";
    } else if ($num == 2) {
        $weather_montu["tomorrow"] = "rainy";
        $weather_montu["day_after_tomorrow"] = "sunny";
    } else if ($num == 3) {
        $weather_montu["tomorrow"] = "rainy";
        $weather_montu["day_after_tomorrow"] = "rainy";
    } else if ($num == 4) {
        $weather_montu["tomorrow"] = "sunny";
        $weather_montu["day_after_tomorrow"] = "sunny";
    }

    if ($today == "monday"){
        $tomorow = "tuesday";
        $day_after_tmrw = "wednesday";
    } else if ($today == "tuesday"){
        $tomorow = "wednesday";
        $day_after_tmrw = "thursday";
    } else if ($today == "wednesday"){
        $tomorow = "thursday";
        $day_after_tmrw = "friday";
    } else if ($today == "thursday"){
        $tomorow = "friday";
        $day_after_tmrw = "saturday";
    } else if ($today == "friday"){
        $tomorow = "saturday";
        $day_after_tmrw = "sunday";
    } else if ($today == "saturday"){
        $tomorow = "sunday";
        $day_after_tmrw = "monday";
    } else if ($today == "sunday"){
        $tomorow = "monday";
        $day_after_tmrw = "tuesday";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Weather Forecast</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://fonts.googleapis.com/css?family=Cherry Bomb One" rel="stylesheet">
</head>

<body>
    <div class="weather-box">
        <h1 class="weather-title">Weather Forecast</h1>

        <form method="POST">
            <div class="weather-row">
                <input type="text" name="day" placeholder="please enter the current day">
            </div>

            <div class="weather-row">
                <input type="text" name="city" placeholder="please enter the city you are in">
            </div>

            <div class="weather-row">
                <button type="submit">Submit</button>
            </div>
        </form>

        <?php
        if (!empty($weather_montu['tomorrow']) && !empty($weather_montu['day_after_tomorrow'])) {
            echo "<p>Weather for $tomorow is {$weather_montu['tomorrow']} in $city</p>";
            echo "<p>Weather for $day_after_tmrw is {$weather_montu['day_after_tomorrow']} in $city</p>";
        }
        ?>
    </div>
</body>
</html>
