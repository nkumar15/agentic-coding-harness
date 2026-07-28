# Portable Agentic Coding Harness installer (Windows PowerShell).
#
# Usage:
#   irm <install-url> | iex
#   & { $s = irm <install-url> } ; Invoke-Expression "$s -Addon migration-workflow"
#
# Testing/offline usage:
#   .\install.ps1 -Source C:\path\to\package-dir-or-tarball.tar.gz
#   .\install.ps1 -AddonSource C:\path\to\addon-dir-or-tarball.tar.gz
#
# Env overrides: $env:INSTALL_REPO (default nkumar15/agentic-coding-harness), $env:INSTALL_VERSION (default latest)

param(
  [string]$Source = "",
  [string]$Addon = "",
  [string]$AddonSource = ""
)

$ErrorActionPreference = "Stop"

$Repo = if ($env:INSTALL_REPO) { $env:INSTALL_REPO } else { "nkumar15/agentic-coding-harness" }
$Version = if ($env:INSTALL_VERSION) { $env:INSTALL_VERSION } else { "latest" }

$Python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $Python) {
  Write-Error "python3 is required but was not found on PATH."
  exit 1
}
$PythonExe = $Python.Source

$TmpRoot = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid())
New-Item -ItemType Directory -Path $TmpRoot | Out-Null

function Copy-Merge($from, $to) {
  Get-ChildItem -Path $from -Recurse -Force | ForEach-Object {
    $relative = $_.FullName.Substring($from.Length).TrimStart('\', '/')
    $destination = Join-Path $to $relative
    if ($_.PSIsContainer) {
      New-Item -ItemType Directory -Force -Path $destination | Out-Null
    } else {
      New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
      Copy-Item -Path $_.FullName -Destination $destination -Force
    }
  }
}

function Fetch-Payload($src, $addonName, $workdir) {
  if ($src) {
    if (Test-Path -PathType Container $src) {
      return $src
    }
    if (Test-Path -PathType Leaf $src) {
      $extracted = Join-Path $workdir "extracted"
      New-Item -ItemType Directory -Force -Path $extracted | Out-Null
      tar -xzf $src -C $extracted
      return $extracted
    }
    Write-Error "-Source path not found: $src"
    exit 1
  }

  $repo = $Repo
  if ($addonName) { $repo = "nkumar15/$addonName" }

  if ($Version -eq "latest") {
    $apiUrl = "https://api.github.com/repos/$repo/releases/latest"
  } else {
    $apiUrl = "https://api.github.com/repos/$repo/releases/tags/$Version"
  }

  $release = Invoke-RestMethod -Uri $apiUrl -Headers @{ "User-Agent" = "install-script" }
  $asset = $release.assets | Where-Object { $_.name -eq "package.tar.gz" } | Select-Object -First 1
  if (-not $asset) {
    Write-Error "could not resolve a package.tar.gz release asset for $repo ($Version)"
    exit 1
  }

  $extracted = Join-Path $workdir "extracted"
  New-Item -ItemType Directory -Force -Path $extracted | Out-Null
  $tarball = Join-Path $workdir "package.tar.gz"
  Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $tarball
  tar -xzf $tarball -C $extracted
  return $extracted
}

try {
  $baseWork = Join-Path $TmpRoot "base"
  New-Item -ItemType Directory -Force -Path $baseWork | Out-Null
  $packageDir = Fetch-Payload $Source "" $baseWork

  $updateMode = Test-Path -PathType Container ".agents"
  $backupDir = Join-Path $TmpRoot "protected"
  New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

  $conventionsPath = ".agents/rules/project-conventions.md"
  $gatesPath = ".agents/process/gates.yaml"
  $configPath = ".agents/process/config.yaml"
  $keptConventions = $false
  $keptGates = $false
  $keptConfig = $false

  if ($updateMode) {
    if ((Test-Path $conventionsPath) -and -not (Select-String -Path $conventionsPath -Pattern "<FILL_IN" -Quiet)) {
      New-Item -ItemType Directory -Force -Path (Join-Path $backupDir ".agents/rules") | Out-Null
      Copy-Item $conventionsPath (Join-Path $backupDir $conventionsPath) -Force
      $keptConventions = $true
    }
    $packageGates = Join-Path $packageDir $gatesPath
    if ((Test-Path $gatesPath) -and (Test-Path $packageGates)) {
      $current = Get-Content $gatesPath -Raw
      $shipped = Get-Content $packageGates -Raw
      if ($current -ne $shipped) {
        New-Item -ItemType Directory -Force -Path (Join-Path $backupDir ".agents/process") | Out-Null
        Copy-Item $gatesPath (Join-Path $backupDir $gatesPath) -Force
        $keptGates = $true
      }
    }
    $packageConfig = Join-Path $packageDir $configPath
    if ((Test-Path $configPath) -and (Test-Path $packageConfig)) {
      $current = Get-Content $configPath -Raw
      $shipped = Get-Content $packageConfig -Raw
      if ($current -ne $shipped) {
        New-Item -ItemType Directory -Force -Path (Join-Path $backupDir ".agents/process") | Out-Null
        Copy-Item $configPath (Join-Path $backupDir $configPath) -Force
        $keptConfig = $true
      }
    }
  }

  Copy-Merge $packageDir "."

  if ($keptConventions) {
    Copy-Item (Join-Path $backupDir $conventionsPath) $conventionsPath -Force
    Write-Host "kept existing $conventionsPath (already filled in)"
  }
  if ($keptGates) {
    Copy-Item (Join-Path $backupDir $gatesPath) $gatesPath -Force
    Write-Host "kept existing $gatesPath (customized commands)"
  }
  if ($keptConfig) {
    Copy-Item (Join-Path $backupDir $configPath) $configPath -Force
    Write-Host "kept existing $configPath (customized provider)"
  }

  if ($Addon -or $AddonSource) {
    $addonWork = Join-Path $TmpRoot "addon"
    New-Item -ItemType Directory -Force -Path $addonWork | Out-Null
    $addonDir = Fetch-Payload $AddonSource $Addon $addonWork
    Copy-Merge $addonDir "."
    Write-Host "installed add-on: $(if ($Addon) { $Addon } else { $AddonSource })"
  }

  & $PythonExe scripts/configure.py
  & $PythonExe scripts/generate-agent-adapters.py
  & $PythonExe scripts/validate-agent-portability.py

  Write-Host "install complete."
}
finally {
  Remove-Item -Recurse -Force $TmpRoot -ErrorAction SilentlyContinue
}
