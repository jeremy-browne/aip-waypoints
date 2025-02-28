Set-Location "$PSScriptRoot"

# Get all .kml files
$kmlFiles = Get-ChildItem -Filter *.kml

foreach ($kmlFile in $kmlFiles) {
    # Load the KML content as XML
    [xml]$doc = Get-Content -Path $kmlFile.FullName
    
    # Save the XML back to the same file, overwriting it
    $doc.Save($kmlFile.FullName)
    
    Write-Host "Overwrote $($kmlFile.Name) with pretty-printed XML"
}
