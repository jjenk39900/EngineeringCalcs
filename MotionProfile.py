# This program creates a position (inches) vs time (seconds) dataset from speed (mph) vs position (ft)

import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

# Assuming you have a list of speeds (in mph) and positions (in feet)
speeds_mph = [0, 7.5, 15, 20, 22.5, 22.5, 20, 10, 0]  # Example speeds in mph
positions_feet = [0, 5, 10, 15, 20, 25, 30, 35, 40]  # Example positions in feet

# Convert positions to inches
positions_inches = [x * 12 for x in positions_feet]

# Create new positions at one-inch increments
new_positions = np.arange(0, max(positions_inches) + 1, 1)

# Interpolate speeds
f = interp1d(positions_inches, speeds_mph, kind='linear')
new_speeds = f(new_positions)

# Convert speeds from mph to feet per second (1 mph = 1.46667 fps)
speeds_fps = [x * 1.46667 for x in new_speeds]

# Calculate time intervals between each pair of positions
time_intervals = [(new_positions[i+1] - new_positions[i]) / ((speeds_fps[i] + speeds_fps[i+1]) / 2) if speeds_fps[i+1] != 0 else 0 for i in range(len(new_positions) - 1)]

# Calculate cumulative time for each position
times = [0]  # Starting at time 0 for position 0
for interval in time_intervals:
    times.append(times[-1] + interval)

# Print the position vs time dataset
#for pos, time in zip(new_positions, times):
#    print(f"Position: {pos} inches, Time: {time:.2f} seconds")

df = pd.DataFrame({
    'Position_in_inches': new_positions,
    'Time_in_seconds': times
})


# Generate evenly spaced time values in 0.1 second intervals
even_times = np.arange(0, times[-1], 0.1)

# Interpolate positions for the even times
# We need to create an interpolation function for position based on time
position_interp = interp1d(times, new_positions, kind='linear', fill_value="extrapolate")

# Use the interpolation function to find positions at the even times
even_positions = position_interp(even_times)

# Create the second DataFrame with even times and interpolated positions
df_even_times = pd.DataFrame({
    'Time_in_seconds': even_times,
    'Interpolated_Position_in_inches': even_positions
})

# Display the second DataFrame
print(df_even_times.head())

# Save the DataFrame to an Excel file
df_even_times.to_excel('motion_profile.xlsx', index=False)

print('Motion profile saved to motion_profile.xlsx')
