<?php
// Iniciar sesión en PHP
session_start();

// Verificar si el estudiante ya está autenticado
if (isset($_SESSION['student_id'])) {
    // Redirigir al usuario a la página principal si ya está autenticado
    header("Location: api3.php"); // Ajusta la URL según tu aplicación
    exit();
}

// Verificar si se enviaron datos de inicio de sesión mediante el formulario
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validar y procesar los datos de inicio de sesión
    $student_id = $_POST['student_id']; // Suponiendo que el campo del formulario se llama "student_id"

    // Conexión a la base de datos
    $servername = "localhost";
    $username = "root"; // Reemplaza con tu nombre de usuario de MySQL
    $password = ""; // Reemplaza con tu contraseña de MySQL
    $database = "upc"; // Reemplaza con el nombre de tu base de datos
    $conn = new mysqli($servername, $username, $password, $database);

    // Verificar la conexión
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    // Consulta SQL para verificar si el student_id existe en la base de datos
    $sql = "SELECT * FROM students WHERE student_id = '$student_id'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Si el student_id existe en la base de datos, establecerlo en la sesión
        $_SESSION['student_id'] = $student_id;
		// Convertir el resultado a un array asociativo
		/**
		$row = $result->fetch_assoc();
    
		// Devolver el resultado en formato JSON
		header('Content-Type: application/json');
		echo json_encode($row);
		// Redirigir al usuario a la página principal
		**/
        header("Location: api3.php"); // Ajusta la URL según tu aplicación
        exit();
    } else {
        // Si el student_id no existe en la base de datos, mostrar un mensaje de error
        $error_message = "El ID de estudiante ingresado no es válido.";
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
    <title>Iniciar sesión</title>
</head>
<body>
    <h2>Iniciar sesión</h2>
    <?php
    // Mostrar mensaje de error si existe
    if (isset($error_message)) {
        echo "<p style='color: red;'>$error_message</p>";
    }
    ?>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <label for="student_id">ID de estudiante:</label><br>
        <input type="text" id="student_id" name="student_id"><br><br>
        <input type="submit" value="Iniciar sesión">
    </form>
</body>
</html>