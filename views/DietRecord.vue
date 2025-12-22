<template>
    <div class="diet-record-container">
        <!-- 顶部导航栏 -->
        <header class="report-header">
            <h1>
                <svg viewBox="0 0 24 24" fill="currentColor" class="header-icon">
                    <path d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z"/>
                </svg>
                饮食记录
            </h1>
            <button @click="$router.push('/dashboard')" class="back-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.42-1.41L7.83 13H20v-2z"/>
                </svg>
                返回首页
            </button>
        </header>

        <main class="main-content">
            <!-- 记录表单 -->
            <div class="record-form-card">
                <h2>
                    <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                        <path
                            d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                    </svg>
                    记录今日饮食
                </h2>

                <form @submit.prevent="submitDiet" class="diet-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label>食物名称</label>
                            <input v-model="dietData.food_name" type="text" required placeholder="请输入食物名称"
                                @input="searchFood" />
                            <!-- 食物建议列表 -->
                            <div v-if="foodSuggestions.length > 0" class="suggestions-list">
                                <div v-for="food in foodSuggestions" :key="food.name" @click="selectFood(food)"
                                    class="suggestion-item">
                                    <span class="food-name">{{ food.name }}</span>
                                    <span class="food-calories">{{ food.calories }}卡/100g</span>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>记录日期</label>
                            <input v-model="dietData.record_date" type="date" required :max="getCurrentDate()" />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>餐次</label>
                            <select v-model="dietData.meal_type" required>
                                <option value="">请选择餐次</option>
                                <option value="breakfast">早餐</option>
                                <option value="lunch">午餐</option>
                                <option value="dinner">晚餐</option>
                                <option value="snack">零食</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>食物重量/份量</label>
                            <input v-model="dietData.quantity" type="text" placeholder="如：100g、1碗、2片等"
                                @input="clearPreview" />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <button type="button" @click="previewNutrition" :disabled="!dietData.food_name"
                                class="preview-btn">
                                预览营养信息
                            </button>
                        </div>
                        <div class="form-group">
                            <div class="manual-input-toggle">
                                <input type="checkbox" id="manualInput" v-model="useManualInput" @change="toggleManualInput" />
                                <label for="manualInput">手动输入营养信息</label>
                            </div>
                        </div>
                    </div>

                    <!-- 手动营养输入区域 -->
                    <div v-if="useManualInput" class="manual-nutrition-section">
                        <h3>手动输入营养信息</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label>热量（卡路里）</label>
                                <input v-model.number="dietData.calories" type="number" min="0" step="0.1"
                                    placeholder="输入热量" />
                            </div>
                            <div class="form-group">
                                <label>蛋白质（克）</label>
                                <input v-model.number="dietData.protein" type="number" min="0" step="0.1"
                                    placeholder="输入蛋白质" />
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>碳水化合物（克）</label>
                                <input v-model.number="dietData.carbs" type="number" min="0" step="0.1"
                                    placeholder="输入碳水化合物" />
                            </div>
                            <div class="form-group">
                                <label>脂肪（克）</label>
                                <input v-model.number="dietData.fat" type="number" min="0" step="0.1"
                                    placeholder="输入脂肪" />
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label>纤维（克）</label>
                                <input v-model.number="dietData.fiber" type="number" min="0" step="0.1"
                                    placeholder="输入纤维" />
                            </div>
                            <div class="form-group">
                                <!-- 空格保持对称 -->
                            </div>
                        </div>
                    </div>

                    <!-- 营养信息预览 -->
                    <div class="nutrition-preview" v-if="nutritionPreview && !useManualInput">
                        <h3>营养信息预览</h3>
                        <div class="nutrition-grid">
                            <div class="nutrition-item">
                                <label>热量</label>
                                <span>{{ nutritionPreview.calories }} 卡路里</span>
                            </div>
                            <div class="nutrition-item">
                                <label>蛋白质</label>
                                <span>{{ nutritionPreview.protein }} g</span>
                            </div>
                            <div class="nutrition-item">
                                <label>碳水化合物</label>
                                <span>{{ nutritionPreview.carbs }} g</span>
                            </div>
                            <div class="nutrition-item">
                                <label>脂肪</label>
                                <span>{{ nutritionPreview.fat }} g</span>
                            </div>
                            <div class="nutrition-item">
                                <label>纤维</label>
                                <span>{{ nutritionPreview.fiber }} g</span>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>备注（可选）</label>
                        <textarea v-model="dietData.notes" placeholder="记录烹饪方式、口感或其他相关信息..." rows="3"></textarea>
                    </div>

                    <div class="form-actions">
                        <button v-if="isEditMode" type="button" @click="cancelEdit" class="cancel-btn">
                            取消编辑
                        </button>
                        <button type="submit" :disabled="loading" class="submit-btn">
                            {{ loading ? '保存中...' : (isEditMode ? '更新饮食记录' : '保存饮食记录') }}
                        </button>
                    </div>
                </form>
            </div>

            <!-- 历史记录 -->
            <div class="history-card">
                <div class="history-header">
                    <h2>
                        <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                            <path
                                d="M13 3c-4.97 0-9 4.03-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42C8.27 19.99 10.51 21 13 21c4.97 0 9-4.03 9-9s-4.03-9-9-9zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z" />
                        </svg>
                        最近饮食记录
                    </h2>
                    <button @click="showAllHistory" class="view-all-btn">
                        查看全部
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </div>

                <div v-if="loading" class="loading">
                    <p>加载中...</p>
                </div>

                <div v-else-if="dietHistory.length === 0" class="no-data">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path
                            d="M18.06 22.99h1.66c.84 0 1.53-.64 1.63-1.46L23 5.05h-5V1h-1.97v4.05h-4.97l.3 2.34c1.71.47 3.31 1.32 4.27 2.26 1.44 1.42 2.43 2.89 2.43 5.29v8.05zM1 21.99V21h15.03v.99c0 .55-.45 1-1.01 1H2.01c-.56 0-1.01-.45-1.01-1zm15.03-7c0-8-15.03-8-15.03 0h15.03zM1.02 17h15v2h-15z" />
                    </svg>
                    <p>暂无饮食记录</p>
                </div>

                <div v-else class="history-list">
                    <div v-for="record in dietHistory.slice(0, 7)" :key="record.id" class="history-item">
                        <div class="record-date">
                            <span class="date-text">{{ formatDate(record.record_date) }}</span>
                            <span class="weekday">{{ getWeekday(record.record_date) }}</span>
                        </div>

                        <div class="record-details">
                            <div class="food-info">
                                <span class="food-name">{{ record.food_name }}</span>
                                <span class="meal-type">{{ getMealTypeName(record.meal_type) }}</span>
                            </div>
                            <div class="nutrition-info">
                                <span class="calories">{{ Math.round(record.calories) }}卡路里</span>
                                <span class="protein">{{ Math.round(record.protein) }}g蛋白质</span>
                                <span class="carbs">{{ Math.round(record.carbs) }}g碳水</span>
                                <span class="fat">{{ Math.round(record.fat) }}g脂肪</span>
                                <span v-if="record.quantity" class="quantity">{{ record.quantity }}</span>
                            </div>
                            <div v-if="record.notes" class="record-notes">{{ record.notes }}</div>
                        </div>

                        <div class="record-actions">
                            <button @click="editRecord(record)" class="edit-btn" title="编辑">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                                </svg>
                            </button>
                            <button @click="deleteRecord(record.id)" class="delete-btn" title="删除">
                                <svg viewBox="0 0 24 24" fill="currentColor">
                                    <path
                                        d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 饮食统计 -->
            <div class="stats-card">
                <h2>
                    <svg viewBox="0 0 24 24" fill="currentColor" class="section-icon">
                        <path
                            d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z" />
                    </svg>
                    本周饮食统计
                </h2>

                <div class="stats-grid">
                    <div class="stat-item">
                        <h3>总摄入热量</h3>
                        <p class="stat-value">{{ weeklyStats.totalCalories }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总蛋白质</h3>
                        <p class="stat-value">{{ weeklyStats.totalProtein }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总碳水化合物</h3>
                        <p class="stat-value">{{ weeklyStats.totalCarbs }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总脂肪</h3>
                        <p class="stat-value">{{ weeklyStats.totalFat }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>总纤维</h3>
                        <p class="stat-value">{{ weeklyStats.totalFiber }}</p>
                    </div>
                    <div class="stat-item">
                        <h3>记录天数</h3>
                        <p class="stat-value">{{ weeklyStats.recordDays }}</p>
                    </div>
                </div>
            </div>
        </main>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-message">
            <span>{{ errorMessage }}</span>
            <button @click="errorMessage = ''" class="close-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </button>
        </div>

        <!-- 成功提示 -->
        <div v-if="successMessage" class="success-message">
            <span>{{ successMessage }}</span>
            <button @click="successMessage = ''" class="close-btn">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
            </button>
        </div>

        <!-- 历史记录管理弹窗 -->
        <HistoryManager
            :visible="showHistoryManager"
            recordType="diet"
            @close="showHistoryManager = false"
            @edit="handleEditFromHistory"
            @deleted="handleRecordDeleted"
            @error="handleError"
        />
    </div>
</template>

<script>
import axios from 'axios';
import HistoryManager from '../components/HistoryManager.vue';

export default {
    name: 'DietRecord',
    components: {
        HistoryManager
    },
    data() {
        return {
            dietData: {
                food_name: '',
                meal_type: 'breakfast',
                quantity: '',
                record_date: '',
                calories: null,
                protein: null,
                carbs: null,
                fat: null,
                fiber: null,
                notes: ''
            },
            nutritionPreview: null,
            dietHistory: [],
            foodSuggestions: [],
            loading: false,
            errorMessage: '',
            successMessage: '',
            // 编辑模式状态管理
            isEditMode: false,
            editingRecordId: null,
            searchTimeout: null,
            useManualInput: false,
            // 常见食物数据库
            commonFoods: [
                '米饭', '面条', '馒头', '包子', '饺子', '粥',
                '鸡蛋', '牛奶', '豆浆', '酸奶', '面包', '饼干',
                '苹果', '香蕉', '橙子', '葡萄', '草莓', '西瓜',
                '鸡胸肉', '牛肉', '猪肉', '鱼肉', '虾', '蟹',
                '豆腐', '青菜', '胡萝卜', '土豆', '西红柿', '黄瓜'
            ],
            showHistoryManager: false
        };
    },
    computed: {
        weeklyStats() {
            if (this.dietHistory.length === 0) {
                return {
                    totalCalories: '0卡路里',
                    totalProtein: '0g',
                    totalCarbs: '0g',
                    totalFat: '0g',
                    totalFiber: '0g',
                    recordDays: '0天'
                };
            }

            // 获取本周的开始（周一）和结束（周日）
            const today = new Date();
            const dayOfWeek = today.getDay(); // 0是周日，1-6是周一到周六
            const daysSinceMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

            const weekStart = new Date(today);
            weekStart.setDate(today.getDate() - daysSinceMonday);
            weekStart.setHours(0, 0, 0, 0);

            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekStart.getDate() + 6);
            weekEnd.setHours(23, 59, 59, 999);

            // 过滤本周的记录（周一到周日）
            const weeklyRecords = this.dietHistory.filter(record => {
                const recordDate = new Date(record.record_date);
                return recordDate >= weekStart && recordDate <= weekEnd;
            });

            if (weeklyRecords.length === 0) {
                return {
                    totalCalories: '0卡路里',
                    totalProtein: '0g',
                    totalCarbs: '0g',
                    totalFat: '0g',
                    totalFiber: '0g',
                    recordDays: '0天'
                };
            }

            const totalCalories = weeklyRecords.reduce((sum, record) => sum + (record.calories || 0), 0);
            const totalProtein = weeklyRecords.reduce((sum, record) => sum + (record.protein || 0), 0);
            const totalCarbs = weeklyRecords.reduce((sum, record) => sum + (record.carbs || 0), 0);
            const totalFat = weeklyRecords.reduce((sum, record) => sum + (record.fat || 0), 0);
            const totalFiber = weeklyRecords.reduce((sum, record) => sum + (record.fiber || 0), 0);

            // 计算不同日期的天数
            const uniqueDates = new Set(weeklyRecords.map(record => record.record_date));
            const recordDays = uniqueDates.size;

            return {
                totalCalories: `${Math.round(totalCalories)}卡路里`,
                totalProtein: `${Math.round(totalProtein)}g`,
                totalCarbs: `${Math.round(totalCarbs)}g`,
                totalFat: `${Math.round(totalFat)}g`,
                totalFiber: `${Math.round(totalFiber)}g`,
                recordDays: `${recordDays}天`
            };
        }
    },
    async mounted() {
        this.dietData.record_date = this.getCurrentDate();
        await this.fetchDietHistory();
    },
    methods: {
        getCurrentDate() {
            return new Date().toISOString().split('T')[0];
        },

        async fetchDietHistory() {
            try {
                const response = await axios.get('/api/diet/');
                this.dietHistory = response.data.results || response.data;
            } catch (error) {
                console.error('获取饮食历史失败：', error);
            }
        },

        getDefaultCalories(foodName) {
            const foodCalories = {
                '米饭': 116, '面条': 109, '馒头': 221, '包子': 227, '饺子': 240, '粥': 46,
                '鸡蛋': 155, '牛奶': 54, '豆浆': 14, '酸奶': 72, '面包': 312, '饼干': 433,
                '苹果': 52, '香蕉': 89, '橙子': 43, '葡萄': 69, '草莓': 30, '西瓜': 25,
                '鸡胸肉': 133, '牛肉': 125, '猪肉': 143, '鱼肉': 104, '虾': 81, '蟹': 103,
                '豆腐': 81, '青菜': 15, '胡萝卜': 25, '土豆': 81, '西红柿': 15, '黄瓜': 15
            };
            return foodCalories[foodName] || 0;
        },

        searchFood() {
            // 清除之前的搜索定时器
            if (this.searchTimeout) {
                clearTimeout(this.searchTimeout);
            }

            // 设置新的搜索定时器，避免频繁搜索
            this.searchTimeout = setTimeout(() => {
                const query = this.dietData.food_name.toLowerCase();
                if (query.length >= 1) {
                    this.foodSuggestions = this.commonFoods
                        .filter(food => food.toLowerCase().includes(query))
                        .map(food => ({
                            name: food,
                            calories: this.getDefaultCalories(food)
                        }))
                        .slice(0, 5);
                } else {
                    this.foodSuggestions = [];
                }
            }, 300);
        },

        selectFood(food) {
            this.dietData.food_name = food.name;
            this.foodSuggestions = [];
        },

        async previewNutrition() {
            if (!this.dietData.food_name) {
                this.errorMessage = '请填写食物名称';
                return;
            }

            this.loading = true;
            this.errorMessage = '';

            try {
                const response = await axios.post('/api/diet/calculate_nutrition/', {
                    food_name: this.dietData.food_name,
                    quantity: this.dietData.quantity
                });

                this.nutritionPreview = response.data;

            } catch (error) {
                console.error('获取营养信息失败：', error);
                if (error.response?.data?.detail) {
                    this.errorMessage = error.response.data.detail;
                } else {
                    this.errorMessage = '获取营养信息失败，请重试';
                }
            } finally {
                this.loading = false;
            }
        },

        clearPreview() {
            this.nutritionPreview = null;
        },

        toggleManualInput() {
            if (this.useManualInput) {
                // 切换到手动输入时，清除预览
                this.nutritionPreview = null;
            } else {
                // 切换到自动计算时，清除手动输入的数据
                this.dietData.calories = null;
                this.dietData.protein = null;
                this.dietData.carbs = null;
                this.dietData.fat = null;
                this.dietData.fiber = null;
            }
        },

        async submitDiet() {
            if (!this.dietData.food_name || !this.dietData.meal_type) {
                this.errorMessage = '请填写食物名称和餐次';
                return;
            }

            // 如果使用手动输入，至少需要输入热量
            if (this.useManualInput && (this.dietData.calories === null || this.dietData.calories === '')) {
                this.errorMessage = '使用手动输入时，至少需要填写热量信息';
                return;
            }

            this.loading = true;
            this.errorMessage = '';

            try {
                if (this.isEditMode && this.editingRecordId) {
                    // 编辑模式：更新现有记录
                    await axios.put(`/api/diet/${this.editingRecordId}/`, this.dietData);
                    this.successMessage = '饮食记录更新成功！';
                } else {
                    // 新增模式：创建新记录
                    await axios.post('/api/diet/', this.dietData);
                    this.successMessage = '饮食记录保存成功！';
                }

                // 重置表单和编辑状态
                this.resetForm();

                // 刷新历史记录
                await this.fetchDietHistory();

                // 清除成功提示
                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('保存饮食记录失败：', error);
                if (error.response?.data?.detail) {
                    this.errorMessage = error.response.data.detail;
                } else {
                    this.errorMessage = '保存失败，请重试';
                }
            } finally {
                this.loading = false;
            }
        },

        async deleteRecord(recordId) {
            if (!confirm('确定要删除这条饮食记录吗？')) return;

            try {
                await axios.delete(`/api/diet/${recordId}/`);
                this.successMessage = '记录删除成功！';
                await this.fetchDietHistory();

                setTimeout(() => {
                    this.successMessage = '';
                }, 2000);
            } catch (error) {
                console.error('删除记录失败：', error);
                this.errorMessage = '删除失败，请重试';
            }
        },

        editRecord(record) {
            // 设置编辑模式
            this.isEditMode = true;
            this.editingRecordId = record.id;

            // 填充表单数据
            this.dietData = {
                food_name: record.food_name,
                record_date: record.record_date,
                meal_type: record.meal_type,
                quantity: record.quantity || '',
                calories: record.calories,
                protein: record.protein,
                carbs: record.carbs,
                fat: record.fat,
                fiber: record.fiber,
                notes: record.notes || ''
            };

            // 设置营养预览（显示当前营养信息）
            this.nutritionPreview = {
                calories: record.calories,
                protein: record.protein,
                carbs: record.carbs,
                fat: record.fat,
                fiber: record.fiber
            };

            // 如果有营养信息，表示原来是通过API获取的，不是手动输入
            this.useManualInput = false;

            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        resetForm() {
            // 重置表单数据
            this.dietData = {
                food_name: '',
                record_date: this.getCurrentDate(),
                meal_type: 'breakfast',
                quantity: '',
                calories: null,
                protein: null,
                carbs: null,
                fat: null,
                fiber: null,
                notes: ''
            };
            // 重置编辑状态
            this.isEditMode = false;
            this.editingRecordId = null;
            // 重置其他状态
            this.nutritionPreview = null;
            this.useManualInput = false;
        },

        cancelEdit() {
            this.resetForm();
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);

            if (date.toDateString() === today.toDateString()) {
                return '今天';
            } else if (date.toDateString() === yesterday.toDateString()) {
                return '昨天';
            } else {
                return date.toLocaleDateString('zh-CN', {
                    month: 'numeric',
                    day: 'numeric'
                });
            }
        },

        getWeekday(dateString) {
            const date = new Date(dateString);
            const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
            return weekdays[date.getDay()];
        },

        getMealTypeName(mealType) {
            const mealNames = {
                breakfast: '早餐',
                lunch: '午餐',
                dinner: '晚餐',
                snack: '零食'
            };
            return mealNames[mealType] || mealType;
        },

        // 历史记录管理相关方法
        showAllHistory() {
            this.showHistoryManager = true;
        },

        handleEditFromHistory(record) {
            // 填充表单数据进行编辑
            this.dietData = {
                food_name: record.food_name,
                meal_type: record.meal_type,
                quantity: record.quantity || '',
                record_date: record.record_date,
                calories: record.calories,
                protein: record.protein,
                carbs: record.carbs,
                fat: record.fat,
                fiber: record.fiber,
                notes: record.notes || ''
            };
            this.isEditMode = true;
            this.editingRecordId = record.id;
            this.useManualInput = true; // 编辑时使用手动输入模式
            // 滚动到表单顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        },

        handleRecordDeleted(recordId) {
            // 从本地历史记录中移除已删除的记录
            this.dietHistory = this.dietHistory.filter(record => record.id !== recordId);
            this.successMessage = '记录已删除';
            setTimeout(() => {
                this.successMessage = '';
            }, 3000);
        },

        handleError(message) {
            this.errorMessage = message;
            setTimeout(() => {
                this.errorMessage = '';
            }, 5000);
        }
    }
};
</script>

<style scoped>
.diet-record-container {
    min-height: 100vh;
    background: #f5f7fa;
}

/* 头部样式 */
.report-header {
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.report-header h1 {
    margin: 0;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
}

.header-icon {
    width: 28px;
    height: 28px;
    color: #e67e22; /* 橙色 - 饮食相关 */
}

.back-btn {
    background: #e67e22;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    transition: background-color 0.3s;
}

.back-btn:hover {
    background: #d35400;
}

.back-btn svg {
    width: 16px;
    height: 16px;
}

/* 主要内容样式 */
.main-content {
    max-width: 1000px;
    margin: 0 auto;
    padding: 30px 20px;
    display: grid;
    gap: 30px;
    grid-template-columns: 1fr 1fr;
}

.record-form-card {
    grid-column: 1 / -1;
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-card,
.stats-card {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.history-header h2 {
    margin: 0;
}

.view-all-btn {
    background: #e67e22;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.view-all-btn:hover {
    background: #d35400;
}

.view-all-btn svg {
    width: 14px;
    height: 14px;
}

.record-form-card h2,
.history-card h2,
.stats-card h2 {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 0 0 24px 0;
    color: #2c3e50;
    font-size: 18px;
}

.section-icon {
    width: 20px;
    height: 20px;
    color: #e67e22;
}

/* 表单样式 */
.diet-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    font-weight: 600;
    color: #555;
    font-size: 14px;
    margin-bottom: 8px;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s;
    box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #e67e22;
    box-shadow: 0 0 0 2px rgba(230, 126, 34, 0.2);
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

/* 建议列表样式 */
.suggestions-list {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 6px 6px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.suggestion-item {
    padding: 10px 12px;
    cursor: pointer;
    transition: background-color 0.2s;
    border-bottom: 1px solid #f0f0f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.suggestion-item:hover {
    background: #f5f5f5;
}

.suggestion-item:last-child {
    border-bottom: none;
}

.food-name {
    font-weight: 500;
}

.food-calories {
    color: #6b7280;
    font-size: 12px;
}

/* 预览按钮样式 */
.preview-btn {
    background: #4caf50;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
    width: 100%;
}

.preview-btn:hover:not(:disabled) {
    background: #45a049;
}

.preview-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

/* 手动输入切换开关 */
.manual-input-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
}

.manual-input-toggle input[type="checkbox"] {
    width: auto;
    padding: 0;
    margin: 0;
}

/* 手动营养输入区域 */
.manual-nutrition-section {
    background: #fff8e1;
    border: 1px solid #ffcc02;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.manual-nutrition-section h3 {
    margin: 0 0 15px 0;
    color: #f57c00;
    font-size: 16px;
}

/* 营养信息预览样式 */
.nutrition-preview {
    background: #f1f8e9;
    border: 1px solid #c8e6c9;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.nutrition-preview h3 {
    margin: 0 0 15px 0;
    color: #2e7d32;
    font-size: 16px;
}

.nutrition-preview .nutrition-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 15px;
}

.nutrition-preview .nutrition-item {
    text-align: center;
    padding: 10px;
    background: white;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
}

.nutrition-preview .nutrition-item label {
    display: block;
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 5px;
}

.nutrition-preview .nutrition-item span {
    font-weight: bold;
    color: #1f2937;
}

/* 表单操作按钮样式 */
.form-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}

.submit-btn {
    background: #e67e22;
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
    flex: 1;
}

.submit-btn:hover:not(:disabled) {
    background: #d35400;
}

.submit-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.cancel-btn {
    padding: 14px 20px;
    background: #f5f5f5;
    color: #666;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cancel-btn:hover {
    background: #e9e9e9;
    border-color: #ccc;
}

/* 消息样式 */
.error-message,
.success-message {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    font-size: 14px;
    z-index: 1000;
    animation: slideIn 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
}

.error-message {
    background: #ffebee;
    color: #d32f2f;
    border: 1px solid #ffcdd2;
}

.success-message {
    background: #e8f5e8;
    color: #388e3c;
    border: 1px solid #c8e6c9;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    margin: 0;
    line-height: 1;
}

.close-btn svg {
    width: 16px;
    height: 16px;
    color: #666;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }

    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* 历史记录样式 */
.loading,
.no-data {
    text-align: center;
    padding: 40px;
    color: #666;
}

.no-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.no-data svg {
    width: 48px;
    height: 48px;
    opacity: 0.5;
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.history-item {
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 16px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 16px;
    align-items: center;
    transition: box-shadow 0.3s;
}

.history-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.record-date {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 60px;
}

.date-text {
    font-weight: bold;
    color: #2c3e50;
}

.weekday {
    font-size: 12px;
    color: #666;
}

.record-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.food-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.food-name {
    font-weight: bold;
    color: #2c3e50;
}

.meal-type {
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    background: #e8f5e8;
    color: #2e7d32;
}

.nutrition-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    flex-wrap: wrap;
}

.calories {
    color: #4caf50;
    font-weight: bold;
}

.protein {
    color: #2196f3;
    font-size: 11px;
}

.carbs {
    color: #ff9800;
    font-size: 11px;
}

.fat {
    color: #9c27b0;
    font-size: 11px;
}

.quantity {
    color: #666;
    font-size: 11px;
}

.record-notes {
    font-size: 12px;
    color: #666;
    font-style: italic;
}

.record-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}

.edit-btn,
.delete-btn {
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s;
}

.edit-btn {
    background: #e8f5e8;
    color: #27ae60;
}

.edit-btn:hover {
    background: #d4edd4;
}

.delete-btn {
    background: #ffebee;
    color: #f56c6c;
}

.delete-btn:hover {
    background: #ffcdd2;
}

.edit-btn svg,
.delete-btn svg {
    width: 16px;
    height: 16px;
}

/* 统计卡片样式 */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.stat-item {
    text-align: center;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 8px;
}

.stat-item h3 {
    margin: 0 0 8px 0;
    color: #666;
    font-size: 12px;
    font-weight: normal;
}

.stat-value {
    font-size: 18px;
    font-weight: bold;
    margin: 0;
    color: #2c3e50;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-content {
        grid-template-columns: 1fr;
        padding: 20px 15px;
    }

    .record-form-card,
    .history-card,
    .stats-card {
        padding: 20px 15px;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .header-content {
        padding: 0 15px;
    }

    .history-item {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .stat-item {
        padding: 12px;
    }

    .stat-item h3 {
        font-size: 11px;
    }

    .stat-value {
        font-size: 14px;
    }

    .food-info,
    .nutrition-info {
        flex-direction: column;
        gap: 8px;
        align-items: flex-start;
    }
}
</style>
