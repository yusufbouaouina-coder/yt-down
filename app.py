'''
Climate Application:

Author: @Carlos Raniel Ariate Arro
Co-Author(s): @Zain Azrak @Yusuf Bouaouina

Description:

This application is a desktop-based version of the Heat Stress Index (HSI) system developed to analyse environmental conditions in a desert climate. 
The program allows users to input daily temperature and humidity values, automatically calculates the Heat Stress Index using a predefined scientific formula, 
and classifies each day into a corresponding risk level.
The system is implemented using the Dear PyGui library, providing an interactive graphical user interface for efficient data entry and real-time visual feedback. 
Compared to the console version, this desktop application improves usability, accessibility, and overall user experience through a structured and user-friendly interface.
The application also enables users to view calculated results, track daily records, and analyse trends such as average heat stress levels and extreme conditions.
This project builds upon a previously developed console application by extending its functionality into a fully interactive desktop environment.
'''

#import
import dearpygui.dearpygui as dpg
import sys
dpg.create_context()
dpg.create_viewport(title = "Heat Stress Index Research App", width=600,height=300)
#temporary storage 
measurements = []

with dpg.theme() as my_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 0, 0))  # red text
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)  # rounded corners

#class to contain data in one value
class measurement():
    def __init__(self, day, temperature, humidity, hsi=0, RL="unknown"):
        self.day = day
        self.temperature = temperature
        self.humidity = humidity
        self.hsi = hsi

    def checklevel(self, hsi):
        if self.hsi < 40:
            self.RL = "Safe"
        elif self.hsi > 40 and self.hsi <= 59.9:
            self.RL = "Caution"
        elif self.hsi > 60 and self.hsi <= 79.9:
            self.RL = "Danger"
        else:
            self.RL = "Extreme"
        return self.RL

#procedure to add into the measurements list
def DataInput():
    day = dpg.get_value("day")
    temperature = dpg.get_value("temp")
    humidity = dpg.get_value("humidity")
    hsi = (0.7 * temperature) + (0.2 * humidity)
    grouped = measurement(day,temperature,humidity,hsi)
    grouped.checklevel(hsi)
    measurements.append(grouped)
    print("Value has been entered")

    # < 40 = safe, between 40 and 59.9 = caution, 60 and 79.9 = danger, and 80 or above = extreme

#procedure to put readings into a csv file
def putInfile(dataReadings):
    if dataReadings == []:
        print("Error cannot empty data readings")


#procedure to open the data entry window
def open_data_entry():

    if dpg.does_item_exist("Data Entry"):
        dpg.delete_item("Data Entry")
    with dpg.window(tag="data_entry_window",label="Data Entry",width = 400,height=350,pos=[100,50]):
        dpg.add_text("Enter heat stress data.")
        dpg.add_separator()
        dpg.add_text("Day No.",)
        dpg.add_input_int(tag="day")
        dpg.add_text("Temperature")
        dpg.add_input_float(tag="temp")
        dpg.add_text("Humidity")
        dpg.add_input_float(min_value=0.0,tag="humidity")
        submit_btn = dpg.add_button(label="Yusuf wants to add something",callback=DataInput)

#procedure to open view_data window
def view_data():
    #mock data:
    data = [
    [1, 34, 45, 72, "High"],
    [2, 30, 55, 60, "Moderate"],
    [3, 28, 65, 48, "Low"],
    [4, 36, 40, 80, "Very High"],
    [5, 33, 50, 68, "High"],
    [6, 27, 70, 42, "Low"],
    [7, 31, 58, 62, "Moderate"],
    [8, 35, 43, 77, "High"],
    [9, 29, 60, 52, "Moderate"],
    [10, 37, 38, 85, "Very High"],
    [11, 32, 52, 66, "High"],
    [12, 26, 75, 40, "Low"],
    [13, 34, 47, 71, "High"],
    [14, 30, 57, 59, "Moderate"]
]
    
    if dpg.does_item_exist("data_view_window"):
        dpg.delete_item("data_view_window")

    with dpg.window(tag="data_view_window", label="Data View", width=400, height=350, pos=[100, 50]):
        dpg.add_text("Data View")
        
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Day No.")
            dpg.add_table_column(label="Temperature")
            dpg.add_table_column(label="Humidity")
            dpg.add_table_column(label="HSI")
            dpg.add_table_column(label="Risk Level")

            for i in range(0,len(data)):
                with dpg.table_row():
                    for j in range(0,len(data[i])):
                        dpg.add_text(f"{data[i][j]}")

            

def center_text(item):
    parent = dpg.get_item_parent(item)
    pw = dpg.get_item_width(parent)
    iw = dpg.get_item_rect_size(item)[0]
    dpg.set_cursor_pos_x((pw-iw)//2)



#procedure to close the program
def exit():
    sys.exit("Exiting")
''
#main window
with dpg.window(tag="Window1"):
    dpg.add_text("HSI system")
    button1 = dpg.add_button(label="Data Entry",callback=open_data_entry,)
    button2 = dpg.add_button(label="Data View",callback=view_data)
    #exit button
    button3 = dpg.add_button(label="Exit",callback=exit,user_data="Value is passed")


dpg.bind_theme(my_theme)
#dearpygui structure - DO NOT DELETE/EDIT
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Window1",True) #keeps it in a singular one
dpg.start_dearpygui()
dpg.destroy_context()
