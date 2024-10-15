import streamlit as st
import subprocess
import os
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

            # Prepare to capture the program's output and input
            output_buffer = StringIO()
            sys.stdout = output_buffer

            # Run the compiled C program
            run_command = "./program" if os.name != "nt" else "program.exe"
            process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Loop to handle input and output
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    output_area.text(output.strip())

                    # Check for input prompts
                    if "Press Enter" in output:
                        user_input = st.text_input("Provide input:", "")
                        if user_input:
                            process.stdin.write(user_input + '\n')
                            process.stdin.flush()  # Send input to the program

            # Get remaining output after the program finishes
            remaining_output, _ = process.communicate()
            output_area.text(remaining_output)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please write some C code.")
