import streamlit as st
import subprocess
import os

# Title of the app
st.title("Online C Compiler")

# Text area to write C code
code = st.text_area("Write your C code here:", height=300)

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
            run_result = subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
