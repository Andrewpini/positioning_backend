CREATE TABLE `rssi_data` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `DateTime` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `NodeID` varchar(45) NOT NULL,
  `IP` varchar(45) NOT NULL,
  `Timestamp` int(11) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Channel` int(11) NOT NULL,
  `Counter` int(11) NOT NULL,
  `RSSI` int(11) NOT NULL,
  `RSSI_filtered` float DEFAULT NULL,
  `True_distance` float DEFAULT NULL,
  `Estimated_distance` float DEFAULT NULL,
  `CRC` int(11) NOT NULL,
  `LPE` int(11) NOT NULL,
  `SyncController` int(11) NOT NULL,
  `Label` varchar(1000) DEFAULT NULL,
  `TX_power` int(11) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=176912 DEFAULT CHARSET=utf8;
