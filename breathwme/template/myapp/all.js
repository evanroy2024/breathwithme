vibration - 
<label for="vibrationLevel">Vibration Intensity:</label>
<select id="vibrationLevel">
    <option value="500">Low</option>
    <option value="1000" selected>Mid</option>
    <option value="1500">High</option>
    <option value="2000">Extreme</option>
</select>


const vibrationDropdown = document.getElementById("vibrationLevel");

audioPlayer.addEventListener("timeupdate", function () {
    let currentTime = Math.floor(audioPlayer.currentTime);
    let selectedVibration = parseInt(vibrationDropdown.value, 10); // Get selected vibration duration

    if (window.vibrationSet === "Default") {
        if (window.calculatedTiming && !isNaN(window.calculatedTiming)) {
            if (currentTime % window.calculatedTiming === 0 && currentTime !== 0) {
                navigator.vibrate(selectedVibration);
            }
        } else {
            console.warn("window.calculatedTiming is not defined or invalid");
        }
    } else if (window.vibrationSet === "Customise") {
        if (timestamps.includes(currentTime)) {
            navigator.vibrate(selectedVibration);
            timestamps = timestamps.filter(t => t !== currentTime);
        }
    }
});
