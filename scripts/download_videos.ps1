# SFitz911 Avatar Generator - Auto Download Videos
# Downloads generated videos from H100 to local folder

param(
    [string]$RemoteHost = "173.207.82.240",
    [int]$Port = 40106,
    [string]$KeyPath = "e:\Avatar-Generator\sfitz911-avatar-generator\agent_key",
    [string]$LocalFolder = "E:\DATA_1TB\Desktop\Ai-Gen-Clips"
)

Write-Host "=================================================="
Write-Host "📥 Downloading Videos from H100"
Write-Host "=================================================="

# Create local folder if it doesn't exist
if (-not (Test-Path $LocalFolder)) {
    New-Item -ItemType Directory -Path $LocalFolder -Force | Out-Null
    Write-Host "✅ Created folder: $LocalFolder"
}

# Download from LTX-2 output
Write-Host ""
Write-Host "📹 Downloading LTX-2 videos..."
scp -P $Port -i $KeyPath "root@${RemoteHost}:/workspace/LTX-2/*.mp4" $LocalFolder 2>$null

# Download from API outputs
Write-Host "📹 Downloading API output videos..."
scp -P $Port -i $KeyPath "root@${RemoteHost}:/workspace/sfitz911-avatar-generator/outputs/*.mp4" $LocalFolder 2>$null

Write-Host ""
Write-Host "✅ Download complete!"
Write-Host "📁 Videos saved to: $LocalFolder"
Write-Host ""

# List downloaded files
Write-Host "Downloaded files:"
Get-ChildItem $LocalFolder -Filter *.mp4 | Sort-Object LastWriteTime -Descending | Select-Object -First 10 | Format-Table Name, Length, LastWriteTime -AutoSize
