-- MySQL dump 10.13  Distrib 8.0.21, for osx10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: variant_db
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_disease`
--

DROP TABLE IF EXISTS `api_disease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_disease` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `others` varchar(20) DEFAULT NULL,
  `report` varchar(20) DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_disease_variant_id_81f53161_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_disease_variant_id_81f53161_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_disease`
--

LOCK TABLES `api_disease` WRITE;
/*!40000 ALTER TABLE `api_disease` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_disease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_evidence`
--

DROP TABLE IF EXISTS `api_evidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_evidence` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_type` varchar(2) NOT NULL,
  `source_id` varchar(20) DEFAULT NULL,
  `statement` longtext,
  `disease_id` int DEFAULT NULL,
  `functional_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_evidence_functional_id_8f0cb7e1_fk_api_functional_id` (`functional_id`),
  KEY `api_evidence_item_id_46e9aba1_fk_api_pathitem_id` (`item_id`),
  KEY `api_evidence_disease_id_0f0c81a5_fk_api_disease_id` (`disease_id`),
  CONSTRAINT `api_evidence_disease_id_0f0c81a5_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`),
  CONSTRAINT `api_evidence_functional_id_8f0cb7e1_fk_api_functional_id` FOREIGN KEY (`functional_id`) REFERENCES `api_functional` (`id`),
  CONSTRAINT `api_evidence_item_id_46e9aba1_fk_api_pathitem_id` FOREIGN KEY (`item_id`) REFERENCES `api_pathitem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_evidence`
--

LOCK TABLES `api_evidence` WRITE;
/*!40000 ALTER TABLE `api_evidence` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_evidence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_functional`
--

DROP TABLE IF EXISTS `api_functional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_functional` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(20) DEFAULT NULL,
  `value` varchar(20) DEFAULT NULL,
  `disease_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_functional_disease_id_9f50e00d_fk_api_disease_id` (`disease_id`),
  CONSTRAINT `api_functional_disease_id_9f50e00d_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_functional`
--

LOCK TABLES `api_functional` WRITE;
/*!40000 ALTER TABLE `api_functional` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_functional` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_gene`
--

DROP TABLE IF EXISTS `api_gene`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_gene` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_gene`
--

LOCK TABLES `api_gene` WRITE;
/*!40000 ALTER TABLE `api_gene` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_gene` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_history`
--

DROP TABLE IF EXISTS `api_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` longtext,
  `timestamp` datetime(6) NOT NULL,
  `object_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_history_object_id_33723063_fk_api_evidence_id` (`object_id`),
  KEY `api_history_user_id_b67a8aac_fk_auth_user_id` (`user_id`),
  KEY `api_history_variant_id_9b04b65b_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_history_object_id_33723063_fk_api_evidence_id` FOREIGN KEY (`object_id`) REFERENCES `api_evidence` (`id`),
  CONSTRAINT `api_history_user_id_b67a8aac_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `api_history_variant_id_9b04b65b_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_history`
--

LOCK TABLES `api_history` WRITE;
/*!40000 ALTER TABLE `api_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_interpretation`
--

DROP TABLE IF EXISTS `api_interpretation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_interpretation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_interpretation`
--

LOCK TABLES `api_interpretation` WRITE;
/*!40000 ALTER TABLE `api_interpretation` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_interpretation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_interpretation_genes`
--

DROP TABLE IF EXISTS `api_interpretation_genes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_interpretation_genes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `interpretation_id` int NOT NULL,
  `gene_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_interpretation_genes_interpretation_id_gene_id_7ce4483b_uniq` (`interpretation_id`,`gene_id`),
  KEY `api_interpretation_genes_gene_id_332b2314_fk_api_gene_id` (`gene_id`),
  CONSTRAINT `api_interpretation_g_interpretation_id_363ce684_fk_api_inter` FOREIGN KEY (`interpretation_id`) REFERENCES `api_interpretation` (`id`),
  CONSTRAINT `api_interpretation_genes_gene_id_332b2314_fk_api_gene_id` FOREIGN KEY (`gene_id`) REFERENCES `api_gene` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_interpretation_genes`
--

LOCK TABLES `api_interpretation_genes` WRITE;
/*!40000 ALTER TABLE `api_interpretation_genes` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_interpretation_genes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_interpretation_variants`
--

DROP TABLE IF EXISTS `api_interpretation_variants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_interpretation_variants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `interpretation_id` int NOT NULL,
  `variant_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `api_interpretation_varia_interpretation_id_varian_626d2605_uniq` (`interpretation_id`,`variant_id`),
  KEY `api_interpretation_v_variant_id_81cb755e_fk_api_varia` (`variant_id`),
  CONSTRAINT `api_interpretation_v_interpretation_id_7712e4a0_fk_api_inter` FOREIGN KEY (`interpretation_id`) REFERENCES `api_interpretation` (`id`),
  CONSTRAINT `api_interpretation_v_variant_id_81cb755e_fk_api_varia` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_interpretation_variants`
--

LOCK TABLES `api_interpretation_variants` WRITE;
/*!40000 ALTER TABLE `api_interpretation_variants` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_interpretation_variants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_pathitem`
--

DROP TABLE IF EXISTS `api_pathitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_pathitem` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(5) DEFAULT NULL,
  `value` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_pathitem`
--

LOCK TABLES `api_pathitem` WRITE;
/*!40000 ALTER TABLE `api_pathitem` DISABLE KEYS */;
INSERT INTO `api_pathitem` VALUES (1,'PVS1',10),(2,'PS1',7),(3,'PS2',7),(4,'PS3',7),(5,'PS4',7),(6,'PM',2),(7,'PM1',2),(8,'PM2',2),(9,'PM3',2),(10,'PM4',2),(11,'PM5',2),(12,'PM6',2),(13,'PP1',1),(14,'PP2',1),(15,'PP3',1),(16,'PP4',1),(17,'PP5',1),(18,'BA1',16),(19,'BS1',8),(20,'BS2',8),(21,'BS3',8),(22,'BS4',8),(23,'BP1',1),(24,'BP2',1),(25,'BP3',1),(26,'BP4',1),(27,'BP5',1),(28,'BP6',1),(29,'BP7',1);
/*!40000 ALTER TABLE `api_pathitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_report`
--

DROP TABLE IF EXISTS `api_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_report` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `content` longtext,
  `disease_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_report_disease_id_7b991380_fk_api_disease_id` (`disease_id`),
  CONSTRAINT `api_report_disease_id_7b991380_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_report`
--

LOCK TABLES `api_report` WRITE;
/*!40000 ALTER TABLE `api_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_score`
--

DROP TABLE IF EXISTS `api_score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `for_score` varchar(20) DEFAULT NULL,
  `against_score` varchar(20) DEFAULT NULL,
  `disease_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_score_disease_id_36796f93_fk_api_disease_id` (`disease_id`),
  CONSTRAINT `api_score_disease_id_36796f93_fk_api_disease_id` FOREIGN KEY (`disease_id`) REFERENCES `api_disease` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_score`
--

LOCK TABLES `api_score` WRITE;
/*!40000 ALTER TABLE `api_score` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_subevidence`
--

DROP TABLE IF EXISTS `api_subevidence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_subevidence` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level` varchar(1) DEFAULT NULL,
  `evid_sig` varchar(4) NOT NULL,
  `evid_dir` tinyint(1) DEFAULT NULL,
  `clin_sig` varchar(25) NOT NULL,
  `drug_class` longtext,
  `evid_rating` int NOT NULL,
  `evidence_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_subevidence_evidence_id_8eb5cfe0_fk_api_evidence_id` (`evidence_id`),
  KEY `api_subevidence_variant_id_46b41725_fk_api_variant_id` (`variant_id`),
  CONSTRAINT `api_subevidence_evidence_id_8eb5cfe0_fk_api_evidence_id` FOREIGN KEY (`evidence_id`) REFERENCES `api_evidence` (`id`),
  CONSTRAINT `api_subevidence_variant_id_46b41725_fk_api_variant_id` FOREIGN KEY (`variant_id`) REFERENCES `api_variant` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_subevidence`
--

LOCK TABLES `api_subevidence` WRITE;
/*!40000 ALTER TABLE `api_subevidence` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_subevidence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_variant`
--

DROP TABLE IF EXISTS `api_variant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `api_variant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `genome_build` varchar(10) DEFAULT NULL,
  `chromosome` varchar(6) DEFAULT NULL,
  `start` varchar(10) DEFAULT NULL,
  `end` varchar(10) DEFAULT NULL,
  `ref` varchar(100) DEFAULT NULL,
  `alt` varchar(100) DEFAULT NULL,
  `transcript` varchar(20) DEFAULT NULL,
  `c` varchar(10) DEFAULT NULL,
  `p` varchar(20) DEFAULT NULL,
  `consequence` varchar(10) DEFAULT NULL,
  `branch` varchar(2) NOT NULL,
  `reported` varchar(1) NOT NULL,
  `gene_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_variant_gene_id_5263a79c_fk_api_gene_id` (`gene_id`),
  CONSTRAINT `api_variant_gene_id_5263a79c_fk_api_gene_id` FOREIGN KEY (`gene_id`) REFERENCES `api_gene` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_variant`
--

LOCK TABLES `api_variant` WRITE;
/*!40000 ALTER TABLE `api_variant` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_variant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add disease',1,'add_disease'),(2,'Can change disease',1,'change_disease'),(3,'Can delete disease',1,'delete_disease'),(4,'Can view disease',1,'view_disease'),(5,'Can add evidence',2,'add_evidence'),(6,'Can change evidence',2,'change_evidence'),(7,'Can delete evidence',2,'delete_evidence'),(8,'Can view evidence',2,'view_evidence'),(9,'Can add gene',3,'add_gene'),(10,'Can change gene',3,'change_gene'),(11,'Can delete gene',3,'delete_gene'),(12,'Can view gene',3,'view_gene'),(13,'Can add path item',4,'add_pathitem'),(14,'Can change path item',4,'change_pathitem'),(15,'Can delete path item',4,'delete_pathitem'),(16,'Can view path item',4,'view_pathitem'),(17,'Can add variant',5,'add_variant'),(18,'Can change variant',5,'change_variant'),(19,'Can delete variant',5,'delete_variant'),(20,'Can view variant',5,'view_variant'),(21,'Can add sub evidence',6,'add_subevidence'),(22,'Can change sub evidence',6,'change_subevidence'),(23,'Can delete sub evidence',6,'delete_subevidence'),(24,'Can view sub evidence',6,'view_subevidence'),(25,'Can add score',7,'add_score'),(26,'Can change score',7,'change_score'),(27,'Can delete score',7,'delete_score'),(28,'Can view score',7,'view_score'),(29,'Can add report',8,'add_report'),(30,'Can change report',8,'change_report'),(31,'Can delete report',8,'delete_report'),(32,'Can view report',8,'view_report'),(33,'Can add interpretation',9,'add_interpretation'),(34,'Can change interpretation',9,'change_interpretation'),(35,'Can delete interpretation',9,'delete_interpretation'),(36,'Can view interpretation',9,'view_interpretation'),(37,'Can add history',10,'add_history'),(38,'Can change history',10,'change_history'),(39,'Can delete history',10,'delete_history'),(40,'Can view history',10,'view_history'),(41,'Can add functional',11,'add_functional'),(42,'Can change functional',11,'change_functional'),(43,'Can delete functional',11,'delete_functional'),(44,'Can view functional',11,'view_functional'),(45,'Can add log entry',12,'add_logentry'),(46,'Can change log entry',12,'change_logentry'),(47,'Can delete log entry',12,'delete_logentry'),(48,'Can view log entry',12,'view_logentry'),(49,'Can add permission',13,'add_permission'),(50,'Can change permission',13,'change_permission'),(51,'Can delete permission',13,'delete_permission'),(52,'Can view permission',13,'view_permission'),(53,'Can add group',14,'add_group'),(54,'Can change group',14,'change_group'),(55,'Can delete group',14,'delete_group'),(56,'Can view group',14,'view_group'),(57,'Can add user',15,'add_user'),(58,'Can change user',15,'change_user'),(59,'Can delete user',15,'delete_user'),(60,'Can view user',15,'view_user'),(61,'Can add content type',16,'add_contenttype'),(62,'Can change content type',16,'change_contenttype'),(63,'Can delete content type',16,'delete_contenttype'),(64,'Can view content type',16,'view_contenttype'),(65,'Can add session',17,'add_session'),(66,'Can change session',17,'change_session'),(67,'Can delete session',17,'delete_session'),(68,'Can view session',17,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$216000$BiNQvCtdCbjG$/jx9RdndQ+Yn0OlaWTZKvAI/qXaVcWgJp1ygRAzH2ss=',NULL,1,'admin','','','',1,1,'2020-09-17 13:57:33.135395');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (12,'admin','logentry'),(1,'api','disease'),(2,'api','evidence'),(11,'api','functional'),(3,'api','gene'),(10,'api','history'),(9,'api','interpretation'),(4,'api','pathitem'),(8,'api','report'),(7,'api','score'),(6,'api','subevidence'),(5,'api','variant'),(14,'auth','group'),(13,'auth','permission'),(15,'auth','user'),(16,'contenttypes','contenttype'),(17,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-09-17 13:56:59.316861'),(2,'auth','0001_initial','2020-09-17 13:56:59.440858'),(3,'admin','0001_initial','2020-09-17 13:56:59.729471'),(4,'admin','0002_logentry_remove_auto_add','2020-09-17 13:56:59.795969'),(5,'admin','0003_logentry_add_action_flag_choices','2020-09-17 13:56:59.807701'),(6,'api','0001_initial','2020-09-17 13:57:00.167884'),(7,'contenttypes','0002_remove_content_type_name','2020-09-17 13:57:00.588769'),(8,'auth','0002_alter_permission_name_max_length','2020-09-17 13:57:00.644233'),(9,'auth','0003_alter_user_email_max_length','2020-09-17 13:57:00.671773'),(10,'auth','0004_alter_user_username_opts','2020-09-17 13:57:00.683885'),(11,'auth','0005_alter_user_last_login_null','2020-09-17 13:57:00.758588'),(12,'auth','0006_require_contenttypes_0002','2020-09-17 13:57:00.761701'),(13,'auth','0007_alter_validators_add_error_messages','2020-09-17 13:57:00.773637'),(14,'auth','0008_alter_user_username_max_length','2020-09-17 13:57:00.822549'),(15,'auth','0009_alter_user_last_name_max_length','2020-09-17 13:57:00.866630'),(16,'auth','0010_alter_group_name_max_length','2020-09-17 13:57:00.895707'),(17,'auth','0011_update_proxy_permissions','2020-09-17 13:57:00.922807'),(18,'auth','0012_alter_user_first_name_max_length','2020-09-17 13:57:00.967029'),(19,'sessions','0001_initial','2020-09-17 13:57:00.985055');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-17  9:59:10
