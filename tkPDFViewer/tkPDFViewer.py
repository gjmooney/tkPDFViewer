try:
    import tkinter as tk
    import fitz
    from tkinter import ttk
    from threading import Thread
    import math
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")

class ShowPdf():

    img_object_li = []

    def pdf_view(self, master, width=1200, height=600, pdf_location="", bar=True, load="after"):

        self.frame = tk.Frame(master, width=width, height=height, bg="white")

        scroll_y = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL)

        scroll_x.pack(fill=tk.X, side=tk.BOTTOM)
        scroll_y.pack(fill=tk.Y, side=tk.RIGHT)

        percentage_view = 0
        percentage_load = tk.StringVar(master)

        if bar and load == "after":
            self.display_msg = ttk.Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL,
                                      length=100, mode='determinate')
            loading.pack(side=tk.TOP, fill=tk.X)

        self.text = tk.Text(self.frame, yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set,
                            width=width, height=height)
        self.text.pack(side="left")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)


        def add_img():
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
                    loading['value'] = percentage_view
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
            if bar and load == "after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for i in self.img_object_li:
                self.text.image_create(tk.END, image=i)
                self.text.insert(tk.END, "\n\n")
            self.text.configure(state="disabled")

        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load == "after":
            master.after(250, start_pack)
        else:
            start_pack()

        return self.frame




def main():
    root = tk.Tk()
    root.geometry("700x780")
    d = ShowPdf().pdf_view(root, pdf_location=r"D:\DELL\Documents\Encyclopedia GUI.pdf", width=50, height=200)
    d.pack()
    root.mainloop()

if __name__  ==  '__main__':
    main()
