#!/bin/bash

# Update and install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv docker.io docker-compose tesseract-ocr

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# Install Node.js (for frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Clone repository (replace with your repo)
git clone https://github.com/yourrepo/job-application-ai.git
cd job-application-ai

# Set up virtual environment for backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up frontend
cd ../frontend
npm install

# Build and start containers
cd ..
docker-compose up -d --build

echo "Setup complete. Access at http://localhost:3000"
