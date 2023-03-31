import streamlit as st

# First view
def view1():
    st.write("View 1")
    if st.button("Go to View 2"):
        st.session_state.view = "view2"
        st.experimental_rerun()

# Second view
def view2():
    st.write("View 2")
    if st.button("Go to View 1"):
        st.session_state.view = "view1"
        st.experimental_rerun()

# Main app
def app():
    if "view" not in st.session_state:
        st.session_state.view = "view1"

    if st.session_state.view == "view1":
        view1()
    elif st.session_state.view == "view2":
        view2()

if __name__ == "__main__":
    app()