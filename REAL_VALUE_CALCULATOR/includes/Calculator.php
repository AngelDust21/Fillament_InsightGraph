<?php
/**
 * Calculator Class voor 3D Print Calculator
 * Kern berekening engine met alle kosten en business logic
 */

class Calculator {
    private $db;
    private $material;
    private $printer;
    private $nozzle;
    
    public function __construct() {
        $this->db = Database::getInstance();
        $this->material = new Material();
        $this->printer = new Printer();
        $this->nozzle = new Nozzle();
    }
    
    /**
     * Voer complete berekening uit
     */
    public function calculate($data) {
        // Valideer input
        $errors = $this->validateInput($data);
        if (!empty($errors)) {
            throw new Exception("Validatie fouten: " . implode(', ', $errors));
        }
        
        // Haal data op
        $material = $this->material->getById($data['material_id']);
        $printer = $this->printer->getById($data['printer_id']);
        $nozzle = $this->nozzle->getById($data['nozzle_id']);
        
        if (!$material || !$printer || !$nozzle) {
            throw new Exception("Materiaal, printer of nozzle niet gevonden");
        }
        
        // Bereken alle kosten
        $result = [
            'input_data' => $data,
            'material' => $material,
            'printer' => $printer,
            'nozzle' => $nozzle,
            'costs' => $this->calculateAllCosts($data, $material, $printer, $nozzle),
            'insights' => $this->generateInsights($data, $material, $printer, $nozzle),
            'recommendations' => $this->generateRecommendations($data, $material, $printer, $nozzle)
        ];
        
        // Sla ALLE berekeningen automatisch op voor data analyse
        // Dit geeft waardevolle inzichten over wat gebruikers berekenen
        $result['calculation_id'] = $this->saveCalculation($data, $result['costs']);
        
        return $result;
    }
    
    /**
     * Bereken alle kosten
     */
    private function calculateAllCosts($data, $material, $printer, $nozzle) {
        $weight_grams = floatval($data['weight_grams']);
        $print_hours = floatval($data['print_hours']);
        $support_percent = floatval($data['support_percent'] ?? 15) / 100;
        $failure_rate = floatval($data['failure_rate'] ?? 10) / 100;
        $electricity_cost = floatval($data['electricity_cost'] ?? 0.40);
        $design_hours = floatval($data['design_hours'] ?? 0.5);
        $hourly_rate = floatval($data['hourly_rate'] ?? 25);
        $markup_percent = floatval($data['markup_percent'] ?? 50) / 100;
        $post_processing_cost = floatval($data['post_processing_cost'] ?? 0);
        $shipping_cost = floatval($data['shipping_cost'] ?? 0);
        $overhead_percent = floatval($data['overhead_percent'] ?? 20) / 100;
        $tax_percent = floatval($data['tax_percent'] ?? 21) / 100;
        
        // === DIRECTE KOSTEN ===
        
        // 1. Materiaal kosten (inclusief support)
        $total_weight = $weight_grams * (1 + $support_percent);
        $material_cost = ($total_weight / 1000) * $material['price_per_kg'];
        
        // 2. Energie kosten
        $kwh_used = ($printer['power_watts'] / 1000) * $print_hours;
        $electricity_cost_total = $kwh_used * $electricity_cost;
        
        // 3. Nozzle wear kosten
        $nozzle_wear_cost = $this->nozzle->getCostForPrintTime($nozzle['id'], $print_hours);
        
        // === INDIRECTE KOSTEN ===
        
        // 4. Failure kosten
        $failure_cost = ($material_cost + $electricity_cost_total) * $failure_rate;
        
        // 5. Printer afschrijving
        $depreciation_cost = $this->printer->getDepreciationPerPrint($printer['id']);
        
        // 6. Onderhoud kosten
        $maintenance_cost = $this->printer->getMaintenancePerPrint($printer['id']);
        
        // 7. Bed adhesion kosten
        $bed_adhesion_cost = $this->calculateBedAdhesionCost($material, $printer);
        
        // === BUSINESS KOSTEN ===
        
        // 8. Arbeidskosten
        $labor_cost = $design_hours * $hourly_rate;
        
        // 9. Post-processing kosten
        $post_processing_total = $post_processing_cost;
        
        // 10. Verzending kosten
        $shipping_total = $shipping_cost;
        
        // 11. Overhead kosten
        $direct_costs = $material_cost + $electricity_cost_total + $nozzle_wear_cost;
        $overhead_cost = $direct_costs * $overhead_percent;
        
        // === TOTAAL BEREKENING ===
        
        $direct_costs_total = $material_cost + $electricity_cost_total + $nozzle_wear_cost;
        $indirect_costs_total = $failure_cost + $depreciation_cost + $maintenance_cost + $bed_adhesion_cost;
        $business_costs_total = $labor_cost + $post_processing_total + $shipping_total + $overhead_cost;
        
        $total_cost = $direct_costs_total + $indirect_costs_total + $business_costs_total;
        
        // BTW berekenen
        $tax_amount = $total_cost * $tax_percent;
        $total_with_tax = $total_cost + $tax_amount;
        
        // Verkoopprijs berekenen
        $selling_price = $total_with_tax * (1 + $markup_percent);
        $profit = $selling_price - $total_with_tax;
        
        // ROI en break-even
        $roi_percent = ($total_with_tax > 0) ? ($profit / $total_with_tax * 100) : 0;
        $break_even_prints = ($profit > 0) ? intval($total_with_tax / $profit) : 0;
        
        return [
            // Directe kosten
            'material_cost' => round($material_cost, 2),
            'electricity_cost' => round($electricity_cost_total, 2),
            'nozzle_wear_cost' => round($nozzle_wear_cost, 2),
            'direct_costs_total' => round($direct_costs_total, 2),
            
            // Indirecte kosten
            'failure_cost' => round($failure_cost, 2),
            'depreciation_cost' => round($depreciation_cost, 2),
            'maintenance_cost' => round($maintenance_cost, 2),
            'bed_adhesion_cost' => round($bed_adhesion_cost, 2),
            'indirect_costs_total' => round($indirect_costs_total, 2),
            
            // Business kosten
            'labor_cost' => round($labor_cost, 2),
            'post_processing_cost' => round($post_processing_total, 2),
            'shipping_cost' => round($shipping_total, 2),
            'overhead_cost' => round($overhead_cost, 2),
            'business_costs_total' => round($business_costs_total, 2),
            
            // Totalen
            'total_cost' => round($total_cost, 2),
            'tax_amount' => round($tax_amount, 2),
            'total_with_tax' => round($total_with_tax, 2),
            'selling_price' => round($selling_price, 2),
            'profit' => round($profit, 2),
            
            // Metrics
            'roi_percent' => round($roi_percent, 1),
            'break_even_prints' => $break_even_prints,
            
            // Details
            'total_weight' => round($total_weight, 0),
            'kwh_used' => round($kwh_used, 2),
            'print_hours' => $print_hours,
            'failure_rate' => $failure_rate * 100,
            'markup_percent' => $markup_percent * 100
        ];
    }
    
    /**
     * Bereken bed adhesion kosten
     */
    private function calculateBedAdhesionCost($material, $printer) {
        $adhesionCosts = [
            'PLA' => 0.05,    // €0.05 per print
            'PLA+' => 0.05,
            'PETG' => 0.10,   // €0.10 per print (meer glue nodig)
            'ABS' => 0.15,    // €0.15 per print (ABS juice)
            'TPU' => 0.20,    // €0.20 per print (specialistisch)
            'PC' => 0.25,     // €0.25 per print (dure adhesives)
            'PA' => 0.30,     // €0.30 per print (specialistisch)
            'CF' => 0.35,     // €0.35 per print (dure adhesives)
            'ASA' => 0.15     // €0.15 per print (ABS juice)
        ];
        
        return $adhesionCosts[$material['type']] ?? 0.05;
    }
    
    /**
     * Genereer insights
     */
    private function generateInsights($data, $material, $printer, $nozzle) {
        $insights = [];
        
        // Failure rate insights
        if ($data['failure_rate'] > 15) {
            $insights[] = [
                'type' => 'warning',
                'title' => 'Hoge mislukkingskans',
                'message' => 'Mislukkingspercentage van ' . ($data['failure_rate'] * 100) . '% is hoog. Overweeg betere printer settings of materiaal.',
                'impact' => 'high'
            ];
        }
        
        // Energy cost insights
        $kwh_used = ($printer['power_watts'] / 1000) * $data['print_hours'];
        if ($kwh_used > 2) {
            $insights[] = [
                'type' => 'info',
                'title' => 'Hoog energieverbruik',
                'message' => 'Print verbruikt ' . round($kwh_used, 1) . ' kWh. Overweeg nachttarief of energie-efficiënte printer.',
                'impact' => 'medium'
            ];
        }
        
        // Material cost insights
        if ($material['price_per_kg'] > 30) {
            $insights[] = [
                'type' => 'info',
                'title' => 'Duur materiaal',
                'message' => '€' . $material['price_per_kg'] . '/kg is duur. Overweeg goedkopere alternatieven voor prototypes.',
                'impact' => 'medium'
            ];
        }
        
        // Nozzle compatibility
        $compatible = $this->nozzle->getCompatibleWithMaterial($material['type']);
        $isCompatible = false;
        foreach ($compatible as $comp) {
            if ($comp['id'] == $nozzle['id']) {
                $isCompatible = true;
                break;
            }
        }
        
        if (!$isCompatible) {
            $insights[] = [
                'type' => 'warning',
                'title' => 'Nozzle incompatibiliteit',
                'message' => 'Nozzle materiaal ' . $nozzle['material'] . ' is mogelijk niet geschikt voor ' . $material['type'] . '.',
                'impact' => 'high'
            ];
        }
        
        return $insights;
    }
    
    /**
     * Genereer aanbevelingen
     */
    private function generateRecommendations($data, $material, $printer, $nozzle) {
        $recommendations = [];
        
        // Nozzle aanbevelingen
        $bestNozzle = $this->nozzle->getBestForMaterialAndDiameter($material['type'], $nozzle['diameter']);
        if ($bestNozzle && $bestNozzle['id'] != $nozzle['id']) {
            $recommendations[] = [
                'type' => 'nozzle',
                'title' => 'Betere nozzle optie',
                'message' => 'Overweeg ' . $bestNozzle['name'] . ' (€' . $bestNozzle['price'] . ') voor betere compatibiliteit.',
                'savings' => 'betere_duurzaamheid'
            ];
        }
        
        // Printer aanbevelingen
        if ($data['failure_rate'] > 10) {
            $recommendations[] = [
                'type' => 'printer',
                'title' => 'Betere printer voor materiaal',
                'message' => 'Overweeg een printer met betere temperatuur controle voor ' . $material['type'] . '.',
                'savings' => 'lagere_mislukkingskans'
            ];
        }
        
        // Materiaal aanbevelingen
        if ($material['price_per_kg'] > 25 && $data['weight_grams'] > 100) {
            $recommendations[] = [
                'type' => 'material',
                'title' => 'Goedkoper materiaal voor prototypes',
                'message' => 'Overweeg standaard PLA voor prototypes om materiaalkosten te besparen.',
                'savings' => '€' . round(($material['price_per_kg'] - 18.50) * ($data['weight_grams'] / 1000), 2)
            ];
        }
        
        return $recommendations;
    }
    
    /**
     * Valideer input data
     */
    private function validateInput($data) {
        $errors = [];
        
        $required = ['material_id', 'printer_id', 'nozzle_id', 'weight_grams', 'print_hours'];
        foreach ($required as $field) {
            if (empty($data[$field])) {
                $errors[] = "Veld '$field' is verplicht";
            }
        }
        
        if (isset($data['weight_grams']) && (!is_numeric($data['weight_grams']) || $data['weight_grams'] <= 0)) {
            $errors[] = "Gewicht moet een positief getal zijn";
        }
        
        if (isset($data['print_hours']) && (!is_numeric($data['print_hours']) || $data['print_hours'] <= 0)) {
            $errors[] = "Print tijd moet een positief getal zijn";
        }
        
        if (isset($data['support_percent']) && (!is_numeric($data['support_percent']) || $data['support_percent'] < 0 || $data['support_percent'] > 100)) {
            $errors[] = "Support percentage moet tussen 0 en 100 zijn";
        }
        
        if (isset($data['failure_rate']) && (!is_numeric($data['failure_rate']) || $data['failure_rate'] < 0 || $data['failure_rate'] > 100)) {
            $errors[] = "Mislukkingspercentage moet tussen 0 en 100 zijn";
        }
        
        return $errors;
    }
    
    /**
     * Sla berekening op in database
     */
    private function saveCalculation($data, $costs) {
        $calculationData = [
            'name' => $data['name'] ?? 'Berekening ' . date('Y-m-d H:i:s'),
            'material_id' => $data['material_id'],
            'printer_id' => $data['printer_id'],
            'nozzle_id' => $data['nozzle_id'],
            'weight_grams' => $data['weight_grams'],
            'print_hours' => $data['print_hours'],
            'support_percent' => $data['support_percent'] ?? 15,
            'failure_rate' => $data['failure_rate'] ?? 10,
            'electricity_cost' => $data['electricity_cost'] ?? 0.40,
            'design_hours' => $data['design_hours'] ?? 0.5,
            'hourly_rate' => $data['hourly_rate'] ?? 25,
            'markup_percent' => $data['markup_percent'] ?? 50,
            'post_processing_cost' => $data['post_processing_cost'] ?? 0,
            'shipping_cost' => $data['shipping_cost'] ?? 0,
            'overhead_percent' => $data['overhead_percent'] ?? 20,
            'tax_percent' => $data['tax_percent'] ?? 21,
            'total_cost' => $costs['total_cost'],
            'selling_price' => $costs['selling_price'],
            'profit' => $costs['profit'],
            'roi_percent' => $costs['roi_percent']
        ];
        
        return $this->db->insert('calculations', $calculationData);
    }
    
    /**
     * Haal opgeslagen berekeningen op
     */
    public function getSavedCalculations($limit = 10) {
        $sql = "SELECT c.*, m.name as material_name, p.name as printer_name, n.name as nozzle_name 
                FROM calculations c 
                LEFT JOIN materials m ON c.material_id = m.id 
                LEFT JOIN printers p ON c.printer_id = p.id 
                LEFT JOIN nozzles n ON c.nozzle_id = n.id 
                ORDER BY c.created_at DESC 
                LIMIT ?";
        
        return $this->db->fetchAll($sql, [$limit]);
    }
    
    /**
     * Haal specifieke berekening op
     */
    public function getCalculation($id) {
        $sql = "SELECT c.*, m.name as material_name, p.name as printer_name, n.name as nozzle_name 
                FROM calculations c 
                LEFT JOIN materials m ON c.material_id = m.id 
                LEFT JOIN printers p ON c.printer_id = p.id 
                LEFT JOIN nozzles n ON c.nozzle_id = n.id 
                WHERE c.id = ?";
        
        return $this->db->fetchOne($sql, [$id]);
    }
    
    /**
     * Verwijder berekening
     */
    public function deleteCalculation($id) {
        return $this->db->delete('calculations', 'id = ?', [$id]);
    }
    
    /**
     * Export berekeningen naar CSV
     */
    public function exportCalculationsToCSV($calculations) {
        $filename = 'calculations_export_' . date('Y-m-d_H-i-s') . '.csv';
        $filepath = __DIR__ . '/../exports/' . $filename;
        
        // Maak exports directory als het niet bestaat
        $exportDir = dirname($filepath);
        if (!is_dir($exportDir)) {
            mkdir($exportDir, 0755, true);
        }
        
        $handle = fopen($filepath, 'w');
        
        if (empty($calculations)) {
            fclose($handle);
            return $filepath;
        }
        
        // Schrijf headers
        fputcsv($handle, array_keys($calculations[0]));
        
        // Schrijf data
        foreach ($calculations as $calculation) {
            fputcsv($handle, $calculation);
        }
        
        fclose($handle);
        return $filepath;
    }
    
    /**
     * Haal statistieken op over alle berekeningen
     * Voor data analyse en business insights - Geoptimaliseerd voor grote datasets
     */
    public function getCalculationStats() {
        $stats = [];
        
        // Totaal aantal berekeningen
        $sql = "SELECT COUNT(*) as total_calculations FROM calculations";
        $stats['total_calculations'] = $this->db->fetchOne($sql)['total_calculations'];
        
        // Gebruik views voor snellere queries bij grote datasets
        // Meest gebruikte materialen (gebruik view)
        $sql = "SELECT * FROM v_popular_materials LIMIT 10";
        $stats['popular_materials'] = $this->db->fetchAll($sql);
        
        // Meest gebruikte printers (gebruik view)
        $sql = "SELECT * FROM v_popular_printers LIMIT 10";
        $stats['popular_printers'] = $this->db->fetchAll($sql);
        
        // Gemiddelde kosten per print (geoptimaliseerde query)
        $sql = "SELECT 
                    AVG(total_cost) as avg_total_cost,
                    AVG(selling_price) as avg_selling_price,
                    AVG(profit) as avg_profit,
                    AVG(roi_percent) as avg_roi,
                    AVG(weight_grams) as avg_weight,
                    AVG(print_hours) as avg_print_hours,
                    COUNT(*) as total_count
                FROM calculations";
        $stats['cost_analysis'] = $this->db->fetchOne($sql);
        
        // Berekeningen per dag (laatste 30 dagen) - geoptimaliseerd
        $sql = "SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as calculations_count,
                    AVG(total_cost) as avg_cost
                FROM calculations 
                WHERE created_at >= DATE('now', '-30 days')
                GROUP BY DATE(created_at)
                ORDER BY date DESC";
        $stats['daily_activity'] = $this->db->fetchAll($sql);
        
        // Gewicht distributie (geoptimaliseerd met index)
        $sql = "SELECT 
                    CASE 
                        WHEN weight_grams < 50 THEN 'Klein (<50g)'
                        WHEN weight_grams < 200 THEN 'Medium (50-200g)'
                        WHEN weight_grams < 500 THEN 'Groot (200-500g)'
                        ELSE 'Zeer groot (>500g)'
                    END as weight_category,
                    COUNT(*) as count,
                    AVG(total_cost) as avg_cost
                FROM calculations 
                GROUP BY weight_category
                ORDER BY count DESC";
        $stats['weight_distribution'] = $this->db->fetchAll($sql);
        
        // Print tijd distributie (geoptimaliseerd met index)
        $sql = "SELECT 
                    CASE 
                        WHEN print_hours < 2 THEN 'Kort (<2u)'
                        WHEN print_hours < 8 THEN 'Medium (2-8u)'
                        WHEN print_hours < 24 THEN 'Lang (8-24u)'
                        ELSE 'Zeer lang (>24u)'
                    END as time_category,
                    COUNT(*) as count,
                    AVG(total_cost) as avg_cost
                FROM calculations 
                GROUP BY time_category
                ORDER BY count DESC";
        $stats['time_distribution'] = $this->db->fetchAll($sql);
        
        // Nieuwe statistieken voor grote datasets
        $stats['performance_metrics'] = $this->getPerformanceMetrics();
        
        return $stats;
    }
    
    /**
     * Haal performance metrics op voor grote datasets
     */
    private function getPerformanceMetrics() {
        // Database grootte en performance info
        $sql = "SELECT 
                    COUNT(*) as total_records,
                    COUNT(DISTINCT material_id) as unique_materials,
                    COUNT(DISTINCT printer_id) as unique_printers,
                    COUNT(DISTINCT nozzle_id) as unique_nozzles,
                    MIN(created_at) as first_calculation,
                    MAX(created_at) as last_calculation,
                    (julianday(MAX(created_at)) - julianday(MIN(created_at))) as days_span
                FROM calculations";
        
        $metrics = $this->db->fetchOne($sql);
        
        // Bereken gemiddelde berekeningen per dag
        if ($metrics['days_span'] > 0) {
            $metrics['avg_calculations_per_day'] = round($metrics['total_records'] / $metrics['days_span'], 2);
        } else {
            $metrics['avg_calculations_per_day'] = 0;
        }
        
        // Top 5 meest winstgevende materialen
        $sql = "SELECT 
                    m.name, m.brand, m.type,
                    AVG(c.profit) as avg_profit,
                    COUNT(c.id) as usage_count
                FROM calculations c
                JOIN materials m ON c.material_id = m.id
                GROUP BY c.material_id
                HAVING COUNT(c.id) >= 5
                ORDER BY AVG(c.profit) DESC
                LIMIT 5";
        $metrics['top_profitable_materials'] = $this->db->fetchAll($sql);
        
        return $metrics;
    }
    
    /**
     * Haal recente berekeningen op met meer details
     */
    public function getRecentCalculationsWithDetails($limit = 20) {
        $sql = "SELECT 
                    c.*,
                    m.name as material_name, 
                    m.brand as material_brand,
                    m.type as material_type,
                    p.name as printer_name, 
                    p.brand as printer_brand,
                    n.name as nozzle_name,
                    n.diameter as nozzle_diameter
                FROM calculations c 
                LEFT JOIN materials m ON c.material_id = m.id 
                LEFT JOIN printers p ON c.printer_id = p.id 
                LEFT JOIN nozzles n ON c.nozzle_id = n.id 
                ORDER BY c.created_at DESC 
                LIMIT ?";
        
        return $this->db->fetchAll($sql, [$limit]);
    }
    
    /**
     * Zoek berekeningen op basis van criteria
     */
    public function searchCalculations($filters = []) {
        $where = [];
        $params = [];
        
        if (!empty($filters['material_type'])) {
            $where[] = "m.type = ?";
            $params[] = $filters['material_type'];
        }
        
        if (!empty($filters['min_cost'])) {
            $where[] = "c.total_cost >= ?";
            $params[] = $filters['min_cost'];
        }
        
        if (!empty($filters['max_cost'])) {
            $where[] = "c.total_cost <= ?";
            $params[] = $filters['max_cost'];
        }
        
        if (!empty($filters['date_from'])) {
            $where[] = "c.created_at >= ?";
            $params[] = $filters['date_from'];
        }
        
        if (!empty($filters['date_to'])) {
            $where[] = "c.created_at <= ?";
            $params[] = $filters['date_to'];
        }
        
        $whereClause = !empty($where) ? "WHERE " . implode(" AND ", $where) : "";
        
        $sql = "SELECT 
                    c.*,
                    m.name as material_name, 
                    m.brand as material_brand,
                    p.name as printer_name, 
                    p.brand as printer_brand,
                    n.name as nozzle_name
                FROM calculations c 
                LEFT JOIN materials m ON c.material_id = m.id 
                LEFT JOIN printers p ON c.printer_id = p.id 
                LEFT JOIN nozzles n ON c.nozzle_id = n.id 
                $whereClause
                ORDER BY c.created_at DESC";
        
        return $this->db->fetchAll($sql, $params);
    }
}
?> 