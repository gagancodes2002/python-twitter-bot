import tkinter as tk
from tkinter import filedialog

def process_file():
    # Open file dialog to select text file
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            # Split content by newline and display in output text area
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, content)

# Create the main application window
root = tk.Tk()
root.title("Text File Viewer")

# Create text area to display file content
output_text = tk.Text(root, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

# Create a button to process the file
submit_button = tk.Button(root, text="Submit", command=process_file)
submit_button.pack(pady=5)

# Create a option select to choose out of 3 options, tweets, replies, mixed
option = tk.StringVar()
option.set("tweets")
option_select = tk.OptionMenu(root, option, "tweets", "replies", "mixed")
option_select.pack(pady=5)



# Run the Tkinter event loop
root.mainloop()
