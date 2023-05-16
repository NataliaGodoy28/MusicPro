function incrementarContador() {
  const contador = document.getElementById("contador");
  contador.stepUp();
}
function decrementarContador() {
  const contador = document.getElementById("contador");
  contador.stepDown();
}

document.addEventListener('DOMContentLoaded', function () {

  // Code Descripcion Producto
  const verDescripcion = document.querySelectorAll('#ver-descripcion');
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


  //Esto Sirve Para Cerrar La Descripcion
  document.addEventListener('click', function (event) {
    const targetElement = event.target;
    if (!targetElement.closest('.descripcion') && !targetElement.closest('#ver-descripcion') && !targetElement.classList.contains('close')) {
      descripcion.classList.remove('show-descripcion');
    }
  });

  const closeBtn = document.querySelector('.descripcion .close');

  closeBtn.addEventListener('click', function () {
    descripcion.classList.remove('show-descripcion');
  });

  // Fin Code Descripcion Producto
});
