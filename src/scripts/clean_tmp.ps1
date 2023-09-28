# Define the path to the tmp folder
$tmpFolderPath = (Get-Item -Path ".\tmp").FullName

# Check if the tmp folder exists
if (Test-Path -Path $tmpFolderPath -PathType Container) {
    # Get all files in the tmp folder
    $files = Get-ChildItem -Path $tmpFolderPath -File

    # Loop through each file and remove it
    foreach ($file in $files) {
        Remove-Item -Path $file.FullName -Force
        Write-Host "Removed $($file.FullName)"
    }

    Write-Host "All files in the tmp folder have been erased."
} else {
    Write-Host "The tmp folder does not exist at path: $tmpFolderPath"
}
