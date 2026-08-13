# Roda todos os patches desta pasta em ordem, um por um.
# Se um patch ja tiver sido aplicado antes (arquivo ja no formato novo),
# ele avisa e continua para o proximo — nao trava o processo.
# Uso: python3 aplicar_tudo.py   (dentro da pasta raiz do repo Buildly3)
import subprocess, sys, pathlib

pasta = pathlib.Path(__file__).parent
patches = sorted(pasta.glob('0*.py'))

print(f"Encontrados {len(patches)} patches para aplicar.\n")

resultados = []
for patch in patches:
    print(f"{'='*60}\n>>> Rodando {patch.name}\n{'='*60}")
    r = subprocess.run([sys.executable, str(patch)], cwd=pasta.parent if (pasta.parent / 'buildly-completo.html').exists() else pathlib.Path.cwd())
    ok = (r.returncode == 0)
    resultados.append((patch.name, ok))
    print()

print(f"{'='*60}\nRESUMO\n{'='*60}")
for nome, ok in resultados:
    print(f"{'✅' if ok else '⚠️  (pulado ou ja aplicado)'} {nome}")
