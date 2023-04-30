
var timerId;
var startTime;

function startTimer() {
  startTime = Date.now();
  timerId = setInterval(updateTimer, 1000);
}

function stopTimer() {
  clearInterval(timerId);
}

function updateTimer() {
  var elapsedTime = Date.now() - startTime;
  var hours = Math.floor(elapsedTime / 3600000);
  var minutes = Math.floor((elapsedTime % 3600000) / 60000);
  var seconds = Math.floor((elapsedTime % 60000) / 1000);

  // add leading zeros if necessary
  if (hours < 10) {
    hours = '0' + hours;
  }
  if (minutes < 10) {
    minutes = '0' + minutes;
  }
  if (seconds < 10) {
    seconds = '0' + seconds;
  }

  var timeString = hours + ':' + minutes + ':' + seconds;
  document.getElementById('timer').innerHTML = timeString;
}