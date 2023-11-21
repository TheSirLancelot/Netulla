import streamlit as st


# Password Complexity Function
def password_complexity():
    st.title("Password Complexity Checker")

    st.write("Enter a password to check its complexity:")
    user_input = st.text_input("Password:", "")

    def check_password_complexity(password):
        # Define your criteria for password complexity here
        score = 0

        # Check password length
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1

        # Check character repetition
        if len(set(password)) >= len(password) / 2:
            score += 1

        # Check for uppercase letters
        if any(c.isupper() for c in password):
            score += 1

        # Check for lowercase letters
        if any(c.islower() for c in password):
            score += 1

        # Check for digits
        if any(c.isdigit() for c in password):
            score += 1

        # Check for special characters
        if any(c in "!@#$%^&*()_+{}[]:;<>,.?~\\/-" for c in password):
            score += 1

            complexity = "Unacceptable"

        # Determine complexity based on the score
        if score <= 2:
            complexity = "Unacceptable"
        elif score <= 4:
            complexity = "Weak"
        elif score <= 6:
            complexity = "Meh"
        elif score <= 8:
            complexity = "Strong"

        return complexity

    if user_input:
        complexity = check_password_complexity(user_input)
        st.write(f"Password Complexity: {complexity}")


# Dictionary of subpage functions
page2_funcs = {
    "Password Complexity": password_complexity
    # "Network Analysis": network_analysis,
    # "Subnet Calculator": subnet_calculator
}
