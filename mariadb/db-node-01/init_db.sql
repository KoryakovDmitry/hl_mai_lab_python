DROP DATABASE archdb;
CREATE DATABASE archdb;
USE archdb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(256) UNIQUE,
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    email VARCHAR(256),
    INDEX(login)
);


CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(256),
    description TEXT,
    cost DECIMAL(10, 2),
    INDEX(name)
);


CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX(user_id)
);


CREATE TABLE IF NOT EXISTS order_service (
    order_id INT,
    service_id INT,
    PRIMARY KEY (order_id, service_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
--
-- INSERT INTO users (login, first_name, last_name, email) VALUES
-- ('john123', 'John', 'Doe', 'john@example.com'),
-- ('jane567', 'Jane', 'Lopes', 'jane@example.com'),
-- ('mike789', 'Mike', 'Johnson', 'mike@example.com'),
-- ('alex123', 'Alex', 'Taylor', 'alex@example.com'),
-- ('lisa789', 'Lisa', 'Moore', 'lisa@example.com'),
-- ('jacob456', 'Jacob', 'Jackson', 'jacob@example.com'),
-- ('grace234', 'Grace', 'Davis', 'grace@example.com'),
-- ('max891', 'Max', 'Martinez', 'max@example.com'),
-- ('olivia765', 'Olivia', 'Garcia', 'olivia@example.com'),
-- ('samuel321', 'Samuel', 'Rodriguez', 'samuel@example.com');