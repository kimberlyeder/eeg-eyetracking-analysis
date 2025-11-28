$dest = "c:\Users\Display\Desktop\Kim-Analysis\eeg-eyetracking-data-analysis\asc_files"
New-Item -ItemType Directory -Path $dest -Force | Out-Null

$files = @("subj01.asc","subj02.asc","subj03.asc")
foreach ($f in $files) {
    $path = Join-Path $dest $f
    if (-not (Test-Path $path)) {
        @(
            "; Placeholder .asc file"
            "; Filename: $f"
            "; Replace this content with your real ASC export"
            ":Start"
        ) | Out-File -FilePath $path -Encoding UTF8
    }
}

Write-Host "Created folder and placeholder .asc files at $dest"
