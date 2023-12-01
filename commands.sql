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

-- Inserting users as per the logs
INSERT INTO users (login, first_name, last_name, email) VALUES
('john123', 'John', 'Doe', 'john@example.com'),
('jane567', 'Jane', 'Lopes', 'jane@example.com'),
('mike789', 'Mike', 'Johnson', 'mike@example.com'),
('alex123', 'Alex', 'Taylor', 'alex@example.com'),
('lisa789', 'Lisa', 'Moore', 'lisa@example.com'),
('jacob456', 'Jacob', 'Jackson', 'jacob@example.com'),
('grace234', 'Grace', 'Davis', 'grace@example.com'),
('max891', 'Max', 'Martinez', 'max@example.com'),
('olivia765', 'Olivia', 'Garcia', 'olivia@example.com'),
('samuel321', 'Samuel', 'Rodriguez', 'samuel@example.com'),
('chloe654', 'Chloe', 'Lee', 'chloe@example.com'),
('ethan789', 'Ethan', 'Perez', 'ethan@example.com'),
('hannah543', 'Hannah', 'Anderson', 'hannah@example.com'),
('noah987', 'Noah', 'Thomas', 'noah@example.com'),
('sophia321', 'Sophia', 'Taylor', 'sophia@example.com'),
('aiden654', 'Aiden', 'Harris', 'aiden@example.com'),
('abigail789', 'Abigail', 'Lopez', 'abigail@example.com'),
('joshua432', 'Joshua', 'Clark', 'joshua@example.com'),
('isabella987', 'Isabella', 'Lewis', 'isabella@example.com'),
('william123', 'William', 'Robinson', 'william@example.com');


-- Inserting services as per the logs
INSERT INTO services (name, description, cost) VALUES
('Web Development', 'Professional website development services', 250.00),
('Graphic Design', 'Creative graphic design services', 150.00),
('Digital Marketing', 'Effective online marketing strategies', 300.00);

-- Inserting orders and associated services as per the logs
INSERT INTO orders (user_id) VALUES (1), (2), (3);

INSERT INTO order_service (order_id, service_id) VALUES
(1, 1), (2, 2), (2, 3), (3, 1), (3, 3);

-- Example of selecting a specific user
SELECT * FROM users WHERE login = 'john123';

-- Example of searching users based on certain criteria
SELECT * FROM users WHERE first_name LIKE 'J%' AND last_name LIKE '%o%';

-- Selecting all services
SELECT * FROM services;

-- Example of getting a specific order and its services
SELECT o.id, o.user_id, o.date_created, s.id AS service_id, s.name, s.description, s.cost
FROM orders o
JOIN order_service os ON o.id = os.order_id
JOIN services s ON os.service_id = s.id
WHERE o.id = 1;

-- Example of adding services to an existing order
INSERT INTO order_service (order_id, service_id) VALUES
(1, 2), (1, 3);


SELECT * FROM users;
SELECT * FROM orders;
SELECT * FROM services;
SELECT * FROM order_service;

DROP DATABASE archdb;
CREATE DATABASE archdb;