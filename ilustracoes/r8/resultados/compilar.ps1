# Compila todos os figura_*.tex em out/ (PDF vetorial + PNG de pré-visualização).
# Uso (PowerShell, a partir de qualquer pasta):  .\ilustracoes\r8\resultados\compilar.ps1
# Requer MiKTeX (pdflatex) e, para o PNG, pdftoppm.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force out | Out-Null

$falhas = @()
foreach ($tex in Get-ChildItem -Filter 'figura_*.tex') {
    $nome = $tex.BaseName
    Write-Host "pdflatex $($tex.Name)"
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=out $tex.Name | Out-Null
    if ($LASTEXITCODE -ne 0) { $falhas += $tex.Name; continue }
    if (Get-Command pdftoppm -ErrorAction SilentlyContinue) {
        pdftoppm -png -r 150 -singlefile "out/$nome.pdf" "out/$nome"
    }
}

# Figura 4: o SVG já é o produto final
Copy-Item figura_04_cruzamento.svg out/ -Force

# limpa auxiliares (mantém .pdf, .png e .log)
Get-ChildItem out -Include *.aux -Recurse | Remove-Item -Force

if ($falhas) { Write-Error "Falhou: $($falhas -join ', ') (veja out/*.log)" } else { Write-Host 'OK' }
