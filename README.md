# 🚀 NiceGUI Interactive Showcase

A modern, feature-rich web application built with NiceGUI that demonstrates real-time interactivity, professional UI components, and production-ready architecture.

## ✨ Features

- **🎨 Modern UI Components**: Beautiful, responsive interface with smooth animations
- **⚡ Real-time Updates**: Live data synchronization without page refreshes
- **📊 Interactive Charts**: Dynamic data visualization with Plotly integration
- **🌐 API Integration**: External API calls with proper error handling
- **📱 Responsive Design**: Mobile-first design that works on all devices
- **🔒 Production Ready**: Security best practices and error handling
- **🐳 Docker Support**: Containerized deployment with health checks
- **☁️ Cloud Deployment**: Ready for Fly.io deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd nicegui-showcase
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Open your browser**:
   Navigate to `http://localhost:8000`

### Environment Configuration

Create a `.env` file in the root directory:

```env
PORT=8000
HOST=0.0.0.0
DEBUG=false
APP_NAME=NiceGUI Showcase
APP_VERSION=1.0.0
```

## 🐳 Docker Deployment

### Build and run with Docker:

```bash
# Build the image
docker build -t nicegui-showcase .

# Run the container
docker run -p 8000:8000 nicegui-showcase
```

### Docker Compose (optional):

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - HOST=0.0.0.0
    restart: unless-stopped
```

## ☁️ Cloud Deployment (Fly.io)

### Deploy to Fly.io:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly.io**:
   ```bash
   fly auth login
   ```

3. **Deploy the application**:
   ```bash
   fly deploy
   ```

4. **Open the deployed app**:
   ```bash
   fly open
   ```

### Fly.io Configuration

The `fly.toml` file is pre-configured with:
- Health checks on `/health` endpoint
- Auto-scaling based on traffic
- 512MB memory allocation
- HTTPS enforcement

## 📁 Project Structure

```
nicegui-showcase/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── dockerfile             # Container configuration
├── fly.toml               # Fly.io deployment config
├── .env                   # Environment variables
├── README.md              # This file
├── app/
│   ├── __init__.py
│   ├── main.py            # UI pages and components
│   └── config.py          # Application configuration
├── core/
│   ├── __init__.py
│   └── utils.py           # Utility functions
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic data models
├── services/
│   ├── __init__.py
│   └── business.py        # Business logic services
└── static/
    ├── css/
    │   └── custom.css     # Custom styling
    └── js/
        └── utils.js       # Client-side utilities
```

## 🎯 Key Components

### Interactive Features

- **Real-time Counter**: Demonstrates state management and UI updates
- **Live Charts**: Dynamic data visualization with Plotly
- **Form Validation**: Client and server-side validation
- **API Integration**: External API calls with error handling
- **File Upload**: Secure file handling with validation
- **Theme Switching**: Dynamic UI theming

### Technical Features

- **Type Safety**: Comprehensive Pydantic models
- **Error Handling**: Graceful error management and user feedback
- **Async Operations**: Non-blocking API calls and data processing
- **Caching**: Intelligent data caching with TTL
- **Health Monitoring**: Built-in health checks and status monitoring
- **Security**: Input validation and secure headers

## 🔧 Development

### Code Quality

The project follows Python best practices:
- Type hints throughout the codebase
- Pydantic models for data validation
- Structured logging
- Error handling with user feedback
- Modular architecture

### Testing

Run tests (when implemented):
```bash
python -m pytest tests/
```

### Code Formatting

Format code with black:
```bash
black .
```

## 📊 Monitoring

### Health Check

The application provides a health check endpoint:
- **URL**: `/health`
- **Method**: GET
- **Response**: JSON with status and uptime

### Logging

Structured logging is configured for:
- Application events
- Error tracking
- Performance monitoring
- API call logging

## 🔒 Security

Security features implemented:
- Input validation with Pydantic
- XSS prevention
- Secure HTTP headers
- Error message sanitization
- File upload restrictions

## 🚀 Performance

Performance optimizations:
- Async/await patterns for non-blocking operations
- Intelligent caching with TTL
- Lazy loading of components
- Optimized Docker image layers
- CDN-ready static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs: `docker logs <container-id>`
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Check the health endpoint: `/health`

For deployment issues on Fly.io:
```bash
fly logs
fly status
```

## 🎉 Demo

Visit the live demo: [Your Deployed URL]

### Demo Features:
- Interactive dashboard with real-time updates
- Dynamic chart generation
- Form validation examples
- API integration demonstrations
- Mobile-responsive design showcase

---

Built with ❤️ using [NiceGUI](https://nicegui.io/) - The Python web framework that makes building web apps a joy!