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
            scanf_matches = re.findall(r'scanf\("%[^"]*"', code)

            # Create output and input sections
            output_display = output_area.empty()
            input_display = output_area.empty()

            if scanf_matches:
                output_display.subheader("Program Output:")
                input_values = input_display.text_area("Input (for scanf if required):", height=100)

                if input_values:
                    # Run the compiled C program with user inputs
                    run_command = "./program" if os.name != "nt" else "program.exe"
                    run_result = subprocess.run(run_command, input=input_values.encode(),
                                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Display the program output
                    output_display.text(run_result.stdout.decode("utf-8"))

                    # Display any runtime errors
                    if run_result.stderr:
                        output_display.subheader("Runtime Errors")
                        output_display.text(run_result.stderr.decode("utf-8"))
            else:
                # If no `scanf`, run the program normally
                run_command = "./program" if os.name != "nt" else "program.exe"
                run_result = subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Display the program output
                output_display.subheader("Program Output:")
                output_display.text(run_result.stdout.decode("utf-8"))

                # Display any runtime errors
                if run_result.stderr:
                    output_display.subheader("Runtime Errors")
                    output_display.text(run_result.stderr.decode("utf-8"))
        else:
            # Display compilation errors
            output_area.subheader("Compilation Errors")
            output_area.text(compile_result.stderr.decode("utf-8"))
    else:
        st.warning("Please write some C code.")
        
