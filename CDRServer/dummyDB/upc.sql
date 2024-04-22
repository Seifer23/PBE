-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-04-2024 a las 18:09:01
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `upc`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marks`
--

CREATE TABLE `marks` (
  `mark_id` int(11) NOT NULL,
  `name` text NOT NULL,
  `mark` float NOT NULL,
  `subject` text NOT NULL,
  `student_id` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `marks`
--

INSERT INTO `marks` (`mark_id`, `name`, `mark`, `subject`, `student_id`) VALUES
(1, 'Parcial', 5.6, 'DSBM', '76E4FBB0'),
(2, 'Psricls', 10, 'CAL', '12345678'),
(3, 'Memoria Lab', 9, 'PSAVC', '76E4FBB0'),
(4, 'Entregable 4', 7.7, 'FISE', '76E4FBB0'),
(5, 'Segon parcial', 3.2, 'ICOM', '76E4FBB0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `students`
--

CREATE TABLE `students` (
  `student_id` varchar(8) NOT NULL,
  `name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `students`
--

INSERT INTO `students` (`student_id`, `name`) VALUES
('12345678', 'Test'),
('71F4A91C', 'Elena Nito'),
('76E4FBB0', 'Salvador Rodo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tasks`
--

CREATE TABLE `tasks` (
  `date` date NOT NULL,
  `subject` text NOT NULL,
  `name` text NOT NULL,
  `task_id` int(11) NOT NULL,
  `student_id` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tasks`
--

INSERT INTO `tasks` (`date`, `subject`, `name`, `task_id`, `student_id`) VALUES
('2024-04-07', 'DSBM', 'Memoria 1', 1, '76E4FBB0'),
('2024-04-08', 'ICOM', 'Previ Lab2', 2, '76E4FBB0'),
('2024-04-21', 'PSAVC', 'Previ 5', 3, '12345678');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `timetables`
--

CREATE TABLE `timetables` (
  `day` varchar(3) NOT NULL,
  `hour` time NOT NULL,
  `subject` text NOT NULL,
  `room` text NOT NULL,
  `timetable_id` int(11) NOT NULL,
  `student_id` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `timetables`
--

INSERT INTO `timetables` (`day`, `hour`, `subject`, `room`, `timetable_id`, `student_id`) VALUES
('Fri', '08:00:00', 'ICOM', 'A3205', 4, '76E4FBB0'),
('Fri', '12:00:00', 'Lab ICOM', 'D4001', 5, '76E4FBB0'),
('Mon', '08:00:00', 'FISE', 'A3205', 6, '76E4FBB0'),
('Tue', '08:00:00', 'AST', 'A3001', 7, '76E4FBB0'),
('Wed', '12:00:00', 'ONELE', 'A4101', 8, '76E4FBB0'),
('Thu', '08:00:00', 'IPAV', 'A3204', 9, '76E4FBB0'),
('Tue', '12:00:00', 'CAL', 'A3001', 10, '12345678'),
('Tue', '08:00:00', 'MATEL', 'A4001', 11, '12345678');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `marks`
--
ALTER TABLE `marks`
  ADD PRIMARY KEY (`mark_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indices de la tabla `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`);

--
-- Indices de la tabla `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`task_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indices de la tabla `timetables`
--
ALTER TABLE `timetables`
  ADD PRIMARY KEY (`timetable_id`),
  ADD KEY `student_id` (`student_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `marks`
--
ALTER TABLE `marks`
  MODIFY `mark_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tasks`
--
ALTER TABLE `tasks`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `timetables`
--
ALTER TABLE `timetables`
  MODIFY `timetable_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `marks`
--
ALTER TABLE `marks`
  ADD CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Filtros para la tabla `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);

--
-- Filtros para la tabla `timetables`
--
ALTER TABLE `timetables`
  ADD CONSTRAINT `timetables_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
