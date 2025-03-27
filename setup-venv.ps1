# Get the current directory dynamically
$currentDir = Get-Location

# Convert the Windows path to a WSL-compatible path
$wslPath = $currentDir.Path -replace '\\', '/'  # Convert backslashes to forward slashes
$wslPath = "/mnt/c" + $wslPath.Substring(2)  # Convert the C: drive to /mnt/c

# Check if WSL is installed
$wslInstalled = wsl --list --verbose 2>&1
if ($wslInstalled -match "No installed distributions") {
    Write-Host "WSL is not installed. Installing Ubuntu..."
    wsl --install
    Write-Host "Please restart your computer to complete WSL installation."
    exit
} else {
    # Check if a default distro is set
    $defaultDistro = wsl --list --verbose | Select-String -Pattern "Default" | ForEach-Object { $_.Line.Trim() }
    if (-not $defaultDistro) {
        Write-Host "No default distribution set. Setting up Ubuntu as default..."
        wsl --set-default Ubuntu
    }

    # Check if Ubuntu is installed
    $ubuntuInstalled = wsl --list --verbose | Select-String "Ubuntu"
    if (-not $ubuntuInstalled) {
        Write-Host "Ubuntu distribution not found. Installing Ubuntu..."
        wsl --install -d Ubuntu
        Write-Host "Ubuntu installation is in progress, please wait..."
        exit
    }

    Write-Host "WSL is installed. Continuing with setup..."

    # Setting up Ubuntu environment in WSL
    Write-Host "Creating and setting up virtual environment in WSL..."

    # Use the converted WSL path for the project directory
    wsl bash -c "cd '$wslPath' && \
                 python3 -m venv .venv && \
                 source .venv/bin/activate && \
                 pip install -r requirements.txt"

    Write-Host "Ubuntu-based virtual environment has been set up successfully in WSL."
}
