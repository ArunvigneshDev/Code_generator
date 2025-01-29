import streamlit as st
import chains
import vectordb
from streamlit.components.v1 import html

def inject_custom_css():
    """Inject custom CSS for styling"""
    st.markdown("""
    <style>
        .main {
            background-color: #F5F5F5;
        }
        
        .stTextInput>div>div>input {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
        }
        
        .stSelectbox>div>div>select {
            background-color: #FFFFFF;
        }
        
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 24px;
            transition: all 0.3s;
        }
        
        .stButton button:hover {
            background-color: #45a049;
            transform: scale(1.05);
        }
        
        .header {
            color: #2C3E50;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        
        .response-box {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .sidebar .sidebar-content {
            background-color: #2C3E50;
            color: white;
        }
        
        .toggle {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        
        .toggle input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        
        input:checked + .slider {
            background-color: #4CAF50;
        }
        
        input:checked + .slider:before {
            transform: translateX(26px);
        }
    </style>
    """, unsafe_allow_html=True)

def code_generator_app():
    """Enhanced Code Generator App with improved UI/UX"""
    
    inject_custom_css()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("<h1 style='color: #4CAF50;'>🔮 Code Wizard</h1>", unsafe_allow_html=True)
        section = st.radio(
            "Navigation Menu",
            ("💻 Code Generator", "📚 Knowledge Base"),
            index=0,
            help="Choose between code generation or managing knowledge base"
        )
        
        st.markdown("---")
        st.markdown("### Settings")
        debug_mode = st.checkbox("🐞 Debug Mode")
        
        st.markdown("---")
        st.markdown("#### About")
        st.markdown("Powered by Streamlit • v1.0")

    # db initialization
    vectordatabase = vectordb.initialize_chroma()

    # Code Generator Section
    if section == "💻 Code Generator":
        st.markdown("<h1 class='header'>✨ AI Code Generator</h1>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                task = st.text_input(
                    "🎯 Programming Task",
                    placeholder="e.g., 'Implement a neural network from scratch'"
                )
            with col2:
                language = st.selectbox(
                    "🌐 Language",
                    ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
                    index=0
                )
        
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown("### ⚙️ Advanced Settings")
                use_rag = st.checkbox("Enable Context-Aware Generation (RAG)", value=True)
                temperature = st.slider("Creativity Level", 0.0, 1.0, 0.7)
            
            with col2:
                st.markdown("### ")
                generate_btn = st.button("🚀 Generate Code", use_container_width=True)
        
        if generate_btn and task:
            with st.spinner("🔮 Crafting code magic..."):
                try:
                    if use_rag:
                        response = chains.generate_code_rag_chain(task, language, vectordatabase)
                    else:
                        response = chains.generate_code_chain(task, language)
                    
                    with st.expander("✨ Generated Code", expanded=True):
                        st.markdown(f"```{language.lower()}\n{response}\n```")
                    
                    if debug_mode:
                        st.markdown("### 🐞 Debug Info")
                        st.json({"task": task, "language": language, "rag_enabled": use_rag})
                        
                except Exception as e:
                    st.error(f"⚠️ Error: {str(e)}")

    # File Ingestion Section
    elif section == "📚 Knowledge Base":
        st.markdown("<h1 class='header'>📚 Knowledge Base Manager</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### 📤 Upload Documents")
            uploaded_file = st.file_uploader(
                "Drag and drop or click to upload",
                type=["txt", "csv", "docx", "pdf", "md"],
                accept_multiple_files=False,
                help="Supported formats: Text, CSV, Word, PDF, Markdown"
            )
            
            if uploaded_file is not None:
                with st.spinner("🧠 Learning from documents..."):
                    try:
                        vectordb.store_pdf_in_chroma(uploaded_file, vectordatabase)
                        st.success(f"✅ Successfully processed '{uploaded_file.name}'")
                        st.balloons()
                    except Exception as e:
                        st.error(f"⚠️ Error processing file: {str(e)}")
        
        st.markdown("---")
        with st.container():
            st.markdown("### 📊 Database Status")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Documents", "1.2k", "+34")
            with col2:
                st.metric("Storage Used", "256MB", "12%")
            with col3:
                st.metric("Index Size", "1.4GB", "4.3%")

if __name__ == "__main__":
    code_generator_app()