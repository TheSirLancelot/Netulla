import streamlit as st


def ascii_animation():
    import time
    import streamlit as st


def ascii_animation():
    animation_text = r"""
                             .';cloooolc:,.                                 
                          .cx0NWMMMMMMMMWWXOo,.                             
                        'dXWMMMMMMMMMMMMMMMMMNO:.                           
                       cKMMMMMMMMMMMMMMMMMMMMMMWk'                          
                      cXMMMMMMMMMMMMMMMMMMMMMMMMW0,                         
                     ;KMMMMMMMMMMMMMMMMMMMMMMMMMMWk.                        
                    .xWMMMMMMMMMMMMMMMMMMMMMMMMMMMX:                        
                    ;KMMMMMMMMMMMMMMMMMMMMMMMMMMMMWd                        
                    lWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMx.                       
                   .dWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMk.                       
                   .xMMWMMMMMMMMMMMMMMMMMMMMMMMMWWMk.                       
                    oWOccokKWMMMMMMMMMMMMMWXkoc::kNd.                       
                    ,K0'   .;dXMMMMMMMMMWOc.    ,0K;                        
                     lXk.     .dNMMMMMMKc.     ;0No.                        
                     .oX0:.     cXMMMMK:     'dXWx.                         
                      .cXNOl,.   oNMMWo. .':xXMNd.                          
                        ;0WMNKOxdkNMMNOxkKNWMMXo.                           
                         .xNMMMMMMMMMMMMMMMMW0;                             
                           :0WMMMMMMMMMMMMMXd.                              
                            .c0WMMMMMMMMMXx,                                
                              .;dOKXXX0xc.                                  
                                 .....                                     
    """
    animation_placeholder = st.empty()
    for i in range(len(animation_text)):
        animation_placeholder.text(animation_text[:i])
        time.sleep(0.001)
    animation_placeholder.empty()


#Password Complexity Function
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

            #Hello 


        return complexity

    if user_input:
        complexity = check_password_complexity(user_input)
        st.write(f"Password Complexity: {complexity}")

   

def hash_cracker():
    if st.sidebar.button("View ASCII Animation"):
        ascii_animation()


# Dictionary of subpage functions
page2_funcs = {
    "Hash Cracker": hash_cracker,
    "Password Complexity": password_complexity
    #"Network Analysis": network_analysis,
    #"Subnet Calculator": subnet_calculator
}
