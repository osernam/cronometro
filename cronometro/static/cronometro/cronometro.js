
var tiempoActual;
var tiempoInicial;
var tiempoParcial = [];
var tiempos = [];



function parcialCronometro() {
    canInterval = document.getElementById("canIntervalos").value;

    if (tiempoParcial.length != 0) {
        tiempoParcial.push(Date.now() - tiempoInicial);
    } 
    else {
        tiempoParcial.push(Date.now() - tiempoParcial[tiempoParcial.length-1]);
    }

    if (tiempoParcial.length === canInterval) {
        pararCronometro();
    }      
    var divTiempos = document.getElementById('tiemposCronometro');
    for (let i = 0; i < tiempoParcial.length; i++) {
        

        divTiempos.innerHTML +=( 

            '<div class="col-xl-3 col-md-6 mb-4">'+
                            '<div class="card border-left-primary shadow h-100 py-2">'+
                                '<div class="card-body">'+
                                    '<div class="row no-gutters align-items-center">'+
                                        '<div class="col mr-2">'+
                                            '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">'+
                                                'Tiempo '+i+
                                            '</div>'+
                                            '<div class="h5 mb-0 font-weight-bold text-gray-800">'+tiempoParcial[i]+'</div>'+
                                        '</div>'+
                                        '<div class="col-auto">'+
                                            '<i class="fas fa-calendar fa-2x text-gray-300"></i>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
            '</div>'

        );

       
    }
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







// Enviar variables a Django
var tiempoPar = {name: "John", age: 30, city: "New York"};
function enviarVariables() {
    
    $.ajax({
        method: "POST",
        url: "cronometro/tiempo-parcial/",
        data: {tiempoParcial: JSON.stringify(tiempoParcial)},
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

// Cronometro experimental
function actualizarTiempo() {
    var tiempoTranscurrido = Date.now() - tiempoInicial;
    var horas = Math.floor(tiempoTranscurrido / 3600000);
    var minutos = Math.floor((tiempoTranscurrido % 3600000) / 60000);
    var segundos = Math.floor((tiempoTranscurrido % 60000) / 1000);
    var centesimas = Math.floor((tiempoTranscurrido %60000)/1000)
    
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

    var tiempoString =  minutos +  ':' + segundos  + ':' + centesimas;
    document.getElementById('tiempo').innerHTML = tiempoString;

    var tiempoDecimal = horasDecimales + ':' + minutosDecimales + ':' + segundosDecimales;
    document.getElementById('tiempoDecimal').innerHTML = tiempoDecimal;
    //var timeString = hours + ':' + minutes + ':' + seconds;
    //document.getElementById('timer').innerHTML = timeString;
}

function iniciarCronometro() {

    

    tiempoInicial = Date.now();
    tiempoActual = setInterval(actualizarTiempo, 100);
}

function pararCronometro() {
    
    clearInterval(tiempoActual);
}


//cronometro centesimas
var centesimas = 0;
var cent = 0;
var segundos = 0;
var minutos = 0;


function cronometroDeci() {
    centesimas++;
    
    if (centesimas == 100) {
        centesimas = 0;
        segundos++;
    }
    if (segundos == 60) {
        segundos = 0;
        minutos++;
    }
    if (minutos == 60) {
        minutos = 0;
        horas++;
    }
    var tiempo = (minutos < 10 ? "0" + minutos : minutos) + ":" +
                 (segundos < 10 ? "0" + segundos : segundos) + ":" +
                 (centesimas < 10 ? "0" + centesimas : centesimas);
    document.getElementById("tiempo").innerHTML = tiempo;
}



function iniciar() {

    var divTiempos = document.getElementById("tiemposCronometro");
    divTiempos.innerHTML = '';

    tiempoInicial = Date.now();
    tiempoActual = setInterval(cronometroDeci, 10);
}

function detener() {
    tiempos=tiempoParcial;
    tiempoParcial = []
    clearInterval(tiempoActual);
}





document.getElementById('iniciarBoton').addEventListener('click', iniciar);
document.getElementById('pararBoton').addEventListener('click', detener);
document.getElementById('enviarBoton').addEventListener('click', enviarVariables);
document.getElementById('tiemposParciales').addEventListener('click', parcialCronometro);