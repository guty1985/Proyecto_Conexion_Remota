-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-06-2017 a las 05:55:03
-- Versión del servidor: 10.1.19-MariaDB
-- Versión de PHP: 5.6.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `paginas_web`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `diccionario`
--

CREATE TABLE `diccionario` (
  `id` int(20) NOT NULL,
  `pa_clave` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `diccionario`
--

INSERT INTO `diccionario` (`id`, `pa_clave`) VALUES
(1, 'Conejitas'),
(2, 'Entretenimiento'),
(3, 'Entrevistas'),
(4, 'Amor'),
(5, 'Mujeres'),
(6, 'Playboy'),
(7, 'Revista'),
(8, 'Soho'),
(9, 'Pornografia'),
(10, 'Orgia'),
(11, 'Actriz');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `id` int(40) NOT NULL,
  `nom_empresa` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`id`, `nom_empresa`) VALUES
(1, 'Soho'),
(2, 'El Universal'),
(3, 'Televisa'),
(4, 'Univision'),
(5, 'Cromos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lista_negra`
--

CREATE TABLE `lista_negra` (
  `id` int(20) NOT NULL,
  `pagina` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `lista_negra`
--

INSERT INTO `lista_negra` (`id`, `pagina`) VALUES
(1, 'www.taringa.net'),
(2, 'www.todorojadirecta.com'),
(3, 'www.pelis24.com '),
(4, 'www.pelitube.net ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paginas`
--

CREATE TABLE `paginas` (
  `id` int(20) NOT NULL,
  `nombre` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `paginas`
--

INSERT INTO `paginas` (`id`, `nombre`) VALUES
(1, 'http://www.soho.co'),
(2, 'http://cromos.elespectador.com/'),
(3, 'http://www.univision.com'),
(4, 'http://www.cromos.com.co');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pa_no_apta`
--

CREATE TABLE `pa_no_apta` (
  `id` int(20) NOT NULL,
  `palabra` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `pa_no_apta`
--

INSERT INTO `pa_no_apta` (`id`, `palabra`) VALUES
(1, 'sexo'),
(2, 'Desnudo'),
(3, 'Denudas'),
(4, 'Porno'),
(5, 'xxx'),
(6, 'putas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `penalizadas`
--

CREATE TABLE `penalizadas` (
  `id` int(10) NOT NULL,
  `pagina` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `penalizadas`
--

INSERT INTO `penalizadas` (`id`, `pagina`) VALUES
(1, 'http://www.soho.co');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ranking`
--

CREATE TABLE `ranking` (
  `Id` int(40) NOT NULL,
  `titulo` varchar(40) NOT NULL,
  `pagina` varchar(40) NOT NULL,
  `externo` varchar(40) NOT NULL,
  `contenido` varchar(40) NOT NULL,
  `claves` varchar(40) NOT NULL,
  `interno` varchar(40) NOT NULL,
  `imagenes` varchar(40) NOT NULL,
  `no_penalizada` varchar(40) NOT NULL,
  `longitud` varchar(40) NOT NULL,
  `redes` varchar(40) NOT NULL,
  `total` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `ranking`
--

INSERT INTO `ranking` (`Id`, `titulo`, `pagina`, `externo`, `contenido`, `claves`, `interno`, `imagenes`, `no_penalizada`, `longitud`, `redes`, `total`) VALUES
(1, '11', 'http://www.soho.co', '33', '859', '1', '183', '35', '1', '11', '5', '1117');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `diccionario`
--
ALTER TABLE `diccionario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `empresas`
--
ALTER TABLE `empresas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `lista_negra`
--
ALTER TABLE `lista_negra`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `paginas`
--
ALTER TABLE `paginas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pa_no_apta`
--
ALTER TABLE `pa_no_apta`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `penalizadas`
--
ALTER TABLE `penalizadas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ranking`
--
ALTER TABLE `ranking`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `diccionario`
--
ALTER TABLE `diccionario`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `id` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT de la tabla `lista_negra`
--
ALTER TABLE `lista_negra`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `paginas`
--
ALTER TABLE `paginas`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `pa_no_apta`
--
ALTER TABLE `pa_no_apta`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT de la tabla `penalizadas`
--
ALTER TABLE `penalizadas`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT de la tabla `ranking`
--
ALTER TABLE `ranking`
  MODIFY `Id` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
