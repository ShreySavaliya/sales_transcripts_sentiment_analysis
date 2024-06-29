import streamlit as st
import requests

# Sample user database (In-memory)
user_db = {
    "user1": "password1",
    "shrey": "shrey0037",
    "admin": "adminpass"
}


def set_page(page):
    st.query_params["page"] = page
    # print(st.query_params)


def login(username, password):
    """Check if the provided username and password match the user database."""
    return True
    # if username in user_db and user_db[username] == password:
    #     return True
    # return False


def main():
    st.set_page_config(layout="centered")  # Set the layout to wide for a better appearance

    # Navigation bar
    st.markdown(
        """
        <style>
        .nav-button {
            display: inline-block;
            margin-right: 15px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Display navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        home_button = st.button("Home", key="home", help="Go to Home", on_click=set_page, args=("home",))
    with col2:
        login_button = st.button("Login", key="login", help="Go to Login", on_click=set_page, args=("login",))
    with col3:
        signup_button = st.button("Sign Up", key="signup", help="Go to Sign Up", on_click=set_page, args=("signup",))

    # Get the current page from the query parameters
    # query_params = st.query_params
    current_page = st.query_params.get("page")

    if current_page == "home":
        st.subheader("Home")
        st.write("Welcome to the home page.")

    elif current_page == "login":
        st.subheader("Login Section")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Submit"):
            print("Login", username, password)
            if login(username, password):
                st.success(f"Logged in as {username}")
                set_page("upload")
                st.rerun()
            else:
                st.warning("Incorrect Username/Password")

    elif current_page == "upload":
        st.write("Upload the transcript file you want sentiment analysis for:")
        uploaded_file = st.file_uploader("Upload a text file", type="txt")
        if st.button("Upload"):
            if uploaded_file is not None:
                print("Uploaded", uploaded_file)
                st.write("Filename:", uploaded_file.name)
                
                # Send the file to the Flask server
                files = {'file': uploaded_file.getvalue()}
                print("Uploaded file:", files)
                try:
                    response = requests.post("http://127.0.0.1:5000/upload", files=files, timeout=500)
                except Exception as e:
                    print("Exception\n", e)
                
                if response.status_code == 200:
                    st.success("File successfully uploaded")
                    st.json(response.json())
                else:
                    st.error("File upload failed")
            else:
                print("No file selected")
                st.warning("No file selected")

    elif current_page == "signup":
        st.subheader("Create New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Signup"):
            if new_user in user_db:
                st.warning("User already exists. Please choose a different username.")
            else:
                user_db[new_user] = new_password
                st.success("You have successfully created an account")
                st.info("Go to the Login section to login")


if __name__ == '__main__':
    if not isinstance(st.query_params, dict):
        st.query_params = dict({
            "page": "login"
        })
    main()
