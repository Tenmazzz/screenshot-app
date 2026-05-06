import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: 'app-key',
    wsHost: window.location.hostname,
    wsPort: 6001,
    forceTLS: false,
    cluster: 'mt1',
    disableStats: true,
    enabledTransports: ['ws', 'wss'],
})

createApp(App).mount('#app')
