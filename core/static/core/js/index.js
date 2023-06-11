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
    const productBtns = document.querySelectorAll('.add-to-cart');
  
    let cartCount = 0;
    let cartTotalPrice = 0;
    let cartItemsArr = [];
  
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
      const productId = e.target.dataset.id;
      const item = {
        id: productId,
        code: productCode,
        img: productImg,
        title: productTitle,
        price: productPrice,
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
      cartIcon.querySelector('.cart-count').textContent = cartCount;
      cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
  
      // Update cart items list
      renderCartItems();
    }
  
    function renderCartItems() {
      cartItems.innerHTML = '';
      cartItemsArr.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `
        <img src="${item.img}" alt="${item.title}" />
        <div>
          <h4>${item.title}</h4>
          <p>$${item.price.toFixed(0)} x ${item.count}</p>
          <button class="remove-item" data-id="${item.id}">Eliminar</button>
        </div>
      `;
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
  
      if (item.count === 0) {
        cartItemsArr = cartItemsArr.filter(item => item.id !== itemId);
      }
  
      // Update cart count and total price
      cartIcon.querySelector('.cart-count').textContent = cartCount;
      cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
  
      // Update cart items list
      renderCartItems();
    }
    function checkout() {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/crearBoletacarro", true); // URL para crear la boleta
      xhr.setRequestHeader("Content-Type", "application/json"); // Establecer el tipo de contenido como JSON
      xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
          if (xhr.status === 200) {
            // La boleta se creó correctamente
          } else {
            // Mostrar mensaje de error si la creación de la boleta falla
            alert('Error al crear la boleta.');
          }
        }
      };
    
      const paymentMethod = obtenerMetodoPago();
      const data = {
        cartItems: cartItemsArr,
        paymentMethod: paymentMethod
      };
    
      xhr.send(JSON.stringify(data));
    
      cartItemsArr = [];
      cartCount = 0;
      cartTotalPrice = 0;
      cartIcon.querySelector('.cart-count').textContent = cartCount;
      cartTotal.textContent = `$${cartTotalPrice.toFixed(0)}`;
      renderCartItems();
      toggleCart();
    }
    
  
    //Fin Code Carrito
    let metodoPagoSeleccionado = '';

    const deb = document.querySelector('#debito');
    deb.addEventListener('click', function() {
      metodoPagoSeleccionado = 'Débito';
    });

    const cred = document.querySelector('#credito');
    cred.addEventListener('click', function() {
      metodoPagoSeleccionado = 'Crédito';
    });

    const trans = document.querySelector('#transferencia');
    trans.addEventListener('click', function() {
      metodoPagoSeleccionado = 'Transferencia';
    });

    function obtenerMetodoPago() {
      return metodoPagoSeleccionado;
    }
    
      //Modales

    const trans2 = document.querySelector('#transferencia');
    trans2.addEventListener('click', openModal2);
    const cmodal1 = document.querySelector('#cmodal1');
    cmodal1.addEventListener('click', closeModal);
    const pago = document.querySelector('#pago');
    pago.addEventListener('click', openModal);
    const cmodal2 = document.querySelector('#cmodal2');
    cmodal2.addEventListener('click', closeModal2);
    const cmodal3 = document.querySelector('#cmodal3');
    cmodal3.addEventListener('click', closeModal3);
    const conf = document.querySelector('#conf');
    conf.addEventListener('click', closeModal3);
    const conftrans = document.querySelector('#conftrans');
    conftrans.addEventListener('click', openModal3);


    function openModal() {
      document.getElementById("modal").style.display = "block";
    }
    function closeModal() {
      document.getElementById("modal").style.display = "none";
    }
    function openModal2() {
      document.getElementById("modal2").style.display = "block";
      document.getElementById("modal").style.display = "none";
    }
    function closeModal2() {
      document.getElementById("modal2").style.display = "none";
    }
    function openModal3() {
      document.getElementById("modal2").style.display = "none";
      document.getElementById("modal3").style.display = "block";
    }
    function closeModal3() {
      checkout();
      document.getElementById("modal3").style.display = "none";
    }
    //Fin Modales
  
  });
  
  
  
  