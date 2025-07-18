$tickersFile = "tickers.txt"
$pythonScript = "gather.py"

# Read tickers and pipe each to Python
Get-Content $tickersFile | ForEach-Object {
    $etf = $_.Trim()

    if (![string]::IsNullOrWhiteSpace($etf)) {
        Write-Host "Processing ticker: $etf"

        # Pipe the ticker into the Python script
        $etf | python $pythonScript

        Write-Host "Done with $etf"
        Write-Host "=============================="
    }
}