# AI-assisted Clinical Forms Frontend

A Streamlit-based frontend application for AI-assisted clinical forms that helps doctors efficiently manage patient appointments through live transcription and AI-powered entity extraction.

## Features

- 🎙️ **Live Audio Recording**: Browser-based audio capture using WebRTC
- 🤖 **AI Entity Extraction**: Automatic detection of symptoms and medications from conversation
- 📋 **Dynamic Forms**: Real-time form updates during consultation
- 👥 **Patient Management**: Complete patient database and history
- 📊 **Form Archive**: Historical form access and management
- 🔧 **Backend Integration Ready**: Designed for easy backend connection

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
│   ├── api_client.py              # Mock API client (backend integration point)
│   └── ai_extractor.py            # Placeholder AI extraction logic
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

- `BACKEND_API_URL`: Backend API service URL (default: `http://localhost:8000`)
- `DEFAULT_DOCTOR_ID` / `DEFAULT_DOCTOR_NAME`: Default doctor for demo
- `ASR_MODEL`: Automatic Speech Recognition model (backend-controlled)
- `AI_AUTOFILL_ENABLED`: Enable AI autofill from microphone
- `MOCK_API`: Use mock API instead of real backend (default: `true`)

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

The frontend is designed to be easily integrated with a backend API. All backend communication is abstracted through the `services/api_client.py` module.

### Integration Steps

#### 1. Update API Client

Replace the mock implementation in `services/api_client.py` with real HTTP calls:

```python
# Example: Replace mock methods with HTTP calls
def create_patient(self, request: CreatePatientRequest) -> Patient:
    response = requests.post(f"{config.BACKEND_API_URL}/patients", json=request.dict())
    response.raise_for_status()
    return Patient(**response.json())
```

#### 2. Configure Backend URL

Update your `.env` file:
```bash
BACKEND_API_URL=http://your-backend-server:8000
MOCK_API=false
```

#### 3. Audio Streaming Integration

For real-time audio processing, integrate with your backend WebSocket:

```python
# In components/audio_recorder.py
def on_audio_frame(self, audio_frame):
    # Send audio frame to backend WebSocket
    websocket.send(audio_frame.to_ndarray())
```

#### 4. AI Extraction Integration

Replace the placeholder AI extraction in `services/ai_extractor.py`:

```python
def extract_entities(self, text: str) -> ExtractionResult:
    # Call your backend AI service
    response = requests.post(f"{config.BACKEND_API_URL}/ai/extract", 
                           json={"text": text})
    return ExtractionResult(**response.json())
```

### Required Backend Endpoints

The backend should implement these REST API endpoints:

#### Patient Management
- `GET /patients` - List patients (with optional search)
- `POST /patients` - Create new patient
- `GET /patients/{id}` - Get patient details
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient

#### Form Management
- `GET /forms` - List forms (with optional patient filter)
- `POST /forms` - Create new form
- `GET /forms/{id}` - Get form details
- `PUT /forms/{id}` - Update form
- `DELETE /forms/{id}` - Delete form

#### Symptoms & Medications
- `GET /symptoms` - List symptoms (with optional form filter)
- `POST /symptoms` - Create new symptom
- `PUT /symptoms/{id}` - Update symptom
- `DELETE /symptoms/{id}` - Delete symptom

- `GET /medications` - List medications (with optional form filter)
- `POST /medications` - Create new medication
- `PUT /medications/{id}` - Update medication
- `DELETE /medications/{id}` - Delete medication

#### AI Services
- `POST /ai/extract` - Extract entities from text
- `WebSocket /ws/audio` - Real-time audio streaming

### Data Models

The frontend uses Pydantic models defined in `models/domain.py`. Ensure your backend API returns data in the same format:

```python
# Example Patient model
{
    "id": "string",
    "name": "string", 
    "email": "string (optional)",
    "date_of_birth": "date (optional)"
}
```

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

The application includes mock data for testing:
- Default doctor: "Dr. Demo" (ID: D001)
- Create test patients through the UI
- All data is stored in memory (resets on restart)

## Troubleshooting

### Common Issues

1. **Audio not working**: Ensure browser microphone permissions are granted
2. **Import errors**: Make sure all dependencies are installed (`uv sync`)
3. **Port conflicts**: Change the port with `--server.port 8502`
4. **Backend connection**: Check `BACKEND_API_URL` in your `.env` file

### Debug Mode

Enable debug logging:
```bash
export DEBUG=true
streamlit run frontend/app.py --logger.level debug
```

## License

This project is part of the IBM Z Datathon.