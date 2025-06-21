<?php
/**
 * Database Class voor 3D Print Calculator
 * Beheert SQLite database connectie en queries
 */

class Database {
    private $db;
    private static $instance = null;
    
    private function __construct() {
        $dbPath = __DIR__ . '/../database/calculator.db';
        $schemaPath = __DIR__ . '/../database/schema.sql';
        
        // Maak database directory als het niet bestaat
        $dbDir = dirname($dbPath);
        if (!is_dir($dbDir)) {
            mkdir($dbDir, 0755, true);
        }
        
        try {
            $this->db = new PDO('sqlite:' . $dbPath);
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
            
            // === PERFORMANCE OPTIMALISATIES VOOR GROTE DATASETS ===
            $this->optimizeDatabase();
            
            // Maak database aan als het niet bestaat
            if (!file_exists($dbPath) || filesize($dbPath) == 0) {
                $this->createDatabase($schemaPath);
                $this->insertSampleData();
            }
            
        } catch (PDOException $e) {
            die("Database connectie mislukt: " . $e->getMessage());
        }
    }
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    private function createDatabase($schemaPath) {
        try {
            $sql = file_get_contents($schemaPath);
            $this->db->exec($sql);
        } catch (PDOException $e) {
            die("Database schema aanmaken mislukt: " . $e->getMessage());
        }
    }
    
    private function insertSampleData() {
        // Sample materialen
        $materials = [
            ['PLA Standard', 'Bambu Lab', 'PLA', 18.50, 1.24, 190, 220, 50, 60, 1.75, 'White', 'Meest gebruikte filament, perfect voor beginners', 5.0],
            ['PLA+ Premium', 'Bambu Lab', 'PLA+', 24.00, 1.24, 200, 230, 50, 65, 1.75, 'Black', 'Sterker dan standaard PLA, betere layer adhesion', 3.0],
            ['PETG', 'Prusa', 'PETG', 26.00, 1.27, 230, 250, 70, 85, 1.75, 'Clear', 'Waterbestendig, sterk, perfect voor functionele prints', 8.0],
            ['ABS', 'Polymaker', 'ABS', 22.00, 1.04, 220, 250, 90, 110, 1.75, 'Gray', 'Hoge temperatuur bestendig, goedkoop', 12.0],
            ['TPU Flex', 'Bambu Lab', 'TPU', 35.00, 1.21, 220, 240, 50, 60, 1.75, 'Black', 'Flexibel materiaal voor grijpers, schoenen, etc.', 15.0],
            ['Polycarbonate', 'Polymaker', 'PC', 45.00, 1.20, 250, 280, 100, 120, 1.75, 'Clear', 'Ultra sterk, hitte bestendig, transparant', 20.0],
            ['ASA', 'Bambu Lab', 'ASA', 32.00, 1.07, 230, 250, 90, 110, 1.75, 'White', 'UV bestendig ABS, perfect voor buiten', 10.0]
        ];
        
        $stmt = $this->db->prepare("
            INSERT INTO materials (name, brand, type, price_per_kg, density, print_temp_min, print_temp_max, bed_temp_min, bed_temp_max, diameter, color, description, failure_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($materials as $material) {
            $stmt->execute($material);
        }
        
        // Sample printers
        $printers = [
            ['Bambu Lab X1-Carbon', 'Bambu Lab', 'X1-Carbon', 1499.00, 256, 256, 256, 350, '["AMS", "LiDAR", "High Speed", "Multi-color"]', 100.0, 3, 500, 'Premium printer met automatische calibratie'],
            ['Bambu Lab P1S', 'Bambu Lab', 'P1S', 699.00, 256, 256, 256, 300, '["AMS Compatible", "High Speed", "Enclosed"]', 80.0, 3, 500, 'Betaalbare high-speed printer'],
            ['Prusa i3 MK4', 'Prusa', 'i3 MK4', 999.00, 250, 210, 250, 250, '["Reliable", "Open Source", "MMU3 Compatible"]', 60.0, 3, 500, 'Betrouwbare workhorse printer'],
            ['Creality Ender 3 V3 SE', 'Creality', 'Ender 3 V3 SE', 199.00, 220, 220, 250, 200, '["Budget", "Auto Leveling", "Direct Drive"]', 30.0, 3, 500, 'Goedkope entry-level printer']
        ];
        
        $stmt = $this->db->prepare("
            INSERT INTO printers (name, brand, model, price, build_volume_x, build_volume_y, build_volume_z, power_watts, features, maintenance_yearly, depreciation_years, prints_per_year, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($printers as $printer) {
            $stmt->execute($printer);
        }
        
        // Sample nozzles
        $nozzles = [
            ['Brass 0.4mm', 0.4, 'brass', 5.00, 1000, 0.001, 'Standaard messing nozzle voor de meeste materialen'],
            ['Hardened Steel 0.4mm', 0.4, 'hardened_steel', 15.00, 2000, 0.0005, 'Gehard staal voor abrasive materialen'],
            ['Ruby 0.4mm', 0.4, 'ruby', 50.00, 5000, 0.0001, 'Ruby tip voor extreme duurzaamheid'],
            ['Brass 0.6mm', 0.6, 'brass', 6.00, 1000, 0.001, 'Grotere nozzle voor snellere prints'],
            ['Brass 0.2mm', 0.2, 'brass', 4.00, 800, 0.002, 'Kleine nozzle voor detail prints']
        ];
        
        $stmt = $this->db->prepare("
            INSERT INTO nozzles (name, diameter, material, price, lifespan_hours, wear_rate, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($nozzles as $nozzle) {
            $stmt->execute($nozzle);
        }
    }
    
    public function getConnection() {
        return $this->db;
    }
    
    public function query($sql, $params = []) {
        try {
            $stmt = $this->db->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch (PDOException $e) {
            throw new Exception("Query mislukt: " . $e->getMessage());
        }
    }
    
    public function fetchAll($sql, $params = []) {
        return $this->query($sql, $params)->fetchAll();
    }
    
    public function fetchOne($sql, $params = []) {
        return $this->query($sql, $params)->fetch();
    }
    
    public function insert($table, $data) {
        $columns = implode(', ', array_keys($data));
        $placeholders = ':' . implode(', :', array_keys($data));
        
        $sql = "INSERT INTO $table ($columns) VALUES ($placeholders)";
        
        try {
            $stmt = $this->db->prepare($sql);
            $stmt->execute($data);
            return $this->db->lastInsertId();
        } catch (PDOException $e) {
            throw new Exception("Insert mislukt: " . $e->getMessage());
        }
    }
    
    public function update($table, $data, $where, $whereParams = []) {
        $setClause = [];
        foreach (array_keys($data) as $column) {
            $setClause[] = "$column = :$column";
        }
        $setClause = implode(', ', $setClause);
        
        $sql = "UPDATE $table SET $setClause WHERE $where";
        
        try {
            $stmt = $this->db->prepare($sql);
            $stmt->execute(array_merge($data, $whereParams));
            return $stmt->rowCount();
        } catch (PDOException $e) {
            throw new Exception("Update mislukt: " . $e->getMessage());
        }
    }
    
    public function delete($table, $where, $params = []) {
        $sql = "DELETE FROM $table WHERE $where";
        
        try {
            $stmt = $this->db->prepare($sql);
            $stmt->execute($params);
            return $stmt->rowCount();
        } catch (PDOException $e) {
            throw new Exception("Delete mislukt: " . $e->getMessage());
        }
    }
    
    public function beginTransaction() {
        return $this->db->beginTransaction();
    }
    
    public function commit() {
        return $this->db->commit();
    }
    
    public function rollback() {
        return $this->db->rollback();
    }
    
    /**
     * Optimaliseer database voor grote hoeveelheden data
     */
    private function optimizeDatabase() {
        // WAL mode voor betere concurrency en performance
        $this->db->exec('PRAGMA journal_mode = WAL');
        
        // Grotere cache voor betere performance (64MB)
        $this->db->exec('PRAGMA cache_size = -64000');
        
        // Synchronous mode voor betere performance
        $this->db->exec('PRAGMA synchronous = NORMAL');
        
        // Temp store in memory voor snellere temp operaties
        $this->db->exec('PRAGMA temp_store = MEMORY');
        
        // Grotere page size voor betere performance
        $this->db->exec('PRAGMA page_size = 4096');
        
        // Foreign keys aanzetten
        $this->db->exec('PRAGMA foreign_keys = ON');
        
        // Memory mapping voor grote databases
        $this->db->exec('PRAGMA mmap_size = 268435456'); // 256MB
        
        // Auto vacuum voor database onderhoud
        $this->db->exec('PRAGMA auto_vacuum = INCREMENTAL');
    }
}
?> 