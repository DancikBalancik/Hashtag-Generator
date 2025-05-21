# Hashtag Generator Web App

This project uses a Python Flask backend and a React (Material UI) frontend.

![License](https://img.shields.io/badge/License-MIT-blue.svg)

![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![Version](https://img.shields.io/badge/Version-0.1.1-orange.svg)

<img src="assets/images/logo.png" alt="Hashtag Generator Logo" style="width: 200px; height: 200px;"/>

## Project Overview

The Hashtag Generator is an open-source application that transforms user input into hashtag-formatted text. It provides a clean, intuitive interface with customization options, file handling capabilities, and a history tracking system. Available in both backend and frontend versions, the application is designed to be cross-platform, extensible, and community-driven.

## Structure

- `src/backend/` — Flask API (hashtag logic, AI providers)
- `src/frontend/` — React app (modern UI, tabs, connects to backend)

## Features

- **Hashtag Generator**: Convert text to properly formatted hashtags
- **AI Hashtag Tab**: Generate hashtags using AI providers (OpenAI, Anthropic, Azure)
- **Settings & History**: Customize and track your hashtag generation

## API Key Storage

API keys for LLM providers are stored **only in your browser's localStorage** (see `src/frontend/README_API_KEYS.md`). They are never written to disk or sent to the backend server.

## Installation

### Backend

```bash
cd src/backend
pip install -r requirements.txt
python app.py
```

```powershell
cd src/backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd src/frontend
npm install
npm start
```

```powershell
cd src/frontend
npm install
npm start
```

## App Icon

The app icon is located at `src/frontend/public/app_icon.png` and is used for the PWA/Electron app manifest.

## Requirements

- Python requirements: `src/backend/requirements.txt`
- Node/React requirements: `src/frontend/package.json`

## Basic Usage

1. Start the backend server using Flask
2. Start the frontend React application
3. Use the modern UI to generate and manage hashtags

## Advanced Features

### Customization Options

- **Remove Special Characters**: Strip non-alphanumeric characters
- **Capitalization**: Control how words are capitalized (first letter, all caps, etc.)
- **Character Limits**: Set warnings for platform-specific constraints

### File Operations

- **Import**: Load text from files to convert to hashtags
- **Export**: Save generated hashtags to various file formats
- **Batch Processing**: Convert multiple text inputs at once (Coming Soon)

### Collections and Templates (Coming Soon)

- Save groups of related hashtags
- Create templates for different contexts
- Apply consistent formatting to groups of hashtags

## Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

### Development Setup

```bash
# Backend
cd src/backend
python -m venv venv
source venv/bin/activate  # On Linux and MacOS
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Frontend
cd src/frontend
npm install
```

> Please update any dependencies if changes are made

## Project Roadmap

View our full [Development Roadmap](ROADMAP.md) to see what's planned for future releases.

## Cleaning Up

Old CLI and GUI code is deprecated and can be removed.

## Support Me

<a href='https://ko-fi.com/R6R51CIYSP' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi6.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: For bug reports and feature requests
- Discussions: For questions and community support
