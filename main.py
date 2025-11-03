
import pandas as pd
import matplotlib.pyplot as plt

#Loading the dataset
data = pd.read_csv('archive/GlobalLandTemperaturesByCity.csv')
df = pd.DataFrame(data)
df_before_cleaning = df.copy()

#Missing Values Analysis before cleaning
print("---------------------- Dataset Information ----------------------")
print(df.info())
print(df.head())
print("df.shape: ", df.shape)

print("---------------------- Outlier Analysis ----------------------")
print(f"Max temperature before cleaning: {df_before_cleaning['AverageTemperature'].max():.2f}°C")
print(f"Min temperature before cleaning: {df_before_cleaning['AverageTemperature'].min():.2f}°C")

#Handling date column
print("Converting 'dt' column to datetime format...")
df['dt'] = pd.to_datetime(df['dt'], errors='coerce')
print("'dt' column converted.")
print("Before conversion:", df_before_cleaning['dt'].dtype)
print("After conversion:", df['dt'].dtype)

print("---------------------- Missing values (%) before cleaning ----------------------")
missing_percent = df.isnull().sum() / len(df) * 100
print(missing_percent.sort_values(ascending=False))


print("----------------------  Cleaning the dataset ----------------------")
#Data Cleaning
df['AverageTemperature'] = df.groupby('Country')['AverageTemperature'].transform(lambda x: x.fillna(x.median()))
df['AverageTemperatureUncertainty'] = df.groupby('Country')['AverageTemperatureUncertainty'].transform(lambda x: x.fillna(x.median()))


missing_before = df_before_cleaning.isnull().sum().sum()
missing_after = df.isnull().sum().sum()
print(f"Total missing values before: {missing_before}")
print(f"Total missing values after: {missing_after}")

#Dropping remaining missing values if any
print("Dropping remaining missing values if any...")
df = df.dropna(subset=['AverageTemperature', 'AverageTemperatureUncertainty'])
rows_before = len(df_before_cleaning)
rows_after = len(df)
print(f"Dropped rows: {rows_before - rows_after}")


print("---------------------- Statistics after cleaning ----------------------")
print(df.describe())
print("Mean of AverageTemperature before cleaning: ", df_before_cleaning['AverageTemperature'].mean())
print("Mean of AverageTemperature after cleaning: ", df['AverageTemperature'].mean())

if len(df) < len(df_before_cleaning):
    dropped = len(df_before_cleaning) - len(df)
    print(f"{dropped} Rows with missing values were dropped.")
    print(f"Before rows: {len(df_before_cleaning)}")
    print(f"After rows: {len(df)}")
else:
    print("No rows were dropped during cleaning. All missing values were handled.")

#Visualizing temperature distribution before and after cleaning
# Calculate cleaning efficiency
missing_before = df_before_cleaning.isnull().sum().sum()
missing_after = df.isnull().sum().sum()
cleaned_percent = (1 - (missing_after / missing_before)) * 100

# Create histogram plots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

axs[0].hist(df_before_cleaning['AverageTemperature'].dropna(), bins=50, color='salmon', alpha=0.7)
axs[0].set_title('Before Cleaning')

axs[1].hist(df['AverageTemperature'].dropna(), bins=50, color='seagreen', alpha=0.7)
axs[1].set_title('After Cleaning')

# Add shared labels
for ax in axs:
    ax.set_xlabel('Average Temperature (°C)')
    ax.set_ylabel('Frequency')
    ax.grid(alpha=0.3)

# Add main figure title and cleaning % text
fig.suptitle('Temperature Distribution Before and After Data Cleaning', fontsize=14, fontweight='bold')
fig.text(0.5, 0.02, f"Missing values reduced by {cleaned_percent:.2f}%", ha='center', fontsize=12, color='gray')


plt.tight_layout( rect=[0, 0.03, 1, 0.95])
plt.show()

#Saving cleaned data
#df.to_csv('cleaned_global_land_temperatures_by_city.csv', index=False)
#print("Cleaned data saved to 'cleaned_global_land_temperatures_by_city.csv'")