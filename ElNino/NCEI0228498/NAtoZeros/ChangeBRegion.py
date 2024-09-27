import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data\Processed_Zero_Coral_Bleaching_Database.csv")

data['MIN_PERCENT_BLEACHED'] = pd.to_numeric(data['MIN_PERCENT_BLEACHED'], errors='coerce')
data['MAX_PERCENT_BLEACHED'] = pd.to_numeric(data['MAX_PERCENT_BLEACHED'], errors='coerce')



regional_min_max_bleaching = data.groupby(['COUNTRY', 'YEAR']).agg({
    'MIN_PERCENT_BLEACHED': 'mean',
    'MAX_PERCENT_BLEACHED': 'mean'
}).reset_index()

selected_countries = ['Australia', 'Fiji', 'Indonesia']

regional_selected = regional_min_max_bleaching[regional_min_max_bleaching['COUNTRY'].isin(selected_countries)]

plt.figure(figsize=(10, 6))

for country in selected_countries:
    country_data = regional_selected[regional_selected['COUNTRY'] == country]
    
    plt.plot(country_data['YEAR'], country_data['MIN_PERCENT_BLEACHED'], label=f'{country} Min Percent Bleached')
    
    plt.plot(country_data['YEAR'], country_data['MAX_PERCENT_BLEACHED'], label=f'{country} Max Percent Bleached', linestyle='--')

plt.title('Regional Change in Min and Max Coral Bleaching Percent Over Time')
plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.legend()
plt.grid(True)

plt.show()
