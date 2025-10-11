"""Audio recorder component using streamlit-webrtc for browser-based audio capture."""

import streamlit as st
import asyncio
from typing import Optional, Callable, Any
from streamlit_webrtc import webrtc_streamer, WebRTCStreamerContext
from utils.state import update_live_session_state, add_transcript_entry
from utils.config import config


class AudioRecorder:
    """Audio recorder component wrapper for streamlit-webrtc."""
    
    def __init__(self, 
                 key: str = "audio_recorder",
                 on_audio_frame: Optional[Callable] = None,
                 on_transcript_update: Optional[Callable] = None):
        """
        Initialize the audio recorder.
        
        Args:
            key: Unique key for the component
            on_audio_frame: Callback function for audio frame processing
            on_transcript_update: Callback function for transcript updates
        """
        self.key = key
        self.on_audio_frame = on_audio_frame
        self.on_transcript_update = on_transcript_update
        self.streamer_context: Optional[WebRTCStreamerContext] = None
    
    def render(self) -> WebRTCStreamerContext:
        """
        Render the audio recorder component.
        
        Returns:
            WebRTCStreamerContext for controlling the stream
        """
        # Configure audio constraints
        audio_constraints = {
            "sampleRate": config.AUDIO_SAMPLE_RATE,
            "channelCount": 1,
            "echoCancellation": True,
            "noiseSuppression": True,
            "autoGainControl": True
        }
        
        # Create the WebRTC streamer
        self.streamer_context = webrtc_streamer(
            key=self.key,
            mode="sendonly",  # Only send audio, don't receive
            audio_receiver_size=1024,
            media_stream_constraints={
                "audio": audio_constraints,
                "video": False
            },
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            async_processing=True
        )
        
        return self.streamer_context
    
    def is_recording(self) -> bool:
        """Check if audio is currently being recorded."""
        return self.streamer_context is not None and self.streamer_context.state.playing
    
    def start_recording(self):
        """Start audio recording."""
        if self.streamer_context:
            update_live_session_state(
                mic_status="recording",
                is_recording=True
            )
    
    def stop_recording(self):
        """Stop audio recording."""
        if self.streamer_context:
            update_live_session_state(
                mic_status="stopped",
                is_recording=False
            )
    
    def pause_recording(self):
        """Pause audio recording."""
        if self.streamer_context:
            update_live_session_state(
                mic_status="paused",
                is_recording=False
            )
    
    def get_status(self) -> str:
        """Get current recording status."""
        if not self.streamer_context:
            return "not_initialized"
        
        if self.streamer_context.state.playing:
            return "recording"
        elif self.streamer_context.state.playing is False:
            return "stopped"
        else:
            return "unknown"


def render_audio_controls(key: str = "audio_controls") -> AudioRecorder:
    """
    Render audio controls with start/pause/stop buttons.
    
    Args:
        key: Unique key for the component
        
    Returns:
        AudioRecorder instance
    """
    st.subheader("🎙️ Audio Controls")
    
    # Create audio recorder
    recorder = AudioRecorder(key=f"{key}_recorder")
    
    # Render the WebRTC component
    streamer_context = recorder.render()
    
    # Control buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start", key=f"{key}_start"):
            recorder.start_recording()
            st.success("Recording started")
    
    with col2:
        if st.button("⏸️ Pause", key=f"{key}_pause"):
            recorder.pause_recording()
            st.info("Recording paused")
    
    with col3:
        if st.button("⏹️ Stop", key=f"{key}_stop"):
            recorder.stop_recording()
            st.warning("Recording stopped")
    
    with col4:
        if st.button("🔄 Reset", key=f"{key}_reset"):
            recorder.stop_recording()
            st.session_state.live_session["transcript_stream"] = []
            st.rerun()
    
    # Status display
    status = recorder.get_status()
    status_colors = {
        "recording": "🟢",
        "stopped": "🔴", 
        "paused": "🟡",
        "not_initialized": "⚪"
    }
    
    st.write(f"**Status:** {status_colors.get(status, '⚪')} {status.title()}")
    
    return recorder


def render_transcript_window(key: str = "transcript"):
    """
    Render the transcript display window.
    
    Args:
        key: Unique key for the component
    """
    st.subheader("📝 Live Transcript")
    
    # Get transcript stream from session state
    transcript_stream = st.session_state.get("live_session", {}).get("transcript_stream", [])
    
    if not transcript_stream:
        st.info("No transcript available. Start recording to see live transcription.")
        return
    
    # Create a scrollable container for transcript
    transcript_container = st.container()
    
    with transcript_container:
        # Display transcript entries in reverse order (newest first)
        for entry in reversed(transcript_stream[-config.TRANSCRIPT_MAX_LINES:]):
            timestamp = entry.get("timestamp", "").strftime("%H:%M:%S") if entry.get("timestamp") else ""
            text = entry.get("text", "")
            
            if timestamp and text:
                st.text(f"[{timestamp}] {text}")
            elif text:
                st.text(text)
    
    # Add mock transcript entry for demo purposes
    if st.button("➕ Add Demo Transcript", key=f"{key}_demo"):
        demo_text = "Patient reports headache for 3 days, moderate intensity, taking ibuprofen twice daily."
        add_transcript_entry(demo_text)
        st.rerun()


def render_status_bar():
    """Render the status bar with mic status, model info, and latency."""
    st.subheader("📊 Status")
    
    live_session = st.session_state.get("live_session", {})
    ai_settings = st.session_state.get("ai_settings", {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mic_status = live_session.get("mic_status", "stopped")
        st.metric("Microphone", mic_status.title())
    
    with col2:
        asr_model = ai_settings.get("asr_model", config.ASR_MODEL)
        st.metric("ASR Model", asr_model)
    
    with col3:
        latency = live_session.get("avg_latency_ms", 0)
        st.metric("Latency", f"{latency} ms")


def render_audio_section(key: str = "audio_section") -> AudioRecorder:
    """
    Render the complete audio section with controls, transcript, and status.
    
    Args:
        key: Unique key for the section
        
    Returns:
        AudioRecorder instance
    """
    st.markdown("---")
    
    # Audio controls
    recorder = render_audio_controls(f"{key}_controls")
    
    st.markdown("---")
    
    # Transcript window
    render_transcript_window(f"{key}_transcript")
    
    st.markdown("---")
    
    # Status bar
    render_status_bar()
    
    return recorder
