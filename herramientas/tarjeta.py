"""Genera tarjeta/index.html (tarjeta virtual) y un .vcf por persona.

Los .vcf van en la misma carpeta que index.html: el botón \"Guardar contacto\" los enlaza
como archivo real, que iPhone y los navegadores de WhatsApp abren mejor que un data: URI.
"""
import html, pathlib, sys
import segno

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from datos import *  # noqa: E402,F403

SALIDA = pathlib.Path(__file__).resolve().parent.parent / "tarjeta"
e = html.escape


def vcard(p):
    return "\r\n".join([
        "BEGIN:VCARD", "VERSION:3.0",
        f"N:{p['apellido']};{p['nombre']};;{p['titulo']};",
        f"FN:{p['titulo']} {p['nombre']} {p['apellido']}",
        f"ORG:{NOMBRE}", f"TITLE:{p['cargo']}",
        f"TEL;TYPE=CELL,VOICE:{p['tel_int']}",
        f"EMAIL;TYPE=WORK:{CORREO}",
        f"URL:{URL}",
        "ADR;TYPE=WORK:;;;Punta del Este;Maldonado;;Uruguay",
        "END:VCARD", ""])


# Margen blanco de 4 módulos, negro puro y viewBox (omitsize) para que el CSS escale el QR entero sin recortarlo
qr = segno.make(URL, error="m").svg_inline(dark="#000000", light="#FFFFFF", border=4, omitsize=True)

personas_html = ""
for p in PERSONAS:
    v = vcard(p)
    (SALIDA / f"{p['id']}.vcf").write_text(v, encoding="utf-8")
    wa = "https://wa.me/" + p["tel_int"].lstrip("+")
    personas_html += f"""
    <article class="persona">
      <p class="area">{e(p['area'])}</p>
      <h2>{e(p['titulo'])} {e(p['nombre'])} {e(p['apellido'])}</h2>
      <p class="cargo">{e(p['cargo'])}</p>
      <div class="acciones">
        <a class="btn principal" href="{wa}" target="_blank" rel="noopener">WhatsApp · {e(p['tel'])}</a>
        <a class="btn" href="tel:{p['tel_int']}">Llamar</a>
        <a class="btn" href="{p['id']}.vcf" type="text/vcard">Guardar contacto</a>
      </div>
    </article>"""

servicios = " · ".join(e(s) for s in SERVICIOS)

pagina = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(NOMBRE)} · Tarjeta</title>
<meta name="description" content="{e(RUBRO)} en Punta del Este. Esc. Lorena Yasinsky y Cr. José Wasiluk.">
<meta name="theme-color" content="#{TINTA}">
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
:root {{ --tinta:#{TINTA}; --dorado:#{DORADO}; --papel:#F4F1EA; --suave:rgba(244,241,234,.66); --linea:rgba(184,149,90,.35); }}
* {{ box-sizing:border-box; margin:0; }}
body {{ background:var(--tinta); color:var(--papel); font-family:Geist,system-ui,sans-serif; font-weight:350;
  min-height:100vh; display:grid; place-items:center; padding:32px 16px; }}
.tarjeta {{ width:100%; max-width:440px; border:1px solid var(--linea); border-radius:20px; padding:36px 28px 28px;
  background:linear-gradient(160deg,#101828 0%,var(--tinta) 60%); box-shadow:0 30px 80px rgba(0,0,0,.45); }}
.marca {{ display:flex; align-items:center; gap:14px; }}
.monograma {{ width:54px; height:54px; border:1px solid var(--dorado); border-radius:50%; display:grid; place-items:center;
  font-family:"Instrument Serif",serif; font-size:24px; color:var(--dorado); letter-spacing:.02em; flex:none; }}
h1 {{ font-family:"Instrument Serif",serif; font-weight:400; font-size:30px; line-height:1.05; }}
h1 em {{ color:var(--dorado); }}
.rubro {{ margin-top:6px; font-size:12px; letter-spacing:.14em; text-transform:uppercase; color:var(--suave); }}
.servicios {{ margin:22px 0 4px; font-size:13px; line-height:1.6; color:var(--suave); }}
.persona {{ border-top:1px solid var(--linea); padding:22px 0 4px; margin-top:20px; }}
.area {{ font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--dorado); }}
h2 {{ font-family:"Instrument Serif",serif; font-weight:400; font-size:26px; margin-top:4px; }}
.cargo {{ font-size:14px; color:var(--suave); }}
.acciones {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }}
.btn {{ font:inherit; font-size:13px; font-weight:500; color:var(--papel); text-decoration:none; padding:9px 14px;
  border:1px solid var(--linea); border-radius:999px; }}
.btn:hover {{ border-color:var(--dorado); }}
.btn.principal {{ background:var(--dorado); border-color:var(--dorado); color:var(--tinta); }}
.pie {{ border-top:1px solid var(--linea); margin-top:24px; padding-top:22px; display:flex; gap:18px; align-items:center; }}
.pie .qr {{ background:#fff; border-radius:8px; flex:none; line-height:0; overflow:hidden; }}
.pie .qr svg {{ width:132px; height:132px; display:block; }}
.pie p {{ font-size:13px; line-height:1.7; color:var(--suave); word-break:break-word; }}
.pie a {{ color:var(--papel); text-decoration:none; }}
</style>
</head>
<body>
<main class="tarjeta">
  <header class="marca">
    <div class="monograma" aria-hidden="true">WY</div>
    <div><h1>Wasiluk Yasinsky <em>&amp;</em> Asociados</h1><p class="rubro">{e(RUBRO)}</p></div>
  </header>
  <p class="servicios">{servicios}</p>
  {personas_html}
  <footer class="pie">
    <div class="qr" aria-label="Código QR a {WEB}">{qr}</div>
    <p><a href="mailto:{CORREO}">{CORREO}</a><br><a href="{URL}">{WEB}</a><br>{e(CIUDAD)}</p>
  </footer>
</main>
</body>
</html>
"""
(SALIDA / "index.html").write_text(pagina, encoding="utf-8")
print("ok", SALIDA)

# Variante para compartir como PDF (sin subir nada a la web): los enlaces tel:, wa.me y
# mailto: siguen funcionando dentro del PDF; un .vcf enlazado no, así que en su lugar va
# un botón de correo y los .vcf viajan adjuntos dentro del PDF.
pdf_html = pagina.replace("</style>", """@page { margin:0; }
body { min-height:0; padding:0; display:block; }
.tarjeta { border-radius:0; border:0; box-shadow:none; max-width:none; width:440px; }
</style>""")
for p in PERSONAS:
    asunto = f"Consulta para {p['titulo']} {p['nombre']} {p['apellido']}".replace(" ", "%20")
    pdf_html = pdf_html.replace(
        f'<a class="btn" href="{p["id"]}.vcf" type="text/vcard">Guardar contacto</a>',
        f'<a class="btn" href="mailto:{CORREO}?subject={asunto}">Correo</a>')
(SALIDA / "_pdf.html").write_text(pdf_html, encoding="utf-8")
