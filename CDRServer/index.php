<?php
// Iniciar sesión en PHP
session_start();

// Verificar si el estudiante ya está autenticado
if (isset($_SESSION['student_id'])) {
    // Redirigir al usuario a la página principal si ya está autenticado
    header("Location: dashboard.php"); // Ajusta la URL según tu aplicación
    exit();
}

/// Verificar si se enviaron datos de inicio de sesión mediante el formulario
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validar y procesar los datos de inicio de sesión
    $username = $_POST['username']; // Nombre de usuario introducido
    $password = $_POST['password']; // Contraseña introducida

    // Conexión a la base de datos
    $servername = "localhost";
    $username_db = "root"; // Reemplaza con tu nombre de usuario de MySQL
    $password_db = ""; // Reemplaza con tu contraseña de MySQL
    $database = "upc"; // Reemplaza con el nombre de tu base de datos
    $conn = new mysqli($servername, $username_db, $password_db, $database);

    // Verificar la conexión
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    // Consulta SQL para verificar el Usuario y la Contraseña en la base de datos
    $sql = "SELECT * FROM students WHERE name = '$username' AND student_id = '$password'";
     $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        // Si el Usuario y la Contraseña coinciden, establecerlo en la sesión
        $_SESSION['student_id'] = $password;
        $_SESSION['name'] = $username;
        header("Location: dashboard.php"); // Redirigir al usuario a la página principal
        exit();
    } else {
        // Si el Usuario o la Contraseña no coinciden, mostrar un mensaje de error
        $error_message = "Usuario o Contraseña incorrectos.";
    }

    // Cerrar la conexión a la base de datos
    $conn->close();
}


?>



<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Course Manager</title>
    <link rel="stylesheet" href="estils.css">
</head>
<body>
    <h2>Welcome to Course Manager</h2>
    <?php
    // Mostrar mensaje de error si existe
    if (isset($error_message)) {
        echo "<p class='error'>$error_message</p>";
    }
    ?>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <div class="form-group">
            <label for="username">Usuario:</label><br>
            <input type="text" id="username" name="username" required><br><br>
        </div>
        <div class="form-group">
            <label for="password">Contraseña:</label><br>
            <input type="password" id="password" name="password" required><br><br>
        </div>
        <input type="submit" value="Iniciar sesión">
    </form>
</body>
</html>
