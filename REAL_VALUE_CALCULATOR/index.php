<?php
/**
 * 3D Print Calculator - Hoofdpagina
 * Moderne Bootstrap 5 interface met CRUD en calculator functionaliteit
 */

// Include alle benodigde classes
require_once 'includes/Database.php';
require_once 'includes/Material.php';
require_once 'includes/Printer.php';
require_once 'includes/Nozzle.php';
require_once 'includes/Calculator.php';

// Initialize classes
$material = new Material();
$printer = new Printer();
$nozzle = new Nozzle();
$calculator = new Calculator();

// Haal data op voor dropdowns
$materials = $material->getAll();
$printers = $printer->getAll();
$nozzles = $nozzle->getAll();

// Process form submission
$calculationResult = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['calculate'])) {
    try {
        $calculationResult = $calculator->calculate($_POST);
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}

// Haal recente berekeningen op
$recentCalculations = $calculator->getSavedCalculations(5);
?>

<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Print Calculator - Professionele Kostprijsberekening</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: #667eea;
            --secondary-color: #764ba2;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --info-color: #3b82f6;
        }
        
        .gradient-bg {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        }
        
        .card-hover {
            transition: all 0.3s ease;
        }
        
        .card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .cost-breakdown {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
        }
        
        .cost-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .cost-item:last-child {
            border-bottom: none;
            font-weight: bold;
            font-size: 1.1em;
        }
    </style>
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg gradient-bg navbar-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#">
                <i class="fas fa-calculator me-2"></i>
                3D Print Calculator
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#calculator">
                            <i class="fas fa-calculator me-1"></i>Calculator
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#materials">
                            <i class="fas fa-cube me-1"></i>Materialen
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#printers">
                            <i class="fas fa-print me-1"></i>Printers
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#nozzles">
                            <i class="fas fa-circle me-1"></i>Nozzles
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#history">
                            <i class="fas fa-history me-1"></i>Geschiedenis
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="analytics.php">
                            <i class="fas fa-chart-bar me-1"></i>Data Analyse
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container py-5">
        <!-- Header Section -->
        <div class="row mb-5">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold text-dark mb-3">
                    Professionele 3D Print Calculator
                </h1>
                <p class="lead text-muted mb-4">
                    Bereken de echte kosten van je 3D prints met onze uitgebreide calculator. 
                    Alle verborgen kosten meegenomen - van materiaal tot energie, van onderhoud tot afschrijving.
                </p>
                <div class="d-flex gap-3">
                    <a href="#calculator" class="btn btn-primary btn-lg">
                        <i class="fas fa-calculator me-2"></i>Start Berekening
                    </a>
                    <a href="#materials" class="btn btn-outline-primary btn-lg">
                        <i class="fas fa-cube me-2"></i>Beheer Materialen
                    </a>
                </div>
            </div>
            <div class="col-lg-4">
                <div class="card card-hover border-0 shadow">
                    <div class="card-body text-center">
                        <i class="fas fa-chart-pie text-primary" style="font-size: 3rem;"></i>
                        <h5 class="mt-3">Uitgebreide Analyse</h5>
                        <p class="text-muted">15+ kostenfactoren meegenomen</p>
                        <div class="row text-center">
                            <div class="col-6">
                                <div class="h4 text-success mb-1">€0.00</div>
                                <div class="small text-muted">Totale Kosten</div>
                            </div>
                            <div class="col-6">
                                <div class="h4 text-primary mb-1">0%</div>
                                <div class="small text-muted">ROI</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Calculator Section -->
        <section id="calculator" class="mb-5">
            <div class="card card-hover border-0 shadow">
                <div class="card-header bg-primary text-white">
                    <h3 class="h5 mb-0">
                        <i class="fas fa-calculator me-2"></i>
                        3D Print Kosten Calculator
                    </h3>
                </div>
                <div class="card-body">
                    <form method="POST" id="calculatorForm">
                        <div class="row">
                            <!-- Basic Settings -->
                            <div class="col-lg-6">
                                <h5 class="mb-3">Basis Instellingen</h5>
                                
                                <!-- Material Selection -->
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-cube me-1"></i>Materiaal
                                    </label>
                                    <select name="material_id" class="form-select" required>
                                        <option value="">Selecteer materiaal...</option>
                                        <?php foreach ($materials as $mat): ?>
                                        <option value="<?= $mat['id'] ?>" <?= ($_POST['material_id'] ?? '') == $mat['id'] ? 'selected' : '' ?>>
                                            <?= $mat['brand'] ?> <?= $mat['name'] ?> - €<?= $mat['price_per_kg'] ?>/kg
                                        </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>

                                <!-- Printer Selection -->
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-print me-1"></i>Printer
                                    </label>
                                    <select name="printer_id" class="form-select" required>
                                        <option value="">Selecteer printer...</option>
                                        <?php foreach ($printers as $prt): ?>
                                        <option value="<?= $prt['id'] ?>" <?= ($_POST['printer_id'] ?? '') == $prt['id'] ? 'selected' : '' ?>>
                                            <?= $prt['brand'] ?> <?= $prt['model'] ?> - €<?= $prt['price'] ?>
                                        </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>

                                <!-- Nozzle Selection -->
                                <div class="mb-3">
                                    <label class="form-label">
                                        <i class="fas fa-circle me-1"></i>Nozzle
                                    </label>
                                    <select name="nozzle_id" class="form-select" required>
                                        <option value="">Selecteer nozzle...</option>
                                        <?php foreach ($nozzles as $nzl): ?>
                                        <option value="<?= $nzl['id'] ?>" <?= ($_POST['nozzle_id'] ?? '') == $nzl['id'] ? 'selected' : '' ?>>
                                            <?= $nzl['name'] ?> (<?= $nzl['diameter'] ?>mm) - €<?= $nzl['price'] ?>
                                        </option>
                                        <?php endforeach; ?>
                                    </select>
                                </div>

                                <!-- Print Parameters -->
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">
                                            <i class="fas fa-weight-hanging me-1"></i>Gewicht (gram)
                                        </label>
                                        <input type="number" name="weight_grams" class="form-control" 
                                               value="<?= $_POST['weight_grams'] ?? 50 ?>" min="1" max="5000" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">
                                            <i class="fas fa-clock me-1"></i>Print Tijd (uren)
                                        </label>
                                        <input type="number" name="print_hours" class="form-control" 
                                               value="<?= $_POST['print_hours'] ?? 3 ?>" min="0.1" max="100" step="0.1" required>
                                    </div>
                                </div>
                            </div>

                            <!-- Advanced Settings -->
                            <div class="col-lg-6">
                                <h5 class="mb-3">Geavanceerde Instellingen</h5>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Support (%)</label>
                                        <input type="range" name="support_percent" class="form-range" 
                                               min="0" max="50" value="<?= $_POST['support_percent'] ?? 15 ?>" 
                                               oninput="updateRangeValue(this, 'support_percent_value')">
                                        <div class="text-muted small">
                                            <span id="support_percent_value"><?= $_POST['support_percent'] ?? 15 ?></span>%
                                        </div>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Mislukkingspercentage (%)</label>
                                        <input type="range" name="failure_rate" class="form-range" 
                                               min="0" max="30" value="<?= $_POST['failure_rate'] ?? 10 ?>" 
                                               oninput="updateRangeValue(this, 'failure_rate_value')">
                                        <div class="text-muted small">
                                            <span id="failure_rate_value"><?= $_POST['failure_rate'] ?? 10 ?></span>%
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Stroomprijs (€/kWh)</label>
                                        <input type="number" name="electricity_cost" class="form-control" 
                                               value="<?= $_POST['electricity_cost'] ?? 0.40 ?>" min="0.1" max="1" step="0.01">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Uurtarief (€)</label>
                                        <input type="number" name="hourly_rate" class="form-control" 
                                               value="<?= $_POST['hourly_rate'] ?? 25 ?>" min="10" max="100">
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Ontwerp Tijd (uren)</label>
                                        <input type="number" name="design_hours" class="form-control" 
                                               value="<?= $_POST['design_hours'] ?? 0.5 ?>" min="0" max="20" step="0.1">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Winstmarge (%)</label>
                                        <input type="range" name="markup_percent" class="form-range" 
                                               min="0" max="200" value="<?= $_POST['markup_percent'] ?? 50 ?>" 
                                               oninput="updateRangeValue(this, 'markup_percent_value')">
                                        <div class="text-muted small">
                                            <span id="markup_percent_value"><?= $_POST['markup_percent'] ?? 50 ?></span>%
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Post-processing (€)</label>
                                        <input type="number" name="post_processing_cost" class="form-control" 
                                               value="<?= $_POST['post_processing_cost'] ?? 0 ?>" min="0" max="100" step="0.5">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Verzending (€)</label>
                                        <input type="number" name="shipping_cost" class="form-control" 
                                               value="<?= $_POST['shipping_cost'] ?? 0 ?>" min="0" max="50" step="0.5">
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Calculate Button -->
                        <div class="text-center mt-4">
                            <button type="submit" name="calculate" class="btn btn-primary btn-lg">
                                <i class="fas fa-calculator me-2"></i>
                                Bereken Eerlijke Prijs
                            </button>
                            <div class="form-check form-check-inline ms-3">
                                <input class="form-check-input" type="checkbox" name="save_calculation" id="saveCalculation" checked>
                                <label class="form-check-label" for="saveCalculation">
                                    Berekening opslaan
                                </label>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </section>

        <!-- Results Section -->
        <?php if ($calculationResult): ?>
        <section class="mb-5">
            <div class="card card-hover border-0 shadow">
                <div class="card-header bg-success text-white">
                    <h3 class="h5 mb-0">
                        <i class="fas fa-chart-pie me-2"></i>
                        Berekening Resultaten
                    </h3>
                </div>
                <div class="card-body">
                    <div class="row">
                        <!-- Summary Cards -->
                        <div class="col-lg-4 mb-4">
                            <div class="row">
                                <div class="col-6 mb-3">
                                    <div class="text-center p-3 bg-primary bg-opacity-10 rounded">
                                        <div class="h4 text-primary mb-1">€<?= $calculationResult['costs']['total_with_tax'] ?></div>
                                        <div class="small text-muted">Totale Kosten</div>
                                    </div>
                                </div>
                                <div class="col-6 mb-3">
                                    <div class="text-center p-3 bg-success bg-opacity-10 rounded">
                                        <div class="h4 text-success mb-1">€<?= $calculationResult['costs']['selling_price'] ?></div>
                                        <div class="small text-muted">Verkoopprijs</div>
                                    </div>
                                </div>
                                <div class="col-6 mb-3">
                                    <div class="text-center p-3 bg-warning bg-opacity-10 rounded">
                                        <div class="h4 text-warning mb-1">€<?= $calculationResult['costs']['profit'] ?></div>
                                        <div class="small text-muted">Winst</div>
                                    </div>
                                </div>
                                <div class="col-6 mb-3">
                                    <div class="text-center p-3 bg-info bg-opacity-10 rounded">
                                        <div class="h4 text-info mb-1"><?= $calculationResult['costs']['roi_percent'] ?>%</div>
                                        <div class="small text-muted">ROI</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Cost Breakdown -->
                        <div class="col-lg-8">
                            <h6 class="mb-3">Kosten Breakdown</h6>
                            <div class="cost-breakdown">
                                <div class="cost-item">
                                    <span>Materiaal</span>
                                    <span>€<?= $calculationResult['costs']['material_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Energie</span>
                                    <span>€<?= $calculationResult['costs']['electricity_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Nozzle Wear</span>
                                    <span>€<?= $calculationResult['costs']['nozzle_wear_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Mislukkingen</span>
                                    <span>€<?= $calculationResult['costs']['failure_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Afschrijving</span>
                                    <span>€<?= $calculationResult['costs']['depreciation_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Onderhoud</span>
                                    <span>€<?= $calculationResult['costs']['maintenance_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Bed Adhesion</span>
                                    <span>€<?= $calculationResult['costs']['bed_adhesion_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Arbeidskosten</span>
                                    <span>€<?= $calculationResult['costs']['labor_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Post-processing</span>
                                    <span>€<?= $calculationResult['costs']['post_processing_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Verzending</span>
                                    <span>€<?= $calculationResult['costs']['shipping_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>Overhead</span>
                                    <span>€<?= $calculationResult['costs']['overhead_cost'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span>BTW</span>
                                    <span>€<?= $calculationResult['costs']['tax_amount'] ?></span>
                                </div>
                                <div class="cost-item">
                                    <span class="fw-bold">TOTAAL</span>
                                    <span class="fw-bold">€<?= $calculationResult['costs']['total_with_tax'] ?></span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Insights -->
                    <?php if (!empty($calculationResult['insights'])): ?>
                    <div class="mt-4">
                        <h6 class="mb-3">Inzichten & Tips</h6>
                        <?php foreach ($calculationResult['insights'] as $insight): ?>
                        <div class="alert alert-<?= $insight['type'] === 'warning' ? 'warning' : ($insight['type'] === 'success' ? 'success' : 'info') ?> alert-sm">
                            <div class="fw-bold"><?= $insight['title'] ?></div>
                            <div class="small"><?= $insight['message'] ?></div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <?php endif; ?>

                    <!-- Recommendations -->
                    <?php if (!empty($calculationResult['recommendations'])): ?>
                    <div class="mt-4">
                        <h6 class="mb-3">Aanbevelingen</h6>
                        <?php foreach ($calculationResult['recommendations'] as $rec): ?>
                        <div class="alert alert-info alert-sm">
                            <div class="fw-bold"><?= $rec['title'] ?></div>
                            <div class="small"><?= $rec['message'] ?></div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </section>
        <?php endif; ?>

        <!-- Error Display -->
        <?php if ($error): ?>
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            <?= htmlspecialchars($error) ?>
        </div>
        <?php endif; ?>

        <!-- Quick Stats -->
        <div class="row mb-5">
            <div class="col-md-3">
                <div class="card card-hover border-0 shadow text-center">
                    <div class="card-body">
                        <i class="fas fa-cube text-primary mb-2" style="font-size: 2rem;"></i>
                        <h5><?= count($materials) ?></h5>
                        <p class="text-muted mb-0">Materialen</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-hover border-0 shadow text-center">
                    <div class="card-body">
                        <i class="fas fa-print text-primary mb-2" style="font-size: 2rem;"></i>
                        <h5><?= count($printers) ?></h5>
                        <p class="text-muted mb-0">Printers</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-hover border-0 shadow text-center">
                    <div class="card-body">
                        <i class="fas fa-circle text-primary mb-2" style="font-size: 2rem;"></i>
                        <h5><?= count($nozzles) ?></h5>
                        <p class="text-muted mb-0">Nozzles</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card card-hover border-0 shadow text-center">
                    <div class="card-body">
                        <i class="fas fa-history text-primary mb-2" style="font-size: 2rem;"></i>
                        <h5><?= count($recentCalculations) ?></h5>
                        <p class="text-muted mb-0">Recente Berekeningen</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>3D Print Calculator</h5>
                    <p class="mb-0">Professionele kostprijsberekening voor 2024</p>
                </div>
                <div class="col-md-6 text-md-end">
                    <p class="mb-0">
                        <i class="fas fa-code me-1"></i>
                        Gemaakt met ❤️ voor de 3D print community
                    </p>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Update range value displays
        function updateRangeValue(input, elementId) {
            document.getElementById(elementId).textContent = input.value;
        }
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html> 