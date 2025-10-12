# AI-assisted Clinical Forms Frontend

A Streamlit-based frontend application for AI-assisted clinical forms that helps doctors efficiently manage patient appointments through live transcription and AI-powered entity extraction.

## Features

- 🎙️ **Live Audio Recording**: Browser-based audio capture using WebRTC
- 🤖 **AI Entity Extraction**: Automatic detection of symptoms and medications from conversation
- 📋 **Dynamic Forms**: Real-time form updates during consultation
- 👥 **Patient Management**: Complete patient database and history
- 📊 **Form Archive**: Historical form access and management
- 🔧 **Backend Integration**: Fully integrated with FastAPI backend

## Project Structure

```
frontend/
├── app.py                          # Main entry point
├── pages/
│   ├── 1_📋_Main_Dashboard.py     # Patient list & cards
│   ├── 2_👤_Patient_Page.py       # Patient details & form archive
│   ├── 3_📝_New_Form.py           # Create form with decision support
│   └── 4_🎙️_Live_Form.py         # Live transcription + form filling
├── components/
│   ├── patient_card.py            # Reusable patient card
│   └── audio_recorder.py          # WebRTC audio component wrapper
├── services/
│   ├── api_client.py              # HTTP API client with backend integration
│   └── ai_extractor.py            # AI extraction logic
├── models/
│   └── domain.py                  # Pydantic models for entities
└── utils/
    ├── state.py                   # Session state management
    └── config.py                  # App configuration
```

## Quick Start

### Prerequisites

- Python 3.13+
- `uv` package manager (recommended) or `pip`
- Modern web browser with microphone access

### Installation & Launch

#### Option 1: Using `uv` (Recommended)

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

2. **Clone and setup**:
```bash
git clone <repository-url>
cd IBMZ-Datathon
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Run the application**:
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

- `BACKEND_API_URL`: Backend API service URL (default: `https://ibm-datathon-api-gateway.onrender.com`)
- `DEFAULT_DOCTOR_ID` / `DEFAULT_DOCTOR_NAME`: Default doctor for demo
- `ASR_MODEL`: Automatic Speech Recognition model (backend-controlled)
- `AI_AUTOFILL_ENABLED`: Enable AI autofill from microphone
- `MOCK_API`: Use mock API instead of real backend (default: `false`)
- `HTTP_TIMEOUT`: HTTP request timeout in seconds (default: `30`)
- `HTTP_RETRY_ATTEMPTS`: Number of retry attempts for failed requests (default: `3`)

## Usage Guide

### 1. Main Dashboard (`/`)
- **Patient Grid**: View all patients in a searchable 3-column grid
- **Search**: Use the sidebar to search patients by name or email
- **Create Patient**: Click "Add Patient" to create new patients
- **Navigation**: Click on patient cards to view details

### 2. Patient Page (`/patient/:id`)
- **Personal Data**: View patient information (name, email, DOB)
- **Form Archive**: List of all forms for the patient with status
- **New Form**: Create a new clinical form for the patient
- **Form Actions**: Open existing forms or delete them

### 3. New Form (`/new-form`)
- **AI Settings**: Configure AI autofill from microphone
- **Initial Notes**: Add pre-session observations
- **Start Session**: Begin live transcription and form filling

### 4. Live Form Session (`/live-form`)
- **Audio Controls**: Start/Pause/Stop/Reset recording
- **Live Transcript**: Real-time conversation display
- **Form Tabs**: 
  - **Symptoms**: Add and manage patient symptoms
  - **Medications**: Add and manage medications
  - **Summary**: Review and finalize the form
- **AI Integration**: Automatic entity extraction from conversation

## Backend Integration

### Overview

The frontend is fully integrated with the FastAPI backend at `https://ibm-datathon-api-gateway.onrender.com`. The integration handles:

- **Patient Management**: Full CRUD operations for patients
- **Doctor Management**: Full CRUD operations for doctors  
- **Form Submission**: Batch submission of complete forms with symptoms and medications
- **Error Handling**: Comprehensive error handling for network and API errors
- **Data Transformation**: Automatic conversion between frontend and backend data models

### Backend API Endpoints

The backend provides the following REST API endpoints:

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

### Data Model Differences

The frontend and backend use different data models that are automatically converted:

#### Field Mappings
- Frontend `name` ↔ Backend `full_name`
- Frontend `id` ↔ Backend `patient_id`/`doctor_id`
- Frontend `date_of_birth` ↔ Backend `dob`
- Frontend `duration`/`intensity` (strings) ↔ Backend (integers)
- Frontend `strength` (string) ↔ Backend (integer)

#### Additional Backend Fields
- `phone`: Patient/doctor phone number
- `sex_at_birth`: Patient's sex at birth
- `created_at`: Creation timestamp

#### Form Workflow
The backend uses a **single-submission model**:
1. Forms are created and managed in session state during consultation
2. Symptoms and medications are added incrementally in the UI
3. When "Submit Form" is clicked, all data is sent to the backend in one request
4. Forms cannot be retrieved or modified after submission (ensures data integrity)

### Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Connection timeouts, DNS failures
- **HTTP Errors**: 404 (Not Found), 422 (Validation Error), 500 (Server Error)
- **API Errors**: Custom `APIError` exception with status codes
- **Validation Errors**: Backend validation error display
- **Graceful Degradation**: Fallback to mock data when backend is unavailable

### Configuration

Set `MOCK_API=false` in your `.env` file to use the real backend:

```bash
BACKEND_API_URL=https://ibm-datathon-api-gateway.onrender.com
MOCK_API=false
HTTP_TIMEOUT=30
HTTP_RETRY_ATTEMPTS=3
```

### Authentication

The backend API does not require authentication - all endpoints are publicly accessible.

## Development

### Tech Stack

- **Streamlit**: Web framework for rapid UI development
- **streamlit-webrtc**: Browser-based audio capture
- **Pydantic**: Data validation and serialization
- **Python-dotenv**: Environment configuration
- **uv**: Fast Python package manager

### Running in Development Mode

1. **Enable debug mode**:
```bash
export DEBUG=true
```

2. **Use mock API** (default):
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

#### Testing Backend Integration

1. **Start with Mock Mode**:
   ```bash
   export MOCK_API=true
   streamlit run frontend/app.py
   ```

2. **Switch to Backend Mode**:
   ```bash
   export MOCK_API=false
   export BACKEND_API_URL=https://ibm-datathon-api-gateway.onrender.com
   streamlit run frontend/app.py
   ```

3. **Test Form Submission**:
   - Create a patient
   - Start a new form
   - Add symptoms and medications
   - Submit the form
   - Verify submission success message

## Troubleshooting

### Common Issues

1. **Audio not working**: Ensure browser microphone permissions are granted
2. **Import errors**: Make sure all dependencies are installed (`uv sync`)
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

## License

This project is part of the IBM Z Datathon.