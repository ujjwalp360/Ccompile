import streamlit as st
import subprocess
import os
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Ace editor for C code input
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300)

# Output display area
output_area = st.empty()  # Placeholder for output display
input_area = st.empty()    # Placeholder for input display
input_buffer = []  # Store inputs for multiple scanf calls

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

            # Output display loop
            while True:
                # Read output line by line
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    output_area.text(output.strip())
                    
                    # Check for input prompts
                    if "Enter" in output or "Press Enter" in output:
                        user_input = input_area.text_input("Provide input:", "")
                        if user_input:
                            # Write input to the process
                            process.stdin.write(user_input + '\n')
                            process.stdin.flush()  # Send input to the program
                            input_area.empty()  # Clear the input area after sending

            # Capture remaining output after the program finishes
            remaining_output, _ = process.communicate()
            output_area.text(remaining_output.strip())

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please write some C code.")
