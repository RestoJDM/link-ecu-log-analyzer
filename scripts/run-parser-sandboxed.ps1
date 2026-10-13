[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$LogPath,

    [switch]$List
)

$ErrorActionPreference = 'Stop'

$projectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$candidatePath = if ([System.IO.Path]::IsPathRooted($LogPath)) {
    [System.IO.Path]::GetFullPath($LogPath)
} else {
    [System.IO.Path]::GetFullPath((Join-Path $projectRoot $LogPath))
}

$relativePath = [System.IO.Path]::GetRelativePath($projectRoot, $candidatePath)
$parentPrefix = '..' + [System.IO.Path]::DirectorySeparatorChar

if (
    $relativePath -eq '..' -or
    $relativePath.StartsWith($parentPrefix, [System.StringComparison]::Ordinal) -or
    [System.IO.Path]::IsPathRooted($relativePath)
) {
    throw "The log must be inside the project folder: $projectRoot"
}

if (-not (Test-Path -LiteralPath $candidatePath -PathType Leaf)) {
    throw "Log file not found: $candidatePath"
}

if ([System.IO.Path]::GetExtension($candidatePath) -ine '.llgx') {
    throw 'The input must be a Link ECU .llgx log.'
}

# Reject junctions and symbolic links so an apparently local path cannot lead
# outside the mounted project directory.
$currentPath = $candidatePath
while ($currentPath -and $currentPath -ne $projectRoot) {
    $item = Get-Item -LiteralPath $currentPath -Force
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Reparse points and symbolic links are not allowed: $currentPath"
    }
    $currentPath = [System.IO.Directory]::GetParent($currentPath).FullName
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker Desktop is required. Install and start Docker, then run this command again.'
}

$imageName = 'link-ecu-log-analyzer-sandbox:local'
$imageExists = docker image inspect $imageName 2>$null
if ($LASTEXITCODE -ne 0) {
    docker build --file (Join-Path $projectRoot 'sandbox\Dockerfile') --tag $imageName $projectRoot
    if ($LASTEXITCODE -ne 0) {
        throw 'Docker could not build the isolated parser image.'
    }
}

$containerPath = '/input/log.llgx'
$dockerArguments = @(
    'run', '--rm',
    '--network', 'none',
    '--read-only',
    '--cap-drop', 'ALL',
    '--security-opt', 'no-new-privileges',
    '--pids-limit', '64',
    '--memory', '512m',
    '--cpus', '1',
    '--tmpfs', '/tmp:rw,noexec,nosuid,nodev,size=64m',
    '--mount', "type=bind,source=$candidatePath,target=$containerPath,readonly",
    $imageName,
    $containerPath
)

if ($List) {
    $dockerArguments += '--list'
}

docker @dockerArguments
if ($LASTEXITCODE -ne 0) {
    throw "The isolated parser exited with code $LASTEXITCODE."
}
