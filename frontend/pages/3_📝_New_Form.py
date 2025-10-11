"""New Form page for creating forms with decision support."""

import streamlit as st
from datetime import datetime
from models.domain import CreateFormRequest, FormStatus
from services.api_client import api_client
from utils.state import (
    initialize_session_state,
    get_current_patient,
    get_current_doctor,
    set_current_form,
    get_ai_settings,
    update_ai_settings,
    reset_live_session
)
from utils.config import config


def render_back_button():
    """Render back button to return to patient page."""
    if st.button("← Back to Patient"):
        st.switch_page("pages/2_👤_Patient_Page.py")


def render_patient_info(patient):
    """Render patient information header."""
    st.markdown("---")
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Patient avatar
        initials = "".join([name[0].upper() for name in patient.name.split()[:2]])
        st.markdown(f"""
        <div style="
            width: 60px; 
            height: 60px; 
            border-radius: 50%; 
            background-color: #2196F3; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            color: white; 
            font-size: 24px; 
            font-weight: bold;
        ">
            {initials}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.title(f"📝 New Form for {patient.name}")
        st.caption(f"Patient ID: {patient.id}")


def render_decision_support_section():
    """Render the decision support section."""
    st.subheader("🤖 Decision Support")
    
    # Info box
    st.info("""
    **How it works:** When you start a live session, the AI will listen to your conversation 
    with the patient and automatically extract symptoms and medications mentioned. These will 
    appear pre-filled in the form fields below.
    """)
    
    # AI settings
    ai_settings = get_ai_settings()
    
    # AI Autofill toggle
    autofill_enabled = st.toggle(
        "Enable AI Autofill from microphone",
        value=ai_settings.get("autofill_enabled", True),
        help="Automatically fill form fields based on conversation"
    )
    
    if autofill_enabled != ai_settings.get("autofill_enabled"):
        update_ai_settings(autofill_enabled=autofill_enabled)
    
    st.markdown("---")


def render_initial_form_section(form):
    """Render the initial form section for optional prefill."""
    st.subheader("📋 Initial Form (Optional)")
    
    st.write("You can add initial notes or observations before starting the live session:")
    
    # Form for initial notes
    with st.form("initial_form", clear_on_submit=False):
        notes = st.text_area(
            "Initial Notes",
            value=form.free_text_notes or "",
            placeholder="Enter any initial observations, patient complaints, or notes...",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            save_button = st.form_submit_button("💾 Save Notes", type="primary")
        
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear")
        
        if save_button:
            # Update form with notes
            updated_form = api_client.update_form(
                form.id,
                free_text_notes=notes
            )
            if updated_form:
                set_current_form(updated_form)
                st.success("Notes saved successfully!")
            else:
                st.error("Failed to save notes.")
        
        if clear_button:
            st.rerun()


def render_start_session_button(form):
    """Render the start live session button."""
    st.markdown("---")
    
    st.subheader("🎙️ Ready to Start?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Start Live Session", type="primary", use_container_width=True):
            # Reset live session state
            reset_live_session()
            
            # Navigate to live form page
            st.switch_page("pages/4_🎙️_Live_Form.py")


def create_new_form(patient, doctor):
    """Create a new form for the patient."""
    try:
        request = CreateFormRequest(
            patient_id=patient.id,
            doctor_id=doctor.id
        )
        
        form = api_client.create_form(request)
        return form
    
    except Exception as e:
        st.error(f"Failed to create form: {str(e)}")
        return None


def main():
    """Main new form page function."""
    # Initialize session state
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="New Form",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Get current patient and doctor
    patient = get_current_patient()
    doctor = get_current_doctor()
    
    if not patient:
        st.error("No patient selected. Please go back to the dashboard and select a patient.")
        if st.button("← Back to Dashboard"):
            st.switch_page("pages/1_📋_Main_Dashboard.py")
        return
    
    if not doctor:
        st.error("No doctor information available.")
        return
    
    # Render back button
    render_back_button()
    
    # Render patient info
    render_patient_info(patient)
    
    # Create or get current form
    current_form = st.session_state.get("current_form")
    if not current_form:
        # Create new form
        with st.spinner("Creating new form..."):
            current_form = create_new_form(patient, doctor)
            if current_form:
                set_current_form(current_form)
            else:
                st.error("Failed to create form. Please try again.")
                return
    
    # Render sections
    render_decision_support_section()
    render_initial_form_section(current_form)
    render_start_session_button(current_form)
    
    # Form info sidebar
    with st.sidebar:
        st.subheader("📊 Form Information")
        
        st.write(f"**Form ID:** {current_form.id[:8]}...")
        st.write(f"**Patient:** {patient.name}")
        st.write(f"**Doctor:** {doctor.name}")
        st.write(f"**Status:** {current_form.status.value}")
        st.write(f"**Created:** {current_form.created_at.strftime('%B %d, %Y at %I:%M %p') if current_form.created_at else 'Just now'}")
        
        st.markdown("---")
        
        st.subheader("💡 Tips")
        st.markdown("""
        - Enable AI Autofill for automatic form completion
        - Add initial notes to capture pre-session observations
        - The live session will record and transcribe your conversation
        - AI will extract symptoms and medications automatically
        """)


if __name__ == "__main__":
    main()
