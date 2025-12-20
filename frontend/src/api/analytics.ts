import request from './request'

export interface UserReportData {
  user_name: string
  report_date: string
  total_plays: number
  total_duration_display: string
  top_songs: {
    song__song_id: number
    song__song_name: string
    song__song_singer__user_name: string
    play_count: number
  }[]
  top_singers: {
    song__song_singer__user_name: string
    play_count: number
  }[]
  hour_distribution: {
    hour: string
    count: number
  }[]
}

export const getUserReport = () => {
  return request.get<UserReportData>('/analytics/user-report/')
}

export const exportUserReport = (format: 'pdf' | 'word' | 'excel') => {
  return request.get(`/analytics/report/export/`, {
    params: { export_type: format },
    responseType: 'blob'
  })
}
