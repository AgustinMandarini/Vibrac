@echo off

REM Activar el entorno virtual
call virtual_env\Scripts\activate.bat

REM Ejecutar PyInstaller para crear el ejecutable
pyinstaller --name rugit --onefile --windowed main.py

REM Definir variables para Inno Setup
set "MyAppName=Rugit"
set "MyAppVersion=0.1"
set "MyAppPublisher=Agustin Mandarini"
set "MyAppURL=https://www.baldorshop.com.ar/"
set "MyAppExeName=rugit.exe"

REM Crear archivo de configuración para Inno Setup
(
    echo #define MyAppName "%MyAppName%"
    echo #define MyAppVersion "%MyAppVersion%"
    echo #define MyAppPublisher "%MyAppPublisher%"
    echo #define MyAppURL "%MyAppURL%"
    echo #define MyAppExeName "%MyAppExeName%"

    echo [Setup]
    echo AppId={{B17A598F-724C-42EA-B219-F8FA8248F710}}
    echo AppName={#MyAppName}
    echo AppVersion={#MyAppVersion}
    echo AppPublisher={#MyAppPublisher}
    echo AppPublisherURL={#MyAppURL}
    echo AppSupportURL={#MyAppURL}
    echo AppUpdatesURL={#MyAppURL}
    echo DefaultDirName={userappdata}\{#MyAppName}
    echo DisableProgramGroupPage=yes
    echo OutputDir=C:\Users\Papablo\Desktop
    echo OutputBaseFilename=RUGIT_WINDOWS_0.1_setup
    echo Compression=lzma
    echo SolidCompression=yes
    echo WizardStyle=modern

    echo [Languages]
    echo Name: "english"; MessagesFile: "compiler:Default.isl"
    echo Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"


    echo [Tasks]
    echo Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

    echo [Files]
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\db\*"; DestDir: "{app}/db"; Flags: ignoreversion recursesubdirs createallsubdirs; Permissions: users-full
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\temp\*"; DestDir: "{app}/temp"; Flags: ignoreversion recursesubdirs createallsubdirs; Permissions: users-full
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\img\*"; DestDir: "{app}/img"; Flags: ignoreversion recursesubdirs createallsubdirs
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\template\*"; DestDir: "{app}/template"; Flags: ignoreversion recursesubdirs createallsubdirs
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\tests\*"; DestDir: "{app}/tests"; Flags: ignoreversion recursesubdirs createallsubdirs
    echo Source: "D:\Pablo\Boreas\Python\Agustin\Vibrac\ext_lib\wkhtmltox-0.12.6-1.msvc2015-win64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

    echo [Icons]
    echo Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
    echo Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

    echo [Run]
    echo Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
    echo Filename: "{tmp}\wkhtmltox-0.12.6-1.msvc2015-win64.exe"; Parameters: "/S"; StatusMsg: "Instalando wkhtmltopdf..."; Flags: waituntilterminated
) > config.iss

REM Ejecutar Inno Setup Compiler
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /O"C:\Users\Papablo\Desktop" config.iss

REM Limpiar archivos temporales
del config.iss

echo [92mInstalador de rugit creado y guardado en el escritorio[0m

REM Pausar para permitir ver los mensajes de error
pause