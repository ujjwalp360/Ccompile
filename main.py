import streamlit as st
import subprocess
import os
import re
import sys
from streamlit_ace import st_ace
from io import StringIO

# Title of the app
st.title("Online C Compiler")

# Ace editor for C code input
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300)

# Output display area
output_area = st.empty()  # Placeholder for output display

# Button to compile and run the code
if st.button("Compile and Run"):
    if code:
        # Save the C code to a file
        with open("program.c", "w") as f:
            f.write(code)

        # Check if the file was created successfully
        if not os.path.exists("program.c"):
            st.error("Failed to create program.c file.")
            st.stop()  # Stop further execution if the file was not created

        # Compile the C code using gcc
        compile_command = "gcc program.c -o program"
        try:
            compile_result = subprocess.run(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if compile_result.returncode != 0:
                st.error(f"Compilation failed: {compile_result.stderr.decode()}")
                st.stop()
        except Exception as e:
            st.error(f"An error occurred while compiling: {str(e)}")
            st.stop()

        # Prepare to capture the program's output and input
        output_buffer = StringIO()
        sys.stdout = output_buffer

        # Run the compiled C program
        run_command = "./program" if os.name != "nt" else "program.exe"

        # Execute the program, while allowing for interactive input
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Loop to handle input and output
        while True:
            # Read output from the program
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                output_area.text(output.strip())

                # Check if there's a prompt for input
                if "Enter" in output:  # Adjust based on the output prompts in your program
                    user_input = st.text_input("Provide input:", "")
                    if user_input:  # If user input is provided, send it to the program
                        process.stdin.write(user_input + '\n')
                        process.stdin.flush()  # Ensure the input is sent to the program

        # Get remaining output after the program finishes
        remaining_output, _ = process.communicate()
        output_area.text(remaining_output)

        # Reset stdout
        sys.stdout = sys.__stdout__
    else:
        st.warning("Please write some C code.")
