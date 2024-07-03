# Importing important libraries
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Sample user database
user_db = {
    "user1": "password1",
    "shrey": "shrey0037",
    "admin": "adminpass"
}


def add_user(username, password):
    if username not in user_db:
        user_db[username] = password
        return True
    return False


# Set page configuration
st.set_page_config(layout="centered")


def set_page(page):
    st.query_params["page"] = page


def login(username, password):
    """Check if the provided username and password match the user database."""

    if username in user_db and user_db[username] == password:
        return True
    return False


def main():
    """Main function for managing actions"""

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
    current_page = st.query_params.get("page")

    # Home page layout
    if current_page == "home":
        st.header("FiXit")
        st.write("Welcome to the home page.")

    # Login page layout
    elif current_page == "login":
        st.header("FiXit")
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

    # Upload page layout
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
                response = None
                try:
                    response = requests.post('https://lemming-devoted-solely.ngrok-free.app/upload', files=files, timeout=1000)
                except Exception as e:
                    print("Exception\n", e)

                if response and response.status_code == 200:
                    st.success("File successfully uploaded")
                    st.header("Transcript")
                    transcript = response.json().get("content", "No Transcript Found")
                    st.text_area("Transcript", value=transcript, height=300)
                    st.session_state.response = response

                    if st.button("Visualize", on_click=set_page("stats")):
                        set_page("stats")
                        st.rerun()
                else:
                    st.error("File upload failed")
            else:
                print("No file selected")
                st.warning("No file selected")

    # Statistics for sentiment analysis
    elif current_page == "stats":
        options = ("Sales Agent", "Customer")
        choice = st.selectbox("Select a person for analysis:", options, index=None)
        display_stats(st.session_state.response, choice)

    # Signup page layout
    elif current_page == "signup":
        st.subheader("Create New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Signup"):
            if new_user in user_db:
                st.warning("User already exists. Please choose a different username.")
            else:
                if add_user(new_user, new_password):
                    st.success("You have successfully created an account")
                    st.info("Go to the Login section to login")
                else:
                    st.error("Failed to create an account. Please try again.")


def display_stats(response, selected_option):
    if selected_option == "Sales Agent":
        sales_agent_sentiments = response.json().get("sales_agent_sentiments", [])
        if sales_agent_sentiments:

            # Pie Chart for Sentiment Analysis
            st.header("Displaying Sentiment Analysis for Sales Agent")
            fig = pie_chart(sales_agent_sentiments)
            st.subheader("Sentiment Analysis Pie Chart")
            st.plotly_chart(fig)

            # Timeline for Sentiment Analysis
            st.subheader("Sentiment Analysis Timeline Chart")
            df = timeline_plot(response.json().get("sales_agent_sentiments", []))
            fig = px.scatter(df, x='index', y='sentiment', size='score', color='sentiment',
                             color_discrete_map={'Positive': 'green', 'Neutral': 'grey',
                                                 'Negative': 'red'},
                             title='Timeline Chart',
                             labels={'index': 'Index', 'sentiment': 'Sentiment'},
                             size_max=20,
                             template='plotly_dark')
            st.plotly_chart(fig)

            # Scatter plot for sentiment analysis
            st.subheader("Sentiment Analysis Scatter Plot")
            sales_agent_timestamps = response.json().get("sales_agent_timestamps", [])
            scatter_plot(sales_agent_timestamps, sales_agent_sentiments)

            # Annotate the text according to the sentiments
            sales_agent_dialogues = response.json().get("sales_agent_dialogues")
            annotate_text(sales_agent_dialogues, sales_agent_sentiments)

        else:
            st.warning("No sentiment analysis data found.")

    elif selected_option == "Customer":

        customer_sentiments = response.json().get("customer_sentiments", [])
        if customer_sentiments:
            st.header("Displaying Sentiment Analysis for Customer")
            fig = pie_chart(customer_sentiments)
            st.subheader("Sentiment Analysis Pie Chart")
            st.plotly_chart(fig)

            # Timeline for Sentiment Analysis
            st.subheader("Sentiment Analysis Scatter Plot")
            df = timeline_plot(response.json().get("customer_sentiments", []))
            fig = px.scatter(df, x='index', y='sentiment', size='score', color='sentiment',
                             color_discrete_map={'Positive': 'green', 'Neutral': 'grey',
                                                 'Negative': 'red'},
                             title='Timeline Chart',
                             labels={'index': 'Index', 'sentiment': 'Sentiment'},
                             size_max=20,
                             template='plotly_dark')
            st.plotly_chart(fig)

            # Scatter plot for sentiment analysis
            st.subheader("Sentiment Analysis Scatter Plot")
            customer_timestamps = response.json().get("customer_timestamps", [])
            scatter_plot(customer_timestamps, customer_sentiments)

            # Annotate the text according to the sentiments
            customer_dialogues = response.json().get("customer_dialogues")
            annotate_text(customer_dialogues, customer_sentiments)
        else:
            st.warning("No sentiment analysis data found.")
    else:
        st.warning("No option selected!")


def pie_chart(sentiment_scores):
    """Create a pie chart for sentiment analysis"""
    color_map = {
        'Neutral': 'grey',
        'Positive': 'green',
        'Negative': 'red'
    }

    merged_scores = {}
    for sentiment in sentiment_scores:
        for key, value in sentiment.items():
            if key in merged_scores:
                merged_scores[key] += value
            else:
                merged_scores[key] = value

    labels = list(merged_scores.keys())
    values = list(merged_scores.values())
    colors = [color_map[label] for label in labels]

    # Create a pie chart using Plotly
    fig = px.pie(values=values, names=labels, title='Sentiments by Percentage', color_discrete_sequence=colors)

    return fig


def timeline_plot(values):
    """Build a scatter plot for sentiment analysis"""

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


def scatter_plot(user_timestamps, user_sentiments):
    """Build a scatter plot according to the sentiments of the conversations"""

    time_in_seconds = []
    for time_str in user_timestamps:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = minutes * 60 + seconds
        time_in_seconds.append(total_seconds)

    # Extract values from values_list
    categories = []
    values = []
    for d in user_sentiments:
        for category, value in d.items():
            categories.append(category)
            values.append(value)

    # Create a DataFrame for Plotly
    df = pd.DataFrame({
        'Time': time_in_seconds[:len(values)],  # Align the length of time_in_seconds with values
        'Category': categories,
        'Value': values
    })

    color_map = {
        'Positive': 'green',
        'Negative': 'red',
        'Neutral': 'Grey'
    }

    # Create the scatter plot using Plotly
    fig = go.Figure()

    # Add traces for each category with corresponding colors
    for category in df['Category'].unique():
        category_df = df[df['Category'] == category]
        fig.add_trace(go.Scatter(
            x=category_df['Time'],
            y=category_df['Value'],
            mode='markers',
            marker=dict(color=color_map[category]),
            name=category
        ))

    # Update layout
    fig.update_layout(
        title='Scatter Plot of Values over Time',
        xaxis_title='Time in seconds',
        yaxis_title='Value'
    )

    # Display the plot using Streamlit
    st.plotly_chart(fig)


def annotate_text(user_dialogues, user_sentiments):
    """Annotate the conversations based on their sentiments"""

    color_map = {
        'Positive': 'green',
        'Negative': 'red',
        'Neutral': 'Grey'
    }
    # Filter positive and negative sentiments
    filtered_data = [(list(item.keys())[0], list(item.values())[0], text) for item, text in
                     zip(user_sentiments, user_dialogues) if list(item.keys())[0]
                     in color_map]

    # Display the annotated text in Streamlit
    st.subheader("Annotated Sentiment Text")

    for sentiment, score, text in filtered_data:
        color = color_map[sentiment]
        st.markdown(f'<span style="color:{color};">{text}</span>', unsafe_allow_html=True)


if __name__ == '__main__':
    if not isinstance(st.query_params, dict):
        st.query_params = dict({
            "page": "login"
        })
    main()
