import streamlit as st
import subprocess
import os

# Title of the app
st.title("Online C Compiler")

# Text area for C code input
code = st.text_area("Enter your C code here:", height=300)

# Button to compile and run the code
if st.button("Compile and Run"):
    if code:
        try:
            # Save the C code to a file
            with open("program.c", "w") as f:
                f.write(code)

            # Compile the C code using gcc
            compile_command = "gcc program.c -o program"
            compile_result = subprocess.run(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if compile_result.returncode != 0:
                st.error(f"Compilation failed:\n{compile_result.stderr.decode()}")
                st.stop()

            # Run the compiled C program
            run_command = "./program" if os.name != "nt" else "program.exe"
            process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Capture the output
            output, errors = process.communicate()

            # Display output and errors
            st.subheader("Output")
            st.text(output)

            if errors:
                st.subheader("Errors")
                st.text(errors)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please write some C code.")
