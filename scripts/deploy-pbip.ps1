param (
  [string]$ModulePath = "./FabricPS-PBIP.psm1",
  [string]$PbipPath = "./powerbi/AdventureWorks Report.pbip",
  [string]$TenantId = $env:TENANT_ID,
  [string]$ClientId = $env:CLIENT_ID,
  [string]$ClientSecret = $env:CLIENT_SECRET,
  [string]$WorkspaceId = $env:WORKSPACE_ID
)

Write-Host "📁 Verifying custom PowerShell module at path: $ModulePath"
if (!(Test-Path $ModulePath)) {
  throw "❌ Module not found: $ModulePath"
}

Import-Module $ModulePath -Force

Write-Host "🔍 Available commands from '$ModulePath':"
Get-Command -Module (Get-Module -Name FabricPS-PBIP).Name | Format-Table Name, CommandType

if ([string]::IsNullOrEmpty($ClientId) -or [string]::IsNullOrEmpty($ClientSecret) -or `
    [string]::IsNullOrEmpty($TenantId) -or [string]::IsNullOrEmpty($WorkspaceId)) {
  throw "🔐 Missing required environment variables."
}

$SecureClientSecret = ConvertTo-SecureString -String $ClientSecret -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential($ClientId, $SecureClientSecret)

# Connect to Power BI
Import-Module MicrosoftPowerBIMgmt.Profile
Connect-PowerBIServiceAccount -ServicePrincipal -TenantId $TenantId -Credential $Credential

Write-Host "📁 Verifying PBIP project folder..."
if (!(Test-Path $PbipPath)) {
  throw "❌ PBIP project folder not found at path: $PbipPath"
}

Write-Host "📦 Deploying PBIP artifact using Import-FabricItem..."
Import-FabricItem -Path $PbipPath -WorkspaceId $WorkspaceId

Write-Host "✅ Deployment successful."
