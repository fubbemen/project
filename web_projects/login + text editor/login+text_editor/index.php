<?php
session_start();

// Users list
$users = [
    "fab" => "1234",
    "seb" => "turkmenistan1234",
    "ompalompa" => "afganistan!"
];

// LOGIN
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["login"])) {
    $username = $_POST["username"];
    $password = $_POST["password"];

    if (isset($users[$username]) && $users[$username] === $password) {
        $_SESSION['username'] = $username; // save session
        header("Location: dashboard.php"); // redirect to dashboard
        exit();
    } else {
        $error = "Sorry, enter the correct credentials";
    }
}

// LOGOUT (if you keep logout button here)
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["logout"])) {
    unset($_SESSION['username']);
    $message = "You have been logged out";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Test Login</title>
    <link rel="stylesheet" href="style.css">
    <!--
Source - https://stackoverflow.com/a
Posted by 1010, modified by community. See post 'Timeline' for change history
Retrieved 2025-12-21, License - CC BY-SA 3.0
-->

<link rel="shortcut icon" type="image/x-icon" href="php.png" />

</head>
<body>

<div class="login-container">
    <h2 class="login_form">Login Form</h2>

    <?php if (!empty($error)) echo "<p style='color:red;'>$error</p>"; ?>
    <?php if (!empty($message)) echo "<p style='color:green;'>$message</p>"; ?>

    <!-- Login form -->
    <form method="POST">
        <div>
            <input type="text" name="username" placeholder="Please enter your username" required>
        </div>
        <div>
            <input type="password" name="password" placeholder="Please enter your password" required>
        </div>
        <div>
            <button type="submit" name="login">Login</button>
        </div>
        <!-- keep your image -->
        <img src="php.png" alt="php">
    </form>
</div>

<div class="logout-container">
    <!-- Logout button -->
    <form method="POST">
        <button type="submit" name="logout" value="1">Log out</button>
    </form>
</div>

</body>
</html>
