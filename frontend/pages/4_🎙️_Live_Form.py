"""Live Form page with audio recording and form filling."""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from models.domain import (
    Form, Symptom, Medication, FormStatus,
    CreateSymptomRequest, CreateMedicationRequest,
    UpdateFormRequest
)
from services.api_client import api_client
from services.ai_extractor import ai_extractor
from components.audio_recorder import render_audio_section
from utils.state import (
    initialize_session_state,
    get_current_patient,
    get_current_doctor,
    get_current_form,
    get_live_session_state,
    add_transcript_entry,
    get_ai_settings
)
from utils.config import config


def render_back_button():
    """Render back button to return to patient page."""
    if st.button("← Back to Patient"):
        st.switch_page("pages/2_👤_Patient_Page.py")


def render_form_header(form: Form, patient, doctor):
    """Render the form header with patient and doctor info."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("🎙️ Live Form Session")
        st.write(f"**Patient:** {patient.name} | **Doctor:** {doctor.name}")
        st.caption(f"Form ID: {form.id[:8]}... | Status: {form.status.value}")
    
    with col2:
        # Form status badge
        status_color = "🟢" if form.status == FormStatus.FINALIZED else "🟡"
        st.metric("Status", f"{status_color} {form.status.value.title()}")
    
    with col3:
        # Session duration (mock)
        st.metric("Duration", "00:05:23")


def render_symptoms_tab(form: Form):
    """Render the symptoms tab."""
    st.subheader("🩺 Symptoms")
    
    # Get existing symptoms
    symptoms = api_client.list_symptoms(form_id=form.id)
    
    # Display existing symptoms
    if symptoms:
        st.write("**Current Symptoms:**")
        for i, symptom in enumerate(symptoms):
            with st.expander(f"Symptom {i+1}: {symptom.name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Name:** {symptom.name}")
                    if symptom.duration:
                        st.write(f"**Duration:** {symptom.duration}")
                    if symptom.intensity:
                        st.write(f"**Intensity:** {symptom.intensity}")
                    if symptom.recurrence:
                        st.write(f"**Recurrence:** {symptom.recurrence}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_symptom_{symptom.id}", help="Delete symptom"):
                        if api_client.delete_symptom(symptom.id):
                            st.success("Symptom deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete symptom.")
    else:
        st.info("No symptoms recorded yet.")
    
    st.markdown("---")
    
    # Add new symptom form
    st.write("**Add New Symptom:**")
    
    with st.form("add_symptom_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Symptom Name *", placeholder="e.g., Headache, Fever")
            duration = st.text_input("Duration", placeholder="e.g., 3 days, 2 weeks")
        
        with col2:
            intensity = st.selectbox(
                "Intensity",
                options=["", "Mild", "Moderate", "Severe", "1/10", "2/10", "3/10", "4/10", "5/10", "6/10", "7/10", "8/10", "9/10", "10/10"]
            )
            recurrence = st.text_input("Recurrence", placeholder="e.g., Daily, Intermittent")
        
        if st.form_submit_button("➕ Add Symptom", type="primary"):
            if name.strip():
                try:
                    request = CreateSymptomRequest(
                        form_id=form.id,
                        name=name.strip(),
                        duration=duration.strip() if duration else None,
                        intensity=intensity if intensity else None,
                        recurrence=recurrence.strip() if recurrence else None
                    )
                    
                    new_symptom = api_client.create_symptom(request)
                    if new_symptom:
                        st.success(f"Symptom '{new_symptom.name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add symptom.")
                except Exception as e:
                    st.error(f"Error adding symptom: {str(e)}")
            else:
                st.error("Please enter a symptom name.")


def render_medications_tab(form: Form):
    """Render the medications tab."""
    st.subheader("💊 Medications")
    
    # Get existing medications
    medications = api_client.list_medications(form_id=form.id)
    
    # Display existing medications
    if medications:
        st.write("**Current Medications:**")
        for i, medication in enumerate(medications):
            with st.expander(f"Medication {i+1}: {medication.name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Name:** {medication.name}")
                    if medication.strength:
                        st.write(f"**Strength:** {medication.strength}")
                    if medication.frequency:
                        st.write(f"**Frequency:** {medication.frequency}")
                    if medication.duration:
                        st.write(f"**Duration:** {medication.duration}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_medication_{medication.id}", help="Delete medication"):
                        if api_client.delete_medication(medication.id):
                            st.success("Medication deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete medication.")
    else:
        st.info("No medications recorded yet.")
    
    st.markdown("---")
    
    # Add new medication form
    st.write("**Add New Medication:**")
    
    with st.form("add_medication_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Medication Name *", placeholder="e.g., Ibuprofen, Aspirin")
            strength = st.text_input("Strength", placeholder="e.g., 500mg, 10ml")
        
        with col2:
            frequency = st.text_input("Frequency", placeholder="e.g., 2x daily, Once a day")
            duration = st.text_input("Duration", placeholder="e.g., 7 days, 2 weeks")
        
        if st.form_submit_button("➕ Add Medication", type="primary"):
            if name.strip():
                try:
                    request = CreateMedicationRequest(
                        form_id=form.id,
                        name=name.strip(),
                        strength=strength.strip() if strength else None,
                        frequency=frequency.strip() if frequency else None,
                        duration=duration.strip() if duration else None
                    )
                    
                    new_medication = api_client.create_medication(request)
                    if new_medication:
                        st.success(f"Medication '{new_medication.name}' added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add medication.")
                except Exception as e:
                    st.error(f"Error adding medication: {str(e)}")
            else:
                st.error("Please enter a medication name.")


def render_summary_tab(form: Form, patient, doctor):
    """Render the summary tab."""
    st.subheader("📋 Form Summary")
    
    # Form information
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Form Details:**")
        st.info(f"**Form ID:** {form.id}")
        st.info(f"**Patient:** {patient.name}")
        st.info(f"**Doctor:** {doctor.name}")
        st.info(f"**Status:** {form.status.value.title()}")
        st.info(f"**Created:** {form.created_at.strftime('%B %d, %Y at %I:%M %p') if form.created_at else 'Unknown'}")
    
    with col2:
        st.write("**Statistics:**")
        symptoms_count = len(api_client.list_symptoms(form_id=form.id))
        medications_count = len(api_client.list_medications(form_id=form.id))
        
        st.metric("Symptoms", symptoms_count)
        st.metric("Medications", medications_count)
    
    # Free text notes
    st.write("**Notes:**")
    if form.free_text_notes:
        st.text_area("", value=form.free_text_notes, height=100, disabled=True)
    else:
        st.info("No notes recorded.")
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Draft", type="secondary"):
            updated_form = api_client.update_form(form.id, status=FormStatus.DRAFT)
            if updated_form:
                st.success("Form saved as draft!")
                st.rerun()
            else:
                st.error("Failed to save form.")
    
    with col2:
        if st.button("✅ Finalize", type="primary"):
            updated_form = api_client.update_form(form.id, status=FormStatus.FINALIZED)
            if updated_form:
                st.success("Form finalized successfully!")
                st.rerun()
            else:
                st.error("Failed to finalize form.")
    
    with col3:
        if st.button("📄 Export", type="secondary"):
            st.info("Export functionality coming soon!")


def process_ai_extraction(form: Form):
    """Process AI extraction from transcript and update form."""
    live_session = get_live_session_state()
    transcript_stream = live_session.get("transcript_stream", [])
    
    if not transcript_stream:
        return
    
    # Extract entities from transcript
    extraction_result = ai_extractor.extract_from_transcript_stream(transcript_stream)
    
    if extraction_result.symptoms or extraction_result.medications:
        st.sidebar.success("🤖 AI extracted entities from transcript!")
        
        # Add extracted symptoms
        for symptom in extraction_result.symptoms:
            try:
                request = CreateSymptomRequest(
                    form_id=form.id,
                    name=symptom.name,
                    duration=symptom.duration,
                    intensity=symptom.intensity,
                    recurrence=symptom.recurrence
                )
                api_client.create_symptom(request)
            except Exception as e:
                st.sidebar.error(f"Failed to add symptom: {str(e)}")
        
        # Add extracted medications
        for medication in extraction_result.medications:
            try:
                request = CreateMedicationRequest(
                    form_id=form.id,
                    name=medication.name,
                    strength=medication.strength,
                    frequency=medication.frequency,
                    duration=medication.duration
                )
                api_client.create_medication(request)
            except Exception as e:
                st.sidebar.error(f"Failed to add medication: {str(e)}")
        
        st.rerun()


def main():
    """Main live form page function."""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Live Form Session",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Get current context
    patient = get_current_patient()
    doctor = get_current_doctor()
    form = get_current_form()
    
    if not patient or not doctor or not form:
        st.error("Missing context. Please go back and start a new form.")
        if st.button("← Back to Dashboard"):
            st.switch_page("pages/1_📋_Main_Dashboard.py")
        return
    
    # Render back button
    render_back_button()
    
    # Render form header
    render_form_header(form, patient, doctor)
    
    # Split layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Left column: Audio section
        st.subheader("🎙️ Live Transcription")
        render_audio_section("live_session")
        
        # AI extraction processing
        ai_settings = get_ai_settings()
        if ai_settings.get("autofill_enabled", False):
            process_ai_extraction(form)
    
    with col2:
        # Right column: Form tabs
        st.subheader("📋 Form")
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["🩺 Symptoms", "💊 Medications", "📋 Summary"])
        
        with tab1:
            render_symptoms_tab(form)
        
        with tab2:
            render_medications_tab(form)
        
        with tab3:
            render_summary_tab(form, patient, doctor)


if __name__ == "__main__":
    main()
