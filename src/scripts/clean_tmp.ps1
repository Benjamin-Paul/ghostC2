# Define the path to the tmp folder
$tmpFolderPath = (Get-Item -Path ".\tmp").FullName

# Check if the tmp folder exists
if (Test-Path -Path $tmpFolderPath -PathType Container) {
    # Get all files in the tmp folder
    $files = Get-ChildItem -Path $tmpFolderPath -File -Filter "*.py"

    if ($pyFiles.Count -gt 0) {
        # Loop through each file and remove it
        foreach ($file in $files) {
            Remove-Item -Path $file.FullName -Force
            Write-Host "Removed $($file.FullName)"
        }
        Write-Host "All .py files in the tmp folder have been erased."
    } else {
        Write-Host "No .py files found in the tmp folder."
    }
} else {
    Write-Host "The tmp folder does not exist at path: $tmpFolderPath"
}
