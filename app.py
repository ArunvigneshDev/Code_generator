from dotenv import load_dotenv
import chain
import streamlit as st
from streamlit.components.v1 import html

load_dotenv()

def code_generator_app():
    """Enhanced Code Generator Application"""
    
    st.title("🖥️ Code Generator AI")
    st.markdown("Generate code snippets in various programming languages")
    
    with st.container(border=True):
        with st.form("code_gen_form"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                language = st.selectbox(
                    "Programming Language",
                    ["C", "Python", "Java", "JavaScript", "C++", "Go", "Rust"],
                    index=0,
                    help="Select target programming language"
                )
                
            with col2:
                problem_statement = st.text_area(
                    "Task Description",
                    height=150,
                    placeholder="Describe the task you want to implement (e.g., 'Implement a stack data structure')",
                    help="Clearly describe the functionality you need"
                )

            submitted = st.form_submit_button(
                "🚀 Generate Code",
                use_container_width=True
            )

    if submitted:
        if not problem_statement:
            st.error("Please provide a task description")
            return
            
        with st.spinner(f"Generating {language} code..."):
            try:
                response = chain.generate_code(language, problem_statement)
                st.subheader("Generated Code")
                
                lang_map = {
                    "C": "c",
                    "C++": "cpp",
                    "Python": "python",
                    "Java": "java",
                    "JavaScript": "javascript",
                    "Go": "go",
                    "Rust": "rust"
                }
                
                with st.expander("View Code", expanded=True):
                    st.code(response, language=lang_map.get(language, "text"))

            except Exception as e:
                st.error(f"Code generation failed: {str(e)}")
                st.info("Please try adjusting your task description")

if __name__ == "__main__":
    code_generator_app()