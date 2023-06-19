
var tiempoActual;
var tiempoInicial;
var tiempoParcial = [];
var tiempos = [];

var restantes = 0;
var canInterval = 10;
canInterval= parseInt(document.getElementById("canIntervalos").value);
var factorRitmo = parseInt(document.getElementById("factorRitmo").value);
var escalaSuplementos = parseInt(document.getElementById("escalaSuplementos").value);
var tPromEstandar = 0
var sumatoriaT= 0
var tiempoNormal = 0

//Crear la cookie para guardar los tiempos

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    //Obtener el valor de la cookie
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') 
            c = c.substring(1,c.length);

        if (c.indexOf(nameEQ) == 0) 
            return c.substring(nameEQ.length,c.length);
    }
    return null;
}

/*
Para consultarla:

if( getCookie('mi_variable') != null ){
        console.log( getCookie('mi_variable') ); // devolverá valor en este caso
}
*/

function eraseCookie(name) {
    //eliminar la cookie
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
//fin cookies
  

function parcialCronometro() {
    
    
    if (restantes== 0) {
        restantes = canInterval;
        
    }else {
        restantes = restantes - 1;        
    }

    if ( restantes == 0) {
        pararCronometro();
    }  
    var minA = 0;
    var segA = 0;
    var centA = 0;
    
    
    var tiem = ((minutos*60)+segundos)/60+centesimas;
    var tiemAnt = ((minA*60)+segA)/60+centA;
    if (factorRitmo == 0) {
        tiempoNormal= tiem ;
    }else{
        tiempoNormal = (tiem-tiemAnt)*factorRitmo;
    }
    //Tiempos anteriores
    minA = minutos;
    segA = segundos;
    centA = centesimas;
    
    tiempoParcial.push(tiempoNormal +tiempoNormal*escalaSuplementos);
    
    /*if (tiempoParcial.length != 0) {
        var tiem = ((minutos*60)+segundos)/60+centesimas;
        tiempoParcial.push(1);
    } */
    //else {
      //  divTiempos.innerHTML = '';
    //}

        
    var divTiempos = document.getElementById('tiemposCronometro');
    divTiempos.innerHTML = '';
    

    for (let i = 0; i < tiempoParcial.length-1; i++) {
        sumatoriaT += tiempoParcial[i];
        console.log(Math.round( tiempoParcial[i]));
        divTiempos.innerHTML +=( 

            '<div class="col-xl-3 col-md-6 mb-4" style="display: flex; >'+
                            
                '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">'+
                    'Tiempo '+(i+1)+
                '</div>'+
                '<div class="h6 mb-0 font-weight-bold text-gray-800">'+tiempoParcial[i]+'</div>'+
                '<br>'+            
            '</div>'

        );

       
    }
    tPromEstandar = sumatoriaT/tiempoParcial.length;

    setCookie('tiempos_estandar',tPromEstandar,30);
    setCookie('tiempos_cookie',tiempoParcial,30);
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
    setCookie('tiempos_cookie',tiempoParcial,30); // nombre, valor, tiempo de expiracion
    tiempoInicial = Date.now();
    tiempoActual = setInterval(cronometroDeci, 10);

    
}

function detener() {
    restantes = 0;
    tiempos=tiempoParcial;
    
    clearInterval(tiempoActual);
    
}





document.getElementById('iniciarBoton').addEventListener('click', iniciar);
document.getElementById('pararBoton').addEventListener('click', detener);
document.getElementById('enviarBoton').addEventListener('click', enviarVariables);
document.getElementById('tiemposParciales').addEventListener('click', parcialCronometro);