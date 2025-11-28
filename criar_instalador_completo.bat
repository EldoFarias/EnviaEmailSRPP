@echo off
echo ===============================================
echo  Sistema de Envio Email SRPP
echo  Build Completo: EXE + Instalador
echo ===============================================
echo.

REM Verificar se Inno Setup está instalado
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%INNO_PATH%" (
    echo [AVISO] Inno Setup 6 nao encontrado!
    echo.
    echo Para criar o instalador profissional:
    echo 1. Baixe Inno Setup em: https://jrsoftware.org/isdl.php
    echo 2. Instale no caminho padrao
    echo 3. Execute este script novamente
    echo.
    echo Por enquanto, apenas o EXE sera criado.
    echo.
    pause
)

echo [ETAPA 1/3] Compilando executavel...
call build.bat
if not exist "dist\EnviaEmailSRPP.exe" (
    echo.
    echo [ERRO] Falha ao criar executavel!
    pause
    exit /b 1
)

echo.
echo [ETAPA 2/3] Copiando arquivos necessarios...
if not exist "dist" mkdir dist
copy /Y "config.ini.example" "dist\"
copy /Y "README.md" "dist\"
copy /Y "INSTALACAO.md" "dist\"

echo.
if exist "%INNO_PATH%" (
    echo [ETAPA 3/3] Criando instalador profissional...
    "%INNO_PATH%" "installer.iss"

    if exist "installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe" (
        echo.
        echo ===============================================
        echo  BUILD COMPLETO COM SUCESSO!
        echo ===============================================
        echo.
        echo Arquivos gerados:
        echo.
        echo 1. EXECUTAVEL STANDALONE:
        echo    dist\EnviaEmailSRPP.exe
        echo.
        echo 2. INSTALADOR PROFISSIONAL:
        echo    installer_output\EnviaEmailSRPP_Setup_v1.0.0.exe
        echo.
        echo RECOMENDACAO:
        echo - Use o INSTALADOR para distribuir nas maquinas
        echo - Ele cria atalhos, configura paths, etc.
        echo.
        echo DISTRIBUICAO:
        echo - Envie apenas: EnviaEmailSRPP_Setup_v1.0.0.exe
        echo - Tamanho tipico: 15-20 MB
        echo.
    ) else (
        echo [ERRO] Falha ao criar instalador!
    )
) else (
    echo [ETAPA 3/3] PULADO - Inno Setup nao instalado
    echo.
    echo ===============================================
    echo  EXE CRIADO COM SUCESSO!
    echo ===============================================
    echo.
    echo Arquivo: dist\EnviaEmailSRPP.exe
    echo.
    echo Para criar instalador profissional:
    echo 1. Instale Inno Setup
    echo 2. Execute este script novamente
    echo.
)

echo.
echo Pressione qualquer tecla para abrir a pasta...
pause > nul
explorer dist

