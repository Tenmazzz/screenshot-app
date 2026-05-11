<template> 
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