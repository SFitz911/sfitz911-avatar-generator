# SFitz911 Avatar Generator - Upload Reference Images
# Uploads photos from local computer to H100 instance

param(
    [string]$LocalFolder = "E:\DATA_1TB\Media\Nextwork-Team-Pic",
    [string]$RemoteHost = "173.207.82.240",
    [int]$Port = 40106,
    [string]$KeyPath = "agent_key",
    [string]$RemoteFolder = "/workspace/LTX-2/natasha_refs"
)

Write-Host "=================================================="
Write-Host "📸 Uploading Reference Images to H100"
Write-Host "=================================================="
Write-Host "Local folder: $LocalFolder"
Write-Host "Remote folder: $RemoteFolder"
Write-Host ""

# Check if local folder exists
if (-not (Test-Path $LocalFolder)) {
    Write-Host "❌ Error: Local folder not found: $LocalFolder" -ForegroundColor Red
    exit 1
}

# Count files
$jpgFiles = Get-ChildItem "$LocalFolder\*.jpg" -ErrorAction SilentlyContinue
$pngFiles = Get-ChildItem "$LocalFolder\*.png" -ErrorAction SilentlyContinue
$totalFiles = $jpgFiles.Count + $pngFiles.Count

if ($totalFiles -eq 0) {
    Write-Host "❌ No JPG or PNG files found in $LocalFolder" -ForegroundColor Red
    exit 1
}

Write-Host "📊 Found $totalFiles image(s) to upload"
Write-Host ""

# Upload JPG files
if ($jpgFiles.Count -gt 0) {
    Write-Host "📤 Uploading JPG files..."
    scp -P $Port -i $KeyPath "$LocalFolder\*.jpg" "root@${RemoteHost}:${RemoteFolder}/"
}

# Upload PNG files
if ($pngFiles.Count -gt 0) {
    Write-Host "📤 Uploading PNG files..."
    scp -P $Port -i $KeyPath "$LocalFolder\*.png" "root@${RemoteHost}:${RemoteFolder}/"
}

Write-Host ""
Write-Host "✅ Upload complete!"
Write-Host "📁 Files uploaded to: $RemoteFolder"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. SSH into instance: ssh -p $Port -i $KeyPath root@$RemoteHost"
Write-Host "2. List files: ls -lh $RemoteFolder/"
Write-Host "3. Run generation with multiple keyframes"
