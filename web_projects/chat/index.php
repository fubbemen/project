<?php
session_start();

// initialize session array properly
if (!isset($_SESSION["all_comments"])) {
    $_SESSION["all_comments"] = [];
}

// handle POST
if ($_SERVER["REQUEST_METHOD"] === "POST" && !empty($_POST["input"])) {
    $input = htmlspecialchars($_POST["input"]); // safe input
    $_SESSION["all_comments"][] = $input;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>minstagrap</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <form method="POST">
        <input type="text" name="input" placeholder="comment to main chat">
        <button type="submit">=></button>
    </form>

    <div class="comments">
        <?php
        foreach ($_SESSION["all_comments"] as $comment) {
            echo "<p>$comment</p>";
        }
        ?>
    </div>
</body>
</html>
