# © ohidurbappy

import tkinter as tk
import tkinter.ttk as ttk
import requests
import threading
import tempfile
import os
import time


progress_window=tk.Tk()
progress_window.geometry('400x60')
progress_window.title("Querying file size..")
progressbar=ttk.Progressbar(master=progress_window, orient = tk.HORIZONTAL, 
        length = 100, mode = 'determinate')
progressbar.pack(ipadx=4,ipady=4,padx=(12,12),pady=(12,12))

def download_file():
    session=requests.Session()
    response=session.get("http://ipv4.download.thinkbroadband.com/10MB.zip",stream=True)
    total_size_in_bytes= int(response.headers.get('Content-Length', 500*1024))
    # we are streaming and don't know content length
    # assuming its 500kb
    # total_size_in_bytes=500*1024
    block_size = 1024*50

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_filename=os.path.join(tmp_dir,'response.data')
    
        with open(tmp_filename, 'wb') as file:
            downloaded=0
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded+=len(data)
                if downloaded==0:
                    progressbar['value']=0
                else:
                    progressbar['value'] = int((downloaded/total_size_in_bytes)*100)
                progress_window.title(f"Downloaded {downloaded} of {total_size_in_bytes} bytes.")
                progress_window.update()
                time.sleep(.1)
    progress_window.destroy()
    
progress_window.after(300,lambda: threading.Thread(target=download_file).start())
progress_window.mainloop()
