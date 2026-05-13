#!/bin/bash
# Script to install Docker on Raspberry Pi, run Ollama and OpenWebUI containers, pull gemma4:e2b model, and set up xrdp for remote desktop

set -euo pipefail

echo "=== Docker + Ollama + OpenWebUI + xrdp Setup for Raspberry Pi ==="

# Check if running as root (docker install needs root)
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo or as root."
    echo "Please run: sudo $0"
    exit 1
fi

# Determine architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"
if [[ "$ARCH" == "armv7l" || "$ARCH" == "armv6l" ]]; then
    DOCKER_PLATFORM="linux/arm/v7"
elif [[ "$ARCH" == "aarch64" ]]; then
    DOCKER_PLATFORM="linux/arm64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# Update package list
echo "Updating package list..."
apt-get update -y

# Install prerequisites
echo "Installing prerequisites (curl, gnupg, lsb-release)..."
apt-get install -y curl gnupg lsb-release

# Install Docker using the official convenience script
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Enable and start Docker service
systemctl enable docker
systemctl start docker

# Add the current user (the one who invoked sudo) to the docker group
if [[ -n "${SUDO_USER:-}" ]]; then
    USERNAME="$SUDO_USER"
else
    USERNAME=$(logname 2>/dev/null || echo "$USER")
fi
echo "Adding user '$USERNAME' to the docker group..."
usermod -aG docker "$USERNAME"

echo "Docker installation complete. Please log out and log back in (or restart) for group changes to take effect."
echo "Alternatively, you can run 'newgrp docker' to apply the group change in this session."

# Wait a moment for Docker to be fully ready
sleep 5

# Install xrdp and a lightweight desktop environment (xfce4) for remote desktop
echo "Installing xrdp and Xfce desktop environment..."
apt-get install -y xrdp xfce4 xfce4-goodies

# Configure xrdp to use Xfce session
echo "xfce4-session" > /etc/skel/.xsession
# Also set for existing users (including pi and the sudo user)
for user_home in /home/* /root; do
    if [[ -d "$user_home" ]]; then
        echo "xfce4-session" > "$user_home/.xsession"
        chown "$(stat -c '%U:%G' "$user_home")" "$user_home/.xsession"
    fi
done

# Enable and start xrdp service
systemctl enable xrdp
systemctl start xrdp

# Optionally, adjust the sesman.ini to allow any user (default is fine)
# Ensure the firewall allows port 3389 if needed (optional)
# ufw allow 3389/tcp  # Uncomment if ufw is active

echo "xrdp installed and configured. You can now connect via Remote Desktop Protocol (RDP) to the Pi's IP address."

# Pull and run Ollama container
#docker network create openllama
echo "Pulling Ollama Docker image (platform: $DOCKER_PLATFORM)..."
docker pull --platform "$DOCKER_PLATFORM" ollama/ollama:latest

echo "Starting Ollama container..."
docker run -d --name ollama \
    --restart unless-stopped \
    -p 11434:11434 \
    -v ollama:/root/.ollama \
    ollama/ollama:latest

# Wait for Ollama to be ready (simple sleep; could be improved with health check)
echo "Waiting for Ollama to start..."
sleep 10

# Pull the gemma4:e2b model via Ollama inside the container
echo "Pulling model 'granite4:350m' (this may take a while)..."
docker exec ollama ollama pull granite4:350m

# Pull and run OpenWebUI container
echo "Pulling OpenWebUI Docker image..."
docker pull --platform "$DOCKER_PLATFORM" ghcr.io/open-webui/open-webui:main

echo "Starting OpenWebUI container..."
docker run -d --name open-webui \
    --restart unless-stopped \
    -p 3000:8080 \
    -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
    -e ENABLE_RAG_EMBEDDING=true \
    -e ENABLE_RAG_WEB_LOADER=true \
    -v open-webui:/app/backend/data \
    ghcr.io/open-webui/open-webui:main


echo "Pulling n8n Docker image..."
docker pull --platform "$DOCKER_PLATFORM" n8nio/n8n:latest


echo "=== Setup Complete ==="
echo "Ollama API is available at: http://localhost:11434"
echo "OpenWebUI is available at: http://localhost:3000"
echo "Remote Desktop (xrdp) is available on port 3389 of the Pi's IP address."
echo ""
echo "Note: If you are accessing from another device, replace localhost with the Raspberry Pi's IP address."
echo "The model 'gemma4:e2b' has been downloaded into the Ollama container."
echo ""
echo "To stop containers later:"
echo "  docker stop ollama open-webui"
echo "To remove containers:"
echo "  docker rm -f ollama open-webui"
echo ""
echo "Remember to log out and back in (or run 'newgrp docker') to use Docker without sudo."
echo ""
echo "To connect via RDP, use a client like Microsoft Remote Desktop, Remmina, or xfreerdp:"
echo "  xfreerdp /v:<Pi-IP> /u:pi /p:raspberry"
echo " (default username/password for Raspberry Pi OS are pi/raspberry unless changed)"
