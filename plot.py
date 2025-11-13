import matplotlib.pyplot as plt
import numpy as np

def plot_points_from_file(filename, output_image_name="2d_points_plot.png"):
    """
    Reads 2D points from a text file that contains ONLY coordinates, one per line,
    and plots them on a 2D axis.
    """
    x_coords = []
    y_coords = []

    try:
        with open(filename, 'r') as f:
            # --- FIX: REMOVED the two f.readline() calls ---
            # The code now starts reading coordinate data from the very first line.
            
            # Read all lines from the file
            for line in f:
                try:
                    # Split the line by spaces and convert to float
                    parts = line.strip().split()
                    
                    # Check if we have at least two parts (x and y)
                    if len(parts) >= 2:
                        x = float(parts[0])
                        y = float(parts[1])
                        x_coords.append(x)
                        y_coords.append(y)
                except ValueError:
                    # Ignore lines that can't be parsed (e.g., empty lines, non-numeric data)
                    continue

        if not x_coords:
            print(f"Error: No valid points found in {filename}. Check file content.")
            return

        # --- Matplotlib Plotting ---
        plt.figure(figsize=(10, 8))
        
        # Use scatter plot for individual points
        plt.scatter(x_coords, y_coords, s=10, alpha=0.7, color='blue', label=f'{len(x_coords)} Points')

        plt.title(f'2D Point Distribution from {filename}')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.axis('equal') 

        # Save the plot
        plt.savefig(output_image_name)
        plt.close()

        print(f"\n✅ Successfully plotted {len(x_coords)} points.")
        print(f"Plot saved as {output_image_name}")

    except FileNotFoundError:
        print(f"\n❌ Error: File not found at {filename}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

# --- Main Execution Block ---

# 1. Ask the user for the filename
file_name = input("Enter the name of the text file containing the 2D points: ")

# 2. Define the output image name
base_name = file_name.rsplit('.', 1)[0]
output_name = f"{base_name}_plot.png"

# 3. Call the plotting function
plot_points_from_file(file_name, output_name)