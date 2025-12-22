/**
 * 音乐相关API
 * 包含歌曲和歌单的相关操作
 */
import request from './request'

export interface Song {
  song_id: number
  song_name: string
  song_cover?: string
  song_file?: string
  song_duration: number
  song_price: number
  song_singer: number
  song_singer_name: string
  song_singer_id: number
  song_createtime: string
  song_updatetime: string
  song_status: number
  is_starred?: boolean
  is_bought?: boolean
  star_count?: number
  buy_count?: number
}

export interface Playlist {
  playlist_id: number
  playlist_name: string
  playlist_cover?: string
  playlist_intro?: string
  playlist_creator: number
  playlist_creator_name: string
  playlist_creator_id: number
  playlist_createtime: string
  playlist_updatetime: string
  playlist_status: boolean
  song_count: number
  is_starred?: boolean
  star_count?: number
  songs?: PlaylistSong[]
}

export interface PlaylistSong {
  playlist_songs_id: number
  playlist: number
  song: Song
  add_time: string
  order: number
}

// 获取歌曲列表
export const getSongs = (params?: any) => {
  return request.get<{ count: number; next: string | null; previous: string | null; results: Song[] }>('/music/songs/', { params })
}

// 获取歌曲详情
export const getSongDetail = (songId: number) => {
  return request.get<Song>(`/music/songs/${songId}/`) as unknown as Song
}

// 收藏歌曲
export const starSong = (songId: number) => {
  return request.post(`/music/songs/${songId}/star/`)
}

// 取消收藏歌曲
export const unstarSong = (songId: number) => {
  return request.delete(`/music/songs/${songId}/unstar/`)
}

// 购买歌曲
export const buySong = (songId: number) => {
  return request.post(`/music/songs/${songId}/buy/`)
}

// 获取我上传的歌曲
export const getMySongs = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: Song[] }>(`/music/songs/my_songs/`, { params: { page, page_size: pageSize } })
    .then(response => {
      return {
        data: {
          songs: response.results,
          total: response.count
        }
      }
    })
}

// 获取我购买的歌曲
export const getMyBoughtSongs = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: Song[] }>(`/music/songs/bought/`, { params: { page, page_size: pageSize } })
    .then(response => {
      return {
        data: {
          songs: response.results,
          total: response.count
        }
      }
    })
}

// 记录播放历史
export const recordPlay = (songId: number, duration: number) => {
  return request.post('/music/record-play/', { song_id: songId, duration })
}

// 导出歌曲
export const exportSongs = (format: 'excel' | 'xml', songIds?: number[]) => {
  const params: any = { export_type: format }
  if (songIds && songIds.length > 0) {
    params.song_ids = songIds.join(',')
  }
  return request.get(`/music/export/`, {
    params,
    responseType: 'blob' 
  })
}

// 导入歌曲
export const importSongs = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post(`/music/import/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 外部搜索
export const searchExternalSongs = (keyword: string) => {
  return request.get<any[]>(`/music/external/search/`, { params: { keyword } })
}

// 外部导入
export const importExternalSong = (data: any) => {
  return request.post(`/music/external/import/`, data)
}


// 获取我收藏的歌曲
export const getMyStarredSongs = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: Song[] }>(`/music/songs/starred/`, { params: { page, page_size: pageSize } })
    .then(response => {
      return {
        data: {
          songs: response.results,
          total: response.count
        }
      }
    })
}

// 上传歌曲
export const uploadSong = (formData: FormData) => {
  return request.post<Song>('/music/songs/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as unknown as Song
}

// 编辑歌曲
export const updateSong = (songId: number, formData: FormData) => {
  return request.put<Song>(`/music/songs/${songId}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as unknown as Song
}

// 删除歌曲
export const deleteSong = (songId: number) => {
  return request.delete(`/music/songs/${songId}/`)
}

// 下载歌曲
export const downloadSong = (song: Song) => {
  return request.get(`/music/songs/${song.song_id}/download/`, {
    responseType: 'blob'
  })
}

// 获取歌单列表
export const getPlaylists = (params?: any) => {
  return request.get<{ count: number; next: string | null; previous: string | null; results: Playlist[] }>('/playlists/', { params }) as unknown as { count: number; next: string | null; previous: string | null; results: Playlist[] }
}

// 获取歌单详情
export const getPlaylistDetail = (playlistId: number) => {
  return request.get<Playlist>(`/playlists/${playlistId}/`) as unknown as Playlist
}

// 推荐歌单
export const getRecommendPlaylists = () => {
  return request.get<{ data: { playlists: Playlist[] } }>('/playlists/recommend/')
}

// 推荐歌曲
export const getRecommendSongs = () => {
  return request.get<Song[]>('/music/songs/recommend/')
}

// 创建歌单
export const createPlaylist = (formData: FormData) => {
  return request.post<Playlist>('/playlists/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as unknown as Playlist
}

// 编辑歌单
export const updatePlaylist = (playlistId: number, formData: FormData) => {
  return request.put<Playlist>(`/playlists/${playlistId}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }) as unknown as Playlist
}

// 收藏歌单
export const starPlaylist = (playlistId: number) => {
  return request.post(`/playlists/${playlistId}/star/`)
}

// 取消收藏歌单
export const unstarPlaylist = (playlistId: number) => {
  return request.delete(`/playlists/${playlistId}/unstar/`)
}

// 获取我的歌单
export const getMyPlaylists = (page: number = 1, pageSize: number = 10) => {
  return request.get<{ count: number; results: Playlist[] }>(`/playlists/my_playlists/`, { params: { page, page_size: pageSize } }) as unknown as { data: { playlists: Playlist[]; total: number } }
}

// 向歌单添加歌曲
export const addSongToPlaylist = (playlistId: number, songId: number) => {
  return request.post(`/playlists/${playlistId}/add_song/`, { song_id: songId })
}

// 从歌单移除歌曲
export const removeSongFromPlaylist = (playlistId: number, songId: number) => {
  return request.delete(`/playlists/${playlistId}/remove_song/`, { data: { song_id: songId } })
}

// 删除歌单
export const deletePlaylist = (playlistId: number) => {
  return request.delete(`/playlists/${playlistId}/`)
}