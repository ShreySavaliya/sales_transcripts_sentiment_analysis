import streamlit as st
import requests
from pie_chart import merge_sentiment_scores
import plotly.express as px
import pandas as pd

st.set_page_config(layout="centered")
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
        st.subheader("Upload the transcript file you want sentiment analysis for:")
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
                    st.header("Transcript")
                    transcript = response.json().get("content", "No Transcript Found")
                    st.text_area("Transcript", value=transcript, height=300)
                    print("Yaha tak pahucha")
                    sales_agent_sentiments = response.json().get("sales_agent_sentiments", [])
                    if sales_agent_sentiments:

                        # Pie Chart for Sentiment Analysis
                        st.header("Sentiment Analysis Pie Chart")
                        merged_scores = {}
                        for sentiment in sales_agent_sentiments:
                            for key, value in sentiment.items():
                                if key in merged_scores:
                                    merged_scores[key] += value
                                else:
                                    merged_scores[key] = value

                        fig = create_pie_chart(merged_scores)
                        st.plotly_chart(fig)

                        # Scatter PLot for Sentiment Analysis
                        st.header("Sentiment Analysis Scatter Plot")
                        df = scatter_plot(response.json().get("sales_agent_sentiments", []))
                        fig = px.scatter(df, x='index', y='sentiment', size='score', color='sentiment',
                                         color_discrete_map={'Positive': 'green', 'Neutral': 'grey', 'Negative': 'red'},
                                         title='Sentiment Analysis Scatter Plot',
                                         labels={'index': 'Index', 'sentiment': 'Sentiment'},
                                         size_max=20,
                                         template='plotly_dark')
                        st.title("Sentiment Analysis Scatter Plot")
                        st.plotly_chart(fig)

                        #

                    else:
                        st.warning("No sentiment analysis data found.")
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


def create_pie_chart(sentiment_scores):
    color_map = {
        'Neutral': 'grey',
        'Positive': 'green',
        'Negative': 'red'
    }

    labels = list(sentiment_scores.keys())
    values = list(sentiment_scores.values())
    colors = [color_map[label] for label in labels]

    # Create a pie chart using Plotly
    fig = px.pie(values=values, names=labels, title='Sentiment Analysis', color_discrete_sequence=colors)

    return fig


def scatter_plot(values):
    sentiments = []
    scores = []
    indices = []

    for idx, score_dict in enumerate(values):
        for sentiment, score in score_dict.items():
            sentiments.append(sentiment)
            scores.append(score)
            indices.append(idx)

    # Create a DataFrame for plotting
    df = pd.DataFrame({
        'index': indices,
        'sentiment': sentiments,
        'score': scores
    })

    return df


if __name__ == '__main__':
    if not isinstance(st.query_params, dict):
        st.query_params = dict({
            "page": "login"
        })
    main()
