<?php
// Iniciar sesión en PHP
session_start();

// Verificar si el estudiante está autenticado
if (!isset($_SESSION['student_id'])) {
    // Redirigir a la página de inicio de sesión si el estudiante no está autenticado
    header("Location: login.php"); // Ajusta la URL según tu aplicación
    exit();
}

// Obtener el "student_id" de la sesión
$student_id = $_SESSION['student_id'];

// Conexión a la base de datos
$servername = "localhost";
$username = "root"; // Tu nombre de usuario de MySQL
$password = ""; // Tu contraseña de MySQL
$database = "upc"; // Nombre de tu base de datos
$conn = new mysqli($servername, $username, $password, $database);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Función para ejecutar una consulta SQL y devolver los resultados en formato JSON
function executeQuery($conn, $sql) {
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $response = array();
        
        while($row = $result->fetch_assoc()) {
            $response[] = $row;
        }
        
        echo json_encode($response);
    } else {
        echo json_encode(array("message" => "No se encontraron resultados"));
    }
}

// Manejar diferentes tipos de consultas según la URL proporcionada
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $params = $_GET;

    // Construir la consulta SQL base
    $sql = "SELECT * FROM ";


    if (strpos($_SERVER['REQUEST_URI'], 'timetables') !== false) {
        $sql .= "timetables WHERE student_id = '$student_id' ";
    } elseif (strpos($_SERVER['REQUEST_URI'], 'tasks') !== false) {
        $sql .= "tasks WHERE student_id = '$student_id' ";
    } elseif (strpos($_SERVER['REQUEST_URI'], 'marks') !== false) {
        $sql .= "marks WHERE student_id = '$student_id' ";
    } else {
		echo json_encode(array("message" => "La tabla solicitada no existe"));
	}

    // Aplicar filtros y orden según los parámetros proporcionados
    if (!empty($params)) {
        $sql .= "AND ";

        foreach ($params as $key => $value) {
            if ($key !== 'limit' && $key !== 'sort') {
                $keyParts = explode('[', $key);
                $fieldName = $keyParts[0];
                $operator = '=';
                $fieldValue = $value;

                if (count($keyParts) > 1) {
                    $operator = rtrim($keyParts[1], ']');
                }

                $sql .= "$fieldName $operator '$fieldValue' AND ";
            }
        }

        // Eliminar el último 'AND' sobrante
        $sql = rtrim($sql, 'AND ');

        // Aplicar límite de resultados
        if (isset($params['limit'])) {
            $limit = intval($params['limit']);
            $sql .= " LIMIT $limit";
        }

        // Aplicar orden
        if (isset($params['sort'])) {
            $sort = $params['sort'];
            $sql .= " ORDER BY $sort";
        }
    }

    // Ejecutar la consulta final
    executeQuery($conn, $sql);
}

// Cerrar la conexión a la base de datos
$conn->close();
?>
