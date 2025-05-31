# generate_episode_data.ps1

$VideosRoot = ".\videos" # Relative path to your videos folder
$OutputJsonFile = "episode_data.json"
$AllEpisodes = @()
$EpisodeIdCounter = 0

# Function to safely create a relative path (using forward slashes for web)
function ConvertTo-WebPath {
    param(
        [string]$Path
    )
    $Path.Replace("\", "/") # Replace backslashes with forward slashes
}

# Recursively find video files
Get-ChildItem -Path $VideosRoot -Recurse -Include @("*.mp4", "*.webm", "*.ogg", "*.mov") | ForEach-Object {
    $EpisodeIdCounter++
    
    $FilePathWeb = ConvertTo-WebPath $_.FullName # Get full path and convert slashes
    
    # Make path relative to the root of the server (my-netflix-clone folder)
    # This assumes generate_episode_data.ps1 is run from my-netflix-clone
    $FilePathWeb = $FilePathWeb.Substring($FilePathWeb.IndexOf("videos/")) 

    # Extract base name for title
    $BaseName = $_.BaseName
    $ParentFolder = ConvertTo-WebPath $_.DirectoryName.Substring($_.DirectoryName.LastIndexOf('\') + 1) # Get direct parent folder name

    # Attempt to create a title - refine this based on your file naming
    $EpisodeTitle = "$ParentFolder - $BaseName"

    # Optional: Check for a poster image with the same base name
    $PosterPathWeb = ""
    $PossiblePosterName = $_.DirectoryName + "\$($_.BaseName).jpg"
    if (Test-Path $PossiblePosterName) {
        $PosterPathWeb = ConvertTo-WebPath $PossiblePosterName
        $PosterPathWeb = $PosterPathWeb.Substring($PosterPathWeb.IndexOf("videos/"))
    }

    $Episode = @{
        id = "ep-$EpisodeIdCounter";
        title = $EpisodeTitle;
        description = "A thrilling episode from this series."; # Generic description
        filePath = $FilePathWeb;
        posterPath = $PosterPathWeb
    }
    $AllEpisodes += $Episode
}

# Sort episodes (e.g., by filePath for alphabetical/sequential order)
$AllEpisodes = $AllEpisodes | Sort-Object -Property filePath

# Convert to JSON and save
$JsonOutput = $AllEpisodes | ConvertTo-Json -Depth 5 -Compress:$false

Set-Content -Path $OutputJsonFile -Value $JsonOutput -Encoding UTF8

Write-Host "Generated $($AllEpisodes.Count) episodes and saved to $OutputJsonFile"