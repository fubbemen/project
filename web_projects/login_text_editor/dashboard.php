<?php
session_start();

// Redirect if not logged in
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

// Show session info for debugging (can remove later)
echo "<p>Hello, " . htmlspecialchars($_SESSION['username']) . "!</p>";
// var_dump($_SESSION);

$uploadsDir = "uploads/";
if (!is_dir($uploadsDir)) {
    mkdir($uploadsDir, 0777, true);
}

// STEP 1: Handle file upload
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_FILES["file"])) {
    $uploadedFile = $_FILES["file"]["tmp_name"];
    $filename = basename($_FILES["file"]["name"]);
    $savePath = $uploadsDir . $filename;

    if (move_uploaded_file($uploadedFile, $savePath)) {
        echo "<p style='color:green;'>File uploaded: $filename</p>";
        $content = file_get_contents($savePath);

        // Show editable textarea
        echo '<form method="POST">';
        echo '<textarea name="new_content" rows="15" cols="70">' . htmlspecialchars($content) . '</textarea><br>';
        echo '<input type="hidden" name="file_path" value="' . htmlspecialchars($savePath) . '">';
        echo '<button type="submit">Save Changes</button>';
        echo '</form>';
    } else {
        echo "<p style='color:red;'>Failed to upload file!</p>";
    }
}

// STEP 2: Save edited file
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["new_content"], $_POST["file_path"])) {
    $filePath = $_POST["file_path"];
    $newContent = $_POST["new_content"];

    if (file_put_contents($filePath, $newContent)) {
        echo "<p style='color:green;'>File saved successfully!</p>";
    } else {
        echo "<p style='color:red;'>Failed to save file!</p>";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <link rel="stylesheet" href="style1.css">
    <link rel="shortcut icon" type="image/x-icon" href="php.png" />
</head>
<body>

<h1>Dashboard</h1>

<!-- Upload form -->
<h2>Upload a new text file</h2>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" accept=".txt" required>
    <button type="submit">Upload</button>
</form>

<!-- Logout button -->
<form method="POST" action="index.php" style="margin-top:20px;">
    <button type="submit" name="logout">Logout</button>
</form>

</body>
</html>
