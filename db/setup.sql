CREATE SCHEMA `sp`;

CREATE TABLE `sp`.`track` (
  `track_id` char(22) PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `album_id` char(22),
  `duration_ms` int,
  `popularity` tinyint,
  `explicit` bool,
  `acousticness` decimal(4,3),
  `danceability` decimal(4,3),
  `energy` decimal(4,3),
  `instrumentalness` decimal(4,3),
  `liveness` decimal(4,3),
  `mode` bool,
  `time_signature` decimal(6,3),
  `valence` decimal(4,3)
);

CREATE TABLE `sp`.`track_artist` (
  `link_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `track_id` char(22) NOT NULL,
  `artist_id` char(22) NOT NULL
);

CREATE TABLE `sp`.`artist` (
  `artist_id` char(22) PRIMARY KEY NOT NULL,
  `name` varchar(255) NOT NULL,
  `popularity` tinyint
);

CREATE TABLE `sp`.`album` (
  `album_id` char(22) PRIMARY KEY NOT NULL,
  `name` varchar(255) NOT NULL,
  `release_year` year
);

CREATE TABLE `sp`.`artist_genre` (
  `link_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `artist_id` char(22) NOT NULL,
  `genre` varchar(255) NOT NULL
);

CREATE TABLE `sp`.`genre` (
  `genre_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `genre` varchar(255) UNIQUE NOT NULL
);

CREATE TABLE `sp`.`track_date` (
  `link_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `track_id` char(22) NOT NULL,
  `date` date NOT NULL
);

CREATE TABLE `sp`.`date` (
  `date_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` date UNIQUE NOT NULL
);

CREATE TABLE `sp`.`date_parameter` (
  `link_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `param_id` int NOT NULL
);

CREATE TABLE `sp`.`parameter` (
  `param_id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `param_value` varchar(255) UNIQUE NOT NULL,
  `param_type` char(3) NOT NULL
);

CREATE INDEX `track_index_0` ON `sp`.`track` (`album_id`);

CREATE INDEX `track_artist_index_1` ON `sp`.`track_artist` (`track_id`);

CREATE INDEX `track_artist_index_2` ON `sp`.`track_artist` (`artist_id`);

CREATE INDEX `artist_genre_index_3` ON `sp`.`artist_genre` (`artist_id`);

CREATE INDEX `artist_genre_index_4` ON `sp`.`artist_genre` (`genre`);

CREATE INDEX `track_date_index_5` ON `sp`.`track_date` (`track_id`);

CREATE INDEX `track_date_index_6` ON `sp`.`track_date` (`date`);

ALTER TABLE `sp`.`track_artist` ADD FOREIGN KEY (`track_id`) REFERENCES `sp`.`track` (`track_id`);

ALTER TABLE `sp`.`track_artist` ADD FOREIGN KEY (`artist_id`) REFERENCES `sp`.`artist` (`artist_id`);

ALTER TABLE `sp`.`track` ADD FOREIGN KEY (`album_id`) REFERENCES `sp`.`album` (`album_id`);

ALTER TABLE `sp`.`artist_genre` ADD FOREIGN KEY (`genre`) REFERENCES `sp`.`genre` (`genre`);

ALTER TABLE `sp`.`artist_genre` ADD FOREIGN KEY (`artist_id`) REFERENCES `sp`.`artist` (`artist_id`);

ALTER TABLE `sp`.`track_date` ADD FOREIGN KEY (`date`) REFERENCES `sp`.`date` (`date`);

ALTER TABLE `sp`.`track_date` ADD FOREIGN KEY (`track_id`) REFERENCES `sp`.`track` (`track_id`);

ALTER TABLE `sp`.`date_parameter` ADD FOREIGN KEY (`date`) REFERENCES `sp`.`date` (`date`);

ALTER TABLE `sp`.`date_parameter` ADD FOREIGN KEY (`param_id`) REFERENCES `sp`.`parameter` (`param_id`);
