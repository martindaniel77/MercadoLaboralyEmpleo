# Carpeta de Archivos de Power BI - Etapa 4

Guarda en este directorio el archivo de tu proyecto de Power BI:

**Nombre de archivo esperado:**
`Tableros_GigEconomy_Etapa4.pbix`

**Ruta completa:**
`MercadoLaboralyEmpleo/powerbi/Tableros_GigEconomy_Etapa4.pbix`

---

## Integración con la Aplicación Web (Flask):

1. **Descarga directa:** 
   Al colocar el archivo `Tableros_GigEconomy_Etapa4.pbix` aquí, la aplicación web Flask habilitará automáticamente la descarga directa desde el botón **"Descargar archivo .PBIX"** en la ruta `/descargar-powerbi`.

2. **Visualización interactiva embebida (Iframe):**
   - Abre el archivo en Power BI Desktop.
   - Ve a **Archivo** > **Publicar** > **Publicar en Power BI**.
   - En tu navegador en `app.powerbi.com`: Abre el informe > **Archivo** > **Insertar informe** > **Publicar en la web (público)**.
   - Copia la URL que te genera (`https://app.powerbi.com/view?r=...`).
   - Pégala en `app.py` en la variable `ETAPA4_POWERBI_URL` o define la variable de entorno:
     ```bash
     $env:ETAPA4_POWERBI_URL="https://app.powerbi.com/view?r=..."
     ```
   - La página web mostrará el informe interactivo embebido en tiempo real.
