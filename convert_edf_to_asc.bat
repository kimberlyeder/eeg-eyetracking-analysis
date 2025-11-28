@echo off
REM Batch script to convert EDF files to ASC format
REM Requires edf2asc.exe from SR Research
REM Download from: https://www.sr-research.com/support/

echo Converting EDF files to ASC format...
echo.

REM Check if edf2asc.exe exists
where edf2asc.exe >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: edf2asc.exe not found!
    echo Please download EyeLink Developers Kit from SR Research
    echo and add edf2asc.exe to your PATH or this directory
    pause
    exit /b 1
)

REM Convert all EDF files in Data directory
for %%f in (Data\*.EDF) do (
    echo Converting %%f...
    edf2asc.exe -t -s -miss -1.0 -y "%%f"
    if %ERRORLEVEL% EQU 0 (
        echo   Success!
    ) else (
        echo   Failed!
    )
    echo.
)

echo.
echo Conversion complete!
echo ASC files should now be in the Data directory
pause
