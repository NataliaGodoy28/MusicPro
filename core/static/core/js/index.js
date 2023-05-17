document.addEventListener('DOMContentLoaded', function () {

  // Code Descripcion Producto

  const verDescripcion = document.querySelectorAll('.ver-descripcion');
  const descripcion = document.querySelector('.descripcion');
  const descItem = document.querySelector('.desc-item');

  verDescripcion.forEach(btn => {
    btn.addEventListener('click', funcionVerDescripcion);
  });

  function funcionVerDescripcion(e) {
    descripcion.classList.toggle('show-descripcion')
    const product = e.target.parentElement;
    const productImg = product.querySelector('img').src;
    const productTitle = product.querySelector('h3').textContent;
    const productCode = product.querySelector('.codigo').textContent;
    const productDesc = product.querySelector('.desc').textContent;
    const productDetalle = product.querySelector('.detalle').textContent;
    const productPrice = parseFloat(product.querySelector('.price').textContent.slice(1));
    const productId = e.target.dataset.id;
    const item = {
      id: productId,
      img: productImg,
      title: productTitle,
      price: productPrice,
      codigo: productCode,
      desc: productDesc,
      detalle: productDetalle

    };

    renderDescItem(item);
  }

  function renderDescItem(item) {
    descItem.innerHTML = '';
    const li = document.createElement('li');

    li.innerHTML = `
        <img src="${item.img}" alt="${item.title}" />
        <div>
          <h4>${item.title}</h4>
          <p>${item.codigo}</p>
          <p>${item.desc}</p>
          <p>${item.detalle}</p>
          <p>$${item.price.toFixed(0)}</p>
        </div>
      `;

    descItem.appendChild(li);
  }

  const closeSpan = document.querySelector('.descripcion .closes');
  closeSpan.addEventListener('click', function () {
    descripcion.classList.remove('show-descripcion');
  });

  //Fin Code Descripcion 

  //Code Carrito

  const verCarrito = document.querySelector('.btncart');
  const carrito = document.querySelector('.carrito');
  const closeSpan2 = document.querySelector('.carrito .closes');
  verCarrito.addEventListener('click', function () {
    carrito.classList.add('show-carrito');
  });
  closeSpan2.addEventListener('click', function () {
    carrito.classList.remove('show-carrito');
  });
  //Fin Code Carrito

  //Modals Inicio
  var sessionElement = document.getElementById('session');
  var sessionValue = parseInt(sessionElement.innerText);

  if (sessionValue === 0) {
    const cerrar0 = document.querySelector('.close0');
    const modal0 = document.getElementById("myModal0");
    const pagarBtn = document.getElementById("pagarcar");

    pagarBtn.onclick = function () {
      modal0.style.display = "block";
    }
    cerrar0.onclick = function () {
      modal0.style.display = "none";
    }

    window.onclick = function (event) {
      if (event.target == modal0) {
        modal0.style.display = "none";
      }


    }
    
    const modal5 = document.getElementById("myModal5");
    var btns = document.querySelectorAll(".metod");

    btns.forEach(function (btn) {
      btn.onclick = function () {
        modal5.style.display = "block";
        modal0.style.display = "none";

      };
    });

   
  } else {
    const pagarBtn = document.getElementById("pagarcar");
    const invitado = document.getElementById("btninvitado");
    const invitado2 = document.getElementById("btnin");
    const modal = document.getElementById("myModal");
    const modal2 = document.getElementById("myModal2");
    const modal3 = document.getElementById("myModal3");

    const cerrar = document.querySelector('.close1');
    const cerrarinv = document.querySelector('.closeinv');
    const cerrarmet = document.querySelector('.close4');

    invitado2.onclick = function () {
      modal2.style.display = "none";
      modal.style.display = "none";
      modal3.style.display = "block";
    }

    invitado.onclick = function () {
      modal2.style.display = "block";
    }

    pagarBtn.onclick = function () {
      modal.style.display = "block";
    }

    cerrar.onclick = function () {
      modal.style.display = "none";
    }
    cerrarinv.onclick = function () {
      modal2.style.display = "none";
    }
    cerrarmet.onclick = function () {
      modal3.style.display = "none";
    }

    window.onclick = function (event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
      if (event.target == modal2) {
        modal2.style.display = "none";
      }
      if (event.target == modal3) {
        modal3.style.display = "none";
      }

    }


    const modal5 = document.getElementById("myModal5");
    var btns = document.querySelectorAll(".metod");

    btns.forEach(function (btn) {
      btn.onclick = function () {
        modal5.style.display = "block";
        modal.style.display = "none";
        modal2.style.display = "none";
        modal3.style.display = "none";
      };
    });



  }
  const modal5 = document.getElementById("myModal5");
  const cerrar6 = document.getElementById('acpago')
  const cerrar5 = document.querySelector('.close5');

  cerrar5.onclick = function () {
    modal5.style.display = "none";
  }

  cerrar6.onclick = function () {
    modal5.style.display = "none";
  }

  window.onclick = function (event) {
    if (event.target == modal5) {
      modal5.style.display = "none";
    }
  };


  //Fin Modal




});

