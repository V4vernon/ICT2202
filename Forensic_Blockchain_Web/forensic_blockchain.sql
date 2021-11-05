CREATE DATABASE IF NOT EXISTS `forensic_blockchain` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forensic_blockchain`;

CREATE TABLE IF NOT EXISTS `accounts` (
`id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('Member','Admin') NOT NULL DEFAULT 'Member',
  `activation_code` varchar(255) NOT NULL DEFAULT '',
  `rememberme` varchar(255) NOT NULL DEFAULT '',
  `reset` varchar(255)  NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `bitcase` (
`id` int(11) NOT NULL AUTO_INCREMENT,
  `case_name` varchar(255) NOT NULL,
  `case_date` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL DEFAULT '',
  `status` varchar(255) NOT NULL DEFAULT '',
  `account_id` int NOT NULL references accounts(id),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


alter table bitcase 
ADD CONSTRAINT fk_account_id 
FOREIGN KEY(account_id) references accounts(id)
ON DELETE CASCADE
ON UPDATE CASCADE;


INSERT INTO `accounts` (`id`, `username`, `password`, `email`, `role`, `activation_code`, `rememberme`, `reset`) VALUES
(1, 'admin', 'b9fc65789ca65526a77b0009f24e9c01a43e32b3', 'admin@forensic.com', 'Admin', 'activated', '', ''),
(2, 'member', 'f046926a90af0b97acbc451bcbde266878f5f963', 'member@forensic.com', 'Member', 'activated', '', '');
