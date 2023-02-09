''' M3U exported Android to local PC Converter
    Converts M3U music playlist file entries from an android format to the format matching your local PC.
    Copyright (C) 2023  Thomas Davey-Spence

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from controllers import readM3U, iterateSongs, findSongPaths, newM3UName, writeM3U



def select_input_file():
    '''Ask for the input filenames.'''
    #Filter to M3U files.
    file_paths = filedialog.askopenfilenames(filetypes = (("M3U Files", "*.m3u*"),("all files", "*.*")))
    input_entry.delete(0, tk.END)
    #Join the paths together with ; as a delimiter.
    input_entry.insert(0, ";".join(file_paths))


def select_output_folder():
    '''Ask for the output directory.'''
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def convert_file():
    '''Called when convert button is pressed, launch the conversion process on the files.'''
    #Get the contents of the user inputs.
    input_paths = input_entry.get().split(";")
    output_path = output_entry.get()
    music_path = music_entry.get()
    #Create a new window for a progress bar.  
    progress_window = tk.Toplevel()
    progress_window.title("Conversion Progress")
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)

    #Create the total steps and counter for the progress bar.
    total_steps = len(input_paths)
    step = 0

    try:
        for x in input_paths:
            #Iterate the steps and add to the progress bar.
            step+=1
            progress_bar["value"] = (step) / total_steps * 100
            if '.m3u' in x:
                lines =  readM3U(x)
                if lines:
                    songFiles = iterateSongs(lines)
                    songPaths = findSongPaths(music_path, songFiles)
                    newName = newM3UName(x, output_path)
                    writeM3U(newName,songPaths, music_path)
                progress_window.update()
        #Update the root window with a success message, the message disappears after a few seconds.
        result_label.config(text="File converted successfully!")
        
    except Exception as ex:
        #Update the root window with the error message.
        result_label.config(text="Error: {}".format(ex))
        
    finally:
        progress_window.destroy()
        root.update_idletasks()
    

def exit_program():
    root.destroy()

def select_music_folder():
    '''Ask for the music directory.'''
    folder_path = filedialog.askdirectory()
    music_entry.delete(0, tk.END)
    music_entry.insert(0, folder_path)



def validate_inputs(*args):
    ''' Validate that all fields have been filled'''
    if input_entry.get() and music_entry.get() and output_entry.get():
        convert_button.config(state='normal')
    else:
        convert_button.config(state='disabled')

#Setup the new window.
root = tk.Tk()
root.title("M3U Converter")
root.columnconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.resizable(True, False)

#Setup the input label.
input_label = tk.Label(root, text="Input:")
input_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)


#Set the input textbox, call validate_inputs anytime the box is modified.
input_var = tk.StringVar()
input_entry = tk.Entry(root, validate="focusout", textvariable=input_var)
input_entry.grid(row=0, column=1, sticky="EW", padx=10, pady=10)
input_var.trace("w", validate_inputs)

#Setup the input button for launching the file explorer.
input_file_button = tk.Button(root, text="File", command=select_input_file)
input_file_button.grid(row=0, column=2, padx=10, pady=10)


music_label = tk.Label(root, text="Music Folder:")
music_label.grid(row=1, column=0, sticky="W", padx=10, pady=10)

music_var = tk.StringVar()
music_entry = tk.Entry(root, validate="focusout", textvariable= music_var)
music_entry.grid(row=1, column=1, sticky="EW",padx=10, pady=10)
music_var.trace("w", validate_inputs)

select_music_button = tk.Button(root, text="Select Folder", command=select_music_folder)
select_music_button.grid(row=1, column=2,padx=(0,10), pady=10)


output_label = tk.Label(root, text="Output:")
output_label.grid(row=2, column=0, sticky="W", padx=10, pady=10)

output_var = tk.StringVar()
output_entry = tk.Entry(root, validate="focusout", textvariable=output_var)
output_entry.grid(row=2, column=1, sticky="EW", padx=10, pady=10)
output_var.trace("w", validate_inputs)

output_button = tk.Button(root, text="Select", command=select_output_folder)
output_button.grid(row=2, column=2, columnspan=2, padx=(0,10), pady=10)

convert_button = tk.Button(root, text="Convert", command=convert_file, state="disabled")
convert_button.grid(row=3, column=2, sticky="E", padx=(0,10), pady=(0,10))

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.grid(row=3, column=1, sticky="E", padx=(0,10), pady=(0,10))


result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=4, sticky="NSEW")


root.mainloop()