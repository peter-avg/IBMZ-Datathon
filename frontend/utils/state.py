"""Session state management utilities for Streamlit."""

import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime
from models.domain import Doctor, Patient, Form, FormStatus
from utils.config import config


def initialize_session_state():
    """Initialize default session state values."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        
        # Current user context
        st.session_state.current_doctor = Doctor(
            id=config.DEFAULT_DOCTOR_ID,
            name=config.DEFAULT_DOCTOR_NAME
        )
        
        # Current patient context
        st.session_state.current_patient = None
        st.session_state.current_form = None
        
        # Live transcription state
        st.session_state.live_session = {
            "mic_status": "stopped",
            "transcript_stream": [],
            "avg_latency_ms": 0,
            "is_recording": False,
            "last_transcript_update": None
        }
        
        # AI settings
        st.session_state.ai_settings = {
            "autofill_enabled": config.AI_AUTOFILL_ENABLED,
            "asr_model": config.ASR_MODEL
        }
        
        # UI state
        st.session_state.show_create_patient_modal = False
        st.session_state.patient_search_query = ""
        
        # Form state
        st.session_state.form_tabs = {
            "active_tab": "symptoms",
            "symptoms_count": 0,
            "medications_count": 0
        }


def get_current_doctor() -> Doctor:
    """Get the current doctor from session state."""
    return st.session_state.get("current_doctor", Doctor(
        id=config.DEFAULT_DOCTOR_ID,
        name=config.DEFAULT_DOCTOR_NAME
    ))


def set_current_doctor(doctor: Doctor):
    """Set the current doctor in session state."""
    st.session_state.current_doctor = doctor


def get_current_patient() -> Optional[Patient]:
    """Get the current patient from session state."""
    return st.session_state.get("current_patient")


def set_current_patient(patient: Optional[Patient]):
    """Set the current patient in session state."""
    st.session_state.current_patient = patient


def get_current_form() -> Optional[Form]:
    """Get the current form from session state."""
    return st.session_state.get("current_form")


def set_current_form(form: Optional[Form]):
    """Set the current form in session state."""
    st.session_state.current_form = form


def get_live_session_state() -> Dict[str, Any]:
    """Get the live session state."""
    return st.session_state.get("live_session", {
        "mic_status": "stopped",
        "transcript_stream": [],
        "avg_latency_ms": 0,
        "is_recording": False,
        "last_transcript_update": None
    })


def update_live_session_state(**updates):
    """Update live session state with provided values."""
    if "live_session" not in st.session_state:
        st.session_state.live_session = {}
    
    st.session_state.live_session.update(updates)


def add_transcript_entry(text: str, timestamp: Optional[datetime] = None):
    """Add a new transcript entry to the stream."""
    if timestamp is None:
        timestamp = datetime.now()
    
    entry = {
        "text": text,
        "timestamp": timestamp,
        "id": len(st.session_state.live_session["transcript_stream"])
    }
    
    st.session_state.live_session["transcript_stream"].append(entry)
    
    # Keep only the last N entries
    max_lines = config.TRANSCRIPT_MAX_LINES
    if len(st.session_state.live_session["transcript_stream"]) > max_lines:
        st.session_state.live_session["transcript_stream"] = \
            st.session_state.live_session["transcript_stream"][-max_lines:]


def clear_transcript():
    """Clear the transcript stream."""
    st.session_state.live_session["transcript_stream"] = []


def get_ai_settings() -> Dict[str, Any]:
    """Get AI settings from session state."""
    return st.session_state.get("ai_settings", {
        "autofill_enabled": config.AI_AUTOFILL_ENABLED,
        "asr_model": config.ASR_MODEL
    })


def update_ai_settings(**updates):
    """Update AI settings."""
    if "ai_settings" not in st.session_state:
        st.session_state.ai_settings = {}
    
    st.session_state.ai_settings.update(updates)


def get_form_tabs_state() -> Dict[str, Any]:
    """Get form tabs state."""
    return st.session_state.get("form_tabs", {
        "active_tab": "symptoms",
        "symptoms_count": 0,
        "medications_count": 0
    })


def update_form_tabs_state(**updates):
    """Update form tabs state."""
    if "form_tabs" not in st.session_state:
        st.session_state.form_tabs = {}
    
    st.session_state.form_tabs.update(updates)


def reset_form_state():
    """Reset form-related state."""
    st.session_state.current_form = None
    st.session_state.form_tabs = {
        "active_tab": "symptoms",
        "symptoms_count": 0,
        "medications_count": 0
    }


def reset_live_session():
    """Reset live session state."""
    st.session_state.live_session = {
        "mic_status": "stopped",
        "transcript_stream": [],
        "avg_latency_ms": 0,
        "is_recording": False,
        "last_transcript_update": None
    }


def get_patient_search_query() -> str:
    """Get the current patient search query."""
    return st.session_state.get("patient_search_query", "")


def set_patient_search_query(query: str):
    """Set the patient search query."""
    st.session_state.patient_search_query = query


def toggle_create_patient_modal():
    """Toggle the create patient modal visibility."""
    current = st.session_state.get("show_create_patient_modal", False)
    st.session_state.show_create_patient_modal = not current


def is_create_patient_modal_open() -> bool:
    """Check if the create patient modal is open."""
    return st.session_state.get("show_create_patient_modal", False)
