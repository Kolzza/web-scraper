@echo off

if "%~4"=="" (
    echo Usage: %0 ^<Seed File^> ^<Number of Pages^> ^<Max Hops^> ^<Output Directory^>
    exit /b 1
)

echo Installing Dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1

if exist "%~1" (
    echo Reading Seed URLs from %~1...
) else (
    echo Seed File %~1 does not exist.
    exit /b 1
)

if not exist "%~4" (
    echo Output directory not found!
    echo Creating %~4\
    mkdir "%~4"
)

echo Crawling...
for /f "delims=" %%a in ('powershell -command "[int](Get-Date -UFormat %%s)"') do set start_time=%%a

python WikiScrape\main.py "%~1" "%~2" "%~3" "%~4"
set exit_code=%ERRORLEVEL%

if %exit_code% neq 0 (
    echo Python script failed with exit code %exit_code%
    exit /b %exit_code%
)

for /f "tokens=*" %%a in ('dir /s /a /b "%~4" ^| find /c /v ""') do set count=%%a
for /f "tokens=*" %%b in ('dir /s /a /b "%~4" ^| findstr /v "^$"') do set size=%%~zb

for /f "delims=" %%a in ('powershell -command "[int](Get-Date -UFormat %%s)"') do set end_time=%%a

set /a duration=%end_time% - %start_time%
if %duration% gtr 0 (
    set /a throughput=%count% / %duration%
) else (
    set throughput=0
)

echo Finished in %duration% seconds!
echo Collected %size% bytes of data across %count% files
echo Scraping throughput: %throughput% files per second
exit /b
