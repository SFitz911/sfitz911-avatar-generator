# SFitz911 Avatar Generator - Auto Sync Videos
# Continuously monitors and downloads new videos from H100

param(
    [string]$RemoteHost = "173.207.82.240",
    [int]$Port = 40106,
    [string]$KeyPath = "e:\Avatar-Generator\sfitz911-avatar-generator\agent_key",
    [string]$LocalFolder = "E:\DATA_1TB\Desktop\Ai-Gen-Clips",
    [int]$IntervalSeconds = 30
)

Write-Host "=================================================="
Write-Host "🔄 Auto-Sync Videos from H100"
Write-Host "=================================================="
Write-Host "Local folder: $LocalFolder"
Write-Host "Check interval: $IntervalSeconds seconds"
Write-Host "Press Ctrl+C to stop"
Write-Host "=================================================="
Write-Host ""

# Create local folder if it doesn't exist
if (-not (Test-Path $LocalFolder)) {
    New-Item -ItemType Directory -Path $LocalFolder -Force | Out-Null
}

$syncCount = 0

while ($true) {
    $syncCount++
    $timestamp = Get-Date -Format "HH:mm:ss"
    
    Write-Host "[$timestamp] Sync #$syncCount - Checking for new videos..."
    
    try {
        # Download from LTX-2
        $ltx2Files = scp -P $Port -i $KeyPath "root@${RemoteHost}:/workspace/LTX-2/*.mp4" $LocalFolder 2>&1
        
        # Download from API outputs
        $apiFiles = scp -P $Port -i $KeyPath "root@${RemoteHost}:/workspace/sfitz911-avatar-generator/outputs/*.mp4" $LocalFolder 2>&1
        
        # Count new files
        $recentFiles = Get-ChildItem $LocalFolder -Filter *.mp4 | Where-Object { $_.LastWriteTime -gt (Get-Date).AddSeconds(-$IntervalSeconds) }
        
        if ($recentFiles.Count -gt 0) {
            Write-Host "  ✅ Downloaded $($recentFiles.Count) new video(s)!" -ForegroundColor Green
            $recentFiles | ForEach-Object { Write-Host "     - $($_.Name)" -ForegroundColor Cyan }
        } else {
            Write-Host "  ⏸️  No new videos"
        }
        
    } catch {
        Write-Host "  ⚠️  Error: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # Wait before next check
    Start-Sleep -Seconds $IntervalSeconds
}
