import requests
from bs4 import BeautifulSoup
import pdfplumber
import io

def scrape_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(strip=True)
    return ""

def extract_pdf_text(pdf_content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text.strip()
