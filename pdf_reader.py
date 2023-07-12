import PyPDF2

def chunk_pdf(pdf_file, chunk_size=4000, overlap=1000):
    chunks = []
    chunk = ""
    with open(pdf_file, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        for page in pdf.pages:
            chunk += page.extract_text()
            while len(chunk) > chunk_size:
                chunks.append(chunk[:chunk_size])
                chunk = chunk[chunk_size-overlap:]

    if len(chunk):
        chunks.append(chunk)

    return chunks
