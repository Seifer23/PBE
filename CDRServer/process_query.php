<?php
session_start();

if (isset($_POST['query'])) {
    // Obtener la consulta del formulario
    $query = $_POST['query'];

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

    // Separar la tabla de los argumentos adicionales
    $query_parts = explode("?", $query);
    $table_name = $query_parts[0]; // Obtener el nombre de la tabla
    $additional_args = isset($query_parts[1]) ? $query_parts[1] : ""; // Obtener los argumentos adicionales, si los hay

    // Consulta SQL para verificar si la tabla existe
    $check_table_query = "SHOW TABLES LIKE '$table_name'";
    $check_table_result = $conn->query($check_table_query);

    // Verificar si la tabla existe
    if ($check_table_result->num_rows > 0) {
        // Si la tabla existe, ejecutar la consulta para listar las entradas
        $student_id = $_SESSION['student_id'];
        $select_query = "SELECT * FROM $table_name WHERE student_id = '$student_id'";

        // Aplicar argumentos adicionales si los hay
        if (!empty($additional_args)) {
            // Verificar si se proporcionó el argumento "limit"
            $limit_pattern = '/^limit=(\d+)$/i';
            if (preg_match($limit_pattern, $additional_args, $matches)) {
                $limit_value = $matches[1];
                // Aplicar el límite de resultados a la consulta SQL
                $select_query .= " LIMIT $limit_value";
            }
        }

        // Ejecutar la consulta
        $result = $conn->query($select_query);

        // Verificar si se obtuvieron resultados
        if ($result->num_rows > 0) {
            // Inicializar la variable para almacenar los resultados en formato HTML
            $result_html = "<table>";
            $result_html .= "<tr>";
            
            // Obtener los nombres de las columnas y agregarlos a la primera fila de la tabla HTML
            $column_count = $result->field_count;
            for ($i = 0; $i < $column_count; $i++) {
                $column_info = $result->fetch_field();
                $result_html .= "<th>{$column_info->name}</th>";
            }
            $result_html .= "</tr>";
            
            // Iterar sobre los resultados y agregarlos a la tabla HTML
            while ($row = $result->fetch_assoc()) {
                $result_html .= "<tr>";
                foreach ($row as $value) {
                    $result_html .= "<td>$value</td>";
                }
                $result_html .= "</tr>";
            }
            
            $result_html .= "</table>";

            // Almacena el resultado en $_SESSION['query_result']
            $_SESSION['query_result'] = $result_html;
        } else {
            // Si no se encontraron resultados, muestra un mensaje de error
            $_SESSION['query_result'] = "<p>No se encontraron resultados para la tabla '$table_name'.</p>";
        }
    } else {
        // Si la tabla no existe, muestra un mensaje de error
        $_SESSION['query_result'] = "<p>La tabla '$table_name' no existe en la base de datos.</p>";
    }

    // Redirige de vuelta al dashboard
    header("Location: dashboard.php");
    exit();
}
?>
