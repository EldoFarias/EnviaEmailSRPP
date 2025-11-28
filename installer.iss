; Script do Inno Setup para Sistema de Envio Email SRPP
; https://jrsoftware.org/isinfo.php

#define MyAppName "Sistema de Envio Email SRPP"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "SINT"
#define MyAppExeName "EnviaEmailSRPP.exe"

[Setup]
; Informações básicas
AppId={{A5B8C3D4-E6F7-8901-2345-67890ABCDEF1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\SINT\EnviaEmailSRPP
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; Arquivo de saída
OutputDir=installer_output
OutputBaseFilename=EnviaEmailSRPP_Setup_v{#MyAppVersion}
; Configurações de compressão
Compression=lzma2/max
SolidCompression=yes
; Configurações de privilégios
PrivilegesRequired=admin
; Informações visuais
WizardStyle=modern
SetupIconFile=compiler:SetupClassicIcon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
; Informações de versão
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Sistema de Envio Automático de PDFs por Email

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos adicionais:"; Flags: unchecked
Name: "startupicon"; Description: "Iniciar automaticamente com o Windows"; GroupDescription: "Inicialização automática:"; Flags: unchecked

[Files]
Source: "dist\EnviaEmailSRPP.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.ini.example"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
; IMPORTANTE: config.ini não é copiado (contém senhas)

[Dirs]
Name: "{app}\logs"; Permissions: users-full

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Configurar Sistema"; Filename: "notepad.exe"; Parameters: """{app}\config.ini"""
Name: "{group}\Ver Logs"; Filename: "{app}\logs"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "notepad.exe"; Parameters: """{app}\config.ini"""; Description: "Configurar credenciais agora"; Flags: postinstall shellexec skipifsilent nowait
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: postinstall skipifsilent nowait

[Code]
// Função para verificar se config.ini existe, senão cria a partir do .example
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  ConfigExample: String;
begin
  if CurStep = ssPostInstall then
  begin
    ConfigFile := ExpandConstant('{app}\config.ini');
    ConfigExample := ExpandConstant('{app}\config.ini.example');

    // Se config.ini não existe, copia do exemplo
    if not FileExists(ConfigFile) then
    begin
      FileCopy(ConfigExample, ConfigFile, False);
      MsgBox('O arquivo config.ini foi criado.' + #13#10 +
             'IMPORTANTE: Configure suas credenciais antes de usar o sistema!',
             mbInformation, MB_OK);
    end;
  end;
end;

// Mensagem de boas-vindas
function InitializeSetup(): Boolean;
begin
  Result := True;
  MsgBox('Bem-vindo ao instalador do Sistema de Envio Email SRPP!' + #13#10 + #13#10 +
         'Este assistente irá instalar o sistema em seu computador.' + #13#10 + #13#10 +
         'REQUISITOS:' + #13#10 +
         '- SQL Server ODBC Driver 17' + #13#10 +
         '- Acesso ao banco de dados SRPP' + #13#10 +
         '- Credenciais de email (Gmail ou Outlook)',
         mbInformation, MB_OK);
end;

// Mensagem final
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    MsgBox('Instalação concluída!' + #13#10 + #13#10 +
           'PRÓXIMOS PASSOS:' + #13#10 +
           '1. Configure o arquivo config.ini com suas credenciais' + #13#10 +
           '2. Execute o sistema' + #13#10 +
           '3. Verifique os logs em caso de erro' + #13#10 + #13#10 +
           'Para suporte, consulte o arquivo README.md',
           mbInformation, MB_OK);
  end;
end;
