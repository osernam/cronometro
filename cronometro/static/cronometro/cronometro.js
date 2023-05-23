
var tiempoActual;
var tiempoInicial;
var tiempoParcial = [];
var tiempos = [];

var restantes = 0;
var canInterval = 10;
canInterval= parseInt(document.getElementById("canIntervalos").value);
function parcialCronometro() {
    
    
    if (restantes== 0) {
        restantes = canInterval;
        
    }else {
        restantes = restantes - 1;

        
    }

    if ( restantes == 0) {
        pararCronometro();
    }  

    if (tiempoParcial.length != 0) {
        tiempoParcial.push(Date.now() - tiempoInicial);
    } 
    else {
        tiempoParcial.push(Date.now() - tiempoParcial[tiempoParcial.length-1]);
    }

        
    var divTiempos = document.getElementById('tiemposCronometro');
    
    divTiempos.innerHTML = '';

    for (let i = 0; i < tiempoParcial.length-1; i++) {
        

        divTiempos.innerHTML +=( 

            '<div class="col-xl-3 col-md-6 mb-4" style="display: flex; >'+
                            
                '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">'+
                    'Tiempo '+i+
                '</div>'+
                '<div class="h6 mb-0 font-weight-bold text-gray-800">'+tiempoParcial[i]+'</div>'+
                '<br>'+            
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
        
    }
    var tiempo = (minutos < 10 ? "0" + minutos : minutos) + ":" +
                 (segundos < 10 ? "0" + segundos : segundos) + ":" +
                 (centesimas < 10 ? "0" + centesimas : centesimas);
    document.getElementById("tiempo").innerHTML = tiempo;
}



function iniciar() {

    /**
 * Inicializa el cronómetro y lo pone en marcha. Establece el elemento HTML `divTiempos` a una cadena vacía,
 * inicializa la matriz `tiempoParcial`, establece el `tiempoInicial` a la hora actual e inicia el
 * Intervalo `tiempoActual`, que llama a la función `cronometroDeci()` cada 10 milisegundos.
 *
 * @param {HTMLDivElement} divTiempos -El elemento HTML que mostrará los tiempos en el cronómetro.
 * @return {void} Esta función no devuelve nada
 */

    var divTiempos = document.getElementById('tiemposCronometro');
    divTiempos.innerHTML = '';
    tiempoParcial = []
    tiempoInicial = Date.now();
    tiempoActual = setInterval(cronometroDeci, 10);
}

function detener() {
    tiempos=tiempoParcial;
    
    clearInterval(tiempoActual);
    
}





document.getElementById('iniciarBoton').addEventListener('click', iniciar);
document.getElementById('pararBoton').addEventListener('click', detener);
document.getElementById('enviarBoton').addEventListener('click', enviarVariables);
document.getElementById('tiemposParciales').addEventListener('click', parcialCronometro);