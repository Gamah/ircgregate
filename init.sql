-- the needed tables and views
CREATE TABLE `coolwords` (
  `word` varchar(50) DEFAULT NULL,
  KEY `cwword` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE TABLE `swagdata` (
  `id` int(11) NOT NULL,
  `user` varchar(45) NOT NULL,
  `word` varchar(45) NOT NULL,
  `timestamp` datetime NOT NULL,
  `intword` int(11) DEFAULT NULL,
  `intuser` varchar(45) DEFAULT NULL,
  KEY `sduser` (`user`),
  KEY `sdword` (`word`),
  KEY `sdtimestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `usermentions` AS select `swagdata`.`word` AS `user`,count(`swagdata`.`word`) AS `count` from `swagdata` where (`swagdata`.`word` in (select distinct `swagdata`.`user` from `swagdata`) and (`swagdata`.`timestamp` >= (now() - interval 1 day))) group by `swagdata`.`word` order by count(`swagdata`.`word`) desc,'user' limit 50;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `userwordcount` AS select `swagdata`.`user` AS `user`,count(`swagdata`.`word`) AS `count` from `swagdata` where (`swagdata`.`timestamp` >= (now() - interval 1 day)) group by `swagdata`.`user` order by count(`swagdata`.`word`) desc,`swagdata`.`user` limit 50;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `worduse` AS select `swagdata`.`word` AS `word`,count(`swagdata`.`word`) AS `count` from `swagdata` where ((`swagdata`.`timestamp` >= (now() - interval 1 day)) and (not(`swagdata`.`word` in (select distinct `swagdata`.`user` from `swagdata`))) and `swagdata`.`word` in (select distinct `coolwords`.`word` from `coolwords`)) group by `swagdata`.`word` order by count(`swagdata`.`word`) desc,'word' limit 50;
