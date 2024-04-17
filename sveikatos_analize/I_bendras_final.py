import pandas as pd
import matplotlib.pyplot as plt


def df_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    return df

def bendras_indeksas(df):
    years_1980_1985 = df[(df['year'] >= 1980) & (df['year'] <= 1985)]
    years_1990_1995 = df[(df['year'] >= 1990) & (df['year'] <= 1995)]
    years_2000_2005 = df[(df['year'] >= 2000) & (df['year'] <= 2005)]
    years_2010_2013 = df[(df['year'] >= 2010) & (df['year'] <= 2013)]
    median_1980_1985 = years_1980_1985['value'].mean().round(2)
    median_1990_1995 = years_1990_1995['value'].mean().round(2)
    median_2000_2005 = years_2000_2005['value'].mean().round(2)
    median_2010_2013 = years_2010_2013['value'].mean().round(2)
    bendras_indeksas = [['1980-1985', median_1980_1985], ['1990_1995', median_1990_1995],
                        ['2000-2005', median_2000_2005], ['2010-2013', median_2010_2013]]
    bendro_indekso_df = pd.DataFrame(bendras_indeksas, columns=['Metai', 'vidutinis indeksas'])
    print('Bendras visų šalių sveikatos indeksas\n', bendro_indekso_df)
    return bendro_indekso_df


def baltijos_saliu_indeksas(df):
    baltijos_salys = df[(df['country'] == 'Lithuania') | (df['country'] == 'Latvia') | (df['country'] == 'Estonia')]
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
    baltijos_saliu_indekso_df.rename(columns={'Estonia': 'Estija', 'Latvia': 'Latvija', 'Lithuania': 'Lietuva'},
                                     inplace=True)
    print('\nBaltijos šalių sveikatos indeksas\n', baltijos_saliu_indekso_df)
    baltijos_saliu_indekso_df.to_csv('baltijos.csv')
    return baltijos_saliu_indekso_df


def skandinavijos_saliu_indeksas(df):
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
    print('\nSkandinavijos šalių sveikatos indeksas\n', skandinavijos_saliu_indekso_df)
    return skandinavijos_saliu_indekso_df


def sveikatos_indeksu_grafikas(skandinavijos_saliu_indekso_df, baltijos_saliu_indekso_df):
    plt.figure(figsize=(14, 8))
    plt.plot(skandinavijos_saliu_indekso_df, label=['Danija', 'Norvegija', 'Švedija'])
    plt.plot(baltijos_saliu_indekso_df, label=['Estija', 'Latvija', 'Lietuva'])
    plt.title('Sveikatos indekso vidurkio tendencijos')
    plt.xlabel('Laikotarpiai')
    plt.ylabel('Sveikatos indekso vidurkis')
    plt.legend()
    plt.show()


def sveikatos_indekso_top_salys(df):
    median_by_country = df.groupby('country')['value'].mean().round(2)
    top_five = median_by_country.nlargest(5)
    worst_five = median_by_country.nsmallest(5)
    print(f'\nAukščiausi HDI:\n{top_five}')
    print(f'\nŽemiausi HDI:\n{worst_five}')
    return top_five, worst_five

def koreliacijos(df):
    bendrakoreliacija = df['year'].corr(df['value']).round(2)
    baltijos_saliu_indeksai = df.loc[(df['country'] == 'Lithuania') | (df['country'] == 'Latvia')
                                     | (df['country'] == 'Estonia')]
    baltijos_saliu_koreliacija = baltijos_saliu_indeksai['year'].corr(baltijos_saliu_indeksai['value']).round(2)
    skandinavijos_saliu_indeksai = df.loc[(df['country'] == 'Sweden') | (df['country'] == 'Norway')
                                          | (df['country'] == 'Denmark')]
    skandinavijos_saliu_koreliacija = (skandinavijos_saliu_indeksai['year'].corr(skandinavijos_saliu_indeksai['value']).
                                       round(2))
    koreliacijos = [['Baltijos šalys', baltijos_saliu_koreliacija],
                    ['Skandinavijos šalys', skandinavijos_saliu_koreliacija], ['Visų šalių', bendrakoreliacija]]
    koreliaciju_df = pd.DataFrame(koreliacijos, columns=['Regionas', 'Koreliacija'])
    koreliaciju_df.set_index('Regionas', inplace=True)
    print('\nKoreliacija - sveikatos indekso priklausomybė nuo metų:\n', koreliaciju_df)
    return koreliaciju_df

def indeksu_pokyciu_grafikas(df):
    bendras_saliu_pokytis = df.groupby('year')['value'].mean().round(2).pct_change()
    plt.figure(figsize=(14, 8))
    plt.plot(bendras_saliu_pokytis)
    plt.title('Sveikatos indekso pokyčio tendencijos')
    plt.xlabel('Metai')
    plt.ylabel('Pokytis proc.')
    plt.show()


def baltijos_indekso_grafikas(baltijos):
    plt.figure(figsize=(20, 12))
    baltijos.plot(kind='bar', label=['Estija', 'Latvija', 'Lietuva'])
    plt.title('Baltijos šalių sveikatos indekso vidurkiai')
    plt.xlabel('Laikotarpis')
    plt.ylabel('Sveikatos indekso vidurkis')
    plt.xticks(rotation=0)
    plt.show()


def main():
    csv_file = 'health-index-1.csv'
    df = df_from_csv(csv_file)
    bendras_indeksas(df)
    baltijos = baltijos_saliu_indeksas(df)
    skandinavijos = skandinavijos_saliu_indeksas(df)
    sveikatos_indeksu_grafikas(skandinavijos, baltijos)
    sveikatos_indekso_top_salys(df)
    koreliacijos(df)
    indeksu_pokyciu_grafikas(df)
    baltijos_indekso_grafikas(baltijos)

if __name__ == '__main__':
    main()
