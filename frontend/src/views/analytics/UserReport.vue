<template>
  <div class="user-report">
    <el-card shadow="hover" class="report-card">
      <template #header>
        <el-page-header @back="handleBack" :content="reportData.user_name + ' 的听歌报告'" title="返回">
          <template #extra>
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
          </template>
        </el-page-header>
      </template>

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
          <template #header>
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <span>听歌时段分布</span>
              <el-switch
                v-model="use30h"
                active-text="30h 制"
                inactive-text="24h 制"
                style="margin-left: 12px"
              />
            </div>
          </template>
          <div ref="chartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed, watch } from 'vue'
import { ArrowDown } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { getUserReport, exportUserReport, type UserReportData } from '@/api/analytics'

const router = useRouter()
const handleBack = () => {
  router.push('/mine')
}

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

const use30h = ref(false)

const chartData = computed(() => {
  const raw = reportData.value.hour_distribution // 0-23 原始数据
  if (!use30h.value) {
    // 24h 制：直接返回 0-23
    return {
      xAxis: raw.map((v) => Number(v.hour) + '时'),
      data: raw.map((v) => v.count)
    }
  }
  /* 30h 制：只保留 6-23 原始点，并把这些点映射成 6-23；
     0-5 点映射成 24-29 点，整体范围 6-29 */
  const normal = raw
    .filter((v) => +v.hour >= 6) // 去掉 0-5
    .map((v) => ({ hour: +v.hour, count: v.count }))

  const extra = raw
    .filter((v) => +v.hour <= 5) // 0-5 点
    .map((v) => ({ hour: +v.hour + 24, count: v.count })) // 变 24-29

  const merged = [...normal, ...extra] // 6-23 在前，24-29 在后
  return {
    xAxis: merged.map((v) => v.hour + '时'),
    data: merged.map((v) => v.count)
  }
})

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  const hours = reportData.value.hour_distribution.map(item => item.hour + '时')
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

const updateChart = () => {
  const dom = chartRef.value
  if (!dom) return // ① 兜底：没有容器直接返回

  if (!chartInstance) {
    chartInstance = echarts.init(dom) // ② 首次再 init
  }
  const { xAxis, data } = chartData.value
  // 颜色：24h 统一蓝色；30h 制把 24-30 设为橙色区分「次日」
  const colors = xAxis.map((h) => (h.includes('24') || h.includes('25') || h.includes('26') || h.includes('27') || h.includes('28') || h.includes('29') || h.includes('30') ? '#FF9A00' : '#409EFF'))

  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: xAxis, name: '时间' },
    yAxis: { type: 'value', name: '播放次数' },
    series: [
      {
        type: 'bar',
        data: data,
        itemStyle: {
          color: (params: { dataIndex: number }) => colors[params.dataIndex]
        }
      }
    ]
  })
}

watch(chartData, updateChart, { immediate: true })

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
    ElMessage.success('导出成功')
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
