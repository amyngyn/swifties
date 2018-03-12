// source: https://developers.google.com/youtube/iframe_api_reference#Getting_Started
var player;
var id = "{{v}}";

function loadYoutubeApi() {
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: '3tmd-ClpJxA',
    events: {
      'onStateChange': onPlayerStateChange
    }
  });
}

var waitingToStart = true;
var intervalID;
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING) {
    if (waitingToStart) {
      startView();
      intervalID = setInterval(updateViewCount, 2000);
	  waitingToStart = false;
	}
  }
}

function updateViewCount() {
  const watchFraction = player.getVideoLoadedFraction();
  if (watchFraction >= 0.60) {
    recordView();
    clearInterval(intervalID);
  }
}

function startView() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/start", true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.send(`{"id": "${id}"}`);
}

function recordView() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/count", true);
  xhttp.setRequestHeader('Content-Type', 'application/json');
  xhttp.send(`{"id": "${id}"}`);
}

loadYoutubeApi();
