CREATE SCHEMA TITANIC;

USE TITANIC;

CREATE TABLE `USER_INPUT_DATA` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pclass` integer NOT NULL,
  `age` integer NOT NULL,
  `sex` varchar(20) NOT NULL,
  `sibsp` integer NOT NULL,
  `parch` integer NOT NULL,
  `survival` boolean,
  `cret_dt` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

