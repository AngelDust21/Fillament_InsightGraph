<?php
/**
 * Material Class voor 3D Print Calculator
 * Beheert filament/materialen CRUD operaties
 */

class Material {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Haal alle materialen op
     */
    public function getAll($filters = []) {
        $sql = "SELECT * FROM materials WHERE 1=1";
        $params = [];
        
        if (!empty($filters['type'])) {
            $sql .= " AND type = :type";
            $params['type'] = $filters['type'];
        }
        
        if (!empty($filters['brand'])) {
            $sql .= " AND brand = :brand";
            $params['brand'] = $filters['brand'];
        }
        
        if (!empty($filters['search'])) {
            $sql .= " AND (name LIKE :search OR brand LIKE :search OR type LIKE :search)";
            $params['search'] = '%' . $filters['search'] . '%';
        }
        
        $sql .= " ORDER BY brand, name";
        
        return $this->db->fetchAll($sql, $params);
    }
    
    /**
     * Haal materiaal op basis van ID
     */
    public function getById($id) {
        return $this->db->fetchOne("SELECT * FROM materials WHERE id = ?", [$id]);
    }
    
    /**
     * Voeg nieuw materiaal toe
     */
    public function create($data) {
        $required = ['name', 'brand', 'type', 'price_per_kg', 'density', 'print_temp_min', 'print_temp_max'];
        
        foreach ($required as $field) {
            if (empty($data[$field])) {
                throw new Exception("Veld '$field' is verplicht");
            }
        }
        
        // Valideer numerieke waarden
        if (!is_numeric($data['price_per_kg']) || $data['price_per_kg'] <= 0) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        if (!is_numeric($data['density']) || $data['density'] <= 0) {
            throw new Exception("Dichtheid moet een positief getal zijn");
        }
        
        if (!is_numeric($data['print_temp_min']) || !is_numeric($data['print_temp_max'])) {
            throw new Exception("Print temperaturen moeten numeriek zijn");
        }
        
        if ($data['print_temp_min'] >= $data['print_temp_max']) {
            throw new Exception("Minimale print temperatuur moet lager zijn dan maximale");
        }
        
        // Default waarden
        $data['diameter'] = $data['diameter'] ?? 1.75;
        $data['failure_rate'] = $data['failure_rate'] ?? 5.0;
        $data['description'] = $data['description'] ?? '';
        $data['color'] = $data['color'] ?? '';
        
        return $this->db->insert('materials', $data);
    }
    
    /**
     * Update materiaal
     */
    public function update($id, $data) {
        $material = $this->getById($id);
        if (!$material) {
            throw new Exception("Materiaal niet gevonden");
        }
        
        // Valideer numerieke waarden
        if (isset($data['price_per_kg']) && (!is_numeric($data['price_per_kg']) || $data['price_per_kg'] <= 0)) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        if (isset($data['density']) && (!is_numeric($data['density']) || $data['density'] <= 0)) {
            throw new Exception("Dichtheid moet een positief getal zijn");
        }
        
        if (isset($data['print_temp_min']) && isset($data['print_temp_max'])) {
            if (!is_numeric($data['print_temp_min']) || !is_numeric($data['print_temp_max'])) {
                throw new Exception("Print temperaturen moeten numeriek zijn");
            }
            
            if ($data['print_temp_min'] >= $data['print_temp_max']) {
                throw new Exception("Minimale print temperatuur moet lager zijn dan maximale");
            }
        }
        
        return $this->db->update('materials', $data, 'id = ?', [$id]);
    }
    
    /**
     * Verwijder materiaal
     */
    public function delete($id) {
        // Check of materiaal wordt gebruikt in berekeningen
        $used = $this->db->fetchOne("SELECT COUNT(*) as count FROM calculations WHERE material_id = ?", [$id]);
        
        if ($used['count'] > 0) {
            throw new Exception("Materiaal kan niet worden verwijderd omdat het wordt gebruikt in berekeningen");
        }
        
        return $this->db->delete('materials', 'id = ?', [$id]);
    }
    
    /**
     * Haal unieke types op
     */
    public function getTypes() {
        $result = $this->db->fetchAll("SELECT DISTINCT type FROM materials ORDER BY type");
        return array_column($result, 'type');
    }
    
    /**
     * Haal unieke merken op
     */
    public function getBrands() {
        $result = $this->db->fetchAll("SELECT DISTINCT brand FROM materials ORDER BY brand");
        return array_column($result, 'brand');
    }
    
    /**
     * Zoek materialen
     */
    public function search($query) {
        return $this->getAll(['search' => $query]);
    }
    
    /**
     * Haal materialen op per type
     */
    public function getByType($type) {
        return $this->getAll(['type' => $type]);
    }
    
    /**
     * Haal materialen op per merk
     */
    public function getByBrand($brand) {
        return $this->getAll(['brand' => $brand]);
    }
    
    /**
     * Valideer materiaal data
     */
    public function validate($data) {
        $errors = [];
        
        if (empty($data['name'])) {
            $errors[] = "Naam is verplicht";
        }
        
        if (empty($data['brand'])) {
            $errors[] = "Merk is verplicht";
        }
        
        if (empty($data['type'])) {
            $errors[] = "Type is verplicht";
        }
        
        if (empty($data['price_per_kg']) || !is_numeric($data['price_per_kg']) || $data['price_per_kg'] <= 0) {
            $errors[] = "Prijs moet een positief getal zijn";
        }
        
        if (empty($data['density']) || !is_numeric($data['density']) || $data['density'] <= 0) {
            $errors[] = "Dichtheid moet een positief getal zijn";
        }
        
        if (empty($data['print_temp_min']) || !is_numeric($data['print_temp_min'])) {
            $errors[] = "Minimale print temperatuur is verplicht";
        }
        
        if (empty($data['print_temp_max']) || !is_numeric($data['print_temp_max'])) {
            $errors[] = "Maximale print temperatuur is verplicht";
        }
        
        if (isset($data['print_temp_min']) && isset($data['print_temp_max'])) {
            if ($data['print_temp_min'] >= $data['print_temp_max']) {
                $errors[] = "Minimale print temperatuur moet lager zijn dan maximale";
            }
        }
        
        return $errors;
    }
    
    /**
     * Import materialen uit CSV
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
     * Export materialen naar CSV
     */
    public function exportToCSV($filters = []) {
        $materials = $this->getAll($filters);
        
        $filename = 'materials_export_' . date('Y-m-d_H-i-s') . '.csv';
        $filepath = __DIR__ . '/../exports/' . $filename;
        
        // Maak exports directory als het niet bestaat
        $exportDir = dirname($filepath);
        if (!is_dir($exportDir)) {
            mkdir($exportDir, 0755, true);
        }
        
        $handle = fopen($filepath, 'w');
        
        if (empty($materials)) {
            fclose($handle);
            return $filepath;
        }
        
        // Schrijf headers
        fputcsv($handle, array_keys($materials[0]));
        
        // Schrijf data
        foreach ($materials as $material) {
            fputcsv($handle, $material);
        }
        
        fclose($handle);
        return $filepath;
    }
}
?> 