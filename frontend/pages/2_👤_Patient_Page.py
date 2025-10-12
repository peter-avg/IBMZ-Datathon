"""Patient Page for viewing patient details and form archive."""

import streamlit as st
from datetime import datetime
from typing import Optional
from models.domain import Patient, Form, FormStatus
from services.api_client import api_client, APIError
from utils.state import (
    initialize_session_state,
    get_current_patient,
    set_current_patient,
    reset_form_state
)
from utils.config import config


def render_patient_header(patient: Patient):
    """Render the patient header with avatar and name."""
    st.markdown("---")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Patient avatar (initials)
        initials = "".join([name[0].upper() for name in patient.name.split()[:2]])
        st.markdown(f"""
        <div style="
            width: 80px; 
            height: 80px; 
            border-radius: 50%; 
            background-color: #4CAF50; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            color: white; 
            font-size: 32px; 
            font-weight: bold;
            margin: 0 auto;
        ">
            {initials}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title(f"👤 {patient.name}")
        st.caption(f"Patient ID: {patient.id}")


def render_personal_data_section(patient: Patient):
    """Render the personal data section."""
    st.subheader("📋 Personal Data")
    
    # Create a nice card-like display
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Full Name:**")
            st.info(patient.name)
            
            st.write("**Email:**")
            if patient.email:
                st.info(patient.email)
            else:
                st.info("Not provided")
        
        with col2:
            st.write("**Date of Birth:**")
            if patient.date_of_birth:
                st.info(patient.date_of_birth.strftime("%B %d, %Y"))
            else:
                st.info("Not provided")
            
            st.write("**Patient ID:**")
            st.info(patient.id)
        
        # Additional fields that might be available from backend
        if hasattr(patient, 'phone') and patient.phone:
            st.write("**Phone:**")
            st.info(patient.phone)
        
        if hasattr(patient, 'sex_at_birth') and patient.sex_at_birth:
            st.write("**Sex at Birth:**")
            st.info(patient.sex_at_birth)


def render_form_archive_section(patient: Patient):
    """Render the form archive section."""
    st.subheader("📁 Form Archive")
    
    # Backend doesn't support form retrieval, so we show a message
    st.info("""
    **Form Archive Information:**
    
    The backend API doesn't support retrieving forms after submission. 
    Forms are submitted as complete records and cannot be edited or viewed later.
    
    To create a new consultation form for this patient, use the "New Form" button below.
    """)
    
    # Show a note about form workflow
    with st.expander("ℹ️ About Form Submission", expanded=False):
        st.markdown("""
        **How forms work with the backend:**
        
        1. **Create Form**: Start a new form session
        2. **Live Session**: Record consultation and add symptoms/medications
        3. **Submit**: Finalize and submit the complete form to the backend
        4. **Archive**: Forms are stored in the backend but cannot be retrieved
        
        This design ensures data integrity and prevents modification of submitted medical records.
        """)


def render_floating_action_button(patient: Patient):
    """Render the floating action button for creating new forms."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("➕ New Form", type="primary", use_container_width=True):
            # Reset form state and navigate to new form page
            reset_form_state()
            st.switch_page("pages/3_📝_New_Form.py")


def render_back_button():
    """Render back button to return to dashboard."""
    if st.button("← Back to Dashboard"):
        st.switch_page("pages/1_📋_Main_Dashboard.py")


def main():
    """Main patient page function."""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Patient Details",
        page_icon="👤",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Get current patient
    patient = get_current_patient()
    
    if not patient:
        st.error("No patient selected. Please go back to the dashboard and select a patient.")
        if st.button("← Back to Dashboard"):
            st.switch_page("pages/1_📋_Main_Dashboard.py")
        return
    
    # Render back button
    render_back_button()
    
    # Render patient header
    render_patient_header(patient)
    
    # Two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Form Archive (left column)
        render_form_archive_section(patient)
    
    with col2:
        # Personal Data (right column)
        render_personal_data_section(patient)
    
    # Floating action button
    render_floating_action_button(patient)


if __name__ == "__main__":
    main()
