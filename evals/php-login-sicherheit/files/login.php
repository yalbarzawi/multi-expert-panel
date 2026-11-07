<?php
session_start();
$db = mysqli_connect("localhost", "root", "", "portal");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user = $_POST["username"];
    $pass = md5($_POST["password"]);
    $sql = "SELECT * FROM users WHERE username = '$user' AND password = '$pass'";
    $result = mysqli_query($db, $sql);
    if (mysqli_num_rows($result) > 0) {
        $_SESSION["user"] = $user;
        header("Location: dashboard.php");
    } else {
        echo "Login fehlgeschlagen für " . $_POST["username"];
    }
}
?>
<form method="post">
  <input name="username"> <input name="password" type="password">
  <button>Login</button>
</form>
