'use strict';

let audioPlayer = document.querySelector('.green-audio-player');
let playPause = audioPlayer.querySelector('#playPause');
let playPauseButton = audioPlayer.querySelector('.play-pause-btn');
let loading = audioPlayer.querySelector('.loading');
let progress = audioPlayer.querySelector('.progress');
let sliders = audioPlayer.querySelectorAll('.slider');
let volumeBtn = audioPlayer.querySelector('.volume-btn');
let volumeControls = audioPlayer.querySelector('.volume-controls');
let volumeProgress = volumeControls.querySelector('.slider .progress');
let player = audioPlayer.querySelector('audio');
let currentTime = audioPlayer.querySelector('.current-time');
let totalTime = audioPlayer.querySelector('.total-time');
let speaker = audioPlayer.querySelector('#speaker');

let draggableClasses = ['pin'];
let currentlyDragged = null;

window.addEventListener('mousedown', function (event) {

    if (!isDraggable(event.target)) return false;

    currentlyDragged = event.target;
    let handleMethod = currentlyDragged.dataset.method;

    this.addEventListener('mousemove', window[handleMethod], false);

    window.addEventListener('mouseup', function () {
        currentlyDragged = false;
        window.removeEventListener('mousemove', window[handleMethod], false);
    }, false);
});

playPauseButton.addEventListener('click', togglePlay);
player.addEventListener('timeupdate', updateProgress);
player.addEventListener('volumechange', updateVolume);
player.addEventListener('loadedmetadata', function () {
    totalTime.textContent = formatTimeToString(player.duration);
});
player.addEventListener('canplay', makePlay);
player.addEventListener('ended', function () {
    playPause.attributes.d.value = "M18 12L0 24V0";
    player.currentTime = 0;
});

volumeBtn.addEventListener('click', function () {
    volumeBtn.classList.toggle('open');
    volumeControls.classList.toggle('hidden');
});

window.addEventListener('resize', directionAware);

sliders.forEach(function (slider) {
    let pin = slider.querySelector('.pin');
    slider.addEventListener('click', window[pin.dataset.method]);
});

directionAware();

function isDraggable(el) {
    let canDrag = false;
    let classes = Array.from(el.classList);
    draggableClasses.forEach(function (draggable) {
        if (classes.indexOf(draggable) !== -1) canDrag = true;
    });
    return canDrag;
}

function inRange(event) {
    let rangeBox = getRangeBox(event);
    let rect = rangeBox.getBoundingClientRect();
    let direction = rangeBox.dataset.direction;
    if (direction === 'horizontal') {
        let min = rangeBox.offsetLeft;
        let max = min + rangeBox.offsetWidth;
        if (event.clientX < min || event.clientX > max) return false;
    } else {
        let min = rect.top;
        let max = min + rangeBox.offsetHeight;
        if (event.clientY < min || event.clientY > max) return false;
    }
    return true;
}

function updateProgress() {
    let current = player.currentTime;
    let percent = current / player.duration * 100;
    
    progress.style.width = percent + '%';

    currentTime.textContent = formatTimeToString(current);
}

function updateVolume() {
    volumeProgress.style.height = player.volume * 100 + '%';
    if (player.volume >= 0.5) {
        speaker.attributes.d.value = 'M14.667 0v2.747c3.853 1.146 6.666 4.72 6.666 8.946 0 4.227-2.813 7.787-6.666 8.934v2.76C20 22.173 24 17.4 24 11.693 24 5.987 20 1.213 14.667 0zM18 11.693c0-2.36-1.333-4.386-3.333-5.373v10.707c2-.947 3.333-2.987 3.333-5.334zm-18-4v8h5.333L12 22.36V1.027L5.333 7.693H0z';
    } else if (player.volume < 0.5 && player.volume > 0.05) {
        speaker.attributes.d.value = 'M0 7.667v8h5.333L12 22.333V1L5.333 7.667M17.333 11.373C17.333 9.013 16 6.987 14 6v10.707c2-.947 3.333-2.987 3.333-5.334z';
    } else if (player.volume <= 0.05) {
        speaker.attributes.d.value = 'M0 7.667v8h5.333L12 22.333V1L5.333 7.667';
    }
}

function getRangeBox(event) {
    let rangeBox = event.target;
    let el = currentlyDragged;
    if (event.type === 'click' && isDraggable(event.target)) {
        rangeBox = event.target.parentElement.parentElement;
    }
    if (event.type === 'mousemove') {
        rangeBox = el.parentElement.parentElement;
    }
    return rangeBox;
}

function getCoefficient(event) {
    let slider = getRangeBox(event);
    let rect = slider.getBoundingClientRect();
    let K = 0;
    if (slider.dataset.direction === 'horizontal') {
        let offsetX = event.clientX - rect.left;
        let width = slider.clientWidth;
        K = offsetX / width;
    } else if (slider.dataset.direction === 'vertical') {

        let height = slider.clientHeight;
        let offsetY = event.clientY - rect.top;
        K = 1 - offsetY / height;
    }
    return K;
}

function rewind(event) {
    if (inRange(event)) {
        console.log("player.duration: ", player.duration)
        console.log("getCoefficient(event): ", getCoefficient(event))
        player.currentTime = player.duration * getCoefficient(event);
    }
}

function changeVolume(event) {
    if (inRange(event)) {
        player.volume = getCoefficient(event);
    }
}

function formatTimeToString(time) {
    let min = Math.floor(time / 60);
    let sec = Math.floor(time % 60);
    return min + ':' + (sec < 10 ? '0' + sec : sec);
}

function formatStringToTime(string) {
    if (string.match(/^(0|[1-9][0-9]*):[0-5][0-9]$/)) {
        let time = parseInt(string.split(":")[0]) * 60 + parseInt(string.split(":")[1]);
        if (time <= player.duration && time >= 0) {
            return time;
        }
    }
    return false;
}

function togglePlay() {
    if (player.paused) {
        playPause.attributes.d.value = "M0 0h6v24H0zM12 0h6v24h-6z";
        player.play();
    } else {
        playPause.attributes.d.value = "M18 12L0 24V0";
        player.pause();
    }
}

function makePlay() {
    playPauseButton.style.display = 'block';
    loading.style.display = 'none';
}

function directionAware() {
    if (window.innerHeight < 250) {
        volumeControls.style.bottom = '-54px';
        volumeControls.style.left = '54px';
    } else if (audioPlayer.offsetTop < 154) {
        volumeControls.style.bottom = '-164px';
        volumeControls.style.left = '-3px';
    } else {
        volumeControls.style.bottom = '52px';
        volumeControls.style.left = '-3px';
    }
}