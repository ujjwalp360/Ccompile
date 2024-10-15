import streamlit as st
import subprocess
import os
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Ace editor for C code input with auto-indentation and auto-closing of quotes, braces, etc.
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300)

# Interactive terminal input box (appears after the user runs the program)
input_values = st.text_area("Enter input for the program (if required):", height=100)

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
            # If compilation was successful, simulate terminal interaction
            st.subheader("Program Output:")

            # Use subprocess.Popen to run the program and send input dynamically
            run_command = "./program" if os.name != "nt" else "program.exe"
            process = subprocess.Popen(run_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Send input to the program (simulate terminal behavior)
            stdout, stderr = process.communicate(input=input_values.encode())

            # Display the output
            st.text(stdout.decode("utf-8"))

            # Display any runtime errors
            if stderr:
                st.subheader("Runtime Errors")
                st.text(stderr.decode("utf-8"))
        else:
            # Display compilation errors
            st.subheader("Compilation Errors")
            st.text(compile_result.stderr.decode("utf-8"))
    else:
        st.warning("Please write some C code.")
