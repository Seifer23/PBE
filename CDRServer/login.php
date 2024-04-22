<?php
session_start();
// Conexión a la base de datos
$servername = "localhost";
$username = "root";
$password = "";
$database = "upc"; // Nombre de tu base de datos

// Crear conexión
$conn = new mysqli($servername, $username, $password, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Obtener el student_id enviado desde la solicitud
$student_id = $_POST['student_id']; 

// Consulta SQL para verificar si el student_id existe en la tabla students
$sql = "SELECT * FROM students WHERE student_id = '$student_id'";
$result = $conn->query($sql);

// Verificar si se encontró algún resultado
if ($result->num_rows > 0) {
	$_SESSION['student_id'] = $student_id;

    // Convertir el resultado a un array asociativo
    $row = $result->fetch_assoc();
    
    // Devolver el resultado en formato JSON
    header('Content-Type: application/json');
    echo json_encode($row);
} else {
    // Si no se encontró ningún resultado, devolver un mensaje de error
    echo "No se encontró ningún estudiante con el ID proporcionado.";
}

// Cerrar la conexión
$conn->close();
?>
