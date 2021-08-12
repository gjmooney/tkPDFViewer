import tkPDFViewer as pdf
from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename


def open_pdf():
    file = askopenfilename(title="Open PDF", defaultextension=".pdf",
                           filetypes=[("PDF", "*.pdf"), ("All files", "*")])
    if file:
        pdf_frame = viewer.pdf_view(pdf_location=file,
                                    width=50, height=100)
        pdf_frame.pack(fill="both", expand=True)

root = Tk()

#create object like this.
viewer = pdf.ShowPdf(root)
viewer2 = pdf.ShowPdf(root)

Button(root, text="Open pdf", command=open_pdf).pack()

root.mainloop()