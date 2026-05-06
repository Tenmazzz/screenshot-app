<script setup>
    const props = defineProps({
    screenshots: Array,
    selectedScreen: Object
    })

    const emit = defineEmits(['update:selectedScreen'])
</script>

<template>
    <div class="grid grid-cols-3 gap-5 mt-8 mx-auto w-8/12">
        <div v-for="screen in screenshots" class="bg-white/5 border border-white/10 rounded-2xl overflow-hidden group transition-transform duration-200 hover:scale-110">

            <div class="aspect-video overflow-hidden bg-black/30 relative cursor-pointer" @click="screen.status === 'done' && emit('update:selectedScreen', screen)">
                <img v-if="screen.status === 'done'" :src="`/storage/${screen.file_path}`" class="w-full h-full object-cover object-top" />

                <div v-else-if="screen.status === 'pending'" class="w-full h-full flex items-center justify-center">
                <div class="w-6 h-6 border-2 border-white/20 border-t-white/60 rounded-full animate-spin"></div>
                </div>

                <div v-else class="w-full h-full flex items-center justify-center">
                <span class="text-red-400/60 text-sm">Échec</span>
                </div>

            </div>

            <div class="px-4 py-3 flex flex-col gap-1">
                <div class="flex items-center justify-between">
                <a :href="screen.url" class="text-white text-xs truncate">{{ screen.url }}</a>
                <a v-if="screen.status === 'done'" :href="`/storage/${screen.file_path}`" download class="text-white/30 hover:text-white/70 transition ml-2 shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-emerald-600">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m9 12.75 3 3m0 0 3-3m-3 3v-7.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                </a>
                </div>
                <div class="flex items-center justify-between">

                <span class="text-white/50 text-xs">{{ new Date(screen.created_at).toLocaleString('fr-FR') }}</span>
                </div>
            </div>
        </div>
  </div>


</template>

