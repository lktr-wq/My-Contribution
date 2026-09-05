param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Output directory already exists' }
$out = New-Item -ItemType Directory -Path $OutputDirectory
$records = @()
function Capture([string]$Name, [string]$Route) {
    $uri = 'https://api.github.com/' + $Route
    try {
        $response = Invoke-RestMethod -Uri $uri -TimeoutSec 30 -Headers @{Accept='application/vnd.github+json'; 'User-Agent'='CCCL-local-evidence-audit'}
    } catch {
        [pscustomobject]@{url=$uri; captured_at_utc=[DateTime]::UtcNow.ToString('o'); error=$_.Exception.Message; details=$_.ErrorDetails.Message} | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out.FullName ($Name+'-error.json')) -Encoding UTF8
        throw
    }
    $response | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath (Join-Path $out.FullName ($Name+'.json')) -Encoding UTF8
    $script:records += [pscustomobject]@{name=$Name; url=$uri; captured_at_utc=[DateTime]::UtcNow.ToString('o')}
    $script:records | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out.FullName 'requests.json') -Encoding UTF8
    return $response
}
$queries = @('repo:NVIDIA/cccl "partial tile" reduce', 'repo:NVIDIA/cccl "tail" "reduce"', 'repo:NVIDIA/cccl "ConsumePartialTile"', 'repo:NVIDIA/cccl "vectorize" "reduce"')
for ($i=0; $i -lt $queries.Count; $i++) {
    $r = Capture ('search-'+$i) ('search/issues?q='+[uri]::EscapeDataString($queries[$i])+'&per_page=100')
    if ($r.incomplete_results -or $r.total_count -gt 100) { throw 'Incomplete search; do not claim full coverage' }
    Write-Output ($queries[$i]+' -> '+$r.total_count)
}
foreach ($number in @(9762,10928,7571)) {
    $r = Capture ('pr-'+$number) ('repos/NVIDIA/cccl/pulls/'+$number)
    Write-Output ($number.ToString()+' '+$r.title+' merged='+$r.merged+' '+$r.merged_at)
}
$null = Capture 'issue-307' 'repos/NVIDIA/cccl/issues/307'
$null = Capture 'issue-307-comments' 'repos/NVIDIA/cccl/issues/307/comments?per_page=100'
$main = Capture 'main-commit' 'repos/NVIDIA/cccl/commits/main'
$source = Capture 'main-agent-reduce' ('repos/NVIDIA/cccl/contents/cub/cub/agent/agent_reduce.cuh?ref='+$main.sha)
[IO.File]::WriteAllBytes((Join-Path $out.FullName 'main-agent-reduce.cuh'), [Convert]::FromBase64String($source.content))
$records | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $out.FullName 'requests.json') -Encoding UTF8
Write-Output ('main='+$main.sha)
