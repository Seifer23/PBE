<?php
session_start();

// Verificar si el usuario está autenticado
if (!isset($_SESSION['student_id'])) {
    // Si no está autenticado, redirigir a la página de inicio de sesión
    header("Location: index.php");
    exit();
}

// Procesar el cierre de sesión
if (isset($_POST['logout'])) {
    session_unset();
    session_destroy();
    header("Location: index.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="dashboard_styles.css">
</head>
<body>
    <div class="container">
        <div class="dashboard-box">
            <h2>Welcome <?php echo $_SESSION['name'] ?> </h2>
            <form method="post" action="process_query.php">
                <label for="query">Consulta:</label><br>
                <input type="text" id="query" name="query" required><br><br>
                <input type="submit" value="Send">
            </form>
            <?php
            // Mostrar resultado de la consulta
            if (isset($_SESSION['query_result'])) {
                echo "<div class='query-result'>";
                echo $_SESSION['query_result'];
                echo "</div>";
                unset($_SESSION['query_result']);
            }
            ?>
            <br>
            <form method="post">
                <input type="submit" name="logout" value="Logout">
            </form>
        </div>
    </div>
</body>
</html>
