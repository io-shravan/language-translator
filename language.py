import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

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

# Language data
LANGUAGES = {
    'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic',
    'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian',
    'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan',
    'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian',
    'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
    'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish',
    'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian',
    'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole',
    'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew',
    'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
    'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian',
    'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh',
    'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz',
    'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian',
    'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
    'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi',
    'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali',
    'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian',
    'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian',
    'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian',
    'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala',
    'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish',
    'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik',
    'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish',
    'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek',
    'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish',
    'yo': 'yoruba', 'zu': 'zulu'
}

# Create language mapping
language_names = sorted([name.title() for name in LANGUAGES.values()])
language_mapping = {name.lower(): code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name.lower(), "en")

def translate_text(input_text, from_language, to_language):
    try:
        translator = GoogleTranslator(source=from_language, target=to_language)
        return translator.translate(input_text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None

# --- UI Layout ---
st.title("📝 Simple Language Translator")
st.markdown("Translate text between different languages easily!")

# Dropdowns for language selection
col1, col2 = st.columns(2)
with col1:
    from_language_name = st.selectbox("From:", language_names, index=language_names.index("English"))
with col2:
    to_language_name = st.selectbox("To:", language_names, index=language_names.index("Spanish"))

# Convert names to codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Text input
input_text = st.text_area("Enter text to translate:", height=150)

# Action buttons
col1, col2 = st.columns(2)
with col1:
    translate_button = st.button("Translate", use_container_width=True)
with col2:
    clear_button = st.button("Clear History", use_container_width=True)

# Translation result area
result_placeholder = st.empty()

# Process text when button is clicked
if translate_button and input_text:
    with st.spinner("Translating..."):
        # Translate the text
        translated_text = translate_text(input_text, from_language, to_language)
        
        if translated_text:
            # Add to transcript
            st.session_state.transcript.append({
                "original": input_text,
                "from_lang": from_language_name,
                "translated": translated_text,
                "to_lang": to_language_name
            })
            
            # Display the translation
            result_placeholder.success(f"Translation: {translated_text}")

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
                <p><strong>{entry['from_lang']}:</strong> {entry['original']}</p>
                <p><strong>{entry['to_lang']}:</strong> {entry['translated']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Create a dataframe for the translation history and allow download
if st.session_state.transcript and len(st.session_state.transcript) > 0:
    st.markdown("---")
    data = pd.DataFrame(st.session_state.transcript)
    
    csv = data.to_csv(index=False)
    st.download_button(
        label="Download Translation History as CSV",
        data=csv,
        file_name="translation_history.csv",
        mime="text/csv",
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
