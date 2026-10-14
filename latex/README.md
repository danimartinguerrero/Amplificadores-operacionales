# Instrumentación Electrónica — Sesión 1: Amplificadores operacionales

Apuntes de fundamentos y PreLab (LaTeX), con el mismo estilo que los apuntes de Electromagnetismo I.

## Compilación

```bash
cd latex
latexmk -pdf main.tex      # pdfLaTeX + biber
```

## Estructura

| Fichero | Contenido |
|---|---|
| `main.tex`, `portada.tex`, `preambulo.tex` | Documento, portada y preámbulo |
| `secciones/01`–`04` | **Parte I. Fundamentos**: señales y amplificadores, impedancia y Laplace, Bode, el AO |
| `secciones/05`–`09` | **Parte II. PreLab**: recuadros amarillos del guion (inversor, no inversor, inversor generalizado/filtro) y resumen |
| `figuras/` | Esquemas (circuitikz) y gráficas (pgfplots) |
| `referencias.bib` | Bibliografía |
