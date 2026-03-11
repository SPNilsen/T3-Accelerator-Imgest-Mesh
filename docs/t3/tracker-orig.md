<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Status Tracker</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="/css/extra.css"> <!-- Correct CSS path -->
</head>


<div class="status-tracker">
    <div class="status-step current">
        <div class="status-icon">
            <i class="fas fa-lightbulb"></i> <!-- Font Awesome check mark for completed -->
        </div>
        <p>Business Understanding</p>
    </div>

    <div class="status-step remaining">
        <div class="status-icon">
            <i class="fas fa-database"></i> <!-- Font Awesome check mark for completed -->
        </div>
        <p>Data Understanding</p>
    </div>

    <div class="status-step remaining">
        <div class="status-icon">
            <i class="fas fa-cogs"></i> <!-- Font Awesome check mark for completed -->
        </div>
        <p>Data Preparation</p>
    </div>

    <div class="status-step remaining">
        <div class="status-icon">
            <i class="fas fa-chart-line"></i> <!-- Font Awesome icon for configuration -->
        </div>
        <p>Modeling</p>
    </div>

    <div class="status-step remaining">
        <div class="status-icon">
            <i class="fas fa-check-circle"></i> <!-- Font Awesome hammer for build -->
        </div>
        <p>Evaluation</p>
    </div>

    <div class="status-step remaining">
        <div class="status-icon">
            <i class="fas fa-rocket"></i> <!-- Font Awesome flag for delivery & closeout -->
        </div>
        <p>Deployment</p>
    </div>

    <!-- Line connecting the icons -->
    <div class="status-line"></div>
</div>
