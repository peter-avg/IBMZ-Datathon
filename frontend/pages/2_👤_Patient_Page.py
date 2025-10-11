"""Patient Page for viewing patient details and form archive."""

import streamlit as st
from datetime import datetime
from typing import Optional
from models.domain import Patient, Form, FormStatus
from services.api_client import api_client
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


def render_form_archive_section(patient: Patient):
    """Render the form archive section."""
    st.subheader("📁 Form Archive")
    
    # Get forms for this patient
    forms = api_client.list_forms(patient_id=patient.id)
    
    if not forms:
        st.info("No forms found for this patient. Create a new form to get started.")
        return
    
    # Display forms in a list
    for form in forms:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                # Form ID and creation date
                created_date = form.created_at.strftime("%B %d, %Y at %I:%M %p") if form.created_at else "Unknown"
                st.write(f"**Form #{form.id[:8]}...**")
                st.caption(f"Created: {created_date}")
            
            with col2:
                # Status badge
                status_color = "🟢" if form.status == FormStatus.FINALIZED else "🟡"
                status_text = "Finalized" if form.status == FormStatus.FINALIZED else "Draft"
                st.write(f"{status_color} **{status_text}**")
            
            with col3:
                # Open button
                if st.button("📝 Open", key=f"open_form_{form.id}"):
                    # Set current form and navigate to live form page
                    st.session_state.current_form = form
                    st.switch_page("pages/4_🎙️_Live_Form.py")
            
            with col4:
                # Delete button
                if st.button("🗑️", key=f"delete_form_{form.id}", help="Delete form"):
                    if api_client.delete_form(form.id):
                        st.success("Form deleted successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete form.")
            
            st.markdown("---")


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
