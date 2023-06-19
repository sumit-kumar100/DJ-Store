// Email Configs
EMAIL_HOST_USER = 'amazonstore295@gmail.com'
EMAIL_HOST_PASSWORD = 'amazonstore295s.t'

// Instamojo Configs
API_KEY = "test_00fdfd80a82bdae553372ec546b"
AUTH_TOKEN = "test_26343b0f40ae03f99bba48b3a58"


const submitForm = () => {
  const colors = document.querySelectorAll('.color-input')
  const categories = document.querySelectorAll('.category-input')
  const sizes = document.querySelectorAll('size-input')

  let categories_filter, colors_filter, sizes_filter = [];

  categories.forEach(element => element.checked ? categories_filter.push(element.value) : null)
  colors.forEach(element => element.checked ? colors_filter.push(element.value) : null)
  sizes.forEach(element => element.checked ? sizes_filter.push(element.value) : null)


  console.log(categories_filter, siz)
  // window.location.assign(`${window.location.href}?categories=${categories.filter(element => element.checked)}`)

} 