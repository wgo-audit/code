param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "opencode-command", "opencode-skill")]
    [string]$Provider,

    [Parameter(Mandatory = $true)]
    [string]$Source,

    [Parameter(Mandatory = $true)]
    [string]$Destination
)

$allowedByProvider = @{
    codex = @("name", "description", "args", "skills")
    claude = @(
        "name", "description", "when_to_use", "argument-hint", "arguments",
        "disable-model-invocation", "user-invocable", "allowed-tools", "model",
        "background", "hooks", "paths", "shell"
    )
    "opencode-command" = @("description", "agent", "model", "variant", "subtask")
    "opencode-skill" = @("name", "description", "license", "compatibility", "metadata")
}

$allowed = $allowedByProvider[$Provider]
$lines = Get-Content -LiteralPath $Source
$inFrontmatter = $false
$keep = $true
$output = foreach ($index in 0..($lines.Count - 1)) {
    $line = $lines[$index]

    if ($index -eq 0 -and $line -eq "---") {
        $inFrontmatter = $true
        $line
        continue
    }
    if ($inFrontmatter -and $line -eq "---") {
        $inFrontmatter = $false
        $line
        if ($Provider -eq "opencode-command") {
            ""
            'OpenCode command arguments: `$ARGUMENTS`.'
            "Load the ``wgo`` skill with the OpenCode skill tool. If it is not listed yet, read ``.opencode/skills/wgo/SKILL.md`` directly."
        }
        continue
    }
    if ($inFrontmatter) {
        if ($line -match '^([A-Za-z][A-Za-z0-9_-]*):') {
            $keep = $allowed -contains $Matches[1]
        }
        if ($keep) {
            $line
        }
        continue
    }
    $line
}

Set-Content -LiteralPath $Destination -Value $output -Encoding utf8
