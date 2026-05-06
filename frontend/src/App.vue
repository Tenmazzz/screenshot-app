<script setup>
import { ref, onMounted, computed } from 'vue'
import Screen_list from './Screen_list.vue'

const url = ref('')
const screenshots = ref([])
const placeholder = ref('https://')
const pending = computed(() => screenshots.value.filter(s => s.status === 'pending').length)
const failed = computed(() => screenshots.value.filter(s => s.status === 'failed').length)
const done = computed(() => screenshots.value.filter(s => s.status === 'done').length)
const fullSize = ref(false)
const selectedScreen = ref(null)
const isZoomed = ref(false)
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
    console.log(data)
  } catch (error) {
    console.error(error)
  }
}

function closeModal(){
  selectedScreen.value = null
  isZoomed.value = false
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
      }
    })
})
</script>

<template>
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

  <Screen_list :screenshots="screenshots" :selectedScreen="selectedScreen" @update:selectedScreen="selectedScreen = $event" />

  <div v-if="selectedScreen" @click="closeModal()" @wheel.prevent class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-8">
    <img :src="`/storage/${selectedScreen.file_path}`" @click.stop="isZoomed = !isZoomed" :class="{ 'scale-200': isZoomed, 'cursor-zoom-in': !isZoomed, 'cursor-zoom-out': isZoomed }" class="max-w-full max-h-full rounded-xl shadow-2xl transition-transform duration-300 " />
  </div>


  <footer class="mt-20 pb-10 px-10 bg-black pt-10 text-white/70">

    <div class="mx-auto w-8/12">
      <p class="text-3xl text-center mb-15 text-white/85">À propos de moi</p>
      <div class="grid grid-cols-3 gap-10 mx-auto justify-items-center">

        <div>
          <p class="text-xl mb-6">Screenshot App</p>
          <p>It's a website in which you can take a screenshot from any website you want</p>
        </div>

        <div class="flex flex-col gap-4 ">
          <p class="text-xl mb-3">Technologies</p>
          <div class="flex flex-col gap-3 ml-4">

            <div class="flex items-center gap-3">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white/60" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 1.61h-9.94L12 5.16 9.94 1.61H0l12 20.78ZM12 14.08 5.16 2.23h4.01L12 6.41l2.83-4.18h4.01Z"/>
              </svg>
              <span>Vue.js</span>
            </div>

            <div class="flex items-center gap-3">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white/60" xmlns="http://www.w3.org/2000/svg">
                <path d="M23.642 5.43a.364.364 0 0 1 .014.1v5.149c0 .135-.073.26-.189.326l-4.323 2.49v4.934a.378.378 0 0 1-.188.326L9.93 23.949a.316.316 0 0 1-.066.027.29.29 0 0 1-.033.012.38.38 0 0 1-.186 0 .29.29 0 0 1-.033-.012.316.316 0 0 1-.066-.027L.657 18.755a.378.378 0 0 1-.188-.326V2.974a.401.401 0 0 1 .014-.1.326.326 0 0 1 .025-.077.379.379 0 0 1 .05-.068L.61 2.71a.316.316 0 0 1 .067-.051L4.972.157a.378.378 0 0 1 .376 0L9.643 2.66h.014a.378.378 0 0 1 .188.326v9.81l3.76-2.164V5.482a.378.378 0 0 1 .188-.326l4.296-2.485a.378.378 0 0 1 .376 0l4.296 2.485a.378.378 0 0 1 .188.326z"/>
              </svg>
              <span>Laravel</span>
            </div>

            <div class="flex items-center gap-3">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white/60" xmlns="http://www.w3.org/2000/svg">
                <path d="M23.111 0H.889A.889.889 0 0 0 0 .889V23.11A.889.889 0 0 0 .889 24H23.11a.889.889 0 0 0 .889-.889V.889A.889.889 0 0 0 23.111 0zM12 17.636c-3.108 0-5.636-2.528-5.636-5.636S8.892 6.364 12 6.364s5.636 2.528 5.636 5.636-2.528 5.636-5.636 5.636z"/>
              </svg>
              <span>Redis</span>
            </div>

            <div class="flex items-center gap-3">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white/60" xmlns="http://www.w3.org/2000/svg">
                <path d="M13.827 0L0 7.158v9.684L13.827 24l13.827-7.158V7.158L13.827 0zm0 2.247l11.29 5.845v7.816l-11.29 5.845L2.537 15.908V8.092L13.827 2.247z"/>
              </svg>
              <span>Python</span>
            </div>

            <div class="flex items-center gap-3">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white/60" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.128 0a10.134 10.134 0 0 0-2.755.403l-.063.02A10.922 10.922 0 0 0 12 1.348a10.927 10.927 0 0 0-2.31-.925 10.133 10.133 0 0 0-2.818-.403C2.896.02 0 2.32 0 5.894c0 2.28 1.3 4.215 2.892 5.502.26.21.527.4.797.575L3.69 12l-.001.029c-.269.175-.536.365-.796.575C1.3 13.89 0 15.824 0 18.105c0 3.575 2.896 5.875 6.872 5.875 1.472 0 3.078-.37 4.613-1.268L12 22.18l.515.532c1.535.899 3.14 1.268 4.613 1.268C21.104 23.98 24 21.68 24 18.105c0-2.28-1.3-4.215-2.892-5.502a9.17 9.17 0 0 0-.796-.575L20.31 12l.001-.029c.27-.175.537-.364.797-.575C22.7 10.109 24 8.175 24 5.894 24 2.32 21.104.02 17.128 0z"/>
              </svg>
              <span>PostgreSQL</span>
            </div>

          </div>
        </div>

        <div class="flex flex-col gap-4">
          <p class="text-xl text-white/70">Contact</p>
          <div class="flex flex-col gap-3 mt-2 ml-4">

            <a href="https://github.com/Tenmazzz" target="_blank" class="flex items-center gap-3 text-white/70 hover:text-white transition cursor-pointer">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white" xmlns="http://www.w3.org/2000/svg">
                <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>GitHub</title><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
              </svg>
              <span>GitHub</span>
            </a>

            <a href="https://linkedin.com/in/rayan-khan-704791389" target="_blank" class="flex items-center gap-3 text-white/70 hover:text-white transition cursor-pointer">
              <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white" xmlns="http://www.w3.org/2000/svg">
                <svg role="img" viewBox="0 0 24 24" class="w-5 h-5 fill-white" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </svg>
              <span>LinkedIn</span>
            </a>

            <a href="mailto:rayan.pro91@gmail.com" class="flex items-center gap-3 text-white/70 hover:text-white transition cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
              </svg>

              <span>Email</span>
            </a>

          </div>
        </div>
        
      </div>

    </div>
  </footer>

</template>