document.addEventListener('DOMContentLoaded', function () {



    btntrans = document.getElementById("trans");
    btntrans.addEventListener('click', crearTrans);

    modaltran = document.getElementById("modaltrans")
    cmodaltran = document.getElementById("cmodaltrans")

    cmodaltran.addEventListener('click', function() {
        modaltran.style.display = "none";
    });

    btntrans.addEventListener('click', function() {
        modaltran.style.display = "block";
    });

    comodal = document.getElementById("comodal")

    comodal.addEventListener('click', function() {
        alert("La boleta será enviada al correo ingresado. cuando se confirme el pago");
        setTimeout(function() {
            window.location.href = "/";
        }, 1000); // Esperar 1 segundo (1000 milisegundos) antes de redirigir
    });
    
    
    

    function crearTrans() {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/transferencia", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Lógica para manejar la respuesta exitosa
                } else {
                    // Mostrar mensaje de error si la creación de la boleta falla
                    alert('Error al crear la boleta.');
                }
            }
        };

        xhr.send();
    }





});
