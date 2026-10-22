"""Adjunta los .vcf al PDF de la tarjeta (en la compu se abren desde el clip de Acrobat)."""
import pathlib
from pypdf import PdfReader, PdfWriter

D = pathlib.Path(__file__).resolve().parent.parent / "tarjeta"
w = PdfWriter(clone_from=PdfReader(D / "tarjeta-sin-adjuntos.pdf"))
for vcf in ("lorena.vcf", "jose.vcf"):
    w.add_attachment(vcf, (D / vcf).read_bytes())
w.add_metadata({"/Title": "Wasiluk Yasinsky & Asociados · Tarjeta"})
w.write(D / "Tarjeta Wasiluk Yasinsky.pdf")
(D / "tarjeta-sin-adjuntos.pdf").unlink()
(D / "_pdf.html").unlink()
print("ok")
