@echo off
echo ========================================
echo  Sistema de Envio Email SRPP - Build
echo ========================================
echo.

echo [1/4] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo [2/4] Instalando dependencias necessarias...
pip install pyinstaller pyodbc watchdog openpyxl --quiet

echo [3/4] Compilando executavel com PyInstaller...
pyinstaller sender.spec --clean --noconfirm

echo [4/4] Verificando resultado...
if exist "dist\EnviaEmailSRPP.exe" (
    echo.
    echo ========================================
    echo  BUILD CONCLUIDO COM SUCESSO!
    echo ========================================
    echo.
    echo Executavel criado: dist\EnviaEmailSRPP.exe
    echo.
    echo PROXIMOS PASSOS:
    echo 1. Copie o arquivo config.ini.example para config.ini
    echo 2. Configure suas credenciais no config.ini
    echo 3. Execute EnviaEmailSRPP.exe
    echo.
) else (
    echo.
    echo ========================================
    echo  ERRO NO BUILD!
    echo ========================================
    echo Verifique os logs acima para detalhes.
    echo.
)

pause
