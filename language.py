import streamlit as st
from gtts import gTTS
from googletrans import LANGUAGES, Translator
from io import BytesIO

# Initialize session state variables
if 'transcript' not in st.session_state:
    st.session_state.transcript = []

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

def translate_text(input_text, from_language, to_language):
    try:
        translation = translator.translate(input_text, src=from_language, dest=to_language)
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

# --- UI Layout ---
st.title("Language Translator")

# Dropdowns for language selection
col1, col2 = st.columns(2)
with col1:
    from_language_name = st.selectbox("Input Language:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("english"))
with col2:
    to_language_name = st.selectbox("Target Language:", list(LANGUAGES.values()), index=list(LANGUAGES.values()).index("spanish"))

# Convert names to codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Text input instead of speech
input_text = st.text_area("Enter text to translate:", height=100)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    translate_button = st.button("Translate", use_container_width=True)
with col2:
    clear_button = st.button("Clear Transcript", use_container_width=True)

# Process text when button is clicked
if translate_button and input_text:
    # Translate the text
    translated_text = translate_text(input_text, from_language, to_language)
    
    if translated_text:
        # Add to transcript
        st.session_state.transcript.append({
            "original": input_text,
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
                <p><strong>Original:</strong> {entry['original']}</p>
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
