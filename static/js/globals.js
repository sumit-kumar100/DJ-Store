$(document).on('click', `#decrease-count`, function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/minus-quantity/',
    data: {
      variantId: $(`#variant-id-${e.target.name}`).val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    data_type: 'html',
    success: function (data) {
      console.log(data)
      if (data?.success && data?.quantity) {
        document.querySelector(`#quantity-${e.target.name}`).value = data?.quantity
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ ${data.total}`
        })
      }
      else {
        document.querySelector(`#cart-item-${e.target.name}`).remove()
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ 0`
        })
      }
    },
    error: function (error) {
      console.log(error)
    }
  });
});

$(document).on('click', '#increase-count', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/plus-quantity/',
    data: {
      variantId: $(`#variant-id-${e.target.name}`).val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    data_type: 'html',
    success: function (data) {
      console.log(data)
      if (data?.success && data?.quantity) {
        document.querySelector(`#quantity-${e.target.name}`).value = data?.quantity
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ ${data.total}`
        })
      }
      else {
        document.querySelector(`#message-${e.target.name}`).innerText = data?.message;
      }
    },
    error: function (error) {
      console.log(error)
    }
  });
});

$(document).on('click', `#checkout-decrease-count`, function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/minus-quantity/',
    data: {
      variantId: $(`#checkout-variant-id-${e.target.name}`).val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    data_type: 'html',
    success: function (data) {
      if (data?.success && data?.quantity) {
        document.querySelector(`#checkout-quantity-${e.target.name}`).value = data?.quantity
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ ${data.total}`
        })
      }
      else {
        document.querySelector(`#checkout-cart-item-${e.target.name}`).remove()
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ 0`
        })
      }
    },
    error: function (error) {
      console.log(error)
    }
  });
});

$(document).on('click', '#checkout-increase-count', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/plus-quantity/',
    data: {
      variantId: $(`#checkout-variant-id-${e.target.name}`).val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    data_type: 'html',
    success: function (data) {
      if (data?.success && data?.quantity) {
        document.querySelector(`#checkout-quantity-${e.target.name}`).value = data?.quantity
        let cartSum = document.querySelectorAll('.cart-sum')
        cartSum.forEach(cart => {
          cart.innerText = `$ ${data.total}`
        })
      }
      else {
        document.querySelector(`#checkout-message-${e.target.name}`).innerText = data?.message
      }
    },
    error: function (error) {
      console.log(error)
    }
  });
});

$(document).on('change', '#post-form', function (e) {
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/ajaxcolor/',
    data: {
      productid: $('#productid').val(),
      size: $('#size').val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    data_type: 'html',
    success: function (data) {
      console.log("success");
      $('#appendHere').html(data.rendered_table);
    },
    error: function (error) {
      console.log(error)
    }
  });
});



$(document).ready(function () {
  $('.thumbnail').click(function () {
    var image = $(this).attr('src');
    $('.main-image').attr('src', image);
  });
});

const submitForm = () => {
  document.getElementById('submitForm').submit()
} 

const showCart = e => {
  window.scrollTo(0, 0)
  const cart = document.querySelector('#cart');
  let classes = Array.from(cart.classList)
  if (classes.includes('translate-x-full')) {
    cart.classList.remove('translate-x-full');
    cart.classList.add('translate-x-0');
  }
  else {
    cart.classList.remove('translate-x-0');
    cart.classList.add('translate-x-full');
  }
}


const switchTheme = () => {
  const root = document.getElementsByTagName('html')[0]
  if (root.className === 'dark') {
    root.className = 'light';
    window.localStorage.setItem('theme', 'light');
  }
  else {
    root.className = 'dark';
    window.localStorage.setItem('theme', 'dark')
  }
}

const showDropDown = e => {
  const dropDown = document.querySelector('#dropDown');
  var classes = Array.from(dropDown.classList)
  classes.includes('hidden') ? dropDown.classList.remove('hidden') : dropDown.classList.add('hidden');
}

const showSideNav = e => {
  const dropDown = document.querySelector('#sideNav');
  var classes = Array.from(dropDown.classList)
  if (classes.includes('-translate-x-full')) {
    dropDown.classList.remove('-translate-x-full');
    dropDown.classList.add('translate-x-0');
  }
  else {
    dropDown.classList.remove('translate-x-0');
    dropDown.classList.add('-translate-x-full');
  }
}

const showMegaMenu = id => {
  const previous = document.querySelectorAll('.mega-menu');
  previous.forEach(element => {
    if(element.id !== `mega-menu-${id}`){
      element.style.visibility = 'hidden';
    }
  })
  const state = document.querySelector(`#mega-menu-${id}`);
  if(state){
    if (state.style.visibility === 'hidden'){
      state.style.visibility = 'visible';
    }
    else{
      state.style.visibility = 'hidden';
    }
  }
}

const handleCarousel = (current, total, action) => {
  if (action === 'increase') {
    document.querySelector(`#carousel-${current}`).classList.remove('translate-x-100');
    document.querySelector(`#next-btn-${current}`).classList.remove('visible');

    document.querySelector(`#carousel-${current}`).classList.add('-translate-x-full');
    document.querySelector(`#next-btn-${current}`).classList.add('invisible');

    if (Number(current) === Number(total)) {
      document.querySelector(`#carousel-1`).classList.remove('-translate-x-full');
      document.querySelector(`#next-btn-1`).classList.remove('invisible');

      document.querySelector(`#carousel-1`).classList.add('translate-x-100');
      document.querySelector(`#next-btn-1`).classList.add('visible');
    }
    else {
      document.querySelector(`#carousel-${Number(current) + 1}`).classList.remove('-translate-x-full');
      document.querySelector(`#next-btn-${Number(current) + 1}`).classList.remove('invisible');

      document.querySelector(`#carousel-${Number(current) + 1}`).classList.add('translate-x-100');
      document.querySelector(`#next-btn-${Number(current) + 1}`).classList.add('visible');
    }
  }
  else {

    document.querySelector(`#carousel-${current}`).classList.remove('translate-x-100');
    document.querySelector(`#prev-btn-${current}`).classList.remove('visible');

    document.querySelector(`#carousel-${current}`).classList.add('-translate-x-full');
    document.querySelector(`#prev-btn-${current}`).classList.add('invisible');


    if (Number(current) === 1) {
      document.querySelector(`#carousel-${total}`).classList.remove('-translate-x-full');
      document.querySelector(`#prev-btn-${total}`).classList.remove('invisible');

      document.querySelector(`#carousel-${total}`).classList.add('translate-x-100');
      document.querySelector(`#prev-btn-${total}`).classList.add('visible');
    }
    else {
      document.querySelector(`#carousel-${Number(current) - 1}`).classList.remove('-translate-x-full');
      document.querySelector(`#prev-btn-${Number(current) - 1}`).classList.remove('invisible');

      document.querySelector(`#carousel-${Number(current) - 1}`).classList.add('translate-x-100');
      document.querySelector(`#prev-btn-${Number(current) - 1}`).classList.add('visible');
    }
  }
}
