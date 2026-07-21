# Sincronizeaza coduri.csv pe server2 pentru skill-ul "printhouse" al lui Otto.
# Ruleaza dupa fiecare regenerare a catalogului (build_site.py).
C:\Windows\System32\OpenSSH\scp.exe "$PSScriptRoot\coduri.csv" cristi@192.168.0.106:printhouse/coduri.csv
Write-Host "coduri.csv sincronizat pe server2 (~/printhouse/)"
