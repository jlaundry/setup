
$commercialIDValue = "eeeeeeee-eeee-eeee-eeee-4be118629b68"

$vCommercialIDPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection"
$GPOCommercialIDPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
New-ItemProperty -Path $vCommercialIDPath -Name CommercialId -PropertyType String -Value $commercialIDValue

$deviceNameOptInPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
New-ItemProperty -Path $deviceNameOptInPath -Name AllowDeviceNameInTelemetry -PropertyType DWord -Value 1

$allowUCProcessingPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
New-ItemProperty -Path $allowUCProcessingPath -Name AllowUpdateComplianceProcessing -PropertyType DWord -Value 16
