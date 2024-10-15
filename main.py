import streamlit as st
import subprocess
import os
import sys

# Title of the app
st.title("Online C Compiler")

# Text area for C code input
code = st.text_area("C Code", height=300)

# Display area for input and output
console_output = st.empty()  # Placeholder for console output

# Input buffer to capture user inputs
input_buffer = []

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

            console_output.text("Running...\n")  # Indicate that the program is running

            # Loop to handle input and output
            while True:
                # Read output from the program
                output = process.stdout.readline()
                
                if output == "" and process.poll() is not None:
                    break
                if output:
                    console_output.text(output.strip())  # Display the output in the console
                    # Check for prompts indicating the program needs input
                    if "Enter" in output or "input" in output.lower():  # More generic prompt detection
                        user_input = st.text_input("Input:", "")
                        if user_input:
                            input_buffer.append(user_input)
                            process.stdin.write(user_input + '\n')
                            process.stdin.flush()  # Send input to the program
                            console_output.text(f"Input: {user_input}\n")  # Show the input in the console

            # Wait for the program to finish and get remaining output
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
