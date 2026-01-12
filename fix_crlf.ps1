$files = Get-ChildItem -Path . -Recurse -Include *.py,*.sh,*.bash,Makefile,pretix.bash
foreach ($file in $files) {
    if ($file.FullName -notmatch "\\.git\\" -and $file.FullName -notmatch "\\venv\\") {
        $content = [IO.File]::ReadAllText($file.FullName)
        if ($content -match "`r`n") {
            $content = $content -replace "`r`n", "`n"
            [IO.File]::WriteAllText($file.FullName, $content)
            Write-Host "Converted: $($file.Name)"
        }
    }
}
