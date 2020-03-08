-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 06. Feb 2020 um 17:54
-- Server-Version: 10.4.11-MariaDB
-- PHP-Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS todo;
USE todo;

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `todo`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `todos`
--

CREATE TABLE `todos` (
  `item_id` int(11) NOT NULL,
  `list_id` int(11) NOT NULL COMMENT 'FK',
  `title` varchar(25) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `finished` tinyint(1) NOT NULL DEFAULT 0,
  `due_date` timestamp NULL DEFAULT current_timestamp(),
  `address` longtext DEFAULT NULL,
  `priority` int(11) NOT NULL DEFAULT 0,
  `subtasks` longtext DEFAULT NULL,
  `reminder` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `todo_lists`
--

CREATE TABLE `todo_lists` (
  `list_id` int(11) NOT NULL,
  `name` varchar(25) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `hex_color` varchar(7) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `todo_lists`
--

INSERT INTO `todo_lists` (`list_id`, `name`, `description`, `hex_color`, `created_at`) VALUES
(1, 'default', 'default', '#FFFFFF', '2020-02-06 16:40:59');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `todos`
--
ALTER TABLE `todos`
  ADD PRIMARY KEY (`item_id`);

--
-- Indizes für die Tabelle `todo_lists`
--
ALTER TABLE `todo_lists`
  ADD PRIMARY KEY (`list_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `todos`
--
ALTER TABLE `todos`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `todo_lists`
--
ALTER TABLE `todo_lists`
  MODIFY `list_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
