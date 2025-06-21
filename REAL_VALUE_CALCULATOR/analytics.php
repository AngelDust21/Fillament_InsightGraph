<?php
/**
 * Analytics Dashboard - Data Analyse van alle berekeningen
 * Toont wat mensen berekenen voor business insights
 */

// Include alle benodigde classes
require_once 'includes/Database.php';
require_once 'includes/Material.php';
require_once 'includes/Printer.php';
require_once 'includes/Nozzle.php';
require_once 'includes/Calculator.php';

// Initialize classes
$calculator = new Calculator();

// Haal statistieken op
$stats = $calculator->getCalculationStats();
$recentCalculations = $calculator->getRecentCalculationsWithDetails(50);

// Export functionaliteit
if (isset($_POST['export'])) {
    $calculations = $calculator->getRecentCalculationsWithDetails(1000);
    $filepath = $calculator->exportCalculationsToCSV($calculations);
    $downloadUrl = 'exports/' . basename($filepath);
}
?>

<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analyse - 3D Print Calculator</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
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
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
    </style>
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg gradient-bg navbar-dark">
        <div class="container">
            <a class="navbar-brand fw-bold" href="index.php">
                <i class="fas fa-calculator me-2"></i>
                3D Print Calculator
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="index.php">
                            <i class="fas fa-calculator me-1"></i>Calculator
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="analytics.php">
                            <i class="fas fa-chart-bar me-1"></i>Data Analyse
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="container py-5">
        <!-- Header -->
        <div class="row mb-5">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold text-dark mb-3">
                    <i class="fas fa-chart-bar me-3"></i>
                    Data Analyse Dashboard
                </h1>
                <p class="lead text-muted mb-4">
                    Inzichten uit <?= number_format($stats['total_calculations']) ?> berekeningen. 
                    Ontdek wat mensen het meest berekenen en ontwikkel betere strategieën.
                </p>
            </div>
            <div class="col-lg-4 text-end">
                <form method="POST" class="d-inline">
                    <button type="submit" name="export" class="btn btn-success btn-lg">
                        <i class="fas fa-download me-2"></i>Export Data
                    </button>
                </form>
                <?php if (isset($downloadUrl)): ?>
                <div class="mt-2">
                    <a href="<?= $downloadUrl ?>" class="btn btn-outline-success btn-sm">
                        <i class="fas fa-file-csv me-1"></i>Download CSV
                    </a>
                </div>
                <?php endif; ?>
            </div>
        </div>

        <!-- Key Statistics -->
        <div class="row mb-5">
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number"><?= number_format($stats['total_calculations']) ?></div>
                    <div class="stat-label">Totaal Berekeningen</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">€<?= number_format($stats['cost_analysis']['avg_total_cost'], 2) ?></div>
                    <div class="stat-label">Gem. Kosten per Print</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number">€<?= number_format($stats['cost_analysis']['avg_selling_price'], 2) ?></div>
                    <div class="stat-label">Gem. Verkoopprijs</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-number"><?= number_format($stats['cost_analysis']['avg_roi'], 1) ?>%</div>
                    <div class="stat-label">Gem. ROI</div>
                </div>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="row mb-5">
            <div class="col-lg-6">
                <div class="card card-hover border-0 shadow">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-cube me-2"></i>
                            Meest Gebruikte Materialen
                        </h5>
                    </div>
                    <div class="card-body">
                        <canvas id="materialsChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="card card-hover border-0 shadow">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-weight me-2"></i>
                            Gewicht Distributie
                        </h5>
                    </div>
                    <div class="card-body">
                        <canvas id="weightChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Popular Materials Table -->
        <div class="row mb-5">
            <div class="col-12">
                <div class="card card-hover border-0 shadow">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-list me-2"></i>
                            Top 10 Meest Gebruikte Materialen
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-hover">
                                <thead>
                                    <tr>
                                        <th>Positie</th>
                                        <th>Materiaal</th>
                                        <th>Type</th>
                                        <th>Aantal Gebruikt</th>
                                        <th>Gem. Kosten</th>
                                        <th>Marktaandeel</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($stats['popular_materials'] as $index => $material): ?>
                                    <tr>
                                        <td><span class="badge bg-primary">#<?= $index + 1 ?></span></td>
                                        <td><strong><?= htmlspecialchars($material['brand'] . ' ' . $material['name']) ?></strong></td>
                                        <td><span class="badge bg-secondary"><?= htmlspecialchars($material['type']) ?></span></td>
                                        <td><?= number_format($material['usage_count']) ?></td>
                                        <td>€<?= number_format($material['avg_cost'], 2) ?></td>
                                        <td><?= number_format(($material['usage_count'] / $stats['total_calculations']) * 100, 1) ?>%</td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Calculations -->
        <div class="row mb-5">
            <div class="col-12">
                <div class="card card-hover border-0 shadow">
                    <div class="card-header bg-warning text-dark">
                        <h5 class="mb-0">
                            <i class="fas fa-history me-2"></i>
                            Recente Berekeningen (Laatste 50)
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-sm table-hover">
                                <thead>
                                    <tr>
                                        <th>Datum</th>
                                        <th>Materiaal</th>
                                        <th>Printer</th>
                                        <th>Gewicht</th>
                                        <th>Tijd</th>
                                        <th>Kosten</th>
                                        <th>Verkoopprijs</th>
                                        <th>Winst</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($recentCalculations as $calc): ?>
                                    <tr>
                                        <td><?= date('d-m H:i', strtotime($calc['created_at'])) ?></td>
                                        <td>
                                            <small><?= htmlspecialchars($calc['material_brand']) ?></small><br>
                                            <strong><?= htmlspecialchars($calc['material_name']) ?></strong>
                                        </td>
                                        <td>
                                            <small><?= htmlspecialchars($calc['printer_brand']) ?></small><br>
                                            <strong><?= htmlspecialchars($calc['printer_name']) ?></strong>
                                        </td>
                                        <td><?= number_format($calc['weight_grams']) ?>g</td>
                                        <td><?= number_format($calc['print_hours'], 1) ?>u</td>
                                        <td>€<?= number_format($calc['total_cost'], 2) ?></td>
                                        <td>€<?= number_format($calc['selling_price'], 2) ?></td>
                                        <td>
                                            <span class="badge <?= $calc['profit'] > 0 ? 'bg-success' : 'bg-danger' ?>">
                                                €<?= number_format($calc['profit'], 2) ?>
                                            </span>
                                        </td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Charts -->
    <script>
        // Materials Chart
        const materialsCtx = document.getElementById('materialsChart').getContext('2d');
        new Chart(materialsCtx, {
            type: 'doughnut',
            data: {
                labels: <?= json_encode(array_map(function($m) { return $m['brand'] . ' ' . $m['name']; }, array_slice($stats['popular_materials'], 0, 5))) ?>,
                datasets: [{
                    data: <?= json_encode(array_map(function($m) { return $m['usage_count']; }, array_slice($stats['popular_materials'], 0, 5))) ?>,
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#f5576c',
                        '#4facfe'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Weight Distribution Chart
        const weightCtx = document.getElementById('weightChart').getContext('2d');
        new Chart(weightCtx, {
            type: 'bar',
            data: {
                labels: <?= json_encode(array_map(function($w) { return $w['weight_category']; }, $stats['weight_distribution'])) ?>,
                datasets: [{
                    label: 'Aantal Prints',
                    data: <?= json_encode(array_map(function($w) { return $w['count']; }, $stats['weight_distribution'])) ?>,
                    backgroundColor: '#10b981'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html> 