import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import 'bootstrap/dist/css/bootstrap.min.css'
// import 'bootstrap' // optional, for JS components like dropdowns if needed
// import './style.css' // your own custom CSS if any

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
