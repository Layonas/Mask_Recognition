import { createApp } from 'vue'
import App from './App.vue'

var path = window.location.pathname;
var page = path.split("/").pop()?.split('.')[0];

if(page === "index"){
    createApp(App).mount('#app')
} else if(page === "about"){
    console.log(page)
}
// better solution to use bus  https://codesandbox.io/s/30mxyw5726?file=/App.vue:421-426