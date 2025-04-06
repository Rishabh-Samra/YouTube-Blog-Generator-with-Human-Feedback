import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,graph,user_message):
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        graph = self.graph
        user_message = self.user_message
        print("user_message: ", user_message)
        for event in graph.stream({'messages':("user",user_message)}):
            print("event values: ", event.values())
            if not event or not hasattr(event, "values"):
                print(f"Error: {event} is empty or lacks 'values'")
                continue  # Skip this iteration
            for value in event.values():
                print("value messages: ", value['messages'])
                with st.chat_message("user"):
                    st.write(user_message)
                with st.chat_message("assistant"):
                    st.write(value["messages"].content)