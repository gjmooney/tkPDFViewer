try:
    import tkinter as tk
    import fitz
    from tkinter import ttk
    from threading import Thread
    import math
    import sys
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")


class ShowPdf():

    def __init__(self, master):
        self.img_object_li = []

        self.frame = tk.Frame(master)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)

        self.percentage_load = tk.StringVar(master)

        # loading bar
        self.display_msg = ttk.Label(self.frame, textvariable=self.percentage_load)
        self.display_msg.grid(row=0, column=0, pady=10)
        self.display_msg.grid_remove()
        self.loading = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL,
                                       length=100, mode='determinate')
        self.loading.grid(row=1, column=0, sticky="ew")
        self.loading.grid_remove()

        # display
        scroll_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.text = tk.Text(self.frame, yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set)
        self.text.grid(row=2, column=0, sticky="esnw")
        scroll_x.grid(row=3, column=0, sticky="ew")
        scroll_y.grid(row=2, column=1, sticky="ns")
        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)


    def pdf_view(self, width=1200, height=600, pdf_location="", bar=True, load="after"):

        if bar and load == "after":
            self.display_msg.grid()
            self.loading.grid()

        self.text.configure(width=width, height=height)

        if load == "after":
            self.frame.after(250, self.start_load, pdf_location, bar, load)
        else:
            self.start_load(pdf_location, bar, load)

        return self.frame

    def add_img(self, pdf_location, bar=True, load="after"):
        precentage_dicide = 0
        open_pdf = fitz.open(pdf_location)

        for page in open_pdf:
            pix = page.getPixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            img = pix1.getImageData("ppm")
            timg = tk.PhotoImage(data=img)
            self.img_object_li.append(timg)
            if bar and load == "after":
                precentage_dicide = precentage_dicide + 1
                percentage_view = (float(precentage_dicide)/float(len(open_pdf))*float(100))
                self.loading['value'] = percentage_view
                self.percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
        if bar and load == "after":
            self.loading.grid_remove()
            self.display_msg.grid_remove()

        for i in self.img_object_li:
            self.text.image_create(tk.END, image=i)
            self.text.insert(tk.END, "\n\n")
        self.text.configure(state="disabled")

    def start_load(self, pdf_location, bar, load):
        t1 = Thread(target=self.add_img, args=(pdf_location, bar, load))
        t1.start()



def main():
    if len(sys.argv) < 2:
        print("Missing argument: path of pdf to open")
        return

    root = tk.Tk()
    #create object like this.
    viewer = ShowPdf(root)
    #Add your pdf location and width and height.
    pdf_frame = viewer.pdf_view(pdf_location=sys.argv[1],
                                width=50, height=100)
    pdf_frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()