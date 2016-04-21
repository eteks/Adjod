CREATE DATABASE  IF NOT EXISTS `adjod` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adjod`;
-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: adjod
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `advertisement_category`
--

DROP TABLE IF EXISTS `advertisement_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `icon` varchar(100) NOT NULL,
  `name` varchar(250) NOT NULL,
  `category_type` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_category`
--

LOCK TABLES `advertisement_category` WRITE;
/*!40000 ALTER TABLE `advertisement_category` DISABLE KEYS */;
INSERT INTO `advertisement_category` VALUES (1,'icons/car.png','Cars & Bikes','Suzuki,Audi,BMW'),(2,'icons/mobile.png','Mobiles & Tablets','Macbooks,Asus laptops'),(3,'icons/plug.png','Electronic & Appliance','Cordless,Electric cooker,Fridge'),(4,'icons/home.png','Real estate','Flats for sale,Space for rent'),(5,'icons/case.png','Jobs','Part timer,Freelancer'),(6,'icons/tree.png','Home & Lifestyle','Light lamps,Luggage'),(7,'icons/tool.png','Services','Architecture,advertising'),(8,'icons/prize.png','Education & Learning','Tuition classes,Online coaching'),(9,'icons/paw.png','Pets & Pet care','SPet Adoption,Pet care'),(10,'icons/game.png','Entertainment','Gaming,Cameramen'),(11,'icons/gift.png','Community & Events','Party, Event, Charity'),(12,'icons/heart.png','Matrimonial','Grooms,bride,planner');
/*!40000 ALTER TABLE `advertisement_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adjod_exchangerate`
--

DROP TABLE IF EXISTS `adjod_exchangerate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adjod_exchangerate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currency` varchar(3) NOT NULL,
  `value` decimal(20,6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjod_exchangerate`
--

LOCK TABLES `adjod_exchangerate` WRITE;
/*!40000 ALTER TABLE `adjod_exchangerate` DISABLE KEYS */;
INSERT INTO `adjod_exchangerate` VALUES (1,'DZD',75.764861),(2,'NAD',10.844404),(3,'GHS',2.709401),(4,'EGP',5.539680),(5,'BGN',1.265722),(6,'PAB',0.707550),(7,'BOB',4.897305),(8,'DKK',4.828006),(9,'BWP',7.904119),(10,'LBP',1068.867230),(11,'TZS',1527.936179),(12,'VND',15878.845298),(13,'AOA',95.724416),(14,'KHR',2871.820944),(15,'MYR',3.037940),(16,'KYD',0.583015),(17,'LYD',0.985462),(18,'UAH',16.936762),(19,'JOD',0.501473),(20,'AWG',1.268872),(21,'SAR',2.654135),(22,'LTL',2.194440),(23,'HKD',5.483787),(24,'CHF',0.701570),(25,'GIP',0.476810),(26,'BYR',13150.185237),(27,'ALL',88.726821),(28,'XPD',0.001274),(29,'MRO',217.303061),(30,'HRK',4.941577),(31,'DJF',125.703923),(32,'SZL',10.843767),(33,'THB',25.521429),(34,'XAF',425.195172),(35,'BND',1.000257),(36,'ISK',91.274566),(37,'UYU',21.121912),(38,'NIO',19.736247),(39,'LAK',5780.255927),(40,'SYP',155.860023),(41,'MAD',6.991969),(42,'MZN',33.870411),(43,'PHP',33.241788),(44,'ZAR',10.851041),(45,'NPR',75.165143),(46,'ZWL',228.059428),(47,'NGN',140.835674),(48,'CRC',380.828868),(49,'AED',2.598867),(50,'EEK',10.114796),(51,'MWK',464.286621),(52,'LKR',102.133121),(53,'PKR',74.244337),(54,'HUF',202.762982),(55,'BMD',0.707550),(56,'LSL',10.840548),(57,'MNT',1410.736455),(58,'AMD',341.396335),(59,'UGX',2394.389931),(60,'QAR',2.576409),(61,'XDR',0.509654),(62,'JMD',84.968670),(63,'GEL',1.696669),(64,'SHP',0.476810),(65,'AFN',48.417636),(66,'SBD',5.752243),(67,'KPW',636.858535),(68,'TRY',2.058961),(69,'BDT',55.553070),(70,'YER',152.115220),(71,'HTG',40.208784),(72,'XOF',425.985732),(73,'MGA',2271.151271),(74,'ANG',1.265647),(75,'LRD',60.552117),(76,'RWF',529.147071),(77,'NOK',6.165521),(78,'MOP',5.653282),(79,'INR',46.950312),(80,'MXN',12.207074),(81,'CZK',17.486974),(82,'TJS',4.935443),(83,'BTC',0.001643),(84,'BTN',46.960306),(85,'COP',2246.754952),(86,'TMT',2.477509),(87,'MUR',25.383085),(88,'IDR',9739.352790),(89,'HNL',15.747831),(90,'XPF',77.204592),(91,'FJD',1.496433),(92,'ETB',15.006191),(93,'PEN',2.408372),(94,'BZD',1.413087),(95,'ILS',2.758433),(96,'DOP',32.265249),(97,'GGP',0.476810),(98,'MDL',13.923987),(99,'XPT',0.000795),(100,'BSD',0.707550),(101,'SEK',5.922913),(102,'ZMK',3716.812555),(103,'JEP',0.476810),(104,'AUD',0.970902),(105,'SRD',2.824893),(106,'CUP',0.708231),(107,'CLF',0.017407),(108,'BBD',1.415100),(109,'KMF',318.866236),(110,'KRW',828.970114),(111,'GMD',27.870657),(112,'VEF',4.472067),(113,'IMP',0.476810),(114,'CUC',0.707550),(115,'CLP',501.344137),(116,'ZMW',7.764970),(117,'EUR',0.647312),(118,'CDF',654.852589),(119,'XCD',1.911106),(120,'KZT',240.174531),(121,'RUB',51.201171),(122,'XAG',0.050758),(123,'TTD',4.549607),(124,'OMR',0.272402),(125,'BRL',2.734331),(126,'MMK',929.122593),(127,'PLN',2.740145),(128,'PYG',4112.568576),(129,'KES',72.368975),(130,'SVC',6.190407),(131,'MKD',39.842910),(132,'GBP',0.476810),(133,'AZN',1.106290),(134,'TOP',1.583536),(135,'MVR',10.851456),(136,'VUV',79.023588),(137,'GNF',5496.807958),(138,'WST',1.799109),(139,'IQD',778.524159),(140,'ERN',10.612186),(141,'BAM',1.265247),(142,'SCR',9.120504),(143,'CAD',0.980305),(144,'CVE',71.375844),(145,'KWD',0.214738),(146,'BIF',1104.099685),(147,'PGK',2.126700),(148,'SOS',443.057983),(149,'TWD',23.270472),(150,'SGD',1.000000),(151,'UZS',1968.775136),(152,'STD',15835.248435),(153,'IRR',21218.712146),(154,'CNY',4.591556),(155,'SLL',2936.331835),(156,'TND',1.432994),(157,'GYD',145.749608),(158,'MTL',0.483682),(159,'NZD',1.033072),(160,'FKP',0.476810),(161,'LVL',0.449250),(162,'USD',0.707550),(163,'KGS',53.673175),(164,'ARS',9.188051),(165,'RON',2.935895),(166,'GTQ',5.393170),(167,'RSD',78.479065),(168,'BHD',0.266581),(169,'JPY',85.187515),(170,'SDG',4.360002),(171,'XAU',0.000659);
/*!40000 ALTER TABLE `adjod_exchangerate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djmoney_rates_ratesource`
--

DROP TABLE IF EXISTS `djmoney_rates_ratesource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djmoney_rates_ratesource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `last_update` datetime NOT NULL,
  `base_currency` varchar(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djmoney_rates_ratesource`
--

LOCK TABLES `djmoney_rates_ratesource` WRITE;
/*!40000 ALTER TABLE `djmoney_rates_ratesource` DISABLE KEYS */;
INSERT INTO `djmoney_rates_ratesource` VALUES (1,'openexchange.org','2015-12-30 07:45:13','USD');
/*!40000 ALTER TABLE `djmoney_rates_ratesource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_dropdown_subcat`
--

DROP TABLE IF EXISTS `advertisement_dropdown_subcat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_dropdown_subcat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dropdown_id` int(11) NOT NULL,
  `subcategory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dropdown_id` (`dropdown_id`,`subcategory_id`),
  KEY `advertisement_dropdown_subcat_e4b139c7` (`dropdown_id`),
  KEY `advertisement_dropdown_subcat_913b3835` (`subcategory_id`),
  CONSTRAINT `dropdown_id_refs_id_cda49e79` FOREIGN KEY (`dropdown_id`) REFERENCES `advertisement_dropdown` (`id`),
  CONSTRAINT `subcategory_id_refs_id_a29aac9b` FOREIGN KEY (`subcategory_id`) REFERENCES `advertisement_subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_dropdown_subcat`
--

LOCK TABLES `advertisement_dropdown_subcat` WRITE;
/*!40000 ALTER TABLE `advertisement_dropdown_subcat` DISABLE KEYS */;
INSERT INTO `advertisement_dropdown_subcat` VALUES (1,1,1),(2,2,8),(3,3,8),(4,4,1),(5,5,1),(6,6,2),(7,7,1),(8,8,1),(9,8,3),(10,9,2),(11,10,2),(12,10,3),(13,11,9);
/*!40000 ALTER TABLE `advertisement_dropdown_subcat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_city`
--

DROP TABLE IF EXISTS `advertisement_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(50) NOT NULL,
  `country_code` varchar(10) NOT NULL,
  `country_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_city`
--

LOCK TABLES `advertisement_city` WRITE;
/*!40000 ALTER TABLE `advertisement_city` DISABLE KEYS */;
INSERT INTO `advertisement_city` VALUES (1,'Singapore','SG','Singapore');
/*!40000 ALTER TABLE `advertisement_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_dropdown`
--

DROP TABLE IF EXISTS `advertisement_dropdown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_dropdown` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_dropdown`
--

LOCK TABLES `advertisement_dropdown` WRITE;
/*!40000 ALTER TABLE `advertisement_dropdown` DISABLE KEYS */;
INSERT INTO `advertisement_dropdown` VALUES (1,'Tata'),(2,'Nokia'),(3,'Micromax'),(4,'Maruti Suzuki'),(5,'Mahindra'),(6,'Kinetic Motors'),(7,'Hyundai'),(8,'Honda'),(9,'Hero Honda'),(10,'Hero'),(11,'HCL');
/*!40000 ALTER TABLE `advertisement_dropdown` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worker_worker`
--

DROP TABLE IF EXISTS `worker_worker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `worker_worker` (
  `id` varchar(128) NOT NULL,
  `name` varchar(128) NOT NULL,
  `cls_path` varchar(512) NOT NULL,
  `interval` bigint(20) NOT NULL,
  `wait_for_approval` bigint(20) NOT NULL,
  `notify_for_approval` varchar(2048) DEFAULT NULL,
  `notify_for_errors` varchar(2048) DEFAULT NULL,
  `options` longtext,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worker_worker`
--

LOCK TABLES `worker_worker` WRITE;
/*!40000 ALTER TABLE `worker_worker` DISABLE KEYS */;
INSERT INTO `worker_worker` VALUES ('email_expiredads','Email_ExpiredAds','worker.workers.EmailNotification_ExpiredAds',5,0,'','','',1),('freealert_notice_email','Freealert Notice Email','worker.workers.EmailNotificationWorker',10,0,'','','',1);
/*!40000 ALTER TABLE `worker_worker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_premiumpriceinfo`
--

DROP TABLE IF EXISTS `advertisement_premiumpriceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_premiumpriceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `premium_price` double DEFAULT NULL,
  `base_currency` varchar(6) NOT NULL,
  `purpose` varchar(30) NOT NULL,
  `duration` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_premiumpriceinfo`
--

LOCK TABLES `advertisement_premiumpriceinfo` WRITE;
/*!40000 ALTER TABLE `advertisement_premiumpriceinfo` DISABLE KEYS */;
INSERT INTO `advertisement_premiumpriceinfo` VALUES (1,5.55,'SGD','account_subscription',30),(2,9.99,'SGD','product_subscription',30),(3,14.99,'SGD','product_subscription',30),(4,19.99,'SGD','product_subscription',30);
/*!40000 ALTER TABLE `advertisement_premiumpriceinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `advertisement_subcategory`
--

DROP TABLE IF EXISTS `advertisement_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `advertisement_subcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `advertisement_subcategory_42dc49bc` (`category_id`),
  CONSTRAINT `category_id_refs_id_538dded2` FOREIGN KEY (`category_id`) REFERENCES `advertisement_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `advertisement_subcategory`
--

LOCK TABLES `advertisement_subcategory` WRITE;
/*!40000 ALTER TABLE `advertisement_subcategory` DISABLE KEYS */;
INSERT INTO `advertisement_subcategory` VALUES (1,1,'Cars'),(2,1,'Motorcycles'),(3,1,'Scooters'),(4,1,'Spare Parts - Accessories'),(5,1,'Bicycles'),(6,1,'Buses - Trucks - Commercial Vehicles'),(7,1,'Construction Vehicles'),(8,2,'Mobile Phones'),(9,2,'Mobiles & Tablets'),(10,2,'Accessories'),(11,3,' Home - Kitchen Appliances'),(12,3,' Laptops - Computers'),(13,3,' Computer Peripherals'),(14,3,'  TV - DVD - Multimedia'),(15,3,'Tools - Machinery - Industrial'),(16,3,'   Video Games - Consoles'),(17,3,' Cameras - Digicams'),(18,3,'  Music Systems - Home Theatre'),(19,3,' Inverters, UPS & Generators'),(20,3,'  Security Equipment - Products'),(21,3,'  Fax, EPABX, Office Equipment'),(22,3,' Camera Accessories'),(23,4,'Houses - Apartments for Rent'),(24,4,'Houses - Apartments for Sale'),(25,4,'Land - Plot For Sale'),(26,4,'Commercial Property for Rent'),(27,4,'Paying Guest - Hostel'),(28,4,'Villas/Bungalows for Sale'),(29,4,'Commercial Property for Sale'),(30,4,'Villas/Bungalows for Rent'),(31,4,'Flatmates'),(32,4,'Vacation Rentals - Timeshare'),(33,4,'Service Apartments'),(34,6,'Home - Office Furniture'),(35,6,'Clothing - Garments'),(36,6,'Health - Beauty Products'),(37,6,'Sport - Fitness Equipment'),(38,6,'Home Decor - Furnishings'),(39,6,'Household'),(40,6,'Fashion Accessories'),(41,6,'Watches'),(42,6,'Coins - Stamps     '),(43,6,'Musical Instruments'),(44,6,'Wholesale - Bulk'),(45,6,'Baby - Infant Products'),(46,5,'Full Time Jobs'),(47,5,'Work From Home'),(48,5,'Part Time Jobs'),(49,5,'Placement - Recruitment Agencies'),(50,5,'Freelancers'),(51,5,'Non-Profit NGOs'),(52,5,'Summer Trainees - Interns'),(53,5,'Other Jobs'),(54,7,'Advertising - Design'),(55,7,'Airline - Train - Bus Tickets'),(56,7,'Architect'),(57,7,'Astrology - Numerology'),(58,7,'Baby Sitters - Nanny'),(59,7,'Business Offers'),(60,7,'Carpenters - Furniture Work'),(61,7,'Catering -Tiffin Services'),(62,7,'Computer Repair and Service'),(63,7,'Cooks'),(64,7,'Courier Services'),(65,7,'Doctors'),(66,10,'Acting - Modeling Roles'),(67,10,'Modeling Agencies'),(68,10,'Photographers - Cameraman'),(69,10,'Musicians'),(70,10,'Acting Schools'),(71,10,'Script Writers'),(72,10,'Actor - Model Portfolios'),(73,10,'Make Up - Hair'),(74,10,'Art Directors - Editors'),(75,10,'Studios - Locations for hire'),(76,10,'Fashion Designers - Stylists'),(77,10,'Sound Engineers');
/*!40000 ALTER TABLE `advertisement_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djmoney_rates_rate`
--

DROP TABLE IF EXISTS `djmoney_rates_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djmoney_rates_rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `currency` varchar(3) NOT NULL,
  `value` decimal(20,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source_id` (`source_id`,`currency`),
  KEY `djmoney_rates_rate_89f89e85` (`source_id`),
  CONSTRAINT `source_id_refs_id_ca2dc046` FOREIGN KEY (`source_id`) REFERENCES `djmoney_rates_ratesource` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=172 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djmoney_rates_rate`
--

LOCK TABLES `djmoney_rates_rate` WRITE;
/*!40000 ALTER TABLE `djmoney_rates_rate` DISABLE KEYS */;
INSERT INTO `djmoney_rates_rate` VALUES (1,1,'DZD',107.080600),(2,1,'NAD',15.326700),(3,1,'GHS',3.829273),(4,1,'EGP',7.829385),(5,1,'BGN',1.788880),(6,1,'PAB',1.000000),(7,1,'BOB',6.921498),(8,1,'DKK',6.823556),(9,1,'BWP',11.171113),(10,1,'LBP',1510.659984),(11,1,'TZS',2159.474984),(12,1,'VND',22442.016667),(13,1,'AOA',135.289998),(14,1,'KHR',4058.824951),(15,1,'MYR',4.293606),(16,1,'KYD',0.823992),(17,1,'LYD',1.392781),(18,1,'UAH',23.937200),(19,1,'JOD',0.708746),(20,1,'AWG',1.793333),(21,1,'SAR',3.751163),(22,1,'LTL',3.101463),(23,1,'HKD',7.750390),(24,1,'CHF',0.991549),(25,1,'GIP',0.673889),(26,1,'BYR',18585.525000),(27,1,'ALL',125.400100),(28,1,'XPD',0.001800),(29,1,'MRO',307.120500),(30,1,'HRK',6.984069),(31,1,'DJF',177.660874),(32,1,'SZL',15.325800),(33,1,'THB',36.070150),(34,1,'XAF',600.940242),(35,1,'BND',1.413691),(36,1,'ISK',129.000900),(37,1,'UYU',29.852190),(38,1,'NIO',27.893790),(39,1,'LAK',8169.397549),(40,1,'SYP',220.281334),(41,1,'MAD',9.881946),(42,1,'MZN',47.870000),(43,1,'PHP',46.981550),(44,1,'ZAR',15.336080),(45,1,'NPR',106.233001),(46,1,'ZWL',322.322775),(47,1,'NGN',199.047001),(48,1,'CRC',538.236103),(49,1,'AED',3.673052),(50,1,'EEK',14.295525),(51,1,'MWK',656.189281),(52,1,'LKR',144.347600),(53,1,'PKR',104.931600),(54,1,'HUF',286.570600),(55,1,'BMD',1.000000),(56,1,'LSL',15.321250),(57,1,'MNT',1993.833333),(58,1,'AMD',482.505000),(59,1,'UGX',3384.058333),(60,1,'QAR',3.641311),(61,1,'XDR',0.720308),(62,1,'JMD',120.088600),(63,1,'GEL',2.397950),(64,1,'SHP',0.673889),(65,1,'AFN',68.430000),(66,1,'SBD',8.129806),(67,1,'KPW',900.090000),(68,1,'TRY',2.909987),(69,1,'BDT',78.514710),(70,1,'YER',214.988700),(71,1,'HTG',56.828200),(72,1,'XOF',602.057562),(73,1,'MGA',3209.881683),(74,1,'ANG',1.788775),(75,1,'LRD',85.580002),(76,1,'RWF',747.858371),(77,1,'NOK',8.713904),(78,1,'MOP',7.989942),(79,1,'INR',66.356190),(80,1,'MXN',17.252600),(81,1,'CZK',24.714830),(82,1,'TJS',6.975400),(83,1,'BTC',0.002322),(84,1,'BTN',66.370316),(85,1,'COP',3175.401683),(86,1,'TMT',3.501533),(87,1,'MUR',35.874625),(88,1,'IDR',13764.900000),(89,1,'HNL',22.256850),(90,1,'XPF',109.115412),(91,1,'FJD',2.114950),(92,1,'ETB',21.208670),(93,1,'PEN',3.403819),(94,1,'BZD',1.997155),(95,1,'ILS',3.898571),(96,1,'DOP',45.601380),(97,1,'GGP',0.673889),(98,1,'MDL',19.679160),(99,1,'XPT',0.001123),(100,1,'BSD',1.000000),(101,1,'SEK',8.371019),(102,1,'ZMK',5253.075255),(103,1,'JEP',0.673889),(104,1,'AUD',1.372203),(105,1,'SRD',3.992500),(106,1,'CUP',1.000963),(107,1,'CLF',0.024602),(108,1,'BBD',2.000000),(109,1,'KMF',450.662579),(110,1,'KRW',1171.606673),(111,1,'GMD',39.390380),(112,1,'VEF',6.320497),(113,1,'IMP',0.673889),(114,1,'CUC',1.000000),(115,1,'CLP',708.563706),(116,1,'ZMW',10.974450),(117,1,'EUR',0.914864),(118,1,'CDF',925.521500),(119,1,'XCD',2.701020),(120,1,'KZT',339.445390),(121,1,'RUB',72.364049),(122,1,'XAG',0.071737),(123,1,'TTD',6.430087),(124,1,'OMR',0.384993),(125,1,'BRL',3.864506),(126,1,'MMK',1313.154976),(127,1,'PLN',3.872723),(128,1,'PYG',5812.408320),(129,1,'KES',102.281099),(130,1,'SVC',8.749076),(131,1,'MKD',56.311100),(132,1,'GBP',0.673889),(133,1,'AZN',1.563550),(134,1,'TOP',2.238056),(135,1,'MVR',15.336667),(136,1,'VUV',111.686249),(137,1,'GNF',7768.792598),(138,1,'WST',2.542731),(139,1,'IQD',1100.309992),(140,1,'ERN',14.998500),(141,1,'BAM',1.788209),(142,1,'SCR',12.890263),(143,1,'CAD',1.385492),(144,1,'CVE',100.877479),(145,1,'KWD',0.303495),(146,1,'BIF',1560.455000),(147,1,'PGK',3.005725),(148,1,'SOS',626.186253),(149,1,'TWD',32.888810),(150,1,'SGD',1.413328),(151,1,'UZS',2782.525025),(152,1,'STD',22380.400000),(153,1,'IRR',29989.000000),(154,1,'CNY',6.489375),(155,1,'SLL',4150.000000),(156,1,'TND',2.025290),(157,1,'GYD',205.992002),(158,1,'MTL',0.683602),(159,1,'NZD',1.460069),(160,1,'FKP',0.673889),(161,1,'LVL',0.634937),(162,1,'USD',1.000000),(163,1,'KGS',75.857801),(164,1,'ARS',12.985730),(165,1,'RON',4.149383),(166,1,'GTQ',7.622318),(167,1,'RSD',110.916660),(168,1,'BHD',0.376766),(169,1,'JPY',120.397900),(170,1,'SDG',6.162113),(171,1,'XAU',0.000932);
/*!40000 ALTER TABLE `djmoney_rates_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worker_workertask`
--

DROP TABLE IF EXISTS `worker_workertask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `worker_workertask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_id` varchar(128) NOT NULL,
  `notes` longtext,
  `worker_options` longtext,
  `status` varchar(64) NOT NULL,
  `scheduled` datetime DEFAULT NULL,
  `started` datetime DEFAULT NULL,
  `completed` datetime DEFAULT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `worker_workertask_20fc5b84` (`worker_id`),
  CONSTRAINT `worker_id_refs_id_6c71c3dc` FOREIGN KEY (`worker_id`) REFERENCES `worker_worker` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worker_workertask`
--

LOCK TABLES `worker_workertask` WRITE;
/*!40000 ALTER TABLE `worker_workertask` DISABLE KEYS */;
INSERT INTO `worker_workertask` VALUES (1,'freealert_notice_email','','','completed','2015-05-27 07:36:32','2015-05-27 07:36:32','2015-05-27 07:36:54','2015-05-27 07:36:54');
/*!40000 ALTER TABLE `worker_workertask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adjod_basecurrency`
--

DROP TABLE IF EXISTS `adjod_basecurrency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adjod_basecurrency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `base_currency` varchar(3) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjod_basecurrency`
--

LOCK TABLES `adjod_basecurrency` WRITE;
/*!40000 ALTER TABLE `adjod_basecurrency` DISABLE KEYS */;
INSERT INTO `adjod_basecurrency` VALUES (1,'SGD','2015-12-15 08:12:26');
/*!40000 ALTER TABLE `adjod_basecurrency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banner_bannerplan`
--

DROP TABLE IF EXISTS `banner_bannerplan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banner_bannerplan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page` varchar(50) NOT NULL,
  `position` varchar(50) NOT NULL,
  `price` double DEFAULT NULL,
  `plan_duration` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `page` (`page`,`position`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banner_bannerplan`
--

LOCK TABLES `banner_bannerplan` WRITE;
/*!40000 ALTER TABLE `banner_bannerplan` DISABLE KEYS */;
INSERT INTO `banner_bannerplan` VALUES (1,'Home page','Bottom',2,30),(2,'Listing page','Bottom',3,30);
/*!40000 ALTER TABLE `banner_bannerplan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-04 15:36:46
