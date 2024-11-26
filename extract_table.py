
import os
import pytesseract
import camelot
import fitz  # PyMuPDF
from PIL import Image

# Set the path to tesseract executable (use the path where Tesseract is installed)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def extract_tables_from_pdf(pdf_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Use Camelot to extract tables from the PDF into DataFrames
    try:
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream', edge_tol=500)
        if not tables:
            raise ValueError("No tables found")
    except Exception as e:
        print(f"Error using Camelot to extract tables: {e}")
        return

    # Step 2: Process each table and save it
    for table_index, table in enumerate(tables, start=1):
        try:
            # Save the table as a CSV
            output_csv_path = os.path.join(output_dir, f"table_{table_index}.csv")
            table.to_csv(output_csv_path)
            print(f"Table {table_index} saved to {output_csv_path}")

            # Step 3: Optionally use Tesseract OCR to extract text from table images
            # Capture the table as an image (zoom factor helps with better quality)
            page_number = table.page
            pdf_document = fitz.open(pdf_path)
            page = pdf_document[page_number - 1]  # Camelot uses 1-based page indexing
            
            # Get the bounding box of the table from Camelot
            x1, y1, x2, y2 = table.rect
            zoom_x = 3.0  # Higher zoom for better quality
            zoom_y = 3.0
            matrix = fitz.Matrix(zoom_x, zoom_y)
            clip = fitz.Rect(x1, y1, x2, y2)
            pix = page.get_pixmap(matrix=matrix, clip=clip)
            
            # Save the table image at higher resolution
            output_image_path = os.path.join(output_dir, f"table_{table_index}.png")
            pix.save(output_image_path)

            # Step 4: Extract text from the table image using Tesseract OCR
            print(f"Extracting text from table image: {output_image_path}")
            table_text = pytesseract.image_to_string(Image.open(output_image_path))

            # Save the OCR extracted text to a separate text file
            ocr_txt_path = os.path.join(output_dir, f"table_{table_index}_ocr.txt")
            with open(ocr_txt_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write(table_text)
            print(f"OCR text for Table {table_index} saved to {ocr_txt_path}")
        
        except Exception as e:
            print(f"Error processing table {table_index}: {e}")
    
    print("Table extraction complete!")

# Example usage
pdf_path = "C:/Users/Hp/Downloads/Press_release_car_registrations_September_2024.pdf"
output_dir = "C:/Users/Hp/Desktop/BeautifulScoup/acea_database/extracted_tables"
extract_tables_from_pdf(pdf_path, output_dir)

