// script.js

// --- 1. Define Your Episode Data ---
// This is where you list all your downloaded episodes.
// Make sure 'filePath' and 'posterPath' match the actual paths in your 'videos' folder.
const episodeData = [
    {
        id: 'showA-s01e01',
        title: 'Your Show A - Episode 1',
        description: 'The first episode of an exciting adventure.',
        filePath: 'videos/Show_A/Episode_S01E01.mp4',
        posterPath: 'videos/Show_A/poster_s01e01.jpg' // Optional: path to an image thumbnail
    },
    {
        id: 'showA-s01e02',
        title: 'Your Show A - Episode 2',
        description: 'The plot thickens in the second episode.',
        filePath: 'videos/Show_A/Episode_S01E02.mp4',
        posterPath: 'videos/Show_A/poster_s01e02.jpg'
    },
    {
        id: 'showB-s01e01',
        title: 'Your Show B - Pilot',
        description: 'Introducing a new series with intriguing characters.',
        filePath: 'videos/Show_B/Episode_S01E01.mp4',
        posterPath: 'videos/Show_B/poster_s01e01.jpg'
    },
    // Add more episodes here following the same structure
    // {
    //     id: 'unique-id-for-episode',
    //     title: 'Episode Title',
    //     description: 'Short description of the episode.',
    //     filePath: 'videos/Your_Show_Folder/Your_Episode_File.mp4',
    //     posterPath: 'videos/Your_Show_Folder/Your_Episode_Poster.jpg' // optional
    // }
];

// --- 2. Get DOM Elements ---
const showsContainer = document.getElementById('shows-container');
const videoPlayerSection = document.getElementById('video-player-section');
const videoPlayer = document.getElementById('video-player');
const currentEpisodeTitle = document.getElementById('current-episode-title');
const currentEpisodeDescription = document.getElementById('current-episode-description');
const closePlayerBtn = document.getElementById('close-player-btn');

// --- 3. Function to Render Episode Cards ---
function renderEpisodeCards() {
    showsContainer.innerHTML = ''; // Clear existing content
    episodeData.forEach(episode => {
        const episodeCard = document.createElement('div');
        episodeCard.id = episode.id; // Set ID for easy lookup
        episodeCard.className = 'episode-card bg-gray-800 rounded-lg overflow-hidden shadow-lg cursor-pointer hover:bg-gray-700 relative';

        // Optional: Add a thumbnail image
        if (episode.posterPath) {
            const posterImg = document.createElement('img');
            posterImg.src = episode.posterPath;
            posterImg.alt = episode.title;
            posterImg.className = 'w-full h-48 object-cover'; // Tailwind classes for image size
            episodeCard.appendChild(posterImg);
        } else {
            // Placeholder div if no poster image
            const placeholder = document.createElement('div');
            placeholder.className = 'w-full h-48 bg-gray-700 flex items-center justify-center text-gray-400 text-center p-4';
            placeholder.textContent = 'No Poster Available';
            episodeCard.appendChild(placeholder);
        }

        const titleOverlay = document.createElement('div');
        titleOverlay.className = 'p-4';
        const titleText = document.createElement('h3');
        titleText.className = 'text-lg font-semibold truncate'; // truncate if title is long
        titleText.textContent = episode.title;
        titleOverlay.appendChild(titleText);
        episodeCard.appendChild(titleOverlay);

        // Add click listener to play the episode
        episodeCard.addEventListener('click', () => playEpisode(episode.id));

        showsContainer.appendChild(episodeCard);
    });
}

// --- 4. Function to Play a Selected Episode ---
function playEpisode(episodeId) {
    const episode = episodeData.find(ep => ep.id === episodeId);

    if (episode) {
        currentEpisodeTitle.textContent = episode.title;
        currentEpisodeDescription.textContent = episode.description;
        videoPlayer.src = episode.filePath;
        videoPlayer.poster = episode.posterPath || ''; // Set poster for video player
        videoPlayerSection.classList.remove('hidden'); // Show the video player section
        videoPlayer.load(); // Load the new video source
        videoPlayer.play(); // Start playing automatically
        
        // Scroll to the video player section
        videoPlayerSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        console.error('Episode not found:', episodeId);
    }
}

// --- 5. Event Listener for Closing Player ---
closePlayerBtn.addEventListener('click', () => {
    videoPlayer.pause(); // Pause the video
    videoPlayer.src = ''; // Clear the video source
    videoPlayerSection.classList.add('hidden'); // Hide the video player section
});

// --- 6. Initial Render ---
// Call this function when the page loads to display all episode cards
document.addEventListener('DOMContentLoaded', renderEpisodeCards);