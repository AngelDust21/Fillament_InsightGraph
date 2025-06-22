-- 3D Print Calculator Database Schema
-- SQLite Database voor uitgebreide calculator - Geoptimaliseerd voor grote hoeveelheden data

-- Materialen tabel
CREATE TABLE materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL, -- PLA, PETG, ABS, etc.
    price_per_kg DECIMAL(10,2) NOT NULL,
    density DECIMAL(5,3) NOT NULL, -- g/cm³
    print_temp_min INTEGER NOT NULL,
    print_temp_max INTEGER NOT NULL,
    bed_temp_min INTEGER,
    bed_temp_max INTEGER,
    diameter DECIMAL(3,1) DEFAULT 1.75, -- mm
    color VARCHAR(50),
    description TEXT,
    failure_rate DECIMAL(5,2) DEFAULT 5.0, -- percentage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Printers tabel
CREATE TABLE printers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    build_volume_x INTEGER NOT NULL, -- mm
    build_volume_y INTEGER NOT NULL, -- mm
    build_volume_z INTEGER NOT NULL, -- mm
    power_watts INTEGER NOT NULL,
    features TEXT, -- JSON: ["AMS", "LiDAR", "Enclosed"]
    maintenance_yearly DECIMAL(10,2) DEFAULT 50.0,
    depreciation_years INTEGER DEFAULT 3,
    prints_per_year INTEGER DEFAULT 500,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nozzles tabel
CREATE TABLE nozzles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    diameter DECIMAL(3,1) NOT NULL, -- mm
    material VARCHAR(50) NOT NULL, -- brass, hardened steel, ruby, etc.
    price DECIMAL(10,2) NOT NULL,
    lifespan_hours INTEGER DEFAULT 1000,
    wear_rate DECIMAL(5,3) DEFAULT 0.001, -- per print hour
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Berekeningen tabel - Geoptimaliseerd voor grote hoeveelheden data
CREATE TABLE calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    material_id INTEGER NOT NULL,
    printer_id INTEGER NOT NULL,
    nozzle_id INTEGER NOT NULL,
    weight_grams DECIMAL(8,2) NOT NULL,
    print_hours DECIMAL(6,2) NOT NULL,
    support_percent DECIMAL(5,2) DEFAULT 15.0,
    failure_rate DECIMAL(5,2) DEFAULT 10.0,
    electricity_cost DECIMAL(5,3) DEFAULT 0.40,
    design_hours DECIMAL(5,2) DEFAULT 0.5,
    hourly_rate DECIMAL(8,2) DEFAULT 25.0,
    markup_percent DECIMAL(5,2) DEFAULT 50.0,
    post_processing_cost DECIMAL(8,2) DEFAULT 0.0,
    shipping_cost DECIMAL(8,2) DEFAULT 0.0,
    overhead_percent DECIMAL(5,2) DEFAULT 20.0,
    tax_percent DECIMAL(5,2) DEFAULT 21.0,
    total_cost DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    profit DECIMAL(10,2) NOT NULL,
    roi_percent DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES materials(id),
    FOREIGN KEY (printer_id) REFERENCES printers(id),
    FOREIGN KEY (nozzle_id) REFERENCES nozzles(id)
);

-- Gebruikers tabel (optioneel voor toekomst)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- === GEAVANCEERDE INDEXEN VOOR PERFORMANCE ===

-- Basis indexen voor snelle lookups
CREATE INDEX idx_materials_type ON materials(type);
CREATE INDEX idx_materials_brand ON materials(brand);
CREATE INDEX idx_materials_price ON materials(price_per_kg);
CREATE INDEX idx_printers_brand ON printers(brand);
CREATE INDEX idx_printers_price ON printers(price);
CREATE INDEX idx_nozzles_diameter ON nozzles(diameter);
CREATE INDEX idx_nozzles_material ON nozzles(material);

-- === KRITIEKE INDEXEN VOOR CALCULATIONS TABEL ===
-- Deze zijn essentieel voor snelle queries bij grote hoeveelheden data

-- Tijdsindexen voor data analyse
CREATE INDEX idx_calculations_created_at ON calculations(created_at);
CREATE INDEX idx_calculations_created_date ON calculations(DATE(created_at));

-- Foreign key indexen voor joins
CREATE INDEX idx_calculations_material_id ON calculations(material_id);
CREATE INDEX idx_calculations_printer_id ON calculations(printer_id);
CREATE INDEX idx_calculations_nozzle_id ON calculations(nozzle_id);

-- Composite indexen voor veel gebruikte queries
CREATE INDEX idx_calculations_material_date ON calculations(material_id, created_at);
CREATE INDEX idx_calculations_printer_date ON calculations(printer_id, created_at);
CREATE INDEX idx_calculations_cost_range ON calculations(total_cost, created_at);
CREATE INDEX idx_calculations_weight_range ON calculations(weight_grams, created_at);
CREATE INDEX idx_calculations_time_range ON calculations(print_hours, created_at);

-- Indexen voor analytics queries
CREATE INDEX idx_calculations_profit_roi ON calculations(profit, roi_percent);
CREATE INDEX idx_calculations_selling_price ON calculations(selling_price);
CREATE INDEX idx_calculations_weight_cost ON calculations(weight_grams, total_cost);

-- === PARTITIONING INDEXEN VOOR ZEER GROTE DATASETS ===
-- Voor databases met miljoenen records

-- Maandelijkse partitioning index
CREATE INDEX idx_calculations_year_month ON calculations(strftime('%Y-%m', created_at));

-- Dagelijkse partitioning index  
CREATE INDEX idx_calculations_year_month_day ON calculations(strftime('%Y-%m-%d', created_at));

-- === TRIGGERS VOOR DATA INTEGRITEIT ===

-- Triggers voor updated_at
CREATE TRIGGER update_materials_timestamp 
    AFTER UPDATE ON materials
    BEGIN
        UPDATE materials SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_printers_timestamp 
    AFTER UPDATE ON printers
    BEGIN
        UPDATE printers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_nozzles_timestamp 
    AFTER UPDATE ON nozzles
    BEGIN
        UPDATE nozzles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER update_calculations_timestamp 
    AFTER UPDATE ON calculations
    BEGIN
        UPDATE calculations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- === VIEWS VOOR VEEL GEBRUIKTE QUERIES ===

-- View voor populaire materialen statistieken
CREATE VIEW v_popular_materials AS
SELECT 
    m.id,
    m.name,
    m.brand,
    m.type,
    COUNT(c.id) as usage_count,
    AVG(c.total_cost) as avg_cost,
    AVG(c.profit) as avg_profit,
    AVG(c.roi_percent) as avg_roi,
    MIN(c.created_at) as first_used,
    MAX(c.created_at) as last_used
FROM materials m
LEFT JOIN calculations c ON m.id = c.material_id
GROUP BY m.id, m.name, m.brand, m.type
ORDER BY usage_count DESC;

-- View voor populaire printers statistieken
CREATE VIEW v_popular_printers AS
SELECT 
    p.id,
    p.name,
    p.brand,
    p.model,
    COUNT(c.id) as usage_count,
    AVG(c.total_cost) as avg_cost,
    AVG(c.profit) as avg_profit,
    AVG(c.roi_percent) as avg_roi,
    MIN(c.created_at) as first_used,
    MAX(c.created_at) as last_used
FROM printers p
LEFT JOIN calculations c ON p.id = c.printer_id
GROUP BY p.id, p.name, p.brand, p.model
ORDER BY usage_count DESC;

-- View voor dagelijkse statistieken
CREATE VIEW v_daily_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as calculations_count,
    AVG(total_cost) as avg_total_cost,
    AVG(selling_price) as avg_selling_price,
    AVG(profit) as avg_profit,
    AVG(roi_percent) as avg_roi,
    AVG(weight_grams) as avg_weight,
    AVG(print_hours) as avg_print_hours,
    SUM(total_cost) as total_costs,
    SUM(selling_price) as total_revenue,
    SUM(profit) as total_profit
FROM calculations
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- === PRAGMA OPTIMALISATIES ===
-- Deze worden uitgevoerd bij database initialisatie

-- WAL mode voor betere concurrency
PRAGMA journal_mode = WAL;

-- Grotere cache voor betere performance
PRAGMA cache_size = -64000; -- 64MB cache

-- Synchronous mode voor betere performance (iets minder veilig maar veel sneller)
PRAGMA synchronous = NORMAL;

-- Temp store in memory voor snellere temp operaties
PRAGMA temp_store = MEMORY;

-- Grotere page size voor betere performance
PRAGMA page_size = 4096; 