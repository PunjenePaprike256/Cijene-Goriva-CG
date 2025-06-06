import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

# Dohvati cijene goriva s web stranice
def get_fuel_prices():
    url = 'https://nafta.hr/sr/cene-goriva-crna-gora/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pronađi cijene goriva
    prices = {
        'Eurodizel': float(soup.find(text='Eurodizel').find_next('td').text.split('€')[0].strip()),
        'BMB 95': float(soup.find(text='Benzin BMB 95').find_next('td').text.split('€')[0].strip()),
        'BMB 98': float(soup.find(text='Benzin BMB 98').find_next('td').text.split('€')[0].strip())
    }
    return prices

# Izračunaj trošak puta
def calculate_trip_cost():
    try:
        distance = float(entry_distance.get())
        fuel_consumption = float(entry_consumption.get())
        fuel_type = fuel_var.get()

        if fuel_type == 'Eurodizel':
            price_per_liter = fuel_prices['Eurodizel']
        elif fuel_type == 'BMB 95':
            price_per_liter = fuel_prices['BMB 95']
        else:
            price_per_liter = fuel_prices['BMB 98']

        total_fuel_needed = (distance / 100) * fuel_consumption
        total_cost = total_fuel_needed * price_per_liter

        label_result.config(text=f"Trošak puta: {total_cost:.2f} €")
    except ValueError:
        messagebox.showerror("Greška", "Molimo unesite valjane brojeve.")

# Dohvati cijene goriva
fuel_prices = get_fuel_prices()

# Postavi glavni prozor
root = tk.Tk()
root.title("Kalkulator troška goriva")

# Unos udaljenosti
label_distance = tk.Label(root, text="Udaljenost (km):")
label_distance.pack()
entry_distance = tk.Entry(root)
entry_distance.pack()

# Unos potrošnje goriva
label_consumption = tk.Label(root, text="Potrošnja goriva (l/100km):")
label_consumption.pack()
entry_consumption = tk.Entry(root)
entry_consumption.pack()

# Odabir vrste goriva
label_fuel_type = tk.Label(root, text="Vrsta goriva:")
label_fuel_type.pack()
fuel_var = tk.StringVar(value='Eurodizel')
fuel_options = ['Eurodizel', 'BMB 95', 'BMB 98']
for fuel in fuel_options:
    tk.Radiobutton(root, text=fuel, variable=fuel_var, value=fuel).pack()

# Izračunaj dugme
button_calculate = tk.Button(root, text="Izračunaj trošak", command=calculate_trip_cost)
button_calculate.pack()

# Rezultat
label_result = tk.Label(root, text="Trošak puta: 0.00 €")
label_result.pack()

# Pokreni aplikaciju
root.mainloop()
