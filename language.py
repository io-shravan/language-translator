import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import LANGUAGES, Translator
import tempfile
import os
from io import BytesIO

# Initialize session state variables
if 'transcript' not in st.session_state:
    st.session_state.transcript = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False

# Background styling
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to bottom, #f5f7fa, #c3cfe2);
        }
        .transcript-box {
            background-color: rgba(255,255,255,0.85);
            color: black;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .footer {
            position: fixed;
            bottom: 15px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 15px;
            font-family: "Gill Sans", sans-serif;
            color: #888888;
            opacity: 0.7;
            text-align: center;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize translator
translator = Translator()

# Create language mapping
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translate_text(spoken_text, from_language, to_language):
    try:
        translation = translator.translate(spoken_text, src=from_language, dest=to_language)
        return translation.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

def text_to_speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code, slow=False)
        
        # Save to a BytesIO object instead of a file
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Return the audio data
        return fp
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

def recognize_speech(from_language):
    status_placeholder = st.empty()
    status_placeholder.markdown(
        """
        <div style="text-align: center;">
            <p>Listening...</p>
            <div class="loader"></div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    try:
        # Initialize recognizer
        r = sr.Recognizer()
        
        # Use microphone as source
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        status_placeholder.markdown(
            """
            <div style="text-align: center;">
                <p>Processing speech...</p>
                <div class="loader"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Recognize speech using Google Speech Recognition
        text = r.recognize_google(audio, language=from_language)
        status_placeholder.empty()
        return text
    
    except sr.WaitTimeoutError:
        status_placeholder.error("No speech detected. Please try again.")
    except sr.UnknownValueError:
        status_placeholder.error("Could not understand audio. Please try again.")
    except sr.RequestError as e:
        status_placeholder.error(f"Speech recognition service error: {e}")
    except Exception as e:
        status_placeholder.error(f"Error: {e}")
    
    return None

# --- UI Layout ---
st.title("Real-Time Language Translator")

# Dropdowns for language selection
col1, col2 = st.columns(2)
with col1:
    from_language_name = st.selectbox("I will speak in:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))
with col2:
    to_language_name = st.selectbox("Translate to:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("spanish"))

# Convert names to codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    start_button = st.button("Start Speaking", use_container_width=True)
with col2:
    clear_button = st.button("Clear Transcript", use_container_width=True)

# Output area
output_placeholder = st.empty()

# Process speech when button is clicked
if start_button:
    spoken_text = recognize_speech(from_language)
    
    if spoken_text:
        output_placeholder.info(f"You said: {spoken_text}")
        
        # Translate the text
        translated_text = translate_text(spoken_text, from_language, to_language)
        
        if translated_text:
            # Add to transcript
            st.session_state.transcript.append({
                "spoken": spoken_text,
                "translated": translated_text
            })
            
            # Generate speech from translated text
            audio_data = text_to_speech(translated_text, to_language)
            
            if audio_data:
                # Display the translation and play the audio
                st.success(f"Translation: {translated_text}")
                st.audio(audio_data, format="audio/mp3")

# Clear transcript if requested
if clear_button:
    st.session_state.transcript = []
    st.experimental_rerun()

# --- Transcript Section ---
if st.session_state.transcript:
    st.markdown("---")
    st.subheader("Translation History")
    
    for i, entry in enumerate(reversed(st.session_state.transcript)):
        st.markdown(
            f"""
            <div class="transcript-box">
                <p><strong>You said:</strong> {entry['spoken']}</p>
                <p><strong>Translated:</strong> {entry['translated']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown(
    """
    <div class="footer">
        Project by Shravan and Sanjay
    </div>
    """,
    unsafe_allow_html=True
)
