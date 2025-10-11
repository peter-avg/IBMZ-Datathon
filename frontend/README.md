# AI-assisted Clinical Forms Frontend

A Streamlit-based frontend application for AI-assisted clinical forms that helps doctors efficiently manage patient appointments through live transcription and AI-powered entity extraction.

## Features

- 🎙️ **Live Audio Recording**: Browser-based audio capture using WebRTC
- 🤖 **AI Entity Extraction**: Automatic detection of symptoms and medications from conversation
- 📋 **Dynamic Forms**: Real-time form updates during consultation
- 👥 **Patient Management**: Complete patient database and history
- 📊 **Form Archive**: Historical form access and management

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

## Installation

1. Install dependencies:
```bash
pip install -e .
```

2. Copy environment configuration:
```bash
cp .env.example .env
```

3. Run the application:
```bash
streamlit run frontend/app.py
```

## Configuration

The application can be configured using environment variables (see `.env.example`):

- `BACKEND_API_URL`: Backend API service URL
- `DEFAULT_DOCTOR_ID` / `DEFAULT_DOCTOR_NAME`: Default doctor for demo
- `ASR_MODEL`: Automatic Speech Recognition model
- `AI_AUTOFILL_ENABLED`: Enable AI autofill from microphone
- `MOCK_API`: Use mock API instead of real backend

## Usage

### 1. Main Dashboard
- View all patients in a searchable grid
- Create new patients
- Navigate to patient details

### 2. Patient Page
- View patient personal information
- Access form archive
- Create new forms

### 3. New Form
- Configure AI settings
- Add initial notes
- Start live session

### 4. Live Form Session
- Record audio with browser microphone
- View live transcript
- Add symptoms and medications manually or via AI extraction
- Save draft or finalize form

## AI Integration

The application includes placeholder AI extraction logic that can be replaced with real backend integration:

- **Audio Processing**: Send audio chunks to backend WebSocket endpoint
- **Entity Extraction**: Call backend API for symptom/medication extraction
- **Real-time Updates**: WebSocket connection for live transcript updates

## Backend Integration Points

1. **API Client** (`services/api_client.py`): Replace mock methods with HTTP calls
2. **Audio Stream** (`components/audio_recorder.py`): Send audio to backend WebSocket
3. **AI Extraction** (`services/ai_extractor.py`): Call backend AI service
4. **Environment Variables**: Configure backend URL and settings

## Development

The application uses:
- **Streamlit**: Web framework
- **streamlit-webrtc**: Browser audio capture
- **Pydantic**: Data validation and models
- **Python-dotenv**: Environment configuration

## Demo Data

The application includes mock data for demonstration:
- Default doctor: "Dr. Demo" (ID: D001)
- Sample patients can be created through the UI
- Forms, symptoms, and medications are stored in memory

## License

This project is part of the IBM Z Datathon.
