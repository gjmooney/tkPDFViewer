import tkPDFViewer as pdf
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()

file = askopenfilename(title="Open PDF", defaultextension=".pdf",
                       filetypes=[("PDF", "*.pdf"), ("All files", "*")])

if file:
    #create object like this.
    viewer = pdf.ShowPdf(root)
    #Add your pdf location and width and height.
    pdf_frame = viewer.pdf_view(pdf_location=file,
                                width=50,height=100)
    pdf_frame.pack()
    root.mainloop()