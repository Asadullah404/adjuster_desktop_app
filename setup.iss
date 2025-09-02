[Setup]
AppName=SMMC - PDF Margin Adjuster
AppVersion=1.0.0
AppVerName=SMMC v1.0.0
AppPublisher=Your Company Name
AppPublisherURL=https://yourwebsite.com
AppSupportURL=https://yourwebsite.com/support
AppUpdatesURL=https://yourwebsite.com/updates
AppId={{B4F5E8A2-1234-4567-8901-123456789ABC}}
DefaultDirName={autopf}\SMMC
DefaultGroupName=SMMC
AllowNoIcons=yes
LicenseFile=license.txt
InfoBeforeFile=readme.txt
OutputDir=output
OutputBaseFilename=SMMC_PDF_Adjuster_v1.0.0_Setup
SetupIconFile=app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64 x86
ArchitecturesInstallIn64BitMode=x64
MinVersion=6.1
UninstallDisplayIcon={app}\SMMC.exe
UninstallDisplayName=SMMC - PDF Margin Adjuster

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "contextmenu"; Description: "Add ""Process with SMMC"" to PDF context menu"; GroupDescription: "File associations:"; Flags: unchecked

[Files]
Source: "dist\SMMC.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "readme.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SMMC - PDF Margin Adjuster"; Filename: "{app}\SMMC.exe"; IconFilename: "{app}\SMMC.exe"; Comment: "Adjust PDF margins and add watermarks"
Name: "{group}\{cm:UninstallProgram,SMMC}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\SMMC - PDF Adjuster"; Filename: "{app}\SMMC.exe"; Tasks: desktopicon; Comment: "PDF Margin Adjuster with Watermark"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\SMMC"; Filename: "{app}\SMMC.exe"; Tasks: quicklaunchicon

[Registry]
; Add context menu for PDF files (optional)
Root: HKCR; Subkey: ".pdf\shell\ProcessWithSMMC"; ValueType: string; ValueName: ""; ValueData: "Process with SMMC"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: ".pdf\shell\ProcessWithSMMC\command"; ValueType: string; ValueName: ""; ValueData: """{app}\SMMC.exe"" ""%1"""; Tasks: contextmenu

[Run]
Filename: "{app}\SMMC.exe"; Description: "{cm:LaunchProgram,SMMC}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"
Type: filesandordirs; Name: "{localappdata}\SMMC"

[Messages]
WelcomeLabel1=Welcome to SMMC PDF Margin Adjuster Setup
WelcomeLabel2=This will install SMMC PDF Margin Adjuster with Watermark functionality on your computer.%n%nSMMC allows you to easily adjust PDF margins and add watermarks to your documents.%n%nIt is recommended that you close all other applications before continuing.