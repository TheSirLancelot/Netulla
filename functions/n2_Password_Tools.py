import streamlit as st
import random
import string

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

def password_generator():
    st.title('Password Generator')

    # Password length slider
    password_length = st.slider('Select password length', min_value=6, max_value=20, value=8)

    # Complexity options
    include_uppercase = st.checkbox('Include Uppercase Letters', value=True)
    include_lowercase = st.checkbox('Include Lowercase Letters', value=True)
    include_numbers = st.checkbox('Include Numbers', value=True)
    include_special_chars = st.checkbox('Include Special Characters', value=False)

    # Number of passwords, easily changed
    num_passwords = st.number_input('How many passwords? (No more than 10)', min_value=1, max_value=10, value=1)

    if st.button('Generate Passwords'):
        characters = ''
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_numbers:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        if characters:
            generated_passwords = '\n'.join(''.join(random.choice(characters) for i in range(password_length)) for _ in range(num_passwords))
            st.text_area('Generated Passwords:', generated_passwords, height=100)
        else:
            st.error('Please select at least one character type.')

# Dictionary of subpage functions
page2_funcs = {
    "Password Complexity": password_complexity,
    "Password Generator": password_generator
    # "Network Analysis": network_analysis,
    # "Subnet Calculator": subnet_calculator
}
