-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 25 mai 2025 à 20:07
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `bdan`
--

-- --------------------------------------------------------

--
-- Structure de la table `app_annonce`
--

DROP TABLE IF EXISTS `app_annonce`;
CREATE TABLE IF NOT EXISTS `app_annonce` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `images` json NOT NULL,
  `titre` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `prix` double NOT NULL,
  `datePublication` datetime(6) NOT NULL,
  `statut` tinyint(1) NOT NULL,
  `isPremieum` tinyint(1) NOT NULL,
  `categorie_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `localisation` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `App_annonce_user_id_76fc1580_fk_App_user_id` (`user_id`),
  KEY `App_annonce_categorie_id_0cb45212_fk_App_categorie_id` (`categorie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `app_annonce`
--

INSERT INTO `app_annonce` (`id`, `images`, `titre`, `description`, `prix`, `datePublication`, `statut`, `isPremieum`, `categorie_id`, `user_id`, `localisation`) VALUES
(16, '[\"annonces/IMG-20250525-WA0018.jpg\", \"annonces/IMG-20250525-WA0019.jpg\"]', 'Rituals', 'Rituals of Sakura Madium Gift Set', 45, '2025-05-24 16:41:24.778186', 1, 0, 32, 2, 'Casablanca'),
(18, '[\"annonces/IMG-20250525-WA0021.jpg\", \"annonces/IMG-20250525-WA0020.jpg\", \"annonces/IMG-20250525-WA0026.jpg\"]', 'Appartement centre ville', 'Bel appartement 3 pièces, 80m², vue dégagée', 1200000, '2025-05-24 18:05:50.000000', 1, 0, 9, 2, 'Casablanca'),
(19, '[\"annonces/IMG-20250525-WA0023.jpg\", \"annonces/IMG-20250525-WA0024.jpg\"]', 'Villa avec jardin', 'Villa spacieuse 5 pièces avec piscine et jardin', 3500000, '2025-05-24 18:05:50.000000', 1, 1, 9, 2, 'Rabat'),
(20, '[\"annonces/IMG-20250525-WA0028.jpg\", \"annonces/IMG-20250525-WA0027.jpg\"]', 'Colocation étudiante', 'Chambre individuelle dans appartement partagé, quartier calme', 1500, '2025-05-24 18:06:29.000000', 1, 0, 10, 2, 'Casablanca'),
(21, '[\"annonces/IMG-20250525-WA0025.jpg\", \"annonces/IMG-20250525-WA0022.jpg\"]', 'Colocation professionnelle', 'Grande chambre avec bureau, proximité transports', 2500, '2025-05-24 18:06:29.000000', 1, 0, 10, 2, 'Marrakech'),
(22, '[\"annonces/IMG-20250525-WA0017.jpg\"]', 'Peugeot 208', 'Voiture 2019, 45000km, diesel, bien entretenue', 145000, '2025-05-24 18:06:45.000000', 1, 0, 13, 2, 'Casablanca'),
(23, '[\"annonces/IMG-20250525-WA0015.jpg\", \"annonces/IMG-20250525-WA0016.jpg\"]', 'Yamaha MT-07', 'Moto 2020, 12000km, couleur bleue', 65000, '2025-05-24 18:06:45.000000', 1, 1, 13, 2, 'Rabat'),
(24, '[\"annonces/IMG-20250525-WA0013.jpg\", \"annonces/IMG-20250525-WA0014.jpg\"]', 'Renault Kangoo', 'Utilitaire 2018, 80000km, bon état général', 85000, '2025-05-24 18:08:02.000000', 1, 0, 14, 2, 'Casablanca'),
(25, '[\"annonces/IMG-20250525-WA0011.jpg\", \"annonces/IMG-20250525-WA0012.jpg\"]', 'Vélo électrique', 'Vélo électrique neuf, autonomie 60km', 7500, '2025-05-24 18:08:02.000000', 1, 0, 14, 2, 'Marrakech'),
(26, '[\"annonces/IMG-20250525-WA0009.jpg\", \"annonces/IMG-20250525-WA0010.jpg\"]', 'Développeur Fullstack', 'CDI pour développeur React/Node.js, 3 ans d\'expérience min.', 0, '2025-05-24 18:08:23.000000', 1, 0, 17, 2, 'Casablanca'),
(27, '[\"annonces/IMG-20250525-WA0007.jpg\", \"annonces/IMG-20250525-WA0008.jpg\"]', 'Comptable senior', 'Poste en cabinet comptable, formation continue offerte', 0, '2025-05-24 18:08:23.000000', 1, 0, 17, 2, 'Rabat'),
(28, '[\"annonces/image4.jpg\"]', 'Costume homme', 'Costume 3 pièces taille 42, couleur anthracite', 450, '2025-05-24 18:08:37.000000', 1, 0, 21, 2, 'Casablanca'),
(29, '[\"annonces/image2.jpg\", \"annonces/image5.jpg\"]', 'Baskets de marque', 'Baskets neuves taille 43, modèle limité', 350, '2025-05-24 18:08:37.000000', 1, 0, 21, 2, 'Marrakech'),
(30, '[\"annonces/image1.jpg\"]', 'iPhone 13 Pro', '128Go, couleur bleu, avec accessoires', 8500, '2025-05-24 18:08:51.000000', 1, 1, 25, 2, 'Casablanca'),
(31, '[\"annonces/image3.jpg\"]', 'iPad Air', 'Dernier modèle, 256Go, écran 10.9\"', 6500, '2025-05-24 18:08:51.000000', 1, 1, 25, 2, 'Rabat'),
(37, '[\"annonces/WhatsApp Image 2025-05-25 à 14.28.31_47c87b4a.jpg\", \"annonces/WhatsApp Image 2025-05-25 à 14.28.32_4ed68ebb.jpg\", \"annonces/WhatsApp Image 2025-05-25 à 14.28.32_4043bcd2.jpg\"]', 'Voilà', 'Shop Skin Care ', 100, '2025-05-25 13:31:19.356516', 1, 1, 32, 1, 'Casablanca'),
(38, '[\"annonces/WhatsApp Image 2025-05-25 à 14.41.30_177da556.jpg\", \"annonces/WhatsApp Image 2025-05-25 à 14.41.30_92499283.jpg\"]', 'Cafe', 'Bakery&Coffe', 100, '2025-05-25 13:45:12.572963', 1, 0, 31, 3, 'Casablanca'),
(39, '[\"annonces/WhatsApp Image 2025-05-25 à 14.53.47_f18cec52.jpg\", \"annonces/WhatsApp Image 2025-05-25 à 14.53.49_48051a77.jpg\"]', 'Vêtement Bebe', 'Vêtements de bébé neutres | style automne hiver | idée de tenue de tout-petit | tenue de patch de citrouille | confortable | ensemble de bébé mignon', 20, '2025-05-25 14:03:44.303790', 0, 0, 21, 3, 'Casablanca');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `app_annonce`
--
ALTER TABLE `app_annonce`
  ADD CONSTRAINT `App_annonce_categorie_id_0cb45212_fk_App_categorie_id` FOREIGN KEY (`categorie_id`) REFERENCES `app_categorie` (`id`),
  ADD CONSTRAINT `App_annonce_user_id_76fc1580_fk_App_user_id` FOREIGN KEY (`user_id`) REFERENCES `app_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
