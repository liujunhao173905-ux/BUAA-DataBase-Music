import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Song } from '@/api/music'
import { recordPlay } from '@/api/music'

export enum PlayMode {
  SEQUENCE = 0, // 顺序播放
  RANDOM = 1,   // 随机播放
  LOOP = 2      // 单曲循环
}

export const usePlayerStore = defineStore('player', () => {
  const currentSong = ref<Song | null>(null)
  const isPlaying = ref(false)
  const playlist = ref<Song[]>([])
  const currentIndex = ref(-1)
  const audio = ref<HTMLAudioElement | null>(null)
  const duration = ref(0)
  const currentTime = ref(0)
  const volume = ref(1)
  const isRecorded = ref(false)
  const playMode = ref<PlayMode>(PlayMode.SEQUENCE)

  const toggleMode = () => {
    playMode.value = (playMode.value + 1) % 3
  }

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
        // Record play history when song ends
        if (currentSong.value && duration.value > 0 && !isRecorded.value) {
          recordPlay(currentSong.value.song_id, Math.floor(duration.value)).catch(err => {
            console.error('Failed to record play history', err)
          })
          isRecorded.value = true
        }
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
    
    // if (currentSong.value?.song_id !== song.song_id) {
      // Record previous song if valid, not recorded, and played enough time (e.g. 5 seconds)
      if (currentSong.value && !isRecorded.value && currentTime.value > 5) {
        recordPlay(currentSong.value.song_id, Math.floor(currentTime.value)).catch(err => {
          console.error('Failed to record play history (switch)', err)
        })
      }

      isRecorded.value = false
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
    // } else {
    //   togglePlay()
    // }
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

  const generateRandomIndex = () => {
  let newIndex = Math.floor(Math.random() * playlist.value.length)
  while (newIndex === currentIndex.value) {
    newIndex = Math.floor(Math.random() * playlist.value.length)
  }
  return newIndex
}

  const playNext = () => {
    if (playlist.value.length === 0) return

    if (playMode.value === PlayMode.RANDOM) {
      const randomIndex = generateRandomIndex()
      playSong(playlist.value[randomIndex])
    } else if (playMode.value === PlayMode.LOOP) {
      playSong(playlist.value[currentIndex.value])
    } else {
      let nextIndex = currentIndex.value + 1
      if (nextIndex >= playlist.value.length) nextIndex = 0
      playSong(playlist.value[nextIndex])
    }
  }

  const playPrev = () => {
    if (playlist.value.length === 0) return

    if (playMode.value === PlayMode.RANDOM) {
      const randomIndex = generateRandomIndex()
      playSong(playlist.value[randomIndex])
    } else if (playMode.value === PlayMode.LOOP) {
      playSong(playlist.value[currentIndex.value])
    } else {
      let prevIndex = currentIndex.value - 1
      if (prevIndex < 0) prevIndex = playlist.value.length - 1
      playSong(playlist.value[prevIndex])
    }
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
    playMode,
    toggleMode,
    playSong,
    togglePlay,
    playNext,
    playPrev,
    setVolume,
    seek,
    setPlaylist
  }
})
