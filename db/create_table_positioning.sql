CREATE TABLE `position_testing_demo` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DateTime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `NodeID` varchar(45) NOT NULL,
  `IP` varchar(45) NOT NULL,
  `Timestamp` int(11) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Channel` int(11) NOT NULL,
  `Counter` int(11) NOT NULL,
  `TX_power` int(11) NOT NULL DEFAULT '0',
  `RSSI` int(11) NOT NULL,
  `RSSI_filtered` float DEFAULT NULL,
  `True_distance` float DEFAULT NULL,
  `Estimated_distance` float DEFAULT NULL,
  `CRC` int(11) NOT NULL,
  `LPE` int(11) NOT NULL,
  `Sync_controller` int(11) NOT NULL,
  `Label` varchar(1000) DEFAULT NULL,
  `Node_setup` mediumtext,
  `Estimated_tag_position` varchar(45) DEFAULT NULL,
  `True_tag_position` varchar(45) DEFAULT NULL,
  `Node_position` varchar(45) NOT NULL,
  `Settings` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
