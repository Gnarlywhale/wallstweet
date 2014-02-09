CREATE TABLE `sentiment_dataset` (
  `tag` varchar(32) NOT NULL,
  `text` varchar(10240) NOT NULL,
  `rating` enum('positive','negative') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `stock_dataset` (
  `id` char(5) NOT NULL,
  `time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `price` double NOT NULL,
  PRIMARY KEY (`id`,`time`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `tweet_dataset` (
  `id` bigint(20) NOT NULL,
  `text` varchar(255) NOT NULL,
  `time` timestamp NOT NULL,
  `polarity` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;