import streamlit as st
import subprocess
import os
import re
from streamlit_ace import st_ace

# Title of the app
st.title("Online C Compiler")

# Sidebar for selecting different practical experiments
st.sidebar.title("Practical Selection")
experiment = st.sidebar.selectbox("Select Practical Experiment", ("Home", "Experiment 1", "Experiment 2", "Experiment 3"))

# Default code for each experiment
home_code = """// Online C compiler to run C program online
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}
"""

exp1_code = """// Experiment 1: Addition of Two Numbers
#include <stdio.h>

int main() {
    int a, b, sum;
    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);
    sum = a + b;
    printf("Sum: %d\\n", sum);
    return 0;
}
"""

exp2_code = """// Experiment 2: Find the Largest of Three Numbers
#include <stdio.h>

int main() {
    int a, b, c;
    printf("Enter three numbers: ");
    scanf("%d %d %d", &a, &b, &c);
    if (a >= b && a >= c)
        printf("%d is the largest number\\n", a);
    else if (b >= a && b >= c)
        printf("%d is the largest number\\n", b);
    else
        printf("%d is the largest number\\n", c);
    return 0;
}
"""

exp3_code = """// Experiment 3: Calculate the Factorial of a Number
#include <stdio.h>

int main() {
    int n, i;
    unsigned long long factorial = 1;
    printf("Enter an integer: ");
    scanf("%d", &n);
    if (n < 0)
        printf("Error! Factorial of a negative number doesn't exist.");
    else {
        for (i = 1; i <= n; ++i) {
            factorial *= i;
        }
        printf("Factorial of %d = %llu\\n", n, factorial);
    }
    return 0;
}
"""

# Determine the default code based on the selected experiment
if experiment == "Home":
    default_code = home_code
elif experiment == "Experiment 1":
    default_code = exp1_code
elif experiment == "Experiment 2":
    default_code = exp2_code
elif experiment == "Experiment 3":
    default_code = exp3_code

# Ace editor for C code input with auto-indentation and auto-closing of quotes, braces, etc.
code = st_ace(language='c', theme='monokai', auto_update=True, keybinding="vscode", height=300, value=default_code)

# Detect `scanf` statements in the code and prompt for user input
scanf_inputs = []
if code:
    scanf_matches = re.findall(r'scanf\("%[^"]*"', code)
    if scanf_matches:
        st.write("Detected scanf. Please provide input values:")
        for i, match in enumerate(scanf_matches):
            user_input = st.text_input(f"Input for scanf #{i + 1}:", "")
            scanf_inputs.append(user_input)

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
            
            # Run the program with the user inputs (if scanf was detected)
            run_result = subprocess.run(run_command, input="\n".join(scanf_inputs).encode(), 
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
