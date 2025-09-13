# CybexDump - Enterprise Database Backup Solution

<div align="center">
    <img src="https://cybexsoft.com/img/logo.png" alt="Cybexsoft Logo" width="200"/>
    <h3>A Product by Cybexsoft Consultancy Services</h3>
    <p><a href="https://cybexsoft.com">cybexsoft.com</a></p>
</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](https://github.com/cybexsoft/cybexdump)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Quick Start

Install CybexDump with a single command:

```bash
curl https://raw.githubusercontent.com/cybexsoft/cybexdump/refs/heads/main/install.sh | bash
```

## 🎯 Features

- 🔄 **Multi-Database Support**
  - MySQL (Current)
  - PostgreSQL (Coming Soon)
  - MongoDB (Coming Soon)

- 📅 **Flexible Scheduling**
  - Hourly backups
  - Daily backups
  - Weekly backups
  - Custom scheduling

- 📬 **Notifications**
  - Email notifications
  - Backup status alerts
  - Error reporting

- 🔐 **Security**
  - Secure credential storage
  - Encrypted backups
  - Safe configuration management

- 🔄 **Easy Migration**
  - Backup/Restore functionality
  - Configuration export/import
  - Cross-server migration support

## 📋 Requirements

- Python 3.7 or higher
- Database clients (installed automatically)
- Linux, macOS, or WSL for Windows

## 💻 Usage

### Initial Setup
```bash
# Configure CybexDump
cybexdump configure
```

### Managing Backups
```bash
# Add a new database host
cybexdump add-host mysql

# List all configured backups
cybexdump list all

# Create backup
cybexdump backup -f /path/to/backup.sql

# Restore from backup
cybexdump restore /path/to/backup.sql
```

### Configuration Management
```bash
# Backup configuration
cybexdump backup --config-only

# Restore configuration
cybexdump restore config_backup.json --config-only

# Clean configuration
cybexdump clean
```

## 🔄 Updates

Keep CybexDump up to date:

```bash
curl https://cybexsoft.com/cybexdump/update.sh | bash
```

## 🗑️ Uninstallation

If needed, uninstall CybexDump:

```bash
curl https://cybexsoft.com/cybexdump/uninstall.sh | bash
```

## 📚 Documentation

For detailed documentation, visit:
[https://cybexsoft.com/docs/cybexdump](https://cybexsoft.com/docs/cybexdump)

## 🤝 Support

- **Community Support**: [GitHub Issues](https://github.com/cybexsoft/cybexdump/issues)
- **Professional Support**: [Contact Cybexsoft](https://cybexsoft.com/contact)
- **Email**: support@cybexsoft.com

## 🔧 Configuration

Configuration file location: `~/.cybexdump/config.json`

Example configuration:
```json
{
    "backup_location": "/path/to/backups",
    "notification": {
        "enabled": true,
        "email": "admin@example.com",
        "smtp_server": "smtp.example.com"
    },
    "databases": [
        {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "schedule": {
                "frequency": "daily",
                "time": "00:00"
            }
        }
    ]
}
```

## 🛣️ Roadmap

- [ ] PostgreSQL support
- [ ] MongoDB support
- [ ] Cloud storage integration (S3, GCS, Azure)
- [ ] Web interface
- [ ] Backup verification
- [ ] Compression options
- [ ] Real-time monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

## 📜 License

Copyright © 2025 [Cybexsoft Consultancy Services](https://cybexsoft.com)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Cybexsoft

[Cybexsoft Consultancy Services](https://cybexsoft.com) is a leading provider of enterprise software solutions. With years of experience in database management and system administration, we deliver robust and reliable tools for businesses of all sizes.

- 🌐 Website: [cybexsoft.com](https://cybexsoft.com)
- 📧 Email: contact@cybexsoft.com
- 📱 Phone: +1-XXX-XXX-XXXX
- 📍 Address: [Your Company Address]

---

<div align="center">
    <p>Made with ❤️ by <a href="https://cybexsoft.com">Cybexsoft Consultancy Services</a></p>
</div>
