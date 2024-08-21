from PIL import Image, ImageTk, UnidentifiedImageError
import tkinter as tk
from tkinter import messagebox
import winreg
import os
import sys

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller tarafından kullanılan geçici dizin
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Function to get the Windows Product Key from the registry
def get_windows_product_key():
    try:
        # Get the Digital Product ID from the Windows Registry
        key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        reg_key = winreg.OpenKey(registry, key)
        
        # Retrieve the necessary registry values
        product_name = winreg.QueryValueEx(reg_key, "ProductName")[0]
        product_id = winreg.QueryValueEx(reg_key, "ProductID")[0]
        digital_id = winreg.QueryValueEx(reg_key, "DigitalProductId")[0]
        
        # Convert the Digital Product ID to the actual product key
        product_key = convert_to_key(bytearray(digital_id))
        
        # Return the formatted product key information
        return f"Operating System Version: {product_name}\n" \
               f"Product ID: {product_id}\n" \
               f"Product Key: {product_key}\n"

    except FileNotFoundError:
        return "Error: Windows Registry keys not found."
    except OSError as e:
        return f"Error accessing the registry: {str(e)}"
    except Exception as e:
        return f"Error retrieving product key: {str(e)}"

# Function to convert the digital ID to a readable product key
def convert_to_key(digital_id):
    try:
        key_offset = 52
        is_win8 = (digital_id[66] >> 3) & 1
        digital_id[66] = (digital_id[66] & 0xF7) | ((is_win8 & 2) << 2)
        chars = "BCDFGHJKMPQRTVWXY2346789"
        key_output = ''

        last = 0
        for i in range(24, -1, -1):
            current = 0
            for x in range(14, -1, -1):
                current = current * 256
                current += digital_id[x + key_offset]
                digital_id[x + key_offset] = current // 24
                current = current % 24
                last = current
            key_output = chars[current] + key_output
        
        # Add 'N' character if it is a Windows 8 key
        if is_win8 == 1:
            key_output = key_output[:last] + 'N' + key_output[last + 1:]

        # Format the key output into 5-character groups
        key_parts = [key_output[i:i + 5] for i in range(0, len(key_output), 5)]
        return '-'.join(key_parts)
    
    except IndexError:
        return "Error converting the product key. Invalid Digital ID format."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Function to save the product key information to a file automatically
def save_product_key_to_file_automatically(product_key_info):
    try:
        # Get the path to save the file in the current directory
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "WindowsProductKey.txt")
        
        # Write the product key information to a text file
        with open(file_path, 'w') as file:
            file.write(product_key_info)
        
        # Show a success message and close the application
        messagebox.showinfo("Success", f"Product key has been saved successfully to {file_path}.")
        root.quit()  # Exit the application
    except OSError as e:
        messagebox.showerror("Error", f"Failed to save the file: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

# Function to display the product key and ask the user if they want to save it
def show_product_key():
    try:
        product_key_info = get_windows_product_key()

        # Create a new Toplevel window to show the product key and ask if the user wants to save it
        top = tk.Toplevel(root)
        top.title("Windows Product Key Finder - by Seker")
        top.geometry("400x200")
        top.resizable(False, False)
        top.configure(bg='white')  # Set the background to white

        # Set the window icon
        try:
            top.iconbitmap(resource_path('icon/logo.ico'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {str(e)}")

        # Display the product key information in a Label
        label = tk.Label(top, text=product_key_info, wraplength=350, justify="left", bg='white')
        label.pack(pady=(10, 0))

        save_label = tk.Label(top, text="Do you want to save the key as a text file?", bg='white')
        save_label.pack(pady=(10, 10))

        # Create a frame for the buttons
        button_frame = tk.Frame(top, bg='white')
        button_frame.pack(pady=10)
        
        # Create 'Yes' and 'No' buttons
        save_button = tk.Button(button_frame, text="Yes", command=lambda: save_and_close(top, product_key_info), width=10)
        save_button.pack(side="left", padx=10)

        cancel_button = tk.Button(button_frame, text="No", command=top.destroy, width=10)
        cancel_button.pack(side="right", padx=10)

        # Center the Toplevel window on the screen
        center_window(top, 400, 200)
    
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

# Function to save the product key and close the window
def save_and_close(window, product_key_info):
    try:
        save_product_key_to_file_automatically(product_key_info)
        window.destroy()  # Close the window
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

# Function to center the window on the screen
def center_window(window, width=300, height=100):
    try:
        # Get the screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the center position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window position to the center of the screen
        window.geometry(f'{width}x{height}+{x}+{y}')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to center the window: {str(e)}")

# Create the main tkinter window
try:
    root = tk.Tk()
    root.title("Windows Product Key Finder - by Seker")

    # Set the window icon
    try:
        root.iconbitmap(resource_path('icon/logo.ico'))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load icon: {str(e)}")

    # Prevent the window from being resized (disables fullscreen)
    root.resizable(False, False)

    # Center the window on the screen
    window_width = 400
    window_height = 200
    center_window(root, window_width, window_height)

    # Load the background image using Pillow and resize it to fit the window
    try:
        background_image = Image.open(resource_path("icon/background.png"))
        background_image = background_image.resize((window_width, window_height), Image.LANCZOS)
        background_photo = ImageTk.PhotoImage(background_image)
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image not found.")
    except UnidentifiedImageError:
        messagebox.showerror("Error", "Failed to identify the image file format.")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    # Create a Label widget to hold the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)  # Fill the entire window with the image

    # Add a button and bind it to the function that shows the product key
    btn_show_key = tk.Button(root, text="Show Product Key", command=show_product_key)
    btn_show_key.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Place the button at the center

    # Start the tkinter event loop
    root.mainloop()

except Exception as e:
    messagebox.showerror("Error", f"Unexpected error during initialization: {str(e)}")
