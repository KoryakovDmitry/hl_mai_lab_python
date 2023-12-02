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


-- CREATE TABLE IF NOT EXISTS services (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(256),
--     description TEXT,
--     cost DECIMAL(10, 2),
--     INDEX(name)
-- );
--
--
-- CREATE TABLE IF NOT EXISTS orders (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT,
--     date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES users(id),
--     INDEX(user_id)
-- );
--
--
-- CREATE TABLE IF NOT EXISTS order_service (
--     order_id INT,
--     service_id INT,
--     PRIMARY KEY (order_id, service_id),
--     FOREIGN KEY (order_id) REFERENCES orders(id),
--     FOREIGN KEY (service_id) REFERENCES services(id)
-- );
--
-- INSERT INTO users (login, first_name, last_name, email) VALUES
-- ('chloe654', 'Chloe', 'Lee', 'chloe@example.com'),
-- ('ethan789', 'Ethan', 'Perez', 'ethan@example.com'),
-- ('hannah543', 'Hannah', 'Anderson', 'hannah@example.com'),
-- ('noah987', 'Noah', 'Thomas', 'noah@example.com'),
-- ('sophia321', 'Sophia', 'Taylor', 'sophia@example.com'),
-- ('aiden654', 'Aiden', 'Harris', 'aiden@example.com'),
-- ('abigail789', 'Abigail', 'Lopez', 'abigail@example.com'),
-- ('joshua432', 'Joshua', 'Clark', 'joshua@example.com'),
-- ('isabella987', 'Isabella', 'Lewis', 'isabella@example.com'),
-- ('william123', 'William', 'Robinson', 'william@example.com');