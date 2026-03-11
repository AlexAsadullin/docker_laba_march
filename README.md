This is a FastAPI service that converts Microsoft Office files (doc, docx, xls, xlsx, ppt, pptx) to PDF using LibreOffice. Converted and uploaded files are stored in /temp and automatically deleted after 24 hours.

The app exposes four endpoints:
- POST /convert_word - upload a Word file, get back a PDF
- POST /convert_excel - upload an Excel file, get back a PDF
- POST /convert_powerpoint - upload a PowerPoint file, get back a PDF
- GET /restore?filename= - download a previously converted file by name if it hasn't expired yet

File metadata (filename, extension, expiration timestamp) is stored in a PostgreSQL database. A separate trash collector process runs every hour and removes expired files from disk and from the database.

The project runs via docker-compose and consists of three services: the FastAPI web app (port 8000), a PostgreSQL database, and the trash collector.

## To build and run:
```bash
docker-compose up --build
```

add /temp to .gitignore

## Testing the Convert Word Endpoint

To test the POST /convert_word endpoint, you can use curl:

```bash
curl -X POST "http://localhost:8000/convert_word" \
  -F "file=@/path/to/your/document.docx" \
  --output result.pdf
```

Replace `/path/to/your/document.docx` with the actual path to a Word document on your system.

The endpoint accepts .doc and .docx files and returns a PDF. The response will be the converted PDF file that you can save and open.

Alternatively, to see the response headers and metadata:

```bash
curl -X POST "http://localhost:8000/convert_word" \
  -F "file=@/path/to/your/document.docx" \
  -v --output result.pdf
```

You can also test using tools like Postman or Thunder Client by sending a POST request with a file in the form-data field named "file".

