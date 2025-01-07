import streamlit as st
import openai
import requests
import datetime
from datetime import datetime


def get_weather_update(city,weather_api_key):
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    complete_url=base_url+"appid="+weather_api_key+"&q="+city
    response=requests.get(complete_url)
    return response.json()

def generate_weather_description(data,openai_api_key):
    openai.api_key=openai_api_key

    try:
        temperature=data['main']['temp'] -273.15
        description=data['weather'][0]['description']
        prompt=f"The current weather in your city is {description} with a temperature of {temperature:.2f} degrees celsius.Explain this in a simple way for general audience."

        response=openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=60
        )


        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)



def get_weekly_updates(city,weather_api_key,lat,lon):
    base_url="https://api.openweathermap.org/data/2.5/"
    complete_url=f"{base_url}forecast?lat={lat}&lon={lon}&appid={weather_api_key}"
    response=requests.get(complete_url)
    return response.json()

def display_weekly_forecast(data):
    try:
        st.write("----------------------------------------------------------------------------------------------")
        st.write("Weekly Weather Forecast")
        displayed_dates=set()

        c1,c2,c3,c4=st.columns(4)
        with c1:
            st.metric("",'Day')

        with c2:
            st.metric("","Desc")
        
        with c3:
            st.metric("","Min_temp")

        with c4:
            st.metric("","Max_temp")


        
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime("%A, %B %d")
            if date not in displayed_dates:
                displayed_dates.add(date)
                min_temp=day['main']['temp_min'] - 273.15
                max_temp=day['main']['temp_max'] - 273.15

                description=day['weather'][0]['description']

                with c1:
                    st.write(f"{date}")

                with c2:
                    st.write(f"{description.capitalize()}")
                
                with c3:
                    st.write(f"{min_temp:.1f} C")

                with c4:
                    st.write(f"{max_temp:.1f} C")

    except Exception as e:
        st.error("Error in displaying weekly forecast :" +str(e))




def main():
    st.sidebar.image("weatherwise.jpeg",width=250)
    st.title("Weather Wise")
    city=st.sidebar.text_input("Enter city name","Buffalo")

    weather_api_key="replace_with_weather_api_key"
    openai_api_key="replace with openai_api_key"

    submit= st.sidebar.button("Get Weather Updates")

    if submit:
        st.title("Weather Updates for "+ city + "is :" )
        with st.spinner("Fetching Weather data ..."):
            weather_data=get_weather_update(city,weather_api_key)
            print(weather_data)


            if weather_data['cod'] !='404':
                col1,col2=st.columns(2)
                with col1:
                    st.metric("Temperature", f"{weather_data['main']['temp'] - 273.15:.2f} C" )
                    st.metric("Humudity", f"{weather_data['main']['humidity']} %")
                with col2:
                    st.metric("Pressure", f"{weather_data['main']['pressure']} hpa")
                    st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")

                lat=weather_data['coord']['lat']
                lon=weather_data['coord']['lon']


                weather_description=generate_weather_description(weather_data,openai_api_key)
                st.write(weather_description)

                forecast_data=get_weekly_updates(city,weather_api_key,lat,lon)
                print("forecast data------------",forecast_data)

                if forecast_data.get("cod")!='404':
                    display_weekly_forecast(forecast_data)

                else:
                    st.error("Error fetching weekly forecast data ")
                

            else:
                st.error("Error occured..Please check your city and try again later")



    

        

if __name__=="__main__":
    main()


