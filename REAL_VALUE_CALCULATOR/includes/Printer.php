<?php
/**
 * Printer Class voor 3D Print Calculator
 * Beheert 3D printer CRUD operaties
 */

class Printer {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Haal alle printers op
     */
    public function getAll($filters = []) {
        $sql = "SELECT * FROM printers WHERE 1=1";
        $params = [];
        
        if (!empty($filters['brand'])) {
            $sql .= " AND brand = :brand";
            $params['brand'] = $filters['brand'];
        }
        
        if (!empty($filters['search'])) {
            $sql .= " AND (name LIKE :search OR brand LIKE :search OR model LIKE :search)";
            $params['search'] = '%' . $filters['search'] . '%';
        }
        
        if (!empty($filters['min_price'])) {
            $sql .= " AND price >= :min_price";
            $params['min_price'] = $filters['min_price'];
        }
        
        if (!empty($filters['max_price'])) {
            $sql .= " AND price <= :max_price";
            $params['max_price'] = $filters['max_price'];
        }
        
        $sql .= " ORDER BY brand, name";
        
        return $this->db->fetchAll($sql, $params);
    }
    
    /**
     * Haal printer op basis van ID
     */
    public function getById($id) {
        return $this->db->fetchOne("SELECT * FROM printers WHERE id = ?", [$id]);
    }
    
    /**
     * Voeg nieuwe printer toe
     */
    public function create($data) {
        $required = ['name', 'brand', 'model', 'price', 'build_volume_x', 'build_volume_y', 'build_volume_z', 'power_watts'];
        
        foreach ($required as $field) {
            if (empty($data[$field])) {
                throw new Exception("Veld '$field' is verplicht");
            }
        }
        
        // Valideer numerieke waarden
        if (!is_numeric($data['price']) || $data['price'] <= 0) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        if (!is_numeric($data['build_volume_x']) || $data['build_volume_x'] <= 0) {
            throw new Exception("Build volume X moet een positief getal zijn");
        }
        
        if (!is_numeric($data['build_volume_y']) || $data['build_volume_y'] <= 0) {
            throw new Exception("Build volume Y moet een positief getal zijn");
        }
        
        if (!is_numeric($data['build_volume_z']) || $data['build_volume_z'] <= 0) {
            throw new Exception("Build volume Z moet een positief getal zijn");
        }
        
        if (!is_numeric($data['power_watts']) || $data['power_watts'] <= 0) {
            throw new Exception("Power usage moet een positief getal zijn");
        }
        
        // Default waarden
        $data['maintenance_yearly'] = $data['maintenance_yearly'] ?? 50.0;
        $data['depreciation_years'] = $data['depreciation_years'] ?? 3;
        $data['prints_per_year'] = $data['prints_per_year'] ?? 500;
        $data['description'] = $data['description'] ?? '';
        $data['features'] = $data['features'] ?? '[]';
        
        // Valideer features JSON
        if (is_array($data['features'])) {
            $data['features'] = json_encode($data['features']);
        }
        
        return $this->db->insert('printers', $data);
    }
    
    /**
     * Update printer
     */
    public function update($id, $data) {
        $printer = $this->getById($id);
        if (!$printer) {
            throw new Exception("Printer niet gevonden");
        }
        
        // Valideer numerieke waarden
        if (isset($data['price']) && (!is_numeric($data['price']) || $data['price'] <= 0)) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        if (isset($data['build_volume_x']) && (!is_numeric($data['build_volume_x']) || $data['build_volume_x'] <= 0)) {
            throw new Exception("Build volume X moet een positief getal zijn");
        }
        
        if (isset($data['build_volume_y']) && (!is_numeric($data['build_volume_y']) || $data['build_volume_y'] <= 0)) {
            throw new Exception("Build volume Y moet een positief getal zijn");
        }
        
        if (isset($data['build_volume_z']) && (!is_numeric($data['build_volume_z']) || $data['build_volume_z'] <= 0)) {
            throw new Exception("Build volume Z moet een positief getal zijn");
        }
        
        if (isset($data['power_watts']) && (!is_numeric($data['power_watts']) || $data['power_watts'] <= 0)) {
            throw new Exception("Power usage moet een positief getal zijn");
        }
        
        // Valideer features JSON
        if (isset($data['features']) && is_array($data['features'])) {
            $data['features'] = json_encode($data['features']);
        }
        
        return $this->db->update('printers', $data, 'id = ?', [$id]);
    }
    
    /**
     * Verwijder printer
     */
    public function delete($id) {
        // Check of printer wordt gebruikt in berekeningen
        $used = $this->db->fetchOne("SELECT COUNT(*) as count FROM calculations WHERE printer_id = ?", [$id]);
        
        if ($used['count'] > 0) {
            throw new Exception("Printer kan niet worden verwijderd omdat het wordt gebruikt in berekeningen");
        }
        
        return $this->db->delete('printers', 'id = ?', [$id]);
    }
    
    /**
     * Haal unieke merken op
     */
    public function getBrands() {
        $result = $this->db->fetchAll("SELECT DISTINCT brand FROM printers ORDER BY brand");
        return array_column($result, 'brand');
    }
    
    /**
     * Zoek printers
     */
    public function search($query) {
        return $this->getAll(['search' => $query]);
    }
    
    /**
     * Haal printers op per merk
     */
    public function getByBrand($brand) {
        return $this->getAll(['brand' => $brand]);
    }
    
    /**
     * Haal printers op per prijsrange
     */
    public function getByPriceRange($minPrice, $maxPrice) {
        return $this->getAll(['min_price' => $minPrice, 'max_price' => $maxPrice]);
    }
    
    /**
     * Bereken build volume in cm³
     */
    public function getBuildVolume($id) {
        $printer = $this->getById($id);
        if (!$printer) {
            return 0;
        }
        
        return ($printer['build_volume_x'] * $printer['build_volume_y'] * $printer['build_volume_z']) / 1000; // cm³
    }
    
    /**
     * Haal printers op met specifieke features
     */
    public function getByFeatures($features = []) {
        $sql = "SELECT * FROM printers WHERE 1=1";
        $params = [];
        
        foreach ($features as $feature) {
            $sql .= " AND features LIKE :feature_" . count($params);
            $params['feature_' . count($params)] = '%"' . $feature . '"%';
        }
        
        $sql .= " ORDER BY brand, name";
        
        return $this->db->fetchAll($sql, $params);
    }
    
    /**
     * Valideer printer data
     */
    public function validate($data) {
        $errors = [];
        
        if (empty($data['name'])) {
            $errors[] = "Naam is verplicht";
        }
        
        if (empty($data['brand'])) {
            $errors[] = "Merk is verplicht";
        }
        
        if (empty($data['model'])) {
            $errors[] = "Model is verplicht";
        }
        
        if (empty($data['price']) || !is_numeric($data['price']) || $data['price'] <= 0) {
            $errors[] = "Prijs moet een positief getal zijn";
        }
        
        if (empty($data['build_volume_x']) || !is_numeric($data['build_volume_x']) || $data['build_volume_x'] <= 0) {
            $errors[] = "Build volume X moet een positief getal zijn";
        }
        
        if (empty($data['build_volume_y']) || !is_numeric($data['build_volume_y']) || $data['build_volume_y'] <= 0) {
            $errors[] = "Build volume Y moet een positief getal zijn";
        }
        
        if (empty($data['build_volume_z']) || !is_numeric($data['build_volume_z']) || $data['build_volume_z'] <= 0) {
            $errors[] = "Build volume Z moet een positief getal zijn";
        }
        
        if (empty($data['power_watts']) || !is_numeric($data['power_watts']) || $data['power_watts'] <= 0) {
            $errors[] = "Power usage moet een positief getal zijn";
        }
        
        return $errors;
    }
    
    /**
     * Bereken afschrijving per print
     */
    public function getDepreciationPerPrint($id) {
        $printer = $this->getById($id);
        if (!$printer) {
            return 0;
        }
        
        $totalPrints = $printer['prints_per_year'] * $printer['depreciation_years'];
        return $printer['price'] / $totalPrints;
    }
    
    /**
     * Bereken onderhoud per print
     */
    public function getMaintenancePerPrint($id) {
        $printer = $this->getById($id);
        if (!$printer) {
            return 0;
        }
        
        return $printer['maintenance_yearly'] / $printer['prints_per_year'];
    }
    
    /**
     * Haal features op als array
     */
    public function getFeaturesArray($id) {
        $printer = $this->getById($id);
        if (!$printer || empty($printer['features'])) {
            return [];
        }
        
        return json_decode($printer['features'], true) ?: [];
    }
    
    /**
     * Import printers uit CSV
     */
    public function importFromCSV($filePath) {
        if (!file_exists($filePath)) {
            throw new Exception("CSV bestand niet gevonden");
        }
        
        $handle = fopen($filePath, 'r');
        if (!$handle) {
            throw new Exception("Kan CSV bestand niet openen");
        }
        
        $headers = fgetcsv($handle);
        $imported = 0;
        $errors = [];
        
        while (($data = fgetcsv($handle)) !== false) {
            $row = array_combine($headers, $data);
            
            try {
                $this->create($row);
                $imported++;
            } catch (Exception $e) {
                $errors[] = "Rij " . ($imported + 1) . ": " . $e->getMessage();
            }
        }
        
        fclose($handle);
        
        return [
            'imported' => $imported,
            'errors' => $errors
        ];
    }
    
    /**
     * Export printers naar CSV
     */
    public function exportToCSV($filters = []) {
        $printers = $this->getAll($filters);
        
        $filename = 'printers_export_' . date('Y-m-d_H-i-s') . '.csv';
        $filepath = __DIR__ . '/../exports/' . $filename;
        
        // Maak exports directory als het niet bestaat
        $exportDir = dirname($filepath);
        if (!is_dir($exportDir)) {
            mkdir($exportDir, 0755, true);
        }
        
        $handle = fopen($filepath, 'w');
        
        if (empty($printers)) {
            fclose($handle);
            return $filepath;
        }
        
        // Schrijf headers
        fputcsv($handle, array_keys($printers[0]));
        
        // Schrijf data
        foreach ($printers as $printer) {
            fputcsv($handle, $printer);
        }
        
        fclose($handle);
        return $filepath;
    }
}
?> 