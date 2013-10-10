delimiter $$

CREATE TABLE `news_info` (
  `news_id` int(11) NOT NULL AUTO_INCREMENT,
  `news_title` varchar(100) NOT NULL,
  `news_content` varchar(10240) DEFAULT NULL,
  `news_pub_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `product_info` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) NOT NULL,
  `product_intro` varchar(1024) DEFAULT NULL,
  `product_price` float NOT NULL,
  `product_sales` int(11) DEFAULT '0',
  `product_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `product_type` int(11) DEFAULT '0',
  `product_image` varchar(256) DEFAULT '/static/images/product_images/default.jpg',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `member_info` (
  `member_id` int(11) NOT NULL AUTO_INCREMENT,
  `member_username` varchar(20) NOT NULL,
  `member_password` varchar(50) NOT NULL,
  `member_email` varchar(100) NOT NULL,
  `head_image` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`member_id`),
  UNIQUE KEY `member_username_UNIQUE` (`member_username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `forum_posts` (
  `post_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_title` varchar(100) NOT NULL,
  `post_content` varchar(10240) NOT NULL,
  `post_type` varchar(10) NOT NULL,
  `username` varchar(20) NOT NULL,
  `post_pub_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_username` varchar(20) DEFAULT NULL,
  `last_time` datetime DEFAULT NULL,
  `back` int(11) NOT NULL DEFAULT '0',
  `top` int(11) NOT NULL DEFAULT '0',
  `essence` int(11) NOT NULL DEFAULT '0',
  `recommend` int(11) NOT NULL DEFAULT '0',
  `view` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`post_id`),
  KEY `fk_forum_posts_idx` (`username`),
  CONSTRAINT `fk_forum_posts` FOREIGN KEY (`username`) REFERENCES `member_info` (`member_username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `forum_backposts` (
  `backpost_id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `backpost_content` varchar(10240) NOT NULL,
  `username` varchar(20) NOT NULL,
  `backpost_pub_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`backpost_id`),
  KEY `fk_forum_backposts_1_idx` (`post_id`),
  CONSTRAINT `fk_forum_backposts_1` FOREIGN KEY (`post_id`) REFERENCES `forum_posts` (`post_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8$$

delimiter $$

CREATE TABLE `post_types` (
  `post_type` int(11) NOT NULL,
  `post_type_name` varchar(45) NOT NULL,
  PRIMARY KEY (`post_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$

