
[Setup]
AppName=Jagdamba Inspection Software
AppVersion=1.0
DefaultDirName={pf}\JagdambaInspection
OutputBaseFilename=JagdambaInspectionSetup
[Files]
Source: "dist\app.exe"; DestDir: "{app}"
[Icons]
Name: "{desktop}\Jagdamba Inspection Software"; Filename: "{app}\app.exe"
