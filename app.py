import streamlit as st
import openai
import requests



def main():
    st.title("WeatherWise")
    city=st.sidebar.text_input("Enter city name","Buffalo")

    weather_api_key=""
    openai_api_key=""


    submit= st.sidebar.submit("Get Weather Updates")



if __name__=="__main__":
    main()


