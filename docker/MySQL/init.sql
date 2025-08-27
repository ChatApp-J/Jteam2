DROP DATABASE IF EXISTS j_team;
DROP USER IF EXISTS 'j_team'@'%';


CREATE USER 'j_team'@'%' IDENTIFIED BY 'j_team';  -- データベースを操作するuserを作成
CREATE DATABASE j_team; -- データベースを作成　名前はChatApp

USE j_team; -- ここからはj_teamのデータベースを操作する

GRANT ALL PRIVILEGES ON j_team.* TO 'j_team'@'%';  -- データベスj_teamでの全権限を付与

CREATE TABLE users(
    uid CHAR(36) PRIMARY KEY,
    name VARCHAR(50)  NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nickname VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    salt CHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_by CHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,    
    FOREIGN KEY (created_by) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE TABLE messages(
    id INT AUTO_INCREMENT PRIMARY KEY,
    uid CHAR(36) NOT NULL,
    cid INT NOT NULL,
    message TEXT NOT NULL,
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (cid) REFERENCES channels(id) ON DELETE CASCADE
);

INSERT INTO users(uid, name, email, nickname, password, salt) VALUES('970af84c-dd40-47ff-af23','杉浦翔太','test@gmail.com', '翔太', '37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578','qwedsrtguh');
INSERT INTO channels(id, name, created_by, description) VALUES(1, '子供を泣き止ます裏技','970af84c-dd40-47ff-af23', '子供が泣き止む裏技を披露する部屋');
INSERT INTO messages(id, uid, cid, message) VALUES(1, '970af84c-dd40-47ff-af23', '1', '泣き止まないよ〜誰か助けて、、😭')