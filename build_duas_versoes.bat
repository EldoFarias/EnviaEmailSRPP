@echo off
echo ========================================
echo  Build - Duas Versoes do Executavel
echo ========================================
echo.
echo Este script vai gerar:
echo 1. EnviaEmailSRPP.exe         (SEM console - Producao)
echo 2. EnviaEmailSRPP_Debug.exe   (COM console - Testes)
echo.
pause

echo.
echo [1/3] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo [2/3] Instalando dependencias...
pip install pyinstaller pyodbc watchdog openpyxl --quiet

echo.
echo ========================================
echo  VERSAO 1: SEM CONSOLE (Producao)
echo ========================================
echo.
echo [3a/3] Compilando versao de PRODUCAO (background, sem console)...

pyinstaller --onefile ^
    --name EnviaEmailSRPP ^
    --noconsole ^
    --hidden-import pyodbc ^
    --hidden-import watchdog ^
    --hidden-import watchdog.observers ^
    --hidden-import watchdog.events ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.styles ^
    --hidden-import openpyxl.utils ^
    --add-data "config.ini.example;." ^
    --clean ^
    --noconfirm ^
    sender.py

if exist "dist\EnviaEmailSRPP.exe" (
    echo [OK] Versao de PRODUCAO criada com sucesso!
) else (
    echo [ERRO] Falha ao criar versao de producao!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  VERSAO 2: COM CONSOLE (Debug/Testes)
echo ========================================
echo.
echo [3b/3] Compilando versao de DEBUG (com console para logs)...

pyinstaller --onefile ^
    --name EnviaEmailSRPP_Debug ^
    --console ^
    --hidden-import pyodbc ^
    --hidden-import watchdog ^
    --hidden-import watchdog.observers ^
    --hidden-import watchdog.events ^
    --hidden-import openpyxl ^
    --hidden-import openpyxl.styles ^
    --hidden-import openpyxl.utils ^
    --add-data "config.ini.example;." ^
    --clean ^
    --noconfirm ^
    sender.py

if exist "dist\EnviaEmailSRPP_Debug.exe" (
    echo [OK] Versao de DEBUG criada com sucesso!
) else (
    echo [ERRO] Falha ao criar versao de debug!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  BUILD CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Arquivos criados em: dist\
echo.
echo 1. EnviaEmailSRPP.exe (~15 MB)
echo    - SEM janela de console
echo    - Roda em background
echo    - Aparece apenas no Gerenciador de Tarefas
echo    - Usuario NAO pode fechar acidentalmente
echo    - IDEAL PARA: Producao / Instalacao em maquinas
echo.
echo 2. EnviaEmailSRPP_Debug.exe (~15 MB)
echo    - COM janela de console
echo    - Mostra logs em tempo real
echo    - Usuario pode ver o que esta acontecendo
echo    - Ctrl+C para encerrar
echo    - IDEAL PARA: Testes / Diagnostico de problemas
echo.
echo ========================================
echo  COMO USAR
echo ========================================
echo.
echo PRODUCAO (Instalacao em maquinas):
echo - Use: EnviaEmailSRPP.exe
echo - Coloque na inicializacao do Windows
echo - Usuario nao ve nada, roda em background
echo - Para parar: Gerenciador de Tarefas
echo.
echo TESTES/DEBUG (Desenvolvimento):
echo - Use: EnviaEmailSRPP_Debug.exe
echo - Abre console com logs em tempo real
echo - Mais facil para diagnosticar problemas
echo - Para parar: Ctrl+C ou fechar janela
echo.
echo ========================================
echo.

echo Deseja abrir a pasta dist?
pause
explorer dist
