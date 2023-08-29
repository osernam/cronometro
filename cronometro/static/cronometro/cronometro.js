
var tiempoActual;
var tiempoInicial;
var tiempoParcial = [];
var tiempos = [];

var restantes = 0;

var factorRitmo = parseInt(document.getElementById("factorRitmo").value);
var escalaSuplementos = parseInt(document.getElementById("escalaSuplementos").value);
var tPromEstandar = 0
var sumatoriaT= 0
var tiempoNormal = 0
var tiempoEstandar =0
var centesimas = 0;
var segundos = 0;
var minutos = 0;

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
  
/*
function parcialCronometro() {
    
    
    if (restantes== 0) {
        restantes = canInterval;
        
    }else {
        restantes = restantes - 1;        
    

    if ( restantes == 0) {
        pararCronometro();
    }  }
    var minA = 0;
    var segA = 0;
    var centA = 0;
    var tiemposMiliseg= [];
    
    var tiem = ((minutos*6000)+segundos*100)+centesimas;
    var tiemAnt = ((minA*6000)+segA*100)+centA;

    tiemposMiliseg.push(tiem); 
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
    
    if (tiempoParcial.length != 0) {
        var tiem = ((minutos*60)+segundos)/60+centesimas;
        tiempoParcial.push(1);
    } 
    //else {
      //  divTiempos.innerHTML = '';
    //}

        
    var divTiempos = document.getElementById('tiemposCronometro');
    divTiempos.innerHTML = '';
    

    for (let i = 0; i < tiempoParcial.length; i++) {
        sumatoriaT = sumatoriaT + tiempoParcial[i];
        console.log(Math.round( tiempoParcial[i]));
        divTiempos.innerHTML +=( 

            '<div class="col-xl-3 col-md-6 mb-4" style="display: flex; >'+
                            
                '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">'+
                    'Tiempo '+(i+1)+
                '</div>'+
                '<div class="h6 mb-0 font-weight-bold text-gray-800">'+tiempoParcial[i]+'  tiempo observado '+tiemposMiliseg+'</div>'+
                '<br>'+            
            '</div>'

        );
        
        console.log("tPromEstandar: ");
        console.log(tPromEstandar);
        console.log(sumatoriaT);
    }
    tPromEstandar = sumatoriaT/tiempoParcial.length;
   
    setCookie('tiempos_estandar',tPromEstandar,30);
    setCookie('tiempos_cookie',tiempoParcial,30);
    setCookie('tiempos_miliseg',tiemposMiliseg,30);
}*/

function parciales(){
    if (tiempoParcial.length == 0) {
        tiempoParcial.push(minutos + segundos/60 + centesimas/600)
    }else{
        var nuevo = (minutos + segundos/60 + centesimas/600)- (tiempoParcial[tiempoParcial.length-1]);
        tiempoParcial.push(nuevo)
    }
    

    
    var tNor = document.getElementById('tiempoNor');
    var tEst = document.getElementById('tiempoEst');
    var divTiempos = document.getElementById('tiemposCronometro');
    divTiempos.innerHTML = '';
    

    for (let i = 0; i < tiempoParcial.length; i++) {
        var tObs = 0
        for (let e = 0; e < tiempoParcial.length; e++) {
            tObs = tiempoParcial[e]/tiempoParcial.length
            
        }
        tiempoNormal= tObs*factorRitmo
        tiempoEstandar = tiempoNormal + tiempoNormal*escalaSuplementos
        
        console.log(Math.round( tiempoParcial[i]));
        divTiempos.innerHTML +=( 

            '<div class="col-xl-3 col-md-6 mb-4" style="display: flex; >'+
                            
                '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">'+
                    'T  '+(i+1)+
                '</div>'+
                '<div class="h6 mb-0 font-weight-bold text-gray-800">'+tiempoParcial[i].toFixed(2) +'</div>'+
                '<br>'+            
            '</div>'

        );

        
        
        tNor.innerHTML = "<p>Tn = " + tiempoNormal.toFixed(3) + " </p>";
        tEst.innerHTML = "<p>Te = " + tiempoEstandar.toFixed(3) + "</p>";
    }

    setCookie('tiempos_estandar',tiempoEstandar,30);

    graficoT();
}




// Enviar variables a Django
/*var tiempoPar = {name: "John", age: 30, city: "New York"};
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
}*/



//cronometro centesimas

var cent = 0;

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
    /* El símbolo `?` se utiliza en JavaScript como operador ternario. Es un
    forma abreviada de escribir una declaración if-else.*/
    var tiempo = (minutos < 10 ? "0" + minutos : minutos) + ":" +
                 (segundos < 10 ? "0" + segundos : segundos) + ":" +
                 (centesimas < 10 ? "0" + centesimas : centesimas);
    document.getElementById("tiempo").innerHTML = tiempo;
}



function iniciar() {

    /**
 Inicializa el cronómetro y lo pone en marcha. Establece el elemento HTML `divTiempos` a una cadena vacía,
 inicializa la matriz `tiempoParcial`, establece el `tiempoInicial` a la hora actual e inicia el
 Intervalo `tiempoActual`, que llama a la función `cronometroDeci()` cada 10 milisegundos.
 
  @param {HTMLDivElement} divTiempos -El elemento HTML que mostrará los tiempos en el cronómetro.
  @return {void} Esta función no devuelve nada
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
    console.log(( tPromEstandar));
    clearInterval(tiempoActual);
    
}





document.getElementById('iniciarBoton').addEventListener('click', iniciar);
document.getElementById('pararBoton').addEventListener('click', detener);
//document.getElementById('enviarBoton').addEventListener('click', enviarVariables);
document.getElementById('tiemposParciales').addEventListener('click', parciales);


//grafico canvas chart para tiempos

var myChart;
function graficoT () {

// Destruir el gráfico existente si ya existe
    if (typeof myChart !== 'undefined') {
    myChart.destroy();
    }

    // Configuración del gráfico
    var graficoTiempos = document.getElementById('graficoTiempos').getContext('2d');
    myChart = new Chart(graficoTiempos, {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],
        datasets: [{
        label: 'Intervalos',
        data: tiempoParcial,
        fill: false,
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
        }]
    },
    options: {
        scales: {
        y: {
            beginAtZero: true
        }
        }
    }
    });
    }

graficoT();

//document.getElementById('graficar').addEventListener('click', graficoTiempos);