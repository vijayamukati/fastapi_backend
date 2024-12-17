import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import io

def scrape_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(strip=True)
    return ""

def extract_pdf_text(pdf_content: bytes) -> str:
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.strip()

