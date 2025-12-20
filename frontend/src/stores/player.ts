import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Song } from '@/api/music'

export const usePlayerStore = defineStore('player', () => {
  const currentSong = ref<Song | null>(null)
  const isPlaying = ref(false)
  const playlist = ref<Song[]>([])
  const currentIndex = ref(-1)
  const audio = ref<HTMLAudioElement | null>(null)
  const duration = ref(0)
  const currentTime = ref(0)
  const volume = ref(1)

  const initAudio = () => {
    if (!audio.value) {
      audio.value = new Audio()
      audio.value.addEventListener('timeupdate', () => {
        if (audio.value) currentTime.value = audio.value.currentTime
      })
      audio.value.addEventListener('loadedmetadata', () => {
        if (audio.value) duration.value = audio.value.duration
      })
      audio.value.addEventListener('ended', () => {
        playNext()
      })
    }
  }

  const setPlaylist = (songs: Song[]) => {
    playlist.value = [...songs]
    // If current song is in the new playlist, update index
    if (currentSong.value) {
      const index = playlist.value.findIndex(s => s.song_id === currentSong.value?.song_id)
      currentIndex.value = index
    }
  }

  const playSong = (song: Song) => {
    if (!audio.value) initAudio()
    
    if (currentSong.value?.song_id !== song.song_id) {
      currentSong.value = song
      // Update currentIndex if song is in playlist
      const index = playlist.value.findIndex(s => s.song_id === song.song_id)
      currentIndex.value = index

      if (audio.value) {
        audio.value.src = song.song_file || ''
        audio.value.play().then(() => {
          isPlaying.value = true
        }).catch(e => {
          console.error('Play error:', e)
          isPlaying.value = false
        })
      }
    } else {
      togglePlay()
    }
  }

  const togglePlay = () => {
    if (!audio.value) return
    if (isPlaying.value) {
      audio.value.pause()
      isPlaying.value = false
    } else {
      audio.value.play()
      isPlaying.value = true
    }
  }

  const playNext = () => {
    if (playlist.value.length === 0) return
    
    let nextIndex = currentIndex.value + 1
    if (nextIndex >= playlist.value.length) {
      nextIndex = 0 // Loop to start
    }
    const nextSong = playlist.value[nextIndex]
    playSong(nextSong)
  }

  const playPrev = () => {
    if (playlist.value.length === 0) return

    let prevIndex = currentIndex.value - 1
    if (prevIndex < 0) {
      prevIndex = playlist.value.length - 1 // Loop to end
    }
    const prevSong = playlist.value[prevIndex]
    playSong(prevSong)
  }

  const setVolume = (val: number) => {
    volume.value = val
    if (audio.value) audio.value.volume = val
  }

  const seek = (time: number) => {
    if (audio.value) {
      audio.value.currentTime = time
      currentTime.value = time
    }
  }

  return {
    currentSong,
    isPlaying,
    playlist,
    currentTime,
    duration,
    volume,
    playSong,
    togglePlay,
    playNext,
    playPrev,
    setVolume,
    seek,
    setPlaylist
  }
})
