<?php
// Start session
session_start();

// Check if student is authenticated
if (!isset($_SESSION['student_id'])) {
    header("Location: login.php");
    exit();
}

// Get student ID from session
$student_id = $_SESSION['student_id'];

// Database connection details
$servername = "localhost";
$username = "root";
$password = "";
$database = "upc";

// Create database connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    echo json_encode(null);
    exit();
}

// Function to execute a query and return results as JSON
function executeQuery($conn, $sql, $params) {
    $stmt = $conn->prepare($sql);
    if ($stmt === false) {
        echo json_encode(null);
        return;
    }
    if (!empty($params)) {
        $types = str_repeat('s', count($params));
        $stmt->bind_param($types, ...$params);
    }
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $response = array();
        while ($row = $result->fetch_assoc()) {
            $response[] = $row;
        }
        echo json_encode($response);
    } else {
        echo json_encode(array("message" => "No results found"));
    }
    $stmt->close();
}

// Get the current day of the week (1 = Monday, 7 = Sunday)
$currentDay = date('N');

// Mapping days of the week to their respective order, starting from the current day
$daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
$orderedDays = array_merge(array_slice($daysOfWeek, $currentDay - 1), array_slice($daysOfWeek, 0, $currentDay - 1));
$orderCaseSql = "CASE day";
foreach ($orderedDays as $index => $day) {
    $orderCaseSql .= " WHEN '$day' THEN $index";
}
$orderCaseSql .= " END";

// Handle different query types based on URL
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $params = $_GET;

    // Extract table name from the URL path
    $uriSegments = explode('/', trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/'));
    $table = end($uriSegments);

    // Validate table name (you might want to use a whitelist of valid table names)
    $valid_tables = ['timetables', 'tasks', 'marks']; // Add your valid table names here
    if (!in_array($table, $valid_tables)) {
        echo json_encode(null);
        $conn->close();
        exit();
    }

    // Check if the table has a 'day' column
    $hasDayColumn = false;
    $result = $conn->query("SHOW COLUMNS FROM $table LIKE 'day'");
    if ($result->num_rows > 0) {
        $hasDayColumn = true;
    }
    $result->free();

    // Initialize the base SQL query
    $baseSql = "SELECT * FROM $table WHERE student_id = ?";
    $queryParams = array($student_id);

    // Apply filters and sort if parameters are provided
    if (!empty($params)) {
        foreach ($params as $key => $value) {
            if ($key !== 'limit' && $key !== 'sort') {
                if (is_array($value)) {
                    foreach ($value as $operator => $v) {
                        $fieldName = $key;
                        switch ($operator) {
                            case 'gt':
                                $operator = '>';
                                break;
                            case 'lt':
                                $operator = '<';
                                break;
                            case 'gte':
                                $operator = '>=';
                                break;
                            case 'lte':
                                $operator = '<=';
                                break;
                            case 'ne':
                                $operator = '!=';
                                break;
                            default:
                                $operator = '=';
                                break;
                        }
                        $baseSql .= " AND $fieldName $operator ?";
                        $queryParams[] = $v;
                    }
                } else {
                    $baseSql .= " AND $key = ?";
                    $queryParams[] = $value;
                }
            }
        }

        // Apply sort if provided, otherwise default to ordering by day if applicable
        if (isset($params['sort'])) {
            $sort = $params['sort'];
            $baseSql .= " ORDER BY $sort";
        } else if ($hasDayColumn) {
            $baseSql .= " ORDER BY $orderCaseSql";
        }

        // Apply limit if provided
        if (isset($params['limit'])) {
            $limit = intval($params['limit']);
            $baseSql .= " LIMIT ?";
            $queryParams[] = $limit;
        }
    } else if ($hasDayColumn) {
        // Default ordering by day if no parameters are provided
        $baseSql .= " ORDER BY $orderCaseSql";
    }

    // Execute the final query
    executeQuery($conn, $baseSql, $queryParams);
}

// Close database connection
$conn->close();
?>
