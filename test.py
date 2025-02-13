import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import random

# Generate a random seed
random_seed = random.randint(0, 2**32 - 1)  # Generate a random integer
np.random.seed(random_seed)  # Use the random integer as the seed

# Generate a random sample size for the number of days
sample_size = random.randrange(120, 360)  # Number of days
sbp = np.random.normal(loc=120, scale=15, size=sample_size).clip(90, 180)  # Systolic BP
dbp = np.random.normal(loc=80, scale=10, size=sample_size).clip(60, 120)    # Diastolic BP

# Create a DataFrame
bp_data = pd.DataFrame({
    'Day': np.arange(1, sample_size + 1),
    'Systolic_BP': sbp,
    'Diastolic_BP': dbp
})

# Create a list to hold images for the GIF
images = []

# Generate plots for each day and save them to images list
for i in range(sample_size):
    # Dynamically set the figure size based on sample_size
    plt.figure(figsize=(10 + (sample_size / 30), 5))  # Width scales with sample_size

    plt.plot(bp_data['Day'][:i+1], bp_data['Systolic_BP'][:i+1], label='Systolic BP', color='red')
    plt.plot(bp_data['Day'][:i+1], bp_data['Diastolic_BP'][:i+1], label='Diastolic BP', color='blue')
    
    # Draw horizontal and vertical lines at the origin
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Horizontal line at y=0
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')  # Vertical line at x=0
    
    plt.title(f'Blood Pressure Readings up to Day {i+1}')
    plt.xlabel('Days')
    plt.ylabel('Blood Pressure (mmHg)')
    plt.legend()
    plt.ylim(60, 160)  # Set y-limits to ensure visibility of the lines
    plt.xlim(0, sample_size)  # Set x-limits to ensure visibility of the lines
    plt.grid()

    # Save the current plot to a temporary file
    plt.savefig('temp_plot.png')
    plt.close()

    # Read the saved plot and append to images list
    images.append(imageio.imread('temp_plot.png'))

# Create a GIF from the images list with increased FPS for smoother animation
imageio.mimsave('blood_pressure_animation.gif', images, fps=45)  # Set FPS to 45 for smoother animation

print("GIF saved as 'blood_pressure_animation.gif'")