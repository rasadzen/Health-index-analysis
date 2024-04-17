import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = pd.read_csv('health-index-1.csv')



def atnaujinti_grafika():

    #Rdio button pasirinkimas
    if pasirinkimas.get() == "Sveikatos indeksų tendencijos":
        
        baltijos_salys = df.loc[(df['country'] == 'Lithuania') | (df['country'] == 'Latvia') | (df['country'] == 'Estonia')]
        laikotarpis_1980_1985 = baltijos_salys[(baltijos_salys['year'] >= 1980) & (baltijos_salys['year'] <= 1985)]
        laikotarpis_1990_1995 = baltijos_salys[(baltijos_salys['year'] >= 1990) & (baltijos_salys['year'] <= 1995)]
        laikotarpis_2000_2005 = baltijos_salys[(baltijos_salys['year'] >= 2000) & (baltijos_salys['year'] <= 2005)]
        laikotarpis_2010_2013 = baltijos_salys[(baltijos_salys['year'] >= 2010) & (baltijos_salys['year'] <= 2013)]

        baltijos_saliu_indekso_vidurkis_1980_1985 = laikotarpis_1980_1985.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_1990_1995 = laikotarpis_1990_1995.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_2000_2005 = laikotarpis_2000_2005.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_2010_2013 = laikotarpis_2010_2013.groupby('country')['value'].mean().round(2)


        skandinavijos_salys = df.loc[(df['country'] == 'Denmark') | (df['country'] == 'Sweden') | (df['country'] == 'Norway')]
        periodas_1980_1985 = skandinavijos_salys[(skandinavijos_salys['year'] >= 1980) & (skandinavijos_salys['year'] <= 1985)]
        periodas_1990_1995 = skandinavijos_salys[(skandinavijos_salys['year'] >= 1990) & (skandinavijos_salys['year'] <= 1995)]
        periodas_2000_2005 = skandinavijos_salys[(skandinavijos_salys['year'] >= 2000) & (skandinavijos_salys['year'] <= 2005)]
        periodas_2010_2013 = skandinavijos_salys[(skandinavijos_salys['year'] >= 2010) & (skandinavijos_salys['year'] <= 2013)]

        saliu_indekso_vidurkis_1980_1985 = periodas_1980_1985.groupby('country')['value'].mean().round(2)
        saliu_indekso_vidurkis_1990_1995 = periodas_1990_1995.groupby('country')['value'].mean().round(2)
        saliu_indekso_vidurkis_2000_2005 = periodas_2000_2005.groupby('country')['value'].mean().round(2)
        saliu_indekso_vidurkis_2010_2013 = periodas_2010_2013.groupby('country')['value'].mean().round(2)
        

        skand1 = pd.merge(saliu_indekso_vidurkis_1980_1985, saliu_indekso_vidurkis_1990_1995, on='country')
        skand2 = pd.merge(saliu_indekso_vidurkis_2000_2005, saliu_indekso_vidurkis_2010_2013, on='country')
        skandinavijos_saliu_indekso_df = pd.merge(skand1, skand2, on='country').transpose()
        skandinavijos_saliu_indekso_df.rename(index={'value_x_x': '1980-1985', 'value_y_x': '1990-1995',
                                                    'value_x_y': '2000-2005', 'value_y_y': '2010-2013'}, inplace=True)
        skandinavijos_saliu_indekso_df.rename(columns={'Denmark': 'Danija', 'Norway': 'Norvegija',
                                                    'Sweden': 'Švedija'}, inplace=True)
        

        balt1 = pd.merge(baltijos_saliu_indekso_vidurkis_1980_1985, baltijos_saliu_indekso_vidurkis_1990_1995, on='country')
        balt2 = pd.merge(baltijos_saliu_indekso_vidurkis_2000_2005, baltijos_saliu_indekso_vidurkis_2010_2013, on='country')
        baltijos_saliu_indekso_df = pd.merge(balt1, balt2, on='country').transpose()
        baltijos_saliu_indekso_df.rename(index={'value_x_x': '1980-1985', 'value_y_x': '1990-1995', 'value_x_y': '2000-2005',
                                                'value_y_y': '2010-2013'}, inplace=True)
        baltijos_saliu_indekso_df.rename(columns={'Estonia': 'Estija', 'Latvia': 'Latvija', 'Lithuania': 'Lietuva'},
                                        inplace=True)

        ax.clear()
        ax.plot(skandinavijos_saliu_indekso_df, label=['Danija', 'Norvegija', 'Švedija'])
        ax.plot(baltijos_saliu_indekso_df, label=['Estija', 'Latvija', 'Lietuva'])
        ax.set_title('Sveikatos indekso vidurkio tendencijos')
        ax.set_xlabel('Laikotarpiai')
        ax.set_ylabel('Sveikatos indekso vidurkis')
        ax.legend(loc='upper left')
        canvas.draw()

    
                
    elif pasirinkimas.get() == "Aukščiausi-žemiausi HDI":

        median_by_country = df.groupby('country')['value'].mean()
        
        top_five = median_by_country.nlargest(5)
        worst_five = median_by_country.nsmallest(5)
        top_five.rename(index={'Hong Kong China (SAR)': 'Hong Kong'}, inplace=True)
        worst_five.rename(index={'Central African Republic': 'CAR','Congo (Democratic Republic of the)': 'DRC'}, inplace=True)

        # Bar chartas penkiem geriausiam ir blogiausiam HDI
        ax.clear()
        ax.bar(top_five.index, top_five.values, color='green', label='Aukščiausias indeksas')
        ax.bar(worst_five.index, worst_five.values, color='red', label='Žemiausias indeksas')
        ax.set_ylabel('Vidutinis HDI')
        ax.set_title('Aukščiausi ir žemiausi sveikatos indeksai 1985-2013')
        ax.legend()
       
        ax.set_xticklabels(top_five.index.append(worst_five.index), rotation=25, fontsize=10)

        canvas.draw()
    
    elif pasirinkimas.get() == "Sveikatos indekso pokyčių tendencijos":

        baltijos_saliu_indeksai = df.loc[(df['country'] == 'Lithuania') | (df['country'] == 'Latvia')
                                 | (df['country'] == 'Estonia')]

        skandinavijos_saliu_indeksai = df.loc[(df['country'] == 'Sweden') | (df['country'] == 'Norway')
                                            | (df['country'] == 'Denmark')]
        
        bendras_saliu_pokytis = df.groupby('year')['value'].mean().round(2).pct_change()
        baltijos_saliu_pokytis = baltijos_saliu_indeksai.groupby('year')['value'].mean().round(2).pct_change()
        skandinavijos_saliu_pokytis = (skandinavijos_saliu_indeksai.groupby('year')['value'].mean().round(2).pct_change()) * 100
        
        ax.clear()
        ax.plot(bendras_saliu_pokytis, label='Visų šalių')
        ax.plot(baltijos_saliu_pokytis, label='Baltijos šalių')
        ax.plot(skandinavijos_saliu_pokytis, label='Skandinavijos šalių')
        ax.set_xlabel('Metai')
        ax.set_ylabel('Pokytis proc.')
        ax.set_title('Sveikatos indekso pokyčio tendencijos')
        ax.legend(loc='upper left')
        canvas.draw()


    elif pasirinkimas.get() == "Baltijos šalių sveikatos indekso vidurkis":

        baltijos_salys = df.loc[(df['country'] == 'Lithuania') | (df['country'] == 'Latvia') | (df['country'] == 'Estonia')]

        laikotarpis_1980_1985 = baltijos_salys[(baltijos_salys['year'] >= 1980) & (baltijos_salys['year'] <= 1985)]
        laikotarpis_1990_1995 = baltijos_salys[(baltijos_salys['year'] >= 1990) & (baltijos_salys['year'] <= 1995)]
        laikotarpis_2000_2005 = baltijos_salys[(baltijos_salys['year'] >= 2000) & (baltijos_salys['year'] <= 2005)]
        laikotarpis_2010_2013 = baltijos_salys[(baltijos_salys['year'] >= 2010) & (baltijos_salys['year'] <= 2013)]

        baltijos_saliu_indekso_vidurkis_1980_1985 = laikotarpis_1980_1985.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_1990_1995 = laikotarpis_1990_1995.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_2000_2005 = laikotarpis_2000_2005.groupby('country')['value'].mean().round(2)
        baltijos_saliu_indekso_vidurkis_2010_2013 = laikotarpis_2010_2013.groupby('country')['value'].mean().round(2)

        balt1 = pd.merge(baltijos_saliu_indekso_vidurkis_1980_1985, baltijos_saliu_indekso_vidurkis_1990_1995, on='country')
        balt2 = pd.merge(baltijos_saliu_indekso_vidurkis_2000_2005, baltijos_saliu_indekso_vidurkis_2010_2013, on='country')
        baltijos_saliu_indekso_df = pd.merge(balt1, balt2, on='country').transpose()
        baltijos_saliu_indekso_df.rename(index={'value_x_x': '1980-1985', 'value_y_x': '1990-1995', 'value_x_y': '2000-2005',
                                                'value_y_y': '2010-2013'}, inplace=True)

        baltijos_saliu_indekso_df = pd.merge(balt1, balt2, on='country').transpose()
        baltijos_saliu_indekso_df.rename(index={'value_x_x': '1980-1985', 'value_y_x': '1990-1995', 'value_x_y': '2000-2005',
                                                'value_y_y': '2010-2013'}, inplace=True)
        baltijos_saliu_indekso_df.rename(columns={'Estonia': 'Estija', 'Latvia': 'Latvija', 'Lithuania': 'Lietuva'},
                                        inplace=True)


        ax.clear()
        baltijos_saliu_indekso_df.plot(kind='bar', ax=ax)

        ax.set_title('Baltijos šalių sveikatos indekso vidurkiai')
        ax.set_xlabel('Laikotarpiai')
        ax.set_ylabel('Sveikatos indekso vidurkis')
        ax.set_xticklabels(baltijos_saliu_indekso_df.index, rotation=0)

        ax.legend(title='Šalys', labels=['Estija', 'Latvija', 'Lietuva'], loc='upper left')
        canvas.draw()

     

#TKINTER 
root = tk.Tk()
root.title("HDI Analizė")
root.geometry("800x950")


pasirinkimas = tk.StringVar()
pasirinkimas.set("Visos šalys")

# Radio button frame'as
radio_frame = ttk.Frame(root)
radio_frame.grid(row=1, column=0, columnspan=4)

ttk.Label(radio_frame, text="Pasirinkite Metų Intervalą:", font=('Helvetica', 16, 'bold'), padding=(5, 5)).grid(row=0, column=0, columnspan=2)
ttk.Radiobutton(radio_frame, text="Sveikatos indeksų tendencijos", variable=pasirinkimas, value="Sveikatos indeksų tendencijos").grid(row=2, column=0, sticky="w")
ttk.Radiobutton(radio_frame, text="Aukščiausi ir žemiausi indeksai globaliai", variable=pasirinkimas, value="Aukščiausi-žemiausi HDI").grid(row=2, column=1, sticky="w")
ttk.Radiobutton(radio_frame, text="Sveikatos indekso pokyčių tendencijos", variable=pasirinkimas, value="Sveikatos indekso pokyčių tendencijos").grid(row=3, column=0, sticky="w")
ttk.Radiobutton(radio_frame, text="Baltijos šalių sveikatos indekso vidurkis", variable=pasirinkimas, value="Baltijos šalių sveikatos indekso vidurkis").grid(row=3, column=1, sticky="w")


atnaujinti_mygtukas = ttk.Button(root, text="Atnaujinti Grafiką", padding=(5, 5), command=atnaujinti_grafika)
atnaujinti_mygtukas.grid(row=3, columnspan=2, padx=5, pady=20)

fig = plt.Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, columnspan=2)
canvas.get_tk_widget().configure(width=800, height=800)

atnaujinti_grafika()
root.mainloop()

