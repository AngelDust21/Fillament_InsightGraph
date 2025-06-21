<?php
/**
 * Database Maintenance Script
 * Voor het onderhoud van grote datasets (1M+ records)
 */

require_once 'includes/Database.php';

class DatabaseMaintenance {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Voer alle maintenance taken uit
     */
    public function runMaintenance() {
        echo "=== Database Maintenance Start ===\n";
        
        $this->analyzeDatabase();
        $this->optimizeDatabase();
        $this->cleanupOldData();
        $this->updateStatistics();
        
        echo "=== Database Maintenance Voltooid ===\n";
    }
    
    /**
     * Analyseer database grootte en performance
     */
    private function analyzeDatabase() {
        echo "Analyseren van database...\n";
        
        // Database grootte
        $dbPath = __DIR__ . '/database/calculator.db';
        $size = filesize($dbPath);
        $sizeMB = round($size / 1024 / 1024, 2);
        
        echo "Database grootte: {$sizeMB} MB\n";
        
        // Aantal records
        $sql = "SELECT COUNT(*) as total FROM calculations";
        $result = $this->db->fetchOne($sql);
        $total = number_format($result['total']);
        
        echo "Totaal aantal berekeningen: {$total}\n";
        
        // Database statistieken
        $sql = "SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT material_id) as unique_materials,
                    COUNT(DISTINCT printer_id) as unique_printers,
                    MIN(created_at) as oldest_record,
                    MAX(created_at) as newest_record
                FROM calculations";
        
        $stats = $this->db->fetchOne($sql);
        
        echo "Unieke materialen: {$stats['unique_materials']}\n";
        echo "Unieke printers: {$stats['unique_printers']}\n";
        echo "Oudste record: {$stats['oldest_record']}\n";
        echo "Nieuwste record: {$stats['newest_record']}\n";
        
        // Performance metrics
        $this->checkPerformance();
    }
    
    /**
     * Controleer database performance
     */
    private function checkPerformance() {
        echo "\nPerformance controle...\n";
        
        // Test query performance
        $start = microtime(true);
        
        $sql = "SELECT COUNT(*) FROM calculations WHERE created_at >= DATE('now', '-30 days')";
        $this->db->fetchOne($sql);
        
        $end = microtime(true);
        $time = round(($end - $start) * 1000, 2);
        
        echo "30-dagen query tijd: {$time}ms\n";
        
        // Test join performance
        $start = microtime(true);
        
        $sql = "SELECT m.name, COUNT(c.id) as count 
                FROM materials m 
                LEFT JOIN calculations c ON m.id = c.material_id 
                GROUP BY m.id 
                ORDER BY count DESC 
                LIMIT 10";
        $this->db->fetchAll($sql);
        
        $end = microtime(true);
        $time = round(($end - $start) * 1000, 2);
        
        echo "Join query tijd: {$time}ms\n";
    }
    
    /**
     * Optimaliseer database
     */
    private function optimizeDatabase() {
        echo "\nOptimaliseren van database...\n";
        
        // Backup bestaande database
        $dbPath = __DIR__ . '/database/calculator.db';
        $backupPath = __DIR__ . '/database/calculator_backup_' . date('Y-m-d_H-i-s') . '.db';
        
        if (file_exists($dbPath)) {
            echo "Backup maken van bestaande database...\n";
            copy($dbPath, $backupPath);
            echo "Backup opgeslagen als: " . basename($backupPath) . "\n";
        }
        
        // VACUUM database (defragmenteer)
        echo "VACUUM uitvoeren...\n";
        $this->db->getConnection()->exec('VACUUM');
        
        // ANALYZE voor query optimizer
        echo "ANALYZE uitvoeren...\n";
        $this->db->getConnection()->exec('ANALYZE');
        
        // Herindexeer alle indexen
        echo "Indexen herindexeren...\n";
        $this->db->getConnection()->exec('REINDEX');
        
        // Update database statistieken
        echo "Database statistieken updaten...\n";
        $this->db->getConnection()->exec('PRAGMA optimize');
    }
    
    /**
     * Ruim oude data op (optioneel)
     */
    private function cleanupOldData() {
        echo "\nOude data opruimen...\n";
        
        // Tel oude records
        $sql = "SELECT COUNT(*) as count FROM calculations WHERE created_at < DATE('now', '-2 years')";
        $result = $this->db->fetchOne($sql);
        $oldRecords = $result['count'];
        
        if ($oldRecords > 0) {
            echo "Gevonden {$oldRecords} records ouder dan 2 jaar\n";
            
            // Vraag om bevestiging
            echo "Wilt u deze oude records verwijderen? (j/n): ";
            $handle = fopen("php://stdin", "r");
            $line = fgets($handle);
            fclose($handle);
            
            if (trim(strtolower($line)) === 'j') {
                echo "Verwijderen van oude records...\n";
                $sql = "DELETE FROM calculations WHERE created_at < DATE('now', '-2 years')";
                $this->db->getConnection()->exec($sql);
                echo "Verwijderd!\n";
            } else {
                echo "Oude records behouden.\n";
            }
        } else {
            echo "Geen oude records gevonden.\n";
        }
    }
    
    /**
     * Update statistieken en views
     */
    private function updateStatistics() {
        echo "\nStatistieken updaten...\n";
        
        // Update views
        echo "Views verversen...\n";
        $this->db->getConnection()->exec('DROP VIEW IF EXISTS v_popular_materials');
        $this->db->getConnection()->exec('DROP VIEW IF EXISTS v_popular_printers');
        $this->db->getConnection()->exec('DROP VIEW IF EXISTS v_daily_stats');
        
        // Hercreëer views
        $this->recreateViews();
        
        echo "Statistieken bijgewerkt!\n";
    }
    
    /**
     * Hercreëer database views
     */
    private function recreateViews() {
        // View voor populaire materialen
        $sql = "CREATE VIEW v_popular_materials AS
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
                ORDER BY usage_count DESC";
        $this->db->getConnection()->exec($sql);
        
        // View voor populaire printers
        $sql = "CREATE VIEW v_popular_printers AS
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
                ORDER BY usage_count DESC";
        $this->db->getConnection()->exec($sql);
        
        // View voor dagelijkse statistieken
        $sql = "CREATE VIEW v_daily_stats AS
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
                ORDER BY date DESC";
        $this->db->getConnection()->exec($sql);
    }
    
    /**
     * Genereer performance rapport
     */
    public function generatePerformanceReport() {
        echo "\n=== Performance Rapport ===\n";
        
        // Database grootte
        $dbPath = __DIR__ . '/database/calculator.db';
        $size = filesize($dbPath);
        $sizeMB = round($size / 1024 / 1024, 2);
        
        // Records per MB
        $sql = "SELECT COUNT(*) as total FROM calculations";
        $result = $this->db->fetchOne($sql);
        $total = $result['total'];
        $recordsPerMB = round($total / $sizeMB, 2);
        
        echo "Database grootte: {$sizeMB} MB\n";
        echo "Totaal records: " . number_format($total) . "\n";
        echo "Records per MB: {$recordsPerMB}\n";
        
        // Performance benchmarks
        $this->runPerformanceBenchmarks();
    }
    
    /**
     * Voer performance benchmarks uit
     */
    private function runPerformanceBenchmarks() {
        echo "\nPerformance benchmarks:\n";
        
        $queries = [
            'Count all' => "SELECT COUNT(*) FROM calculations",
            'Count last 30 days' => "SELECT COUNT(*) FROM calculations WHERE created_at >= DATE('now', '-30 days')",
            'Popular materials' => "SELECT * FROM v_popular_materials LIMIT 10",
            'Daily stats' => "SELECT * FROM v_daily_stats LIMIT 30",
            'Cost analysis' => "SELECT AVG(total_cost), AVG(profit) FROM calculations"
        ];
        
        foreach ($queries as $name => $sql) {
            $start = microtime(true);
            $this->db->fetchAll($sql);
            $end = microtime(true);
            $time = round(($end - $start) * 1000, 2);
            
            echo "  {$name}: {$time}ms\n";
        }
    }
    
    /**
     * Herbouw database met geoptimaliseerde schema
     */
    public function rebuildDatabase() {
        echo "=== Database Herbouw Start ===\n";
        
        $dbPath = __DIR__ . '/database/calculator.db';
        $schemaPath = __DIR__ . '/database/schema.sql';
        
        // Backup bestaande database
        if (file_exists($dbPath)) {
            $backupPath = __DIR__ . '/database/calculator_backup_' . date('Y-m-d_H-i-s') . '.db';
            echo "Backup maken van bestaande database...\n";
            copy($dbPath, $backupPath);
            echo "Backup opgeslagen als: " . basename($backupPath) . "\n";
        }
        
        // Sluit database connectie
        $this->db->getConnection()->close();
        
        // Verwijder oude database
        if (file_exists($dbPath)) {
            echo "Verwijderen van oude database...\n";
            unlink($dbPath);
        }
        
        // Maak nieuwe database met geoptimaliseerde schema
        echo "Nieuwe database aanmaken met geoptimaliseerde schema...\n";
        
        try {
            // Maak nieuwe database connectie
            $newDb = new PDO('sqlite:' . $dbPath);
            $newDb->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Lees en voer schema uit
            $schema = file_get_contents($schemaPath);
            $newDb->exec($schema);
            
            echo "Database schema succesvol toegepast!\n";
            
            // Voeg sample data toe
            echo "Sample data toevoegen...\n";
            $this->insertSampleData($newDb);
            
            echo "Database herbouw voltooid!\n";
            
        } catch (PDOException $e) {
            echo "Fout bij database herbouw: " . $e->getMessage() . "\n";
            
            // Herstel backup als er een fout optreedt
            if (file_exists($backupPath)) {
                echo "Herstellen van backup...\n";
                copy($backupPath, $dbPath);
                echo "Backup hersteld!\n";
            }
        }
    }
    
    /**
     * Voeg sample data toe aan nieuwe database
     */
    private function insertSampleData($db) {
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
        
        $stmt = $db->prepare("
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
        
        $stmt = $db->prepare("
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
        
        $stmt = $db->prepare("
            INSERT INTO nozzles (name, diameter, material, price, lifespan_hours, wear_rate, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ");
        
        foreach ($nozzles as $nozzle) {
            $stmt->execute($nozzle);
        }
        
        echo "Sample data toegevoegd!\n";
    }
}

// Run maintenance als script direct wordt uitgevoerd
if (php_sapi_name() === 'cli') {
    $maintenance = new DatabaseMaintenance();
    
    if (isset($argv[1])) {
        switch ($argv[1]) {
            case 'report':
                $maintenance->generatePerformanceReport();
                break;
            case 'rebuild':
                $maintenance->rebuildDatabase();
                break;
            case 'help':
                echo "Database Maintenance Script\n";
                echo "Gebruik:\n";
                echo "  php database_maintenance.php          - Normale maintenance\n";
                echo "  php database_maintenance.php report   - Performance rapport\n";
                echo "  php database_maintenance.php rebuild  - Herbouw database met geoptimaliseerd schema\n";
                echo "  php database_maintenance.php help     - Deze help\n";
                break;
            default:
                echo "Onbekende optie: {$argv[1]}\n";
                echo "Gebruik 'php database_maintenance.php help' voor meer informatie.\n";
                break;
        }
    } else {
        $maintenance->runMaintenance();
    }
}
?> 