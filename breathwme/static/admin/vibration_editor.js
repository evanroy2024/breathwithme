document.addEventListener("DOMContentLoaded", function() {
    const editor = document.getElementById('vibration-editor');
    const input = document.getElementById('vibration-cues');
    const totalTime = 120; // Total time for the exercise (e.g., 2 minutes)
    let cues = JSON.parse(input.value || '[]');

    function renderCues() {
        editor.innerHTML = '';
        cues.forEach((cue, index) => {
            let el = document.createElement('div');
            el.style.position = 'absolute';
            el.style.left = (cue / totalTime) * editor.clientWidth + 'px';
            el.style.width = '10px';
            el.style.height = '100%';
            el.style.background = 'red';
            el.style.cursor = 'pointer';
            el.dataset.index = index;
            el.onclick = () => {
                cues.splice(index, 1);
                renderCues();
            };
            editor.appendChild(el);
        });
        input.value = JSON.stringify(cues);
    }

    editor.onclick = function(e) {
        let rect = editor.getBoundingClientRect();
        let time = ((e.clientX - rect.left) / editor.clientWidth) * totalTime;
        cues.push(time);
        renderCues();
    };

    renderCues();
});
