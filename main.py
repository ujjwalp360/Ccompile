import streamlit as st
import subprocess
import os
import re
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Ace editor for C code input
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300)

# Output display area
output_area = st.empty()  # Placeholder for output and input display

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
            # Detect any `scanf` statements in the code
            scanf_matches = re.findall(r'scanf\("([^"]*)"', code)

            # If there are scanf statements, prompt for input values
            input_values = {}
            if scanf_matches:
                for i, match in enumerate(scanf_matches):
                    input_value = st.text_input(f"Input for scanf #{i+1}: ", "")
                    if input_value:
                        input_values[i] = input_value  # Store the input values

                # Only run the program if all inputs are provided
                if len(input_values) == len(scanf_matches):
                    # Combine input values into a single string separated by newlines
                    user_input = "\n".join(input_values.values())

                    # Run the compiled C program with user inputs
                    run_command = "./program" if os.name != "nt" else "program.exe"
                    run_result = subprocess.run(run_command, input=user_input.encode(),
                                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Display the program output
                    output_area.subheader("Program Output:")
                    output_area.text(run_result.stdout.decode("utf-8"))

                    # Display any runtime errors
                    if run_result.stderr:
                        output_area.subheader("Runtime Errors")
                        output_area.text(run_result.stderr.decode("utf-8"))
            else:
                # If no `scanf`, run the program normally
                run_command = "./program" if os.name != "nt" else "program.exe"
                run_result = subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Display the program output
                output_area.subheader("Program Output:")
                output_area.text(run_result.stdout.decode("utf-8"))

                # Display any runtime errors
                if run_result.stderr:
                    output_area.subheader("Runtime Errors")
                    output_area.text(run_result.stderr.decode("utf-8"))
        else:
            # Display compilation errors
            output_area.subheader("Compilation Errors")
            output_area.text(compile_result.stderr.decode("utf-8"))
    else:
        st.warning("Please write some C code.")
