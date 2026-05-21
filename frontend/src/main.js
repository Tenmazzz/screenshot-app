import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: 'screenshot_app_key',
    wsHost: window.location.hostname,
    wsPort: window.location.port || 443,
    wssPort: window.location.port || 443,
    forceTLS: window.location.protocol === 'https:',
    cluster: 'mt1',
    disableStats: true,
    enabledTransports: ['ws', 'wss'],
})

createApp(App).mount('#app')
