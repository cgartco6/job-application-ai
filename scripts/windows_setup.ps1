# Windows Setup Script
Write-Host "Installing Chocolatey..."
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

Write-Host "Installing Docker, Node.js, Python..."
choco install -y docker-desktop nodejs python

Write-Host "Cloning repository..."
git clone https://github.com/yourrepo/job-application-ai.git
cd job-application-ai

# Start Docker
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Write-Host "Building Docker containers..."
docker-compose up -d --build

Write-Host "Setup complete. Access at http://localhost:3000"
