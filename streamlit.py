import json
import requests
import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional

# Base URL and identifiers for the flow
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "b8766986-8463-4ac4-b496-c82ed89df3db"
FLOW_ID = "322c40a4-d482-4f66-91db-e13940b8185f"
APPLICATION_TOKEN = "AstraCS:QdSXuCyYWfPxGrTyKgYRwhwM:4ca263756cbce02a012e0760e6321ed8abc720cbf98bfe1b58910947fc7d7fd7"
ENDPOINT = "endpoint"  # Specific endpoint name in the flow settings

# Default tweaks dictionary to modify flow behavior
DEFAULT_TWEAKS = {
    "ChatInput-bm0G5": {},
    "ChatOutput-Yba4s": {},
    "GoogleGenerativeAIModel-k6jtC": {},
    "CustomComponent-yytgm": {},
    "Prompt-e1urX": {}
}

# Function to run the flow with the provided message
def run_flow(message: str,
             endpoint: str = ENDPOINT,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = APPLICATION_TOKEN) -> dict:
    """
    Run a flow with a given message and optional tweaks.
    :param message: The message to send to the flow
    :param endpoint: The endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}?stream=false"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    if tweaks:
        payload["tweaks"] = tweaks
    headers = {
        "Authorization": "Bearer " + application_token,
        "Content-Type": "application/json"
    }

    # Track the start time
    start_time = time.time()
    
    # Send the request to the flow
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Calculate response time
    response_time = time.time() - start_time

    # Check if the response is valid
    if response.status_code == 200:
        return response.json(), response_time
    else:
        return {"error": "Failed to fetch response", "details": response.text}, response_time

# Streamlit app for UI
def main():
    st.title("Social Media Performance Analysis")

    # Initialize session state for messages and performance stats
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "response_times" not in st.session_state:
        st.session_state["response_times"] = []

    # Input form for user message
    with st.form(key="input_form"):
        message = st.text_area("Enter your message:", "")
        submit_button = st.form_submit_button(label="Run Flow")

    # Add an option for tweaking the flow
    tweaks_option = st.checkbox("Customize Flow Tweaks")
    tweaks = DEFAULT_TWEAKS
    if tweaks_option:
        tweak_json_input = st.text_area("Enter custom tweaks (JSON format):", value=json.dumps(DEFAULT_TWEAKS, indent=2))
        try:
            tweaks = json.loads(tweak_json_input)
        except json.JSONDecodeError:
            st.error("Invalid JSON format for tweaks.")

    # When the submit button is clicked
    if submit_button:
        if message.strip() == "":
            st.error("Please enter a message.")
        else:
            # Run the flow
            try:
                with st.spinner("Running flow..."):
                    response, response_time = run_flow(message, tweaks=tweaks)
                    
                    if "error" in response:
                        st.error(response["details"])
                    else:
                        response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response from flow.")
                        
                        # Save the chat history and response time in the session state
                        st.session_state["messages"].append({"user": message, "bot": response_text})
                        st.session_state["response_times"].append(response_time)

            except Exception as e:
                st.error(f"Error: {e}")

    # Display the chat history
    st.subheader("Chat History")
    for chat in st.session_state["messages"]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.divider()  # Adds a divider between chat messages for better readability

    # Display performance metrics (response times and message statistics)
    st.subheader("Performance Metrics")
    
    # Display response time graph
    if st.session_state["response_times"]:
        st.write("Response Time (in seconds) for each request:")
        response_times = st.session_state["response_times"]
        st.bar_chart(response_times)
    
    # Display message length statistics
    message_lengths = [len(chat['user']) for chat in st.session_state["messages"]]
    if message_lengths:
        st.write("Message Length Statistics")
        st.write(f"Average message length: {np.mean(message_lengths):.2f}")
        st.write(f"Max message length: {max(message_lengths)}")
        st.write(f"Min message length: {min(message_lengths)}")
        
        # Message length distribution plot
        plt.figure(figsize=(10, 6))
        plt.hist(message_lengths, bins=10, color='skyblue', edgecolor='black')
        plt.title("Distribution of Message Lengths")
        plt.xlabel("Message Length")
        plt.ylabel("Frequency")
        st.pyplot(plt)

# Run the Streamlit app
if __name__ == "__main__":
    main()
