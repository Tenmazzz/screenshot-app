<script setup>
import { ref, onMounted, computed } from 'vue'
import Screen_list from './Screen_list.vue'
import Footer from './Footer.vue'

const url = ref('')
const screenshots = ref([])
const placeholder = ref('https://')
const pending = computed(() => screenshots.value.filter(s => s.status === 'pending').length)
const failed = computed(() => screenshots.value.filter(s => s.status === 'failed').length)
const done = computed(() => screenshots.value.filter(s => s.status === 'done').length)
const fullSize = ref(false)
const selectedScreen = ref(null)
const isZoomed = ref(false)
const showToast = ref(false)
const toastStatus = ref('')
const toastScreenId = ref('')
const highlightedScreenId = ref('')
const mostFailed = computed(() => {
  const counts = {}
  screenshots.value.filter(s => s.status === 'failed').forEach(s => {
    counts[s.url] = (counts[s.url] || 0) + 1
  })
  return Object.entries(counts)
    .sort((a,b) => b[1] - a[1])
    .slice(0,3)
})

const mostSuccessful = computed(() => {
  const counts = {}
  screenshots.value.filter(s => s.status === 'done').forEach(s => {
    counts[s.url] = (counts[s.url] || 0) + 1
  })
  return Object.entries(counts)
    .sort((a,b) => b[1] - a[1])
    .slice(0,3)
})

const sites = ['youtube.com', 'google.com', 'github.com', 'instagram.com', 'facebook.com', 'steam.com']
let siteIndex = 0
let charIndex = 0
let isDeleting = false

function typePlaceholder() {
  const current = 'https://' + sites[siteIndex]

  if (!isDeleting) {
    placeholder.value = current.slice(0, charIndex + 1)
    charIndex++
    if (charIndex === current.length) {
      isDeleting = true
      setTimeout(typePlaceholder, 1500)
      return
    }
  } else {
    placeholder.value = current.slice(0, charIndex - 1)
    charIndex--
    if (charIndex === 8) {
      isDeleting = false
      siteIndex = (siteIndex + 1) % sites.length
    }
  }
  setTimeout(typePlaceholder, isDeleting ? 100 : 100)
}

async function submit() {
  try {
    const response = await fetch('/api/screenshots', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url.value , full_size: fullSize.value})
    })
    const data = await response.json()
    screenshots.value.unshift(data)
    url.value = ''
    toastStatus.value = 'pending'
    showToast.value = true
    toastScreenId.value = data.id
    console.log(data)
  } catch (error) {
    console.error(error)
  }
}

function closeModal(){
  selectedScreen.value = null
  isZoomed.value = false
}

function scrollToScreen() {
  document.getElementById('screen-' + toastScreenId.value)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  highlightedScreenId.value = Number(toastScreenId.value)
  setTimeout(() => {
    highlightedScreenId.value = null
  }, 4000)
}

onMounted(async () => {
  const response = await fetch('/api/screenshots')
  const data = await response.json()
  screenshots.value = data.slice().reverse()
  console.log(data)

  setTimeout(typePlaceholder, 500)

  window.Echo.channel('screenshots')
    .listen('ScreenshotCompleted', (e) => {
      console.log(e)
      const index = screenshots.value.findIndex(s => s.id === e.id)
      if (index !== -1) {
        screenshots.value[index] = { ...screenshots.value[index], ...e }
        toastStatus.value = e.status
      }
      showToast.value = true
      setTimeout(() => {
        showToast.value = false
      }, 8000)
    })
})
</script>

<template>

    <div v-if="showToast && toastStatus === 'pending'" class="flex items-center w-full max-w-sm p-4 text-white bg-gray-800 rounded-xl border border-white/20 fixed top-4 left-1/2 -translate-x-1/2 z-50 cursor-wait" role="alert">
      <div class="inline-flex items-center justify-center shrink-0 w-7 h-7 rounded">
        <div class="w-5 h-5 border-2 border-orange-400 border-t-white/60 rounded-full animate-spin"></div>
      </div>
      <div class="ms-3 text-sm font-normal">Screenshot en cours...</div>
    </div>

    <!-- Toast done -->
    <div v-if="showToast && toastStatus === 'done'" @click="scrollToScreen()" class="flex items-center w-full max-w-sm p-4 text-white bg-gray-800 rounded-xl border border-white/20 fixed top-4 left-1/2 -translate-x-1/2 z-50 cursor-pointer" role="alert">
      <div class="inline-flex items-center justify-center shrink-0 w-7 h-7 text-emerald-400 bg-emerald-400/20 rounded">
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 11.917 9.724 16.5 19 7.5"/></svg>
      </div>
      <div class="ms-3 text-sm font-normal">Screenshot réussi !</div>
      <button type="button" @click="showToast = false" class="ms-auto flex items-center justify-center text-white/50 hover:text-white bg-transparent border border-transparent rounded text-sm h-8 w-8 cursor-pointer">
        <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"/></svg>
      </button>
    </div>

    <!-- Toast failed -->
    <div v-if="showToast && toastStatus === 'failed'" @click="scrollToScreen()" class="flex items-center w-full max-w-sm p-4 text-white bg-gray-800 rounded-xl border border-white/20 fixed top-4 left-1/2 -translate-x-1/2 z-50 cursor-pointer" role="alert">
      <div class="inline-flex items-center justify-center shrink-0 w-7 h-7 text-red-400 bg-red-400/20 rounded">
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"/></svg>
      </div>
      <div class="ms-3 text-sm font-normal">Screenshot échoué</div>
      <button type="button" @click="showToast = false" class="ms-auto flex items-center justify-center text-white/50 hover:text-white bg-transparent border border-transparent rounded text-sm h-8 w-8 cursor-pointer">
        <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 17.94 6M18 18 6.06 6"/></svg>
      </button>
    </div>



  <nav :style="{ backgroundColor: 'rgba(62, 27, 94, 0.5)' }" class="flex items-center justify-between px-8 py-4 rounded-full mx-auto mt-4 w-8/12">
    <div class="flex items-center gap-4">
      <svg class="w-6 h-6 text-white" fill="none" stroke-width="1.5" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <span class="font-semibold text-white">Screen App</span>
    </div>

  </nav>

  <div class="flex flex-col bg-white/10 border border-white/20 rounded-3xl px-10 py-10 mx-auto mt-10 w-8/12">
    <span class="text-white text-5xl mb-6">Screenshot tool online</span>
    <span class="text-white/50 text-lg mb-2">Enter the URL to capture it.</span>

    <div class="flex items-center gap-4 justify-center py-6">
      <input type="text" :placeholder="placeholder" v-model="url" class="w-80 bg-white/10 border border-white/30 text-white placeholder-white/50 rounded-full px-6 py-3 focus:outline-none focus:border-white/60" />
      <button @click="submit" type="button" class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm px-6 py-3 cursor-pointer">
        Envoyer
      </button>
    </div>

    <div class="border-t border-white/20 mx-4"></div>
    <div class="flex items-center gap-2 text-white text-sm mt-2">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 mt-2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 1 1-3 0m3 0a1.5 1.5 0 1 0-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m-9.75 0h9.75" />
      </svg>
      <span class="text-2xl self-start mt-2 text-white">Screenshot options</span>
    </div>

    <div class="flex items-center justify-between px-4 py-4">
      <div class="flex items-center gap-2 text-white text-sm">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
        </svg>
        <span>Full page</span>
      </div>
      <button @click="fullSize = !fullSize" :class="fullSize ? 'bg-blue-500' : 'bg-white/20'" class="w-10 h-6 rounded-full transition-all duration-300 relative cursor-pointer">
        <span :class="fullSize ? 'left-5' : 'left-1'" class="absolute top-1 w-4 h-4 bg-white rounded-full transition-all duration-300"></span>
      </button>
    </div>
  </div>

  <div class="flex gap-6 mx-auto mt-10 w-8/12">
    <div class="flex flex-col bg-white/10 border border-white/20 rounded-3xl px-10 py-10 w-1/2 break-words text-white">

      <span class="text-3xl mb-5">How it works ?</span>

      <div class="flex items-center gap-3 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-blue-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
        </svg>
        <span class="text-xl">Put a url</span>
      </div>

      <div class="flex items-center gap-3 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-purple-400">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z" />
        </svg>
        <span class="text-xl">Screenshoting...</span>
      </div>

      <div class="flex items-center gap-3 mb-4 ">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-emerald-400">
        <path stroke-linecap="round" stroke-linejoin="round" d="m9 12.75 3 3m0 0 3-3m-3 3v-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
      </svg>
      <span class="text-xl">Download !</span>
      </div>

    </div>

    <div class="flex flex-col bg-white/10 border border-white/20 rounded-3xl px-10 py-10 w-1/2 break-words text-white">
      <span class="text-3xl mb-5">Simple and free</span>

      <div class="flex items-center gap-3 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-lime-500">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
        </svg>
        <p class="text-xl">100% free</p>
      </div>

      <div class="flex items-center gap-2 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-amber-500">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5V6.75a4.5 4.5 0 1 1 9 0v3.75M3.75 21.75h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H3.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
        </svg>
        <p class="text-xl">No account required</p>
      </div>

      
      <div class="flex items-center gap-2 mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-yellow-500">
          <path stroke-linecap="round" stroke-linejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z" />
        </svg>
      <p class="text-xl">Less than 30s</p>
      </div>

    </div>
  </div>

  <div class="flex gap-6 mx-auto mt-10 w-8/12">

    <div class="flex flex-col bg-white/10 border border-white/20 rounded-3xl px-10 py-10 w-1/2 break-words text-white">
      <p class="text-white text-8xl">{{ done }}</p>
      <p class="bg-gradient-to-r from-emerald-300 to-emerald-600 bg-clip-text text-transparent text-2xl mt-6">screenshots done</p>
      <div v-for="(success_website, index) in mostSuccessful" class="flex items-center gap-3 mt-3">
        <span :class="{
          'bg-emerald-400/20 text-emerald-400': index === 0,
          'bg-teal-400/20 text-teal-400': index === 1,
          'bg-green-400/20 text-green-400': index === 2
        }" class="w-6 h-6 rounded-full flex items-center justify-center text-xs shrink-0">{{ index + 1 }}</span>
        <p class="text-white/60 text-sm truncate">{{ success_website[0] }}</p>
      </div>
    </div>

    <div class="flex flex-col bg-white/10 border border-white/20 rounded-3xl px-10 py-10 w-1/2 break-words">
      <p class="text-white text-8xl">{{ failed }}</p>
      <p class="bg-gradient-to-r from-red-300 to-red-600 bg-clip-text text-transparent text-2xl mt-6">screenshots failed</p>
      <div v-for="(failed_website, index) in mostFailed" class="flex items-center gap-3 mt-3">
        <span :class="{
          'bg-red-400/20 text-red-400': index === 0,
          'bg-orange-400/20 text-orange-400': index === 1,
          'bg-yellow-400/20 text-yellow-400': index === 2
        }" class="w-6 h-6 rounded-full flex items-center justify-center text-xs shrink-0">{{ index + 1 }}</span>
        <p class="text-white/60 text-sm truncate">{{ failed_website[0] }}</p>
      </div>
    </div>

  </div>

  <Screen_list :screenshots="screenshots" :selectedScreen="selectedScreen" :highlightedScreenId="highlightedScreenId" @update:selectedScreen="selectedScreen = $event" />

  <div v-if="selectedScreen" @click="closeModal()" @wheel.prevent class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-8">
    <img :src="`/storage/${selectedScreen.file_path}`" @click.stop="isZoomed = !isZoomed" :class="{ 'scale-200': isZoomed, 'cursor-zoom-in': !isZoomed, 'cursor-zoom-out': isZoomed }" class="max-w-full max-h-full rounded-xl shadow-2xl transition-transform duration-300 " />
  </div>

  <Footer></Footer>

</template>