def ascii_animation():
    import time
    import streamlit as st

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


def hash_cracker():
    import streamlit as st

    if st.sidebar.button("View ASCII Animation"):
        ascii_animation()


# Dictionary of subpage functions
page2_funcs = {
    "Hash Cracker": hash_cracker
    # "Network Analysis": network_analysis,
    # "Subnet Calculator": subnet_calculator
}
