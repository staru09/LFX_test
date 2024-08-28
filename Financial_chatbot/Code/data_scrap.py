from pathlib import Path
from typing import List, Optional
import itertools

import pdfkit
from file_utils import filing_exists
from fire import Fire
from sec_edgar_downloader import Downloader

DEFAULT_OUTPUT_DIR = "data/"
DEFAULT_CIKS = [
    "320193",  # AAPL
 
    '''
    "789019",  # MSFT
    "0001018724",  # AMZN
    "1652044",  # GOOGL
    "1326801",  # META
    "1318605",  # TSLA
    "1045810",  # NVDA
    "1065280",  # NFLX
    "0001633917",  # PYPL
    "78003",  # PFE (Pfizer)
    "901832",  # AZNCF (AstraZeneca)
    "59478",  # LLY (Eli Lilly)
    "1682852",  # MRNA (Moderna)
    "200406",  # JNJ (Johnson & Johnson)
    '''
]
DEFAULT_FILING_TYPES = [
    "10-K",
    "10-Q",
]

# Replace settings.SEC_EDGAR_COMPANY_NAME and settings.SEC_EDGAR_EMAIL with direct values
COMPANY_NAME = "Your Company Name"
EMAIL = "your-email@example.com"

def _download_filing(
    cik: str, filing_type: str, output_dir: str, limit=None, before=None, after=None
):
    dl = Downloader(COMPANY_NAME, EMAIL, output_dir)
    dl.get(filing_type, cik, limit=limit, before=before, after=after, download_details=True)

def _convert_to_pdf(output_dir: str):
    """Converts all html files in a directory to pdf files."""
    data_dir = Path(output_dir) / "sec-edgar-filings"

    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_doc = filing_dir / "primary-document.html"
                filing_pdf = filing_dir / "primary-document.pdf"
                if filing_doc.exists() and not filing_pdf.exists():
                    print(f"- Converting {filing_doc}")
                    input_path = str(filing_doc.absolute())
                    output_path = str(filing_pdf.absolute())
                    try:
                        options = {'enable-local-file-access': None}
                        pdfkit.from_file(input_path, output_path, options=options, verbose=True)
                    except Exception as e:
                        print(f"Error converting {input_path} to {output_path}: {e}")

def main(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    ciks: List[str] = DEFAULT_CIKS,
    file_types: List[str] = DEFAULT_FILING_TYPES,
    before: Optional[str] = None,
    after: Optional[str] = None,
    limit: Optional[int] = 3,
    convert_to_pdf: bool = True,
):
    print(f'Downloading filings to "{Path(output_dir).absolute()}"')
    print(f"File Types: {file_types}")
    
    if convert_to_pdf:
        # Check if pdfkit can find wkhtmltopdf
        if pdfkit.configuration().wkhtmltopdf is None:
            raise Exception(
                "ERROR: wkhtmltopdf (https://wkhtmltopdf.org/) not found, "
                "please install it to convert html to pdf "
                "`sudo apt-get install wkhtmltopdf`"
            )
    
    for symbol, file_type in itertools.product(ciks, file_types):
        try:
            if filing_exists(symbol, file_type, output_dir):
                print(f"- Filing for {symbol} {file_type} already exists, skipping")
            else:
                print(f"- Downloading filing for {symbol} {file_type}")
                _download_filing(symbol, file_type, output_dir, limit, before, after)
        except Exception as e:
            print(f"Error downloading filing for symbol={symbol} & file_type={file_type}: {e}")

    if convert_to_pdf:
        print("Converting html files to pdf files")
        _convert_to_pdf(output_dir)

if __name__ == "__main__":
    Fire(main)
