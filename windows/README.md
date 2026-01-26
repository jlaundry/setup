
```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jlaundry/setup/refs/heads/main/windows/setup.reg" -OutFile "setup.reg"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jlaundry/setup/refs/heads/main/windows/tzformat.reg" -OutFile "tzformat.reg"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jlaundry/setup/refs/heads/main/windows/Remove-EdgeNonsense.reg" -OutFile "Remove-EdgeNonsense.reg"

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jlaundry/setup/refs/heads/main/windows/Add-ASRRules.ps1" -OutFile "Add-ASRRules.ps1"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/jlaundry/setup/refs/heads/main/windows/Remove-DefaultApps.ps1" -OutFile "Remove-DefaultApps.ps1"

reg.exe import setup.reg
reg.exe import tzformat.reg
reg.exe import Remove-EdgeNonsense.reg

powershell.exe -ExecutionPolicy Bypass .\Remove-DefaultApps.ps1
powershell.exe -ExecutionPolicy Bypass .\Add-ASRRules.ps1

```