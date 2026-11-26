@echo off
REM ==============================================================
REM Doble clic para instalar librerias y abrir la aplicacion
REM ==============================================================
cd /d "%~dp0"
if not exist ".streamlit\secrets.toml" (
    echo FALTA el archivo .streamlit\secrets.toml con la URL y la llave de Supabase.
    echo Copia .streamlit\secrets.toml.example como secrets.toml y completa los datos.
    pause
    exit /b
)
python -m pip install -r requirements.txt
python -m pruebas.prueba_calculos
python -m streamlit run app.py
pause
