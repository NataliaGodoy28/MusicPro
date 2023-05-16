function incrementarContador(){
    const contador = document.getElementById("contador");
    contador.stepUp();
}
function decrementarContador(){
    const contador = document.getElementById("contador");
    contador.stepDown();
}

document.addEventListener('DOMContentLoaded', function () {

    const cartIcon = document.querySelector('.cart-icon');
    const overlay = document.querySelector('.overlay');
    const cart = document.querySelector('.cart');
    const cartItems = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.total');
    const checkoutBtn = document.querySelector('.checkout');
    const productBtns = document.querySelectorAll('.add-to-cart');
    const invitado = document.querySelector('#invitado');
    const verDescripcion = document.querySelector('.ver-descripcion');
    const cocont = document.querySelector('#cocont');
    const descripcion = document.querySelector('.descripcion');
    const descItem = document.querySelector('.desc-item');
    
    let cartCount = 0;
    let cartTotalPrice = 0;
    let cartItemsArr = [];
  
    // Event Listeners
    cocont.addEventListener('click', cerrarcorreo)
    invitado.addEventListener('click', ingcorreo)
    cartIcon.addEventListener('click', toggleCart);
    overlay.addEventListener('click', toggleCart);
    checkoutBtn.addEventListener('click', checkout);
    productBtns.forEach(btn => {
      btn.addEventListener('click', addToCart);
    });
    verDescripcion.addEventListener('click', funcionVerDescripcion);

    var correo = document.getElementById("correo");

    // Functions
    function funcionVerDescripcion(e){
      descripcion.classList.toggle('show-descripcion')
      // overlay.classList.toggle('show-overlay')
      const product = e.target.parentElement;
      const productImg = product.querySelector('img').src;
      const productTitle = product.querySelector('h3').textContent;
      const productCode = product.querySelector('.codigo').textContent;
      const productDesc = product.querySelector('.desc').textContent;
      const productPrice = parseFloat(product.querySelector('.price').textContent.slice(1));
      const productId = e.target.dataset.id;
      const item = {
        id: productId,
        img: productImg,
        title: productTitle,
        price: productPrice,
        codigo: productCode,
        desc: productDesc,
        count: 1
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
          <p>$${item.price.toFixed(0)}</p>
        </div>
      `;

      descItem.appendChild(li);
    }

    function ingcorreo(){
      modal.style.display = "none";
      correo.style.display = "block";
    }

    function cerrarcorreo(){
      alert("Correo guardado");
      correo.style.display = "none";
    }
  
    function toggleCart() {
      descripcion.classList.toggle('show-description')
      cart.classList.toggle('show-cart');
      overlay.classList.toggle('show-overlay');
    }
  
    function addToCart(e) {
      const product = e.target.parentElement;
      const productImg = product.querySelector('img').src;
      const productTitle = product.querySelector('h3').textContent;
      const productPrice = parseFloat(product.querySelector('.price').textContent.slice(1));
      const productId = e.target.dataset.id;
      const item = {
        id: productId,
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
      cartTotal.textContent = `$${cartTotalPrice.toFixed(2)}`;
  
      // Update cart items list
      renderCartItems();
    }
  
    // Obtener el botón y el modal
  
    var modal = document.getElementById("myModal");

    // Obtener el elemento span que cierra el modal
    var span = document.getElementsByClassName("close")[0];
    var span2 = document.getElementsByClassName("close2")[0];
    // Cuando el usuario haga clic en el botón, abra el modal
    
    span2.onclick = function() {
      correo.style.display = "none";
      
    }
    // Cuando el usuario haga clic en el span (x), cierre el modal
    span.onclick = function() {
      modal.style.display = "none";
      
    }

    // Cuando el usuario haga clic fuera del modal, cierre el modal
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
       
      }
      if(event.target == correo){
        correo.style.display = "none";
      }
    }





    function checkout() {
      modal.style.display = "block";

      cartItemsArr = [];
      cartCount = 0;
      cartTotalPrice = 0;
      cartIcon.querySelector('.cart-count').textContent = cartCount;
      cartTotal.textContent = `$${cartTotalPrice.toFixed(2)}`;
      renderCartItems();
      toggleCart();
    }
  
  
  });
