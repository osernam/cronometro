
var tiempoActual;
var tiempoInicial;
var tiempoParcial = [];


function iniciarCronometro() {
    tiempoInicial = Date.now();
    tiempoActual = setInterval(actualizarTiempo, 100);
}
function parcialCronometro() {
    tiempoParcial.push (Date.now() - tiempoInicial);
}
function pararCronometro() {
    
    clearInterval(tiempoActual);
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

function enviarVariables() {
    
    $.ajax({
        type: 'POST',
        url: 'cronometro/tiempo-parcial/',
        data: {'tiempoParcial':tiempoParcial},
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(response) {
            console.log('Enviado correcto!');
        },
        error: function(response) {
            console.log('Error enviando datos!');
        }
    });
}
function actualizarTiempo() {
    var tiempoTranscurrido = Date.now() - tiempoInicial;
    var horas = Math.floor(tiempoTranscurrido / 3600000);
    var minutos = Math.floor((tiempoTranscurrido % 3600000) / 60000);
    var segundos = Math.floor((tiempoTranscurrido % 60000) / 1000);
    
    var centecimasMinuto = Math.floor(tiempoTranscurrido/ 10000);
    // 24 horas = 10 horas decimales, 1 hora decimal = 100 minutos decimales, 1 minuto decimal = 100 segundos decimales

    var horasDecimales = Math.floor(((tiempoTranscurrido / 3600000)*24)/10);
    var minutosDecimales = Math.floor((((tiempoTranscurrido / 3600000)*24)/10)*100);
    var segundosDecimales = Math.floor((((tiempoTranscurrido / 60000)*24)/10)*1000);

    // add leading zeros if necessary
    if (horas < 10) {
    horas = '0' + horas;
    }
    if (minutos < 10) {
    minutos = '0' + minutos;
    }
    if (segundos < 10) {
    segundos = '0' + segundos;
    }
    if( centecimasMinuto < 10) {
    centecimasMinuto = '0' + centecimasMinuto;
    }

    if (horasDecimales < 10) {
    horasDecimales = '0' + horasDecimales;
    }
    if (minutosDecimales < 10) {
    minutosDecimales = '0' + minutosDecimales;
    }
    if (segundosDecimales < 10) {
    segundosDecimales = '0' + segundosDecimales;
    }

    var tiempoString = horas + ':' + minutos +  ':' + segundos  + ':' + centecimasMinuto;
    document.getElementById('tiempo').innerHTML = tiempoString;

    var tiempoDecimal = horasDecimales + ':' + minutosDecimales + ':' + segundosDecimales;
    document.getElementById('tiempoDecimal').innerHTML = tiempoDecimal;
    //var timeString = hours + ':' + minutes + ':' + seconds;
    //document.getElementById('timer').innerHTML = timeString;
}


document.getElementById('iniciarBoton').addEventListener('click', iniciarCronometro);
document.getElementById('pararBoton').addEventListener('click', pararCronometro);
document.getElementById('enviarBoton').addEventListener('click', enviarVariables);