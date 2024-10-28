
# https://docs.microsoft.com/en-us/windows/application-management/apps-in-windows-10

# Things that won't be missed on a corporate laptop
Get-AppxPackage Microsoft.BingNews | Remove-AppxPackage
Get-AppxPackage Microsoft.Getstarted | Remove-AppxPackage
Get-AppxPackage Microsoft.MicrosoftOfficeHub | Remove-AppxPackage
Get-AppxPackage Microsoft.SkypeApp | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsMaps | Remove-AppxPackage
Get-AppxPackage Microsoft.YourPhone | Remove-AppxPackage
Get-AppxPackage MicrosoftTeams | Remove-AppxPackage  # Personal account, this is not Teams (Work or School)
Get-AppxPackage MicrosoftWindows.Client.WebExperience | Remove-AppxPackage

# Things that won't be missed on a lightweight VM
Get-AppxPackage Clipchamp.Clipchamp | Remove-AppxPackage
Get-AppxPackage Microsoft.549981C3F5F10 | Remove-AppxPackage  # Cortana
Get-AppxPackage Microsoft.Advertising.Xaml | Remove-AppxPackage
Get-AppxPackage Microsoft.BingWeather | Remove-AppxPackage
Get-AppxPackage Microsoft.DesktopAppInstaller | Remove-AppxPackage
Get-AppxPackage Microsoft.GetHelp | Remove-AppxPackage
Get-AppxPackage Microsoft.Microsoft3DViewer | Remove-AppxPackage
Get-AppxPackage Microsoft.MicrosoftSolitaireCollection | Remove-AppxPackage
Get-AppxPackage Microsoft.MicrosoftStickyNotes | Remove-AppxPackage
Get-AppxPackage Microsoft.MixedReality.Portal | Remove-AppxPackage
Get-AppxPackage Microsoft.Office.OneNote | Remove-AppxPackage
Get-AppxPackage Microsoft.OutlookForWindows | Remove-AppxPackage
Get-AppxPackage Microsoft.People | Remove-AppxPackage
Get-AppxPackage Microsoft.ScreenSketch | Remove-AppxPackage
Get-AppxPackage Microsoft.Services.Store.Engagement | Remove-AppxPackage
Get-AppxPackage Microsoft.StorePurchaseApp | Remove-AppxPackage
Get-AppxPackage Microsoft.Wallet | Remove-AppxPackage
Get-AppxPackage Microsoft.Windows.Photos | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsAlarms | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsCalculator | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsCamera | Remove-AppxPackage
Get-AppxPackage microsoft.windowscommunicationsapps | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsSoundRecorder | Remove-AppxPackage
Get-AppxPackage Microsoft.ZuneMusic | Remove-AppxPackage
Get-AppxPackage Microsoft.ZuneVideo | Remove-AppxPackage

# Things that you __might__ still want on a lightweight VM, but probably not
Get-AppxPackage Microsoft.MSPaint | Remove-AppxPackage
Get-AppxPackage Microsoft.WindowsFeedbackHub | Remove-AppxPackage
Get-AppxPackage Microsoft.Xbox.TCUI | Remove-AppxPackage
Get-AppxPackage Microsoft.XboxApp | Remove-AppxPackage
Get-AppxPackage Microsoft.XboxGameOverlay | Remove-AppxPackage
Get-AppxPackage Microsoft.XboxGamingOverlay | Remove-AppxPackage
Get-AppxPackage Microsoft.XboxIdentityProvider | Remove-AppxPackage
Get-AppxPackage Microsoft.XboxSpeechToTextOverlay | Remove-AppxPackage

# Disable Print Spooler
Stop-Service -Name Spooler -Force
Set-Service -Name Spooler -StartupType Disabled

# Remove OneDrive
foreach ($onedrive in (Get-ChildItem $Env:localappdata\Microsoft\OneDrive\*\OneDriveSetup.exe)) {Start-Process -FilePath $onedrive /uninstall}

# Disable Widgets
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Dsh" -Name AllowNewsAndInterests -PropertyType DWord -Value 0

# On Windows IoT LTSC, install Windows Store
wsreset -i
