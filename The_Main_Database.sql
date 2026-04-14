PRAGMA foreign_keys = ON;

-- DROP TABLES (if rerunning)---
DROP TABLE IF EXISTS Order_Items;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Instructions;
DROP TABLE IF EXISTS Product_Targets;
DROP TABLE IF EXISTS Chat_Logs;
DROP TABLE IF EXISTS Targets;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Farmers;

-- FARMERS---
CREATE TABLE Farmers (
    farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    location TEXT,
    budget REAL
);

-- PRODUCTS --
CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_name TEXT NOT NULL,
    category TEXT,
    price REAL,
    description TEXT
);

-- TARGETS (Pests/Diseases)--
CREATE TABLE Targets (
    target_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- PRODUCT_TARGETS --
CREATE TABLE Product_Targets (
    product_id INTEGER,
    target_id INTEGER,
    PRIMARY KEY (product_id, target_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (target_id) REFERENCES Targets(target_id)
);

-- INSTRUCTIONS
CREATE TABLE Instructions (
    instruction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    instruction TEXT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- ORDERS
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES Farmers(farmer_id)
);

-- ORDER ITEMS
CREATE TABLE Order_Items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- CHAT LOGS
CREATE TABLE Chat_Logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    query TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES Farmers(farmer_id)
);

-- ==========================================
-- INSERT SAMPLE DATA
-- ==========================================

-- Farmers
INSERT INTO Farmers (name, phone, email, location, budget)
VALUES ('John Mokoena', '0712345678', 'john@email.com', 'Limpopo', 5000);

-- Products (Extracted from Seed2Harvest PDF)
INSERT INTO Products (p_name, category, price, description) VALUES
('BioBoost 250ml', 'Organic Fertilizer', 65.00, 'Improves soil fertility'),
('BioBoost 1L', 'Organic Fertilizer', 200.00, 'Improves soil fertility'),
('BioBoost 5L', 'Organic Fertilizer', 600.00, 'Improves soil fertility'),
('iBatech 500ml', 'Bio-Stimulant', 150.00, 'Growth Enhancer'),
('iBatech 5L', 'Bio-Stimulant', 1500.00, 'Growth Enhancer'),
('Wood Vinegar 1L', 'Organic Fertilizer', 200.00, 'Soil Enhancer'),
('Bio-Tricho 1L', 'Biological Fungicide', 476.00, 'Trichoderma spp.'),
('Bio-Tode 1L', 'Biological Nematicide', 650.00, 'Paecilomyces lilacinus'),
('Bio-Insek 1L', 'Biological Insecticide', 550.00, 'Beauveria bassiana'),
('Bio-neem 1L', 'Organic Insecticide', 430.00, 'Pest & disease control'),
('Exterminator 1L', 'Organic Insecticide', 795.00, 'Pesticide'),
('501 Microbial Solution 1L', 'Microbial', 510.00, 'Microbial bio-stimulant'),
('401 Microbial Solution 1L', 'Microbial', 510.00, 'Microbial bio-stimulant'),
('Carbon + 5kg', 'Soil Conditioner', 450.00, 'Carbon Sequestration'),
('Terra Charge 2kg', 'Soil Conditioner', 120.00, 'Soil preparation'),
('Hydrocache 5kg', 'Water Retention', 1500.00, 'Water-retaining product'),
('Aquaboost 1L', 'Water Retention', 300.00, 'Water-retaining product'),
('Garden Starter Kit', 'Kits', 599.00, 'Organic Garden Starter Kits');

-- Targets
INSERT INTO Targets (name) VALUES
('Aphids'),
('Powdery Mildew'),
('Root Rot');

-- Product Targets (Mapped to new product IDs)
INSERT INTO Product_Targets VALUES (10, 1); -- Bio-neem 1L -> Aphids
INSERT INTO Product_Targets VALUES (7, 3);  -- Bio-Tricho 1L -> Root Rot

-- Instructions (Mapped to new product IDs)
INSERT INTO Instructions (product_id, instruction) VALUES
(2, 'Dilute 1.5L–2L per hectare'), -- BioBoost 1L
(10, 'Dilute 5ml per 1L water'),   -- Bio-neem 1L
(7, 'Apply as soil drench');       -- Bio-Tricho 1L

-- Orders
INSERT INTO Orders (farmer_id) VALUES (1);

-- Order Items
INSERT INTO Order_Items (order_id, product_id, quantity) VALUES
(1, 2, 2),  -- 2x BioBoost 1L
(1, 10, 1); -- 1x Bio-neem 1L

-- Chat Logs
INSERT INTO Chat_Logs (farmer_id, query)
VALUES (1, 'What can I use for aphids?');