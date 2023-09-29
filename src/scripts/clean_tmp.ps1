# Define the path to the tmp folder
$tmpFolderPath = (Get-Item -Path ".\tmp").FullName

# Check if the tmp folder exists
if (Test-Path -Path $tmpFolderPath -PathType Container) {
    # Get all files in the tmp folder
    $files = Get-ChildItem -Path $tmpFolderPath -File | Where-Object { $_.Extension -eq ".py" -or $_.Extension -eq ".exe" }

    if ($files.Count -gt 0) {
        # Loop through each file and remove it
        foreach ($file in $files) {
            Remove-Item -Path $file.FullName -Force
            Write-Host "Removed $($file.FullName)"
        }
        Write-Host "All temporary files in the tmp folder have been erased."
    } else {
        Write-Host "No temporary files found in the tmp folder."
    }
} else {
    Write-Host "The tmp folder does not exist at path: $tmpFolderPath"
}
