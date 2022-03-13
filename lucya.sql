-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 13, 2022 at 07:16 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lucya`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `banned` int(255) NOT NULL DEFAULT 0,
  `money` int(225) NOT NULL DEFAULT 0,
  `blurb` varchar(225) NOT NULL DEFAULT 'Hello, i''m new to Lucya!',
  `following` int(255) NOT NULL DEFAULT 0,
  `followers` int(255) NOT NULL DEFAULT 0,
  `created` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `gender` varchar(255) NOT NULL DEFAULT 'male',
  `birthday` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`id`, `username`, `password`, `email`, `banned`, `money`, `blurb`, `following`, `followers`, `created`, `gender`, `birthday`) VALUES
(1, 'Example', 'Example', 'Undefined', 0, 15, 'Yeah...', 0, 0, '2022-03-13 18:09:59.558461', 'male', '22Aug1923');

-- --------------------------------------------------------

--
-- Table structure for table `badges`
--

CREATE TABLE `badges` (
  `authorid` int(255) NOT NULL,
  `badgeid` int(225) NOT NULL,
  `deleted` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `freinds`
--

CREATE TABLE `freinds` (
  `author` int(255) NOT NULL,
  `friend` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `freinds`
--

INSERT INTO `freinds` (`author`, `friend`) VALUES
(7, 2);

-- --------------------------------------------------------

--
-- Table structure for table `friendrequests`
--

CREATE TABLE `friendrequests` (
  `senderid` int(255) NOT NULL,
  `recipientid` int(225) NOT NULL,
  `accepted` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `itemname` varchar(255) NOT NULL,
  `price` int(255) NOT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'hat',
  `itemdesc` varchar(255) DEFAULT NULL,
  `authorid` int(11) DEFAULT NULL,
  `favs` int(255) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `itemname`, `price`, `type`, `itemdesc`, `authorid`, `favs`) VALUES
(1, 'ROBLOX \'R\' Baseball Cap', 99999999, 'Hat', 'Imagine a world where you own this baseball cap. Oh - that\'s this world!', 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `owneditems`
--

CREATE TABLE `owneditems` (
  `itemid` int(255) NOT NULL,
  `userid` int(225) NOT NULL,
  `type` varchar(255) NOT NULL,
  `deleted` int(225) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
