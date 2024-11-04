import pandas as pd

class OilPriceAnalysis:
    def __init__(self, oil_prices_file, inflation_file, gdp_file, unemployment_file):
        # Load the datasets
        self.oil_prices = pd.read_csv(oil_prices_file, parse_dates=['Date'], dayfirst=True)
        self.inflation = pd.read_csv(inflation_file, parse_dates=['Date'], dayfirst=True)
        self.gdp = pd.read_csv(gdp_file, parse_dates=['DATE'])
        self.unemployment = pd.read_csv(unemployment_file, parse_dates=['Date'], dayfirst=True)
        self.data = None

    def preprocess_data(self):
        # Process and resample oil prices to annual average to match other data frequency
        self.oil_prices['Year'] = self.oil_prices['Date'].dt.year

        # Ensure 'Price' column is numeric, coerce any non-numeric values to NaN
        self.oil_prices['Price'] = pd.to_numeric(self.oil_prices['Price'], errors='coerce')

        # Group by 'Year' and calculate the mean, ignoring NaNs
        annual_oil = self.oil_prices.groupby('Year', as_index=False)['Price'].mean()

        # Align dates and create a unified dataset
        self.inflation['Year'] = self.inflation['Date'].dt.year
        self.unemployment['Year'] = self.unemployment['Date'].dt.year
        self.gdp['Year'] = self.gdp['DATE'].dt.year

        # Merge all datasets on 'Year'
        self.data = pd.merge(annual_oil[['Year', 'Price']], self.inflation[['Year', 'Inflation Rate']], on='Year')
        self.data = pd.merge(self.data, self.gdp[['Year', 'GDP']], on='Year')
        self.data = pd.merge(self.data, self.unemployment[['Year', 'Unemployment Rate']], on='Year')

        # Drop NA values in case there are missing rows
        self.data.dropna(inplace=True)