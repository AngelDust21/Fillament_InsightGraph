<?php
/**
 * Nozzle Class voor 3D Print Calculator
 * Beheert nozzle CRUD operaties en wear calculations
 */

class Nozzle {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Haal alle nozzles op
     */
    public function getAll($filters = []) {
        $sql = "SELECT * FROM nozzles WHERE 1=1";
        $params = [];
        
        if (!empty($filters['diameter'])) {
            $sql .= " AND diameter = :diameter";
            $params['diameter'] = $filters['diameter'];
        }
        
        if (!empty($filters['material'])) {
            $sql .= " AND material = :material";
            $params['material'] = $filters['material'];
        }
        
        if (!empty($filters['search'])) {
            $sql .= " AND (name LIKE :search OR material LIKE :search)";
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
        
        $sql .= " ORDER BY diameter, material, name";
        
        return $this->db->fetchAll($sql, $params);
    }
    
    /**
     * Haal nozzle op basis van ID
     */
    public function getById($id) {
        return $this->db->fetchOne("SELECT * FROM nozzles WHERE id = ?", [$id]);
    }
    
    /**
     * Voeg nieuwe nozzle toe
     */
    public function create($data) {
        $required = ['name', 'diameter', 'material', 'price'];
        
        foreach ($required as $field) {
            if (empty($data[$field])) {
                throw new Exception("Veld '$field' is verplicht");
            }
        }
        
        // Valideer numerieke waarden
        if (!is_numeric($data['diameter']) || $data['diameter'] <= 0) {
            throw new Exception("Diameter moet een positief getal zijn");
        }
        
        if (!is_numeric($data['price']) || $data['price'] <= 0) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        // Valideer diameter (gebruikelijke maten)
        $validDiameters = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2];
        if (!in_array($data['diameter'], $validDiameters)) {
            throw new Exception("Diameter moet een van de volgende waarden zijn: " . implode(', ', $validDiameters));
        }
        
        // Default waarden
        $data['lifespan_hours'] = $data['lifespan_hours'] ?? 1000;
        $data['wear_rate'] = $data['wear_rate'] ?? 0.001;
        $data['description'] = $data['description'] ?? '';
        
        // Valideer lifespan en wear rate
        if (!is_numeric($data['lifespan_hours']) || $data['lifespan_hours'] <= 0) {
            throw new Exception("Lifespan moet een positief getal zijn");
        }
        
        if (!is_numeric($data['wear_rate']) || $data['wear_rate'] < 0) {
            throw new Exception("Wear rate moet een positief getal zijn");
        }
        
        return $this->db->insert('nozzles', $data);
    }
    
    /**
     * Update nozzle
     */
    public function update($id, $data) {
        $nozzle = $this->getById($id);
        if (!$nozzle) {
            throw new Exception("Nozzle niet gevonden");
        }
        
        // Valideer numerieke waarden
        if (isset($data['diameter']) && (!is_numeric($data['diameter']) || $data['diameter'] <= 0)) {
            throw new Exception("Diameter moet een positief getal zijn");
        }
        
        if (isset($data['price']) && (!is_numeric($data['price']) || $data['price'] <= 0)) {
            throw new Exception("Prijs moet een positief getal zijn");
        }
        
        if (isset($data['lifespan_hours']) && (!is_numeric($data['lifespan_hours']) || $data['lifespan_hours'] <= 0)) {
            throw new Exception("Lifespan moet een positief getal zijn");
        }
        
        if (isset($data['wear_rate']) && (!is_numeric($data['wear_rate']) || $data['wear_rate'] < 0)) {
            throw new Exception("Wear rate moet een positief getal zijn");
        }
        
        // Valideer diameter als het wordt gewijzigd
        if (isset($data['diameter'])) {
            $validDiameters = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2];
            if (!in_array($data['diameter'], $validDiameters)) {
                throw new Exception("Diameter moet een van de volgende waarden zijn: " . implode(', ', $validDiameters));
            }
        }
        
        return $this->db->update('nozzles', $data, 'id = ?', [$id]);
    }
    
    /**
     * Verwijder nozzle
     */
    public function delete($id) {
        // Check of nozzle wordt gebruikt in berekeningen
        $used = $this->db->fetchOne("SELECT COUNT(*) as count FROM calculations WHERE nozzle_id = ?", [$id]);
        
        if ($used['count'] > 0) {
            throw new Exception("Nozzle kan niet worden verwijderd omdat het wordt gebruikt in berekeningen");
        }
        
        return $this->db->delete('nozzles', 'id = ?', [$id]);
    }
    
    /**
     * Haal unieke diameters op
     */
    public function getDiameters() {
        $result = $this->db->fetchAll("SELECT DISTINCT diameter FROM nozzles ORDER BY diameter");
        return array_column($result, 'diameter');
    }
    
    /**
     * Haal unieke materialen op
     */
    public function getMaterials() {
        $result = $this->db->fetchAll("SELECT DISTINCT material FROM nozzles ORDER BY material");
        return array_column($result, 'material');
    }
    
    /**
     * Zoek nozzles
     */
    public function search($query) {
        return $this->getAll(['search' => $query]);
    }
    
    /**
     * Haal nozzles op per diameter
     */
    public function getByDiameter($diameter) {
        return $this->getAll(['diameter' => $diameter]);
    }
    
    /**
     * Haal nozzles op per materiaal
     */
    public function getByMaterial($material) {
        return $this->getAll(['material' => $material]);
    }
    
    /**
     * Haal nozzles op per prijsrange
     */
    public function getByPriceRange($minPrice, $maxPrice) {
        return $this->getAll(['min_price' => $minPrice, 'max_price' => $maxPrice]);
    }
    
    /**
     * Bereken nozzle wear per print uur
     */
    public function getWearPerHour($id) {
        $nozzle = $this->getById($id);
        if (!$nozzle) {
            return 0;
        }
        
        return $nozzle['wear_rate'];
    }
    
    /**
     * Bereken nozzle kosten per print uur
     */
    public function getCostPerHour($id) {
        $nozzle = $this->getById($id);
        if (!$nozzle) {
            return 0;
        }
        
        return $nozzle['price'] / $nozzle['lifespan_hours'];
    }
    
    /**
     * Bereken nozzle kosten voor specifieke print tijd
     */
    public function getCostForPrintTime($id, $printHours) {
        $nozzle = $this->getById($id);
        if (!$nozzle) {
            return 0;
        }
        
        return ($nozzle['price'] / $nozzle['lifespan_hours']) * $printHours;
    }
    
    /**
     * Haal nozzles op die geschikt zijn voor materiaal
     */
    public function getCompatibleWithMaterial($materialType) {
        $compatibility = [
            'PLA' => ['brass', 'hardened_steel', 'ruby'],
            'PLA+' => ['brass', 'hardened_steel', 'ruby'],
            'PETG' => ['brass', 'hardened_steel', 'ruby'],
            'ABS' => ['brass', 'hardened_steel', 'ruby'],
            'TPU' => ['brass', 'hardened_steel'],
            'PC' => ['hardened_steel', 'ruby'],
            'PA' => ['hardened_steel', 'ruby'],
            'CF' => ['hardened_steel', 'ruby', 'tungsten_carbide'],
            'ASA' => ['brass', 'hardened_steel', 'ruby']
        ];
        
        $compatibleMaterials = $compatibility[$materialType] ?? ['brass'];
        
        $sql = "SELECT * FROM nozzles WHERE material IN (" . str_repeat('?,', count($compatibleMaterials) - 1) . "?) ORDER BY diameter, material";
        
        return $this->db->fetchAll($sql, $compatibleMaterials);
    }
    
    /**
     * Haal beste nozzle op voor materiaal en diameter
     */
    public function getBestForMaterialAndDiameter($materialType, $diameter) {
        $compatible = $this->getCompatibleWithMaterial($materialType);
        
        // Filter op diameter
        $filtered = array_filter($compatible, function($nozzle) use ($diameter) {
            return $nozzle['diameter'] == $diameter;
        });
        
        if (empty($filtered)) {
            return null;
        }
        
        // Sorteer op prijs (goedkoopste eerst)
        usort($filtered, function($a, $b) {
            return $a['price'] <=> $b['price'];
        });
        
        return $filtered[0];
    }
    
    /**
     * Valideer nozzle data
     */
    public function validate($data) {
        $errors = [];
        
        if (empty($data['name'])) {
            $errors[] = "Naam is verplicht";
        }
        
        if (empty($data['diameter']) || !is_numeric($data['diameter']) || $data['diameter'] <= 0) {
            $errors[] = "Diameter moet een positief getal zijn";
        }
        
        if (empty($data['material'])) {
            $errors[] = "Materiaal is verplicht";
        }
        
        if (empty($data['price']) || !is_numeric($data['price']) || $data['price'] <= 0) {
            $errors[] = "Prijs moet een positief getal zijn";
        }
        
        // Valideer diameter
        if (isset($data['diameter'])) {
            $validDiameters = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2];
            if (!in_array($data['diameter'], $validDiameters)) {
                $errors[] = "Diameter moet een van de volgende waarden zijn: " . implode(', ', $validDiameters);
            }
        }
        
        return $errors;
    }
    
    /**
     * Haal nozzle materialen op met eigenschappen
     */
    public function getMaterialProperties() {
        return [
            'brass' => [
                'name' => 'Messing',
                'hardness' => 3,
                'cost' => 'low',
                'durability' => 'medium',
                'description' => 'Standaard nozzle voor de meeste materialen'
            ],
            'hardened_steel' => [
                'name' => 'Gehard Staal',
                'hardness' => 7,
                'cost' => 'medium',
                'durability' => 'high',
                'description' => 'Voor abrasive materialen zoals CF, glasvezel'
            ],
            'ruby' => [
                'name' => 'Ruby',
                'hardness' => 9,
                'cost' => 'high',
                'durability' => 'very_high',
                'description' => 'Extreme duurzaamheid voor professioneel gebruik'
            ],
            'tungsten_carbide' => [
                'name' => 'Tungsten Carbide',
                'hardness' => 9,
                'cost' => 'very_high',
                'durability' => 'extreme',
                'description' => 'Ultra hard voor extreme abrasive materialen'
            ]
        ];
    }
    
    /**
     * Bereken nozzle efficiency score
     */
    public function getEfficiencyScore($id) {
        $nozzle = $this->getById($id);
        if (!$nozzle) {
            return 0;
        }
        
        $properties = $this->getMaterialProperties();
        $materialProps = $properties[$nozzle['material']] ?? [];
        
        // Score gebaseerd op levensduur, wear rate en materiaal eigenschappen
        $lifespanScore = min(100, ($nozzle['lifespan_hours'] / 1000) * 100);
        $wearScore = max(0, 100 - ($nozzle['wear_rate'] * 10000));
        $hardnessScore = ($materialProps['hardness'] ?? 3) * 10;
        
        return round(($lifespanScore + $wearScore + $hardnessScore) / 3, 1);
    }
    
    /**
     * Import nozzles uit CSV
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
     * Export nozzles naar CSV
     */
    public function exportToCSV($filters = []) {
        $nozzles = $this->getAll($filters);
        
        $filename = 'nozzles_export_' . date('Y-m-d_H-i-s') . '.csv';
        $filepath = __DIR__ . '/../exports/' . $filename;
        
        // Maak exports directory als het niet bestaat
        $exportDir = dirname($filepath);
        if (!is_dir($exportDir)) {
            mkdir($exportDir, 0755, true);
        }
        
        $handle = fopen($filepath, 'w');
        
        if (empty($nozzles)) {
            fclose($handle);
            return $filepath;
        }
        
        // Schrijf headers
        fputcsv($handle, array_keys($nozzles[0]));
        
        // Schrijf data
        foreach ($nozzles as $nozzle) {
            fputcsv($handle, $nozzle);
        }
        
        fclose($handle);
        return $filepath;
    }
}
?> 