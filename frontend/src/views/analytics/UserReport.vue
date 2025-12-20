<template>
  <div class="user-report">
    <div class="header">
      <h2>{{ reportData.user_name }} 的听歌报告</h2>
      <div class="actions">
        <el-dropdown @command="handleExport">
          <el-button type="primary">
            导出报告 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
              <el-dropdown-item command="pdf">导出 PDF</el-dropdown-item>
              <el-dropdown-item command="word">导出 Word</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <template #header>累计听歌</template>
          <div class="stat-value">{{ reportData.total_plays }} <span class="unit">首</span></div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <template #header>总听歌时长</template>
          <div class="stat-value">{{ reportData.total_duration_display }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>最常听的歌曲 Top 10</template>
          <el-table :data="reportData.top_songs" stripe style="width: 100%">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="song__song_name" label="歌曲" />
            <el-table-column prop="song__song_singer__user_name" label="歌手" />
            <el-table-column prop="play_count" label="播放次数" width="100" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>最常听的歌手 Top 5</template>
          <el-table :data="reportData.top_singers" stripe style="width: 100%">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="song__song_singer__user_name" label="歌手" />
            <el-table-column prop="play_count" label="播放次数" width="100" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header>听歌时段分布</template>
          <div ref="chartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getUserReport, exportUserReport, type UserReportData } from '@/api/analytics'

const reportData = ref<UserReportData>({
  user_name: '',
  report_date: '',
  total_plays: 0,
  total_duration_display: '',
  top_songs: [],
  top_singers: [],
  hour_distribution: []
})

const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  const hours = reportData.value.hour_distribution.map(item => item.hour + '点')
  const counts = reportData.value.hour_distribution.map(item => item.count)

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: hours,
      name: '时间'
    },
    yAxis: {
      type: 'value',
      name: '播放次数'
    },
    series: [
      {
        data: counts,
        type: 'bar',
        itemStyle: {
          color: '#409EFF'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

const fetchData = async () => {
  try {
    const res = await getUserReport()
    reportData.value = res as any
    nextTick(() => {
      initChart()
    })
  } catch (error) {
    console.error(error)
  }
}

const handleExport = async (format: 'pdf' | 'word' | 'excel') => {
  try {
    const res = await exportUserReport(format)
    // res is Blob
    const blob = new Blob([res as any], { 
      type: format === 'pdf' ? 'application/pdf' : 
            format === 'word' ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `music_report.${format === 'excel' ? 'xlsx' : format === 'word' ? 'docx' : 'pdf'}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<style scoped>
.user-report {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}
.unit {
  font-size: 14px;
  color: #666;
}
.mt-4 {
  margin-top: 20px;
}
</style>
