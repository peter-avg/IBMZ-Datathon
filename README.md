# Hippocrates' Feather

**An AI-powered medical form filling system for the IBM Z Datathon**

## Overview

Hippocrates' Feather is an innovative AI-assisted clinical forms system designed to help medical professionals efficiently manage patient appointments. The system uses live transcription and AI-powered entity extraction to automatically fill medical forms during patient-doctor consultations, reducing administrative burden and allowing doctors to focus on patient care.

### Core Concept

The project addresses a critical challenge in modern healthcare: the time-consuming task of manually filling out medical forms during or after patient consultations. Hippocrates' Feather solves this by:

1. **Live Transcription**: Capturing real-time audio from patient-doctor appointments using browser-based WebRTC technology
2. **AI-Powered Extraction**: Automatically extracting medical entities (symptoms, medications, patient information) from the transcribed conversation
3. **Intelligent Form Filling**: Populating structured clinical forms with extracted information in real-time
4. **Seamless Integration**: Providing a complete patient management system with form archives and history

## Project Architecture

The system consists of three main components:

### 1. Frontend Application (`frontend/`)

A Streamlit-based web application that provides the user interface for doctors:

- **Live Audio Recording**: Browser-based audio capture using WebRTC
- **Real-time Transcription**: Live display of patient-doctor conversation
- **AI Entity Extraction**: Automatic detection of symptoms and medications from conversation
- **Dynamic Forms**: Real-time form updates during consultation
- **Patient Management**: Complete patient database with search and filtering
- **Form Archive**: Historical form access and management

**Key Technologies:**
- Streamlit for rapid UI development
- streamlit-webrtc for browser-based audio capture
- Pydantic for data validation
- Python-dotenv for configuration

### 2. Backend API Gateway (`API_Gateway/`)

A FastAPI-based REST API that handles data persistence and business logic:

- **Patient Management**: Full CRUD operations for patient records
- **Doctor Management**: Full CRUD operations for doctor records
- **Form Submission**: Batch submission of complete forms with symptoms and medications
- **Database Integration**: PostgreSQL database with async SQLAlchemy ORM

**Key Technologies:**
- FastAPI for REST API
- SQLAlchemy for database ORM
- PostgreSQL for data persistence
- Pydantic for request/response validation

### 3. AI Agent (`agent/`)

An intelligent agent that processes transcribed text and extracts medical information:

- **Intent Detection**: Identifies different types of information in conversation (PII, medications, symptoms)
- **Entity Extraction**: Extracts structured data from unstructured text
- **LLM Integration**: Uses OpenAI's API for intelligent extraction
- **Form Building**: Constructs structured patient forms from extracted entities
- **Recommendations**: Provides medical recommendations based on form data

**Key Technologies:**
- OpenAI API for LLM-powered extraction
- Instructor library for structured LLM outputs
- Custom prompt engineering for medical domain

## Features

### For Medical Professionals

- 🎙️ **Live Audio Recording**: Start recording directly in the browser during consultations
- 📝 **Real-time Transcription**: See the conversation transcribed as it happens
- 🤖 **AI Autofill**: Automatically extract symptoms and medications from conversation
- 📋 **Structured Forms**: Organised clinical forms with symptoms, medications, and notes
- 👥 **Patient Database**: Manage patient information and history
- 📊 **Form Archive**: Access and review historical consultations
- ✅ **Quick Review**: Review and edit AI-extracted information before submission

### Technical Features

- **Mock Mode**: Development mode with in-memory storage for testing
- **Backend Integration**: Full integration with FastAPI backend
- **Error Handling**: Comprehensive error handling for network and API errors
- **Data Transformation**: Automatic conversion between frontend and backend data models
- **Session Management**: State management for multi-page workflows
- **Responsive Design**: Works on desktop and tablet devices

## Project Structure

```
IBMZ-Datathon/
├── frontend/                    # Streamlit frontend application
│   ├── app.py                   # Main entry point
│   ├── pages/                   # Multi-page application
│   │   ├── 1_📋_Main_Dashboard.py
│   │   ├── 2_👤_Patient_Page.py
│   │   ├── 3_📝_New_Form.py
│   │   └── 4_🎙️_Live_Form.py
│   ├── components/              # Reusable UI components
│   ├── services/                # Business logic and API clients
│   ├── models/                  # Data models (Pydantic)
│   └── utils/                   # Utilities and configuration
├── API_Gateway/                 # FastAPI backend
│   └── api_gateway.py           # Main API server
├── agent/                       # AI agent for entity extraction
│   ├── form_agent/              # Form processing agent
│   ├── api_gateway.py           # Agent API endpoints
│   └── schemas.py               # Data schemas
├── db/                          # Database migrations and schemas
├── tests/                       # Test suite
├── pyproject.toml               # Python project configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Quick Start

### Prerequisites

- Python 3.13+
- `uv` package manager (recommended) or `pip`
- PostgreSQL database (for backend)
- Modern web browser with microphone access
- OpenAI API key (for AI agent)

### Installation

#### Option 1: Using `uv` (Recommended)

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

2. **Clone the repository**:
```bash
git clone <repository-url>
cd IBMZ-Datathon
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the frontend application**:
```bash
uv run streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
```

#### Option 2: Using pip

1. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -e .
```

3. **Run the application**:
```bash
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:8501
```

## Configuration

The application can be configured using environment variables (see `.env.example`):

### Frontend Configuration

- `BACKEND_API_URL`: Backend API service URL (default: `https://ibm-datathon-api-gateway.onrender.com`)
- `DEFAULT_DOCTOR_ID` / `DEFAULT_DOCTOR_NAME`: Default doctor for demo
- `ASR_MODEL`: Automatic Speech Recognition model (backend-controlled)
- `AI_AUTOFILL_ENABLED`: Enable AI autofill from microphone
- `MOCK_API`: Use mock API instead of real backend (default: `false`)
- `HTTP_TIMEOUT`: HTTP request timeout in seconds (default: `30`)
- `HTTP_RETRY_ATTEMPTS`: Number of retry attempts for failed requests (default: `3`)

### Backend Configuration

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI agent

## Usage Guide

### 1. Main Dashboard

- View all patients in a searchable grid
- Search patients by name or email
- Create new patients
- Navigate to patient details

### 2. Patient Page

- View patient personal information
- Access form archive with all historical forms
- Create new clinical forms
- Manage existing forms

### 3. New Form

- Configure AI autofill settings
- Add pre-session observations
- Start live transcription session

### 4. Live Form Session

- **Audio Controls**: Start/Pause/Stop/Reset recording
- **Live Transcript**: Real-time conversation display
- **Form Tabs**:
  - **Symptoms**: Add and manage patient symptoms
  - **Medications**: Add and manage medications
  - **Summary**: Review and finalise the form
- **AI Integration**: Automatic entity extraction from conversation
- **Submit**: Finalise and submit the form to the backend

## Backend Integration

The frontend is fully integrated with the FastAPI backend. The integration handles:

- **Patient Management**: Full CRUD operations for patients
- **Doctor Management**: Full CRUD operations for doctors
- **Form Submission**: Batch submission of complete forms with symptoms and medications
- **Error Handling**: Comprehensive error handling for network and API errors
- **Data Transformation**: Automatic conversion between frontend and backend data models

### Backend API Endpoints

#### Patient Management
- `GET /patients/` - List all patients
- `POST /patients/` - Create new patient
- `GET /patients/{patient_id}` - Get patient details
- `PATCH /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

#### Doctor Management
- `GET /doctors/` - List all doctors
- `POST /doctors/` - Create new doctor
- `GET /doctors/{doctor_id}` - Get doctor details
- `PATCH /doctors/{doctor_id}` - Update doctor
- `DELETE /doctors/{doctor_id}` - Delete doctor

#### Form Submission
- `POST /forms/` - Submit complete form with symptoms and medications

## Development

### Tech Stack

**Frontend:**
- Streamlit: Web framework for rapid UI development
- streamlit-webrtc: Browser-based audio capture
- Pydantic: Data validation and serialisation
- Python-dotenv: Environment configuration

**Backend:**
- FastAPI: Modern, fast web framework
- SQLAlchemy: Database ORM
- PostgreSQL: Relational database
- Pydantic: Request/response validation

**AI Agent:**
- OpenAI API: Large language model integration
- Instructor: Structured LLM outputs
- Custom prompt engineering

### Running in Development Mode

1. **Enable debug mode**:
```bash
export DEBUG=true
```

2. **Use mock API** (for frontend-only development):
```bash
export MOCK_API=true
```

3. **Run with auto-reload**:
```bash
streamlit run frontend/app.py --server.runOnSave true
```

### Testing

The application includes comprehensive testing capabilities:

- **Mock Mode**: Set `MOCK_API=true` to use in-memory mock data for development
- **Backend Integration**: Set `MOCK_API=false` to test with real backend API
- **Error Scenarios**: Test network failures, validation errors, and API errors
- **Data Validation**: Verify field type conversions and data transformations

## Troubleshooting

### Common Issues

1. **Audio not working**: Ensure browser microphone permissions are granted
2. **Import errors**: Make sure all dependencies are installed (`uv sync` or `pip install -e .`)
3. **Port conflicts**: Change the port with `--server.port 8502`
4. **Backend connection**: Check `BACKEND_API_URL` in your `.env` file
5. **API errors**: Check network connectivity and backend service status
6. **Form submission fails**: Ensure at least one symptom or medication is added
7. **Data not saving**: Check if `MOCK_API` is set correctly for your use case

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
streamlit run frontend/app.py --logger.level debug
```

## Project Goals

Hippocrates' Feather was developed for the IBM Z Datathon with the following objectives:

1. **Reduce Administrative Burden**: Automate the time-consuming task of filling medical forms
2. **Improve Accuracy**: Reduce human error in form transcription
3. **Enhance Patient Care**: Allow doctors to focus on patients rather than paperwork
4. **Real-time Processing**: Provide immediate feedback during consultations
5. **Scalable Solution**: Build a system that can handle multiple consultations simultaneously

## Future Enhancements

Potential improvements and extensions:

- Multi-language support for international use
- Integration with Electronic Health Records (EHR) systems
- Advanced AI models for better entity extraction
- Voice recognition for speaker identification
- Mobile app for on-the-go consultations
- Analytics dashboard for medical insights
- Export functionality for forms (PDF, JSON, etc.)

## License

This project is part of the IBM Z Datathon. All rights reserved.

## Contributors

Developed for the IBM Z Datathon by the Hippocrates' Feather team.

---

**Note**: This project is a demonstration system for the IBM Z Datathon. For production use, additional security measures, authentication, and compliance with healthcare regulations (such as HIPAA) would be required.
