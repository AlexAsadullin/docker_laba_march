This is a FastAPI service that converts Microsoft Office files (doc, docx, xls, xlsx, ppt, pptx) to PDF using LibreOffice. Converted and uploaded files are stored in /temp and automatically deleted after 24 hours.

The app exposes four endpoints:
- POST /convert_word - upload a Word file, get back a PDF
- POST /convert_excel - upload an Excel file, get back a PDF
- POST /convert_powerpoint - upload a PowerPoint file, get back a PDF
- GET /restore?filename= - download a previously converted file by name if it hasn't expired yet

File metadata (filename, extension, expiration timestamp) is stored in a PostgreSQL database. A separate trash collector process runs every hour and removes expired files from disk and from the database.

The project runs via docker-compose and consists of three services: the FastAPI web app (port 8000), a PostgreSQL database, and the trash collector.

To build and run:
docker-compose up --build

add /temp to .gitignore