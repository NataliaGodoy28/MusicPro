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
  const cartIcon = document.querySelector('.cart-icon');
  const overlay = document.querySelector('.overlay');
  const cart = document.querySelector('.cart');
  const cartItems = document.querySelector('.cart-items');
  const cartTotal = document.querySelector('.total');
  const cartTotalc = document.querySelector('.totalc');
  const productBtns = document.querySelectorAll('.add-to-cart');

  let cartCount = 0;
  let cartTotalPrice = 0;
  let cartItemsArr = [];
  let cartTotalPricec = 0;
  // Event Listeners
  cartIcon.addEventListener('click', toggleCart);
  overlay.addEventListener('click', toggleCart);
  productBtns.forEach(btn => {
    btn.addEventListener('click', addToCart);
  });

  // Functions
  function toggleCart() {
    cart.classList.toggle('show-cart');
    overlay.classList.toggle('show-overlay');
  }

  function addToCart(e) {
    const product = e.target.parentElement;
    const productImg = product.querySelector('img').src;
    const productTitle = product.querySelector('h3').textContent;
    const productCode = product.querySelector('.codigo').textContent;
    const productPrice = parseFloat(product.querySelector('.price').textContent.slice(1));
    const productPriced = parseFloat(product.querySelector('.priced').textContent.slice(1));
    const productId = e.target.dataset.id;
    const item = {
      id: productId,
      code: productCode,
      img: productImg,
      title: productTitle,
      price: productPrice,
      priced: productPriced,
      count: 1
    };

    // Check if item is already in cart
    const existingItem = cartItemsArr.find(item => item.id === productId);
    if (existingItem) {
      existingItem.count++;
    } else {
      cartItemsArr.push(item);
    }

    // Update cart count and total price
    cartCount++;
    cartTotalPrice += productPrice;
    cartTotalPricec += productPriced;
    cartIcon.querySelector('.cart-count').textContent = cartCount;
    cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
    cartTotalc.textContent = `$${cartTotalPricec.toFixed(2)}`;
    // Update cart items list
    renderCartItems();
  }

  function renderCartItems() {
    cartItems.innerHTML = '';
    cartItemsArr.forEach(item => {
      const li = document.createElement('li');
      var select = document.getElementById("precioSelect");
      var selectedOption = select.options[select.selectedIndex].value;
      if (selectedOption === "chileno") {
        li.innerHTML = `
            <img src="${item.img}" alt="${item.title}" />
            <div class="productc">
              <h4>${item.title}</h4>
              <p class="pricec chileno"><strong>$${item.price.toFixed(0)} x ${item.count}</strong> </p>
              <p class="pricecd dolar" style="display: none;"><strong>$${item.priced.toFixed(2)} x ${item.count}</strong> </p>
              <button class="remove-item" data-id="${item.id}">Eliminar</button>
            </div>
          `;
      } else if (selectedOption === "dolar") {
        li.innerHTML = `
          <img src="${item.img}" alt="${item.title}" />
          <div class="productc">
            <h4>${item.title}</h4>
            <p class="pricec chileno" style="display: none;"><strong>$${item.price.toFixed(0)} x ${item.count}</strong> </p>
            <p class="pricecd dolar" ><strong>$${item.priced.toFixed(2)} x ${item.count}</strong> </p>
            <button class="remove-item" data-id="${item.id}">Eliminar</button>
          </div>
        `;
      }

      cartItems.appendChild(li);
    });

    // Add event listeners to remove buttons
    const removeButtons = document.querySelectorAll('.remove-item');
    removeButtons.forEach(btn => {
      btn.addEventListener('click', removeItem);
    });
  }

  function removeItem(e) {
    const itemId = e.target.dataset.id;
    const item = cartItemsArr.find(item => item.id === itemId);
    item.count--;
    cartCount--;
    cartTotalPrice -= item.price;
    cartTotalPricec -= item.priced;
    if (item.count === 0) {
      cartItemsArr = cartItemsArr.filter(item => item.id !== itemId);
    }

    // Update cart count and total price
    cartIcon.querySelector('.cart-count').textContent = cartCount;
    cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
    cartTotalc.textContent = `$${cartTotalPricec.toFixed(2)}`;

    // Update cart items list
    renderCartItems();
  }
  function checkout() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/crearBoletacarro", true); // URL para crear la boleta
    xhr.setRequestHeader("Content-Type", "application/json"); // Establecer el tipo de contenido como JSON
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          // La boleta se creó correctamente
        } else {
          // Mostrar mensaje de error si la creación de la boleta falla
          alert('Error al crear la boleta.');
        }
      }
    };
    const data = {
      cartItems: cartItemsArr
    };

    xhr.send(JSON.stringify(data));

    cartItemsArr = [];
    cartCount = 0;
    cartTotalPrice = 0;
    cartTotalPricec = 0;
    cartIcon.querySelector('.cart-count').textContent = cartCount;
    cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
    cartTotalc.textContent = `$${cartTotalPricec.toFixed(2)}`;
    renderCartItems();
    toggleCart();
  }

  const pago = document.querySelector('#pago');
  pago.addEventListener('click', function () {
    // Obtener el elemento <h1> con la clase "session"
    var h1Element = document.querySelector('.session');

    // Verificar si el elemento existe
    if (h1Element !== null) {
      // Obtener el contenido del <h1>
      var valorH1 = h1Element.textContent;

      if (valorH1 === "invitado") {
        document.getElementById("modalinv").style.display = "block";
        checkout()
      }
    }
    else {
      checkout();
      setTimeout(function () {
        window.location.href = "resumen";
      }, 0);
    }
  });

  var modali = document.querySelector('#modalinv');

  if (modali !== null) {
    const cmodalinv = document.querySelector('#cmodalinv');
    cmodalinv.addEventListener('click', closeinv);

    const btninv = document.querySelector('#btniv');
    btninv.addEventListener('click', invitado);

    function invitado() {
      document.getElementById("modalinv").style.display = "none";
      document.getElementById("modalinvd").style.display = "block";
    }
    function closeinv() {
      document.getElementById("modalinv").style.display = "none";
    }



  }
});



