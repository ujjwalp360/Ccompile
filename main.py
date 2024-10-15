import streamlit as st
import subprocess
import os
import re
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Default C code snippet
default_code = """// Online C compiler to run C program online
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""

# Ace editor for C code input with auto-indentation and auto-closing of quotes, braces, etc.
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300, value=default_code)

# Detect `scanf` statements in the code and prompt for user input
scanf_inputs = []
if code:
    scanf_matches = re.findall(r'scanf\("%[^"]*"', code)
    if scanf_matches:
        st.write("Detected scanf. Please provide input values:")
        for i, match in enumerate(scanf_matches):
            user_input = st.text_input(f"Input for scanf #{i + 1}:", "")
            scanf_inputs.append(user_input)

# Button to compile and run the code
if st.button("Compile and Run"):
    if code:
        # Save the C code to a file
        with open("program.c", "w") as f:
            f.write(code)

        # Compile the C code using gcc
        compile_command = "gcc program.c -o program"
        compile_result = subprocess.run(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if compile_result.returncode == 0:
            # If compilation was successful, run the program
            run_command = "./program" if os.name != "nt" else "program.exe"
            
            # Run the program with the user inputs (if scanf was detected)
            run_result = subprocess.run(run_command, input="\n".join(scanf_inputs).encode(), 
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Display the output or errors
            st.subheader("Output")
            st.text(run_result.stdout.decode("utf-8"))

            if run_result.stderr:
                st.subheader("Runtime Errors")
                st.text(run_result.stderr.decode("utf-8"))
        else:
            # Display compilation errors
            st.subheader("Compilation Errors")
            st.text(compile_result.stderr.decode("utf-8"))
    else:
        st.warning("Please write some C code.")
        
