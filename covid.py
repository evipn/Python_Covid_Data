
import requests
import pandas
import matplotlib.pyplot as plt
import xlrd
import mysql.connector
import io
import tkinter as tk
from tkinter import ttk

# URL of the CSV 
url = 'https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv'

# Retrieve the CSV file with get
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Get the CSV data 
    csv_data = response.content.decode('utf-8')
    # Convert the CSV data to a pandas DataFrame
    Df = pandas.read_csv(io.StringIO(csv_data))
    Df['Date'] = pandas.to_datetime(Df['Date'], format='%d/%m/%Y')
    Df['Month'] = Df['Date'].dt.month
    Df['Direction'] = Df['Direction'].astype('category')
    Df['Year'] = Df['Date'].dt.year.astype('category')
    Df['DayOfWeek'] = Df['Date'].dt.day_name().astype('category')
    Df['Country'] = Df['Country'].astype('category')
    Df['Commodity'] = Df['Commodity'].astype('category')
    Df['Transport_Mode'] = Df['Transport_Mode'].astype('category')
    Df['Measure'] = Df['Measure'].astype('category')
    Df['Value'] = Df['Value'].astype('int64')

    
    # Create the turnovers
    monthly_turnover = Df.groupby(['Month' , 'Measure'])['Value'].sum()
    
    turnover_per_country = Df.groupby(['Country' , 'Measure'])['Value'].sum()
    
    transport_turnover = Df.groupby(['Transport_Mode' , 'Measure'])['Value'].sum()
    
    daily_turnover = Df.groupby(['DayOfWeek' , 'Measure'])['Value'].sum()
    
    commodity_turnover = Df.groupby(['Commodity' , 'Measure'])['Value'].sum()
    
    top_five_months = Df.groupby('Month')['Value'].sum().nlargest(5)
    
    country_commodity_turnover = Df.groupby(['Country', 'Commodity'])['Value'].sum()
    
    top_day_per_commodity = Df.groupby(['DayOfWeek', 'Commodity'])['Value'].sum()
    top_day_turnover = top_day_per_commodity.groupby('Commodity').idxmax()
    top_day_final = top_day_per_commodity.loc[top_day_turnover]
    top_day_final = top_day_final.reset_index()
    
    # Make the GUI
    window = tk.Tk()
    
    GUI_COLOR = '#FFB6C1'  # Light pink 
    window.configure(bg=GUI_COLOR)
    
    # Create list of plot options for the menu
    plot_options = [
        'Total Turnover by Month',
        'Total Turnover by Country',
        'Total Turnover by Means of Transport',
        'Total Turnover by Day of the Week',
        'Total Turnover by Category of Goods',
        'Top 5 Months with Highest Turnover',
        'Top 5 Categories of Goods with Highest Turnover by Country',
        'Day with Highest Turnover by Category'
    ]

    # Function to select which plot the user wants
    def generate_plot(plot):
        # Plots
        if plot == 'Total Turnover by Month':
            monthly_turnover.plot(kind='bar')
            plt.yscale('log')
            plt.title('Total Turnover by Month')
            plt.xlabel('Month')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Total Turnover by Country':
            turnover_per_country.plot(kind='bar')
            plt.yscale('log')
            plt.title('Total Turnover by Country')
            plt.xlabel('Country')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Total Turnover by Means of Transport':
            transport_turnover.plot(kind='bar')
            plt.yscale('log')
            plt.title('Total Turnover by Means of Transport')
            plt.xlabel('Means of Transport')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Total Turnover by Day of the Week':
            daily_turnover.plot(kind='bar')
            plt.yscale('log')
            plt.title('Total Turnover by Day of the Week')
            plt.xlabel('Day of the Week')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Total Turnover by Category of Goods':
            commodity_turnover.plot(kind='bar')
            plt.yscale('log')
            plt.title('Total Turnover by Category of Goods')
            plt.xlabel('Category of Goods')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Top 5 Months with Highest Turnover':
            top_five_months.plot(kind='bar')
            plt.title('Top 5 Months with Highest Turnover')
            plt.xlabel('Month')
            plt.ylabel('Turnover')
            plt.show()

        elif plot == 'Top 5 Categories of Goods with Highest Turnover by Country':
            for country in Df['Country'].unique():
                top_categories_of_goods = country_commodity_turnover[country].nlargest(5)
                top_categories_of_goods.plot(kind='bar')
                plt.title(f'Top 5 Categories of Goods with Highest Turnover in {country}')
                plt.xlabel('Category')
                plt.ylabel('Turnover')
                plt.show()
            
        elif plot == 'Day with Highest Turnover by Category': 
            #used str because + ',' + gets error
            plt.bar(top_day_final['DayOfWeek'].str.cat(top_day_final['Commodity'], sep=', '), top_day_final['Value'])
            plt.yscale('log')
            plt.title('Day with Highest Turnover by Category')
            plt.xticks(rotation=90)
            plt.xlabel('Day of The Week - Commodity')
            plt.ylabel('Turnover')
            plt.show()



    for plot in plot_options:
        button = ttk.Button(window, text=plot, command=lambda p=plot: generate_plot(p), style='Custom.TButton')
        button.configure(style='Custom.TButton')
        button.pack(pady=5)

    style = ttk.Style()
    style.configure('Custom.TButton', background=GUI_COLOR)

    title_label = tk.Label(window, text="Menu", font=("Arial", 16), bg=GUI_COLOR)
    title_label.pack(pady=10)
    
    # Keep the window open until user closes it
    window.mainloop()
    
    # Make connection with sql
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345',
        database='coviddata'
    )
    
    # Create cursor for SQL
    cursor = connection.cursor()
    
    # Take data from URL to SQL
    response = requests.get(url)3
    

    # Convert data to CSV files
    monthly_turnover.to_csv('monthly_turnover.csv')
    turnover_per_country.to_csv('turnover_per_country.csv')
    transport_turnover.to_csv('transport_turnover.csv')
    daily_turnover.to_csv('daily_turnover.csv')
    commodity_turnover.to_csv('commodity_turnover.csv')
    top_five_months.to_csv('top_five_months.csv')
    country_commodity_turnover.to_csv('country_commodity_turnover.csv')
    top_day_final.to_csv('top_day_final.csv')
        
    
    # Insert data into the monthly_turnover table
    for (month, measure), turnover in monthly_turnover.items():
        sql = "INSERT INTO monthly_turnover (month, measure, turnover) VALUES (%s, %s, %s)"
        values = (month, measure, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the turnover_per_country table
    for (country, measure), turnover in turnover_per_country.items():
        sql = "INSERT INTO turnover_per_country (country, measure, turnover) VALUES (%s, %s, %s)"
        values = (country, measure, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the transport_turnover table
    for (transport_mode, measure), turnover in transport_turnover.items():
        sql = "INSERT INTO transport_turnover (transport_mode, measure, turnover) VALUES (%s, %s, %s)"
        values = (transport_mode, measure, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the daily_turnover table
    for (day, measure), turnover in daily_turnover.items():
        sql = "INSERT INTO daily_turnover (day, measure, turnover) VALUES (%s, %s, %s)"
        values = (day, measure, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the commodity_turnover table
    for (category, measure), turnover in commodity_turnover.items():
        sql = "INSERT INTO commodity_turnover (category, measure, turnover) VALUES (%s, %s, %s)"
        values = (category, measure, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the top_five_months table
    for month, turnover in top_five_months.items():
        sql = "INSERT INTO top_five_months (month, turnover) VALUES (%s, %s)"
        values = (month, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the country_commodity_turnover table
    for (country, category), turnover in country_commodity_turnover.items():
        sql = "INSERT INTO country_commodity_turnover (country, category, turnover) VALUES (%s, %s, %s)"
        values = (country, category, turnover)
        cursor.execute(sql, values)
    connection.commit()

    # Insert data into the top_day_turnover table
    for index, row in top_day_final.iterrows():
        day = row['DayOfWeek']
        category = row['Commodity']
        turnover = row['Value']
        sql = "INSERT INTO top_day_final (day, category, turnover) VALUES (%s, %s, %s)"
        values = (day, category, turnover)
        cursor.execute(sql, values)
    connection.commit()

else:
    # Print an error message if the request failed
    print('Failed to retrieve the CSV file.')
