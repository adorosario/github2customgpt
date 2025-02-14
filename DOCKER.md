# Docker Setup Guide

## Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Configure Streamlit:
   - Create `.streamlit/config.toml` with your AWS credentials
   - Ensure the config file is in the project root

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Open your browser
   - Navigate to `http://localhost:8501`

## Development

For development with live reload:
```bash
docker-compose up
```

## Troubleshooting

If you encounter permission issues:
```bash
sudo chown -R $USER:$USER .
```

If the container fails to start, check:
- Port 8501 is not in use
- Config file exists and is properly formatted
