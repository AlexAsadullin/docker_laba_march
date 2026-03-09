import os
import subprocess

TEMP_DIR = "/temp"


def convert_to_pdf(input_path: str) -> str:
    """Convert a Microsoft Office file to PDF using LibreOffice.

    Args:
        input_path: Path to the source file inside /temp.

    Returns:
        Path to the resulting PDF in /temp.

    Raises:
        RuntimeError: If the conversion fails.
        FileNotFoundError: If the input file does not exist.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    result = subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            TEMP_DIR,
            input_path,
        ],
        capture_output=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"LibreOffice conversion failed: {result.stderr.decode()}"
        )

    base = os.path.splitext(os.path.basename(input_path))[0]
    pdf_path = os.path.join(TEMP_DIR, f"{base}.pdf")

    if not os.path.isfile(pdf_path):
        raise RuntimeError("Conversion produced no output file")

    return pdf_path
