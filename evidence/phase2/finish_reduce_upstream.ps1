param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$out = (Resolve-Path -LiteralPath $OutputDirectory).Path
$main = '486de1c44daf7d1a343cbbf0f5477e9bea8ad600'
$paths = @('cub/cub/agent/agent_reduce.cuh', 'cub/cub/warp/specializations/warp_reduce_shfl.cuh', 'cub/cub/block/specializations/block_reduce_warp_reductions.cuh')
$records = @()
foreach ($path in $paths) {
    $url = 'https://raw.githubusercontent.com/NVIDIA/cccl/'+$main+'/'+$path
    $file = Join-Path $out ('main-'+[IO.Path]::GetFileName($path))
    if (Test-Path -LiteralPath $file) { throw 'Refusing to overwrite existing artifact' }
    try {
        Invoke-WebRequest -Uri $url -OutFile $file -TimeoutSec 25
        $records += [pscustomobject]@{url=$url; commit=$main; captured_at_utc=[DateTime]::UtcNow.ToString('o'); sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $file).Hash}
    } catch {
        $records += [pscustomobject]@{url=$url; error=$_.Exception.Message; captured_at_utc=[DateTime]::UtcNow.ToString('o')}
    }
    $records | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out 'raw-source-requests.json') -Encoding UTF8
}
$local = 'D:/Projects/Open-Source Contribution/CCCL_CUB'
foreach ($commit in @('1fb7869e6c', '8f2803715e')) {
    & git -c ('safe.directory='+$local) -C $local show $commit -- cub/cub/agent/agent_reduce.cuh | Set-Content -LiteralPath (Join-Path $out ('local-'+$commit+'.patch')) -Encoding UTF8
    if ($LASTEXITCODE -ne 0) { throw 'git show failed' }
}
$items = @{}
for ($i=0; $i -lt 4; $i++) {
    $r = Get-Content -LiteralPath (Join-Path $out ('search-'+$i+'.json')) -Raw | ConvertFrom-Json
    if ($r.incomplete_results -or $r.items.Count -ne $r.total_count) { throw 'Search capture incomplete' }
    foreach ($item in $r.items) { $items[$item.number] = $item }
}
$items.Values | Sort-Object number | Select-Object number,title,state,html_url,updated_at | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out 'search-index.json') -Encoding UTF8
Write-Output ('Unique search results: '+$items.Count)
$records | Format-Table -AutoSize
