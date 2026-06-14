from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


BASE_DIR = Path(__file__).resolve().parent.parent.parent

PDF_DIR = (BASE_DIR /"assets" /"generated_pdfs")

PDF_DIR.mkdir(parents=True,exist_ok=True)


def generate_trip_pdf(image_paths):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = (f"trip_packet_{timestamp}.pdf")
    
    pdf_path = (PDF_DIR /pdf_filename)
    
    c = canvas.Canvas(str(pdf_path),pagesize=letter)
    
    page_width, page_height = letter
    
    for image_path in image_paths:

        img = ImageReader(image_path)

        img_width, img_height = img.getSize()

        scale = min(page_width / img_width,page_height / img_height)

        new_width = img_width * scale

        new_height = (img_height * scale)

        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        c.drawImage(image_path,x,y,width=new_width,height=new_height)

        c.showPage()
    c.save()

    return (
        f"/media/generated_pdfs/"
        f"{pdf_filename}"
    )