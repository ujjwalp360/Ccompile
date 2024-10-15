import streamlit as st
import subprocess
import os
import sys
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Ace editor for C code input
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300)

# Display area for input and output
console_output = st.empty()  # Placeholder for console output

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

            # Prepare to run the compiled C program
            run_command = "./program" if os.name != "nt" else "program.exe"
            process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Read output and handle input
            input_needed = True
            user_inputs = []

            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    console_output.text(output.strip())

                    # Check for input prompts
                    if "Enter" in output and input_needed:
                        user_input = st.text_input("Provide input:", "")
                        if user_input:
                            process.stdin.write(user_input + '\n')
                            process.stdin.flush()  # Send input to the program
                            user_inputs.append(user_input)
                            input_needed = False  # Avoid repeated input prompts

            # Wait for the program to finish
            remaining_output, errors = process.communicate()

            # Show any remaining output
            if remaining_output:
                console_output.text(remaining_output)

            # Show errors if any
            if errors:
                console_output.error(errors)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please write some C code.")
