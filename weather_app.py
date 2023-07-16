from tkinter import *
from tkinter import messagebox
from geopy.geocoders import Nominatim
import requests,geopy
from datetime import datetime
import pytz

root = Tk()
root.title('Weather app')
root.geometry('975x660')
root.configure(bg='#0080FF')

utc=pytz.utc # It is the object to find timezones
geolocator = Nominatim(user_agent="weather_app") # Object to get latitude and longitude
api='6ad7295594024647927161fbd617a35a'

# Pass cities to deffault_city function to get weather data of searched cities
def weather_data():
    city=search_entry.get()
    deffault_city(city)

#  this will append cities to external file and also check weather the city is already is in fav_city or not
def fav_city():
    city = search_entry.get()
    with open('Cities.txt', 'a+') as file:
        cities = file.readlines()
        for line in cities:
            if line.strip() == city:
                messagebox.showwarning('Attention!', f"{city} is already in favorites.")
                return
        file.write(city + "\n")
    messagebox.showinfo("Favourite", "Favourite city added")

#  This function is used to get weather data fram the city in listbox
def view_weather(window):
    global view_listbox
    selected_cities = view_listbox.curselection()
    if selected_cities:
        selected_city = view_listbox.get(selected_cities[0])
        deffault_city(selected_city)
        window.destroy()

# remove the individual cities of the listbox and txt file 
def remove():
    global view_listbox
    selected_index = view_listbox.curselection()
    if selected_index:
        view_listbox.delete(selected_index[0])
        with open('Cities.txt', 'r') as file:
            content = file.read()
            selected_city = view_listbox.get(selected_index[0])
            Remove = content.replace(selected_city, '')
        with open('Cities.txt', 'w') as file:
            file.write(Remove)


# Remove all the cities of listbox and txt file
def removeall(window):
    global view_listbox
    view_listbox.delete(0,END)
    with open('Cities.txt','w')as file:
        file.truncate(0)
        file.close()
    window.destroy()   

#  This  function is to view our favorite cities forom a list box it will open a extra window containg a listbox
def view_favourite():
    global view_listbox  
    view_window=Toplevel()
    view_window.geometry("500x500")
    view_window.title("Favorite")

    status_bar = Frame(view_window, bg='#0066CC', height=50)
    status_bar.pack(side=BOTTOM, fill=X)

    view_button = Button(status_bar, text='View weather condition', font='calibri 15', borderwidth=0, bg='#0066CC', command=lambda: view_weather(view_window))
    view_button.pack(side=RIGHT, padx=10)

    remove_button = Button(status_bar, text='Remove', font='calibri 15', borderwidth=0, bg='#0066CC', command=remove)
    remove_button.pack(side=RIGHT, padx=10)

    removeall_button = Button(status_bar, text='RemoveAll', font='calibri 15', borderwidth=0, bg='#0066CC', command=lambda: removeall(view_window))
    removeall_button.pack(side=RIGHT, padx=10)
    
    scrollbar = Scrollbar(view_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    view_listbox = Listbox(view_window, font="Kokila 15 bold", yscrollcommand=scrollbar.set)
    view_listbox.pack(fill=BOTH, expand=True)
    scrollbar.config(command=view_listbox.yview)

# Read cites from file and insert it to the list box
    with open('Cities.txt', 'r+') as file:
        cities= file.readlines()
        file.seek(0)  

        for city in cities:
            if city.strip():  
                file.write(city)
                full_city = city.strip()  
                view_listbox.insert(END,full_city)  
        file.truncate()

access_bar = Frame(root, bg='#0066CC', height=50)
access_bar.pack(side=TOP, fill=X)

refresh_button = Button(access_bar, text='Refresh', font='calibri 15', borderwidth=0, bg='#0066CC',command=lambda:deffault_city(search_entry.get()))
refresh_button.pack(side=RIGHT, padx=5)

search_button = Button(access_bar, text='Search', font='calibri 15', borderwidth=0, bg='#0066CC',command=weather_data)
search_button.pack(side=RIGHT, padx=5)

search_entry = Entry(access_bar, borderwidth=0, font='Arial 15')
search_entry.pack(side=RIGHT)


forcast_text = Canvas(access_bar, bg='#0066CC', highlightthickness=0, width=150, height=50)
forcast_text.create_text(70, 25, text='Forecast', font='Arial 20 bold')
forcast_text.pack(side=LEFT)

fav_button = Button(access_bar, text='Fav', font='calibri 15', borderwidth=0, bg='#0066CC',command=fav_city)
fav_button.pack(side=RIGHT, padx=20)

view_button = Button(access_bar, text='View', font='calibri 15', borderwidth=0, bg='#0066CC',command=view_favourite)
view_button.pack(side=RIGHT, padx=10)

weather_data_frame = Frame(root, height=20, width=50, bg='#0080FF')
weather_data_frame.pack(side=TOP)

city_name = Label(weather_data_frame, font='Kokila 35', fg='white', bg='#0080FF')
city_name.pack()

temperature_frame = Frame(weather_data_frame, bg='#0080FF')  
temperature_frame.pack()

temperature = Label(temperature_frame, font='Kokila 70', fg='white', bg='#0080FF')
temperature.pack(side=LEFT,padx=5)

celcius_text = Label(temperature_frame, font='Kokila 30', fg='white', bg='#0080FF')
celcius_text.pack(side=LEFT, padx=5)

weather_condition = Label(weather_data_frame, font='Kokila 30', fg='white', bg='#0080FF')
weather_condition.pack()

current_time = Label(weather_data_frame, font='Kokila 15', fg='white', bg='#0080FF')
current_time.pack()

weather_humidity=Frame(weather_data_frame, bg='#0080FF')
weather_humidity.pack()

humidity = Label(weather_humidity, font='Kokila 20',fg='white', bg='#0080FF')
humidity.grid(row=1,column=0)

wind_speed = Label(weather_humidity, font='Kokila 20', fg='white', bg='#0080FF')
wind_speed.grid(row=1,column=1,columnspan=7,sticky=E)

daily_weather_data = Frame(root, bg='#0080FF', height=250)
daily_weather_data.pack(side=BOTTOM, fill=X)
daily_text=Label(daily_weather_data,text='Daily', font='Arial 20 bold',fg='Black',bg='#0080FF')
daily_text.pack(side=TOP)

# lables to print the weather data of next 6 days
def labels(frame,day_date,temperature,humidity,wind_speed,weather):

    daily_day= Label(frame, font='Kokila 20', text=day_date, fg='white', bg='#0080FF')
    daily_day.pack()
    daily_temperature = Label(frame, font='Kokila 20', text=temperature + u'\u00b0', fg='white', bg='#0080FF')
    daily_temperature.pack()
    daily_humidity = Label(frame, font='Kokila 20', text='Humidity '+humidity+'%', fg='white', bg='#0080FF')
    daily_humidity.pack()

    daily_wind_speed = Label(frame, font='Kokila 20', text='Wind '+wind_speed+'Km/hr', fg='white', bg='#0080FF')
    daily_wind_speed.pack()
    daily_weather_condition = Label(frame, font='Kokila 15', text=weather, fg='white', bg='#0080FF')
    daily_weather_condition.pack()

#  Six frames to store all the six days weather data
day1=Frame(daily_weather_data,height=250,bg='#0080FF')
day1.pack(side=LEFT)
day2=Frame(daily_weather_data,height=250,bg='#0080FF')
day2.pack(side=LEFT)
day3=Frame(daily_weather_data,height=250,bg='#0080FF')
day3.pack(side=LEFT)
day4=Frame(daily_weather_data,height=250,bg='#0080FF')
day4.pack(side=LEFT)
day5=Frame(daily_weather_data,height=250,bg='#0080FF')
day5.pack(side=LEFT)
day6=Frame(daily_weather_data,height=250,bg='#0080FF')
day6.pack(side=LEFT,padx=5)

# This is the main function to get all the weather data 
def deffault_city(city):
    global city_name, temperature, weather_condition, humidity, wind_speed, current_time, refresh_button

# Remove refresh button 
    def remove_refresh_button():
        refresh_button.destroy()

# This will delete all the widget from all six frames
    for widget in day1.winfo_children():
        widget.destroy()
    for widget in day2.winfo_children():
        widget.destroy()
    for widget in day3.winfo_children():
        widget.destroy()
    for widget in day4.winfo_children():
        widget.destroy()
    for widget in day5.winfo_children():
        widget.destroy()
    for widget in day6.winfo_children():
        widget.destroy()
    
    try:
        
        Enterted_city = city

        location = geolocator.geocode(Enterted_city) # Gets coordinests of the entered cites
        city_name.config(text=Enterted_city.capitalize())
        url = f'https://api.weatherbit.io/v2.0/forecast/daily?lat={location.latitude}&lon={location.longitude}&days=7&key={api}' # Weatherbit api

        weather_data = requests.get(url).json()

        forecast_data = weather_data['data'] # sorting our only required weather data

        list1 = []

# Appending our weather data to list
        for forecast in forecast_data:
            list1.extend([forecast['valid_date'], forecast['temp'], forecast['rh'], forecast['wind_spd'],forecast['weather']['description']])

#This will configure the day first weather data 
        temperature.config(text=str(int(list1[1])) + u'\u00b0')
        weather_condition.config(text=list1[4])
        humidity.config(text='Humidity ' + str(list1[2]) + '%')
        wind_speed.config(text='Wind ' + str(list1[3]) + 'km/hr',)

        timezone = weather_data["timezone"] # gets the timezone of entered cities from API
        time = pytz.timezone(timezone)
        dt = datetime.now(time) # converts timezone into current time
        current_time.config(text=f"Current time {dt.strftime('%I:%M %p')}") # it will give current time in 12 hour clock with AM/PM

#  To get day of next 6 date from current day
        day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day1_date = list1[5].split('-')[2]
        day2_date = list1[10].split('-')[2]
        day3_date = list1[15].split('-')[2]
        day4_date = list1[20].split('-')[2]
        day5_date = list1[25].split('-')[2]
        day6_date = list1[30].split('-')[2]

#  To get day of next 6 date from current day
        day1_weekday = day[datetime.strptime(list1[5], '%Y-%m-%d').weekday()]
        day2_weekday = day[datetime.strptime(list1[10], '%Y-%m-%d').weekday()]
        day3_weekday = day[datetime.strptime(list1[15], '%Y-%m-%d').weekday()]
        day4_weekday = day[datetime.strptime(list1[20], '%Y-%m-%d').weekday()]
        day5_weekday = day[datetime.strptime(list1[25], '%Y-%m-%d').weekday()]
        day6_weekday = day[datetime.strptime(list1[30], '%Y-%m-%d').weekday()]

# Passes all the perametrs to all the lables to display all six dayes weather data
        labels(day1, f"{day1_weekday} {day1_date}", str(int(list1[6])), str(list1[7]), str(list1[8]), list1[9])
        labels(day2, f"{day2_weekday} {day2_date}", str(int(list1[11])), str(list1[12]), str(list1[13]), list1[14])
        labels(day3, f"{day3_weekday} {day3_date}", str(int(list1[16])), str(list1[17]), str(list1[18]), list1[19])
        labels(day4, f"{day4_weekday} {day4_date}", str(int(list1[21])), str(list1[22]), str(list1[23]), list1[24])
        labels(day5, f"{day5_weekday} {day5_date}", str(int(list1[26])), str(list1[27]), str(list1[28]), list1[29])
        labels(day6, f"{day6_weekday} {day6_date}", str(int(list1[31])), str(list1[32]), str(list1[33]), list1[34])

# Handle error aries from API 
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "An error occurred while retrieving weather data. Please check your internet connection.")


    except (KeyError, IndexError):
        messagebox.showerror("Error", "Unable to fetch weather data for the specified city.")


# Handle error aries from geocoder due to network issue
    except geopy.exc.GeocoderUnavailable:
        messagebox.showerror("Error", " Unavailable to fetch. Please check your internet connection.")

# Check weather city name is correct or a empty search
    except (AttributeError, KeyError):
        messagebox.showerror("Error","Please enter valid city")

deffault_city('indore')

root.mainloop()
