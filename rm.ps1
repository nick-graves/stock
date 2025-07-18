Write-Host "Removing temporary and output files..."

$filesToRemove = @(
    "data/output_summary.txt",
    "data/top_holdings.csv",
    "data/stock_fundamentals.csv"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
    }
}

# Remove all PDF files from the report folder
$reportFiles = Get-ChildItem -Path "report" -Filter "*.pdf" -File -ErrorAction SilentlyContinue
foreach ($file in $reportFiles) {
    Remove-Item $file.FullName -Force
}