<template>
    <div class="profile-container">
        <header class="header">
            <div class="header-content">
                <button @click="$router.back()" class="back-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
                    </svg>
                    返回
                </button>
                <h1>个人信息</h1>
                <div></div>
            </div>
        </header>

        <main class="main-content">
            <div class="profile-card">
                <div class="profile-header">
                    <div class="profile-background"></div>
                    <div class="profile-content">
                        <div class="avatar">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
                            </svg>
                        </div>
                        <h2>{{ profile.user?.username || '用户' }}</h2>
                        <p class="join-date">加入时间：{{ formatDate(profile.user?.date_joined) }}</p>
                        <div class="current-time">{{ currentTime }}</div>
                    </div>
                </div>

                <form @submit.prevent="updateProfile" class="profile-form">
                    <div class="form-section">
                        <h3>基本信息</h3>
                        <div class="form-row">
                            <div class="form-group">
                                <label>用户名</label>
                                <input v-model="username" type="text" readonly class="readonly-input"
                                    placeholder="未获取到用户名" />
                            </div>
                            <div class="form-group">
                                <label>出生日期</label>
                                <input v-model="profile.date_of_birth" type="date" :max="getCurrentDate()" />
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>身高 (cm)</label>
                                <input v-model.number="profile.height_cm" type="number" step="0.1" min="50" max="250"
                                    placeholder="请输入身高" />
                            </div>
                            <div class="form-group">
                                <label>体重 (kg)</label>
                                <input v-model.number="profile.weight_kg" type="number" step="0.1" min="20" max="300"
                                    placeholder="请输入体重" />
                            </div>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label>性别</label>
                                <select v-model="profile.gender">
                                    <option value="">请选择</option>
                                    <option value="male">男</option>
                                    <option value="female">女</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>年龄</label>
                                <input :value="age || ''" type="text" readonly class="readonly-input"
                                    placeholder="请先设置出生日期" />
                            </div>
                        </div>
                    </div>

                    <div class="form-section">
                        <h3>数据分享设置</h3>
                        <small style="margin-bottom: 16px; display: block;">开启后，好友可以查看您的健康数据</small>

                        <div class="form-row" >
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input v-model="profile.share_data" type="checkbox" />
                                    <span class="checkmark"></span>
                                    分享健康动态
                                </label>

                            </div>
                        </div>

                        <div v-if="profile.share_data" class="form-row">
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input v-model="profile.share_sleep" type="checkbox" />
                                    <span class="checkmark"></span>
                                    分享睡眠数据
                                </label>
                            </div>
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input v-model="profile.share_exercise" type="checkbox" />
                                    <span class="checkmark"></span>
                                    分享运动数据
                                </label>
                            </div>
                        </div>

                        <div v-if="profile.share_data" class="form-row">
                            <div class="form-group checkbox-group">
                                <label class="checkbox-label">
                                    <input v-model="profile.share_diet" type="checkbox" />
                                    <span class="checkmark"></span>
                                    分享饮食数据
                                </label>
                            </div>
                            <div class="form-group">
                                <label>分享时间范围</label>
                                <select v-model="profile.share_range">
                                    <option value="week">近一周</option>
                                    <option value="month">近一月</option>
                                    <option value="half_year">近半年</option>
                                    <option value="year">近一年</option>
                                    <option value="all">全部</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- 安全设置 -->
                    <div class="form-section">
                        <h3>安全设置</h3>
                        <div class="security-actions">
                            <button
                                @click="showPasswordModal = true"
                                class="change-password-btn"
                                type="button"
                            >
                                修改密码
                            </button>
                            <button
                                @click="showDeleteAccountModal = true"
                                class="delete-account-btn"
                                type="button"
                            >
                                注销账号
                            </button>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" :disabled="loading" class="save-btn">
                            {{ loading ? '保存中...' : '保存信息' }}
                        </button>
                    </div>
                </form>

                <!-- 健康指标卡片 -->
                <div class="health-metrics" v-if="profile.height && profile.weight">
                    <h3>健康指标</h3>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h4>BMI指数</h4>
                            <p class="metric-value">{{ bmi }}</p>
                            <span class="metric-status" :class="bmiStatus.class">{{ bmiStatus.text }}</span>
                        </div>
                        <div class="metric-card">
                            <h4>基础代谢率</h4>
                            <p class="metric-value">{{ bmr }}</p>
                            <span class="metric-unit">卡路里/天</span>
                        </div>
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

        <!-- 修改密码模态框 -->
        <div v-if="showPasswordModal" class="modal-overlay" @click.self="closePasswordModal">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>修改密码</h3>
                    <button @click="closePasswordModal" class="modal-close-btn">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                        </svg>
                    </button>
                </div>
                <form @submit.prevent="changePassword" class="password-form">
                    <div class="form-group">
                        <label>当前密码</label>
                        <input
                            v-model="passwordForm.oldPassword"
                            type="password"
                            placeholder="请输入当前密码"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label>新密码</label>
                        <input
                            v-model="passwordForm.newPassword"
                            type="password"
                            placeholder="请输入新密码（至少6位）"
                            required
                            minlength="6"
                        />
                    </div>
                    <div class="form-group">
                        <label>确认新密码</label>
                        <input
                            v-model="passwordForm.confirmPassword"
                            type="password"
                            placeholder="请再次输入新密码"
                            required
                        />
                    </div>
                    <div v-if="passwordError" class="password-error">
                        {{ passwordError }}
                    </div>
                    <div class="modal-actions">
                        <button type="button" @click="closePasswordModal" class="cancel-btn">
                            取消
                        </button>
                        <button type="submit" :disabled="passwordLoading" class="confirm-btn">
                            {{ passwordLoading ? '修改中...' : '确认修改' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- 注销账号模态框 -->
        <div v-if="showDeleteAccountModal" class="modal-overlay delete-modal" @click.self="closeDeleteAccountModal">
            <div class="modal-container">
                <div class="modal-header">
                    <h3>注销账号</h3>
                    <button @click="closeDeleteAccountModal" class="modal-close-btn">
                        <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                        </svg>
                    </button>
                </div>
                <div class="delete-account-content">
                    <div class="warning-message">
                        <svg viewBox="0 0 24 24" fill="currentColor" class="warning-icon">
                            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                        </svg>
                        <div>
                            <h4>注意：此操作不可恢复</h4>
                            <p>注销账号将永久删除您的所有数据，包括：</p>
                            <ul>
                                <li>个人信息和健康档案</li>
                                <li>所有健康记录（睡眠、运动、饮食）</li>
                                <li>好友关系和社交数据</li>
                                <li>健康报告和分析数据</li>
                            </ul>
                        </div>
                    </div>
                    <form @submit.prevent="deleteAccount" class="delete-account-form">
                        <div class="form-group">
                            <label>请输入您的密码以确认注销</label>
                            <input
                                v-model="deleteAccountForm.password"
                                type="password"
                                placeholder="请输入您的密码"
                                required
                            />
                        </div>
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input
                                    v-model="deleteAccountForm.confirmed"
                                    type="checkbox"
                                    required
                                />
                                <span class="checkmark"></span>
                                我确认要永久注销我的账号，并明白此操作不可恢复
                            </label>
                        </div>
                        <div v-if="deleteAccountError" class="delete-account-error">
                            {{ deleteAccountError }}
                        </div>
                        <div class="modal-actions">
                            <button type="button" @click="closeDeleteAccountModal" class="cancel-btn">
                                取消
                            </button>
                            <button
                                type="submit"
                                :disabled="deleteAccountLoading || !deleteAccountForm.confirmed"
                                class="delete-confirm-btn"
                            >
                                {{ deleteAccountLoading ? '注销中...' : '确认注销' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Profile',
    data() {
        return {
            profile: {
                user: null,
                date_of_birth: '',
                height_cm: null,
                weight_kg: null,
                gender: '',
                share_data: true,
                share_sleep: true,
                share_exercise: true,
                share_diet: true,
                share_range: 'week'
            },
            loading: false,
            errorMessage: '',
            successMessage: '',
            currentTime: '',
            timeTimer: null,
            // 密码修改相关
            showPasswordModal: false,
            passwordLoading: false,
            passwordError: '',
            passwordForm: {
                oldPassword: '',
                newPassword: '',
                confirmPassword: ''
            },
            // 注销账号相关
            showDeleteAccountModal: false,
            deleteAccountLoading: false,
            deleteAccountError: '',
            deleteAccountForm: {
                password: '',
                confirmed: false
            }
        };
    },
    computed: {
        username() {
            return this.$store?.state?.user?.username || localStorage.getItem('username') || '未知用户';
        },
        age() {
            if (!this.profile.date_of_birth) return null;
            const birthDate = new Date(this.profile.date_of_birth);
            const today = new Date();
            let age = today.getFullYear() - birthDate.getFullYear();
            const monthDiff = today.getMonth() - birthDate.getMonth();
            if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }
            return age;
        },
        bmi() {
            if (!this.profile.height_cm || !this.profile.weight_kg) return 0;
            const heightInM = this.profile.height_cm / 100;
            return (this.profile.weight_kg / (heightInM * heightInM)).toFixed(1);
        },
        bmiStatus() {
            const bmi = parseFloat(this.bmi);
            if (bmi < 18.5) return { text: '偏瘦', class: 'underweight' };
            if (bmi < 25) return { text: '正常', class: 'normal' };
            if (bmi < 30) return { text: '偏胖', class: 'overweight' };
            return { text: '肥胖', class: 'obese' };
        },
        bmr() {
            if (!this.profile.height_cm || !this.profile.weight_kg || !this.age || !this.profile.gender) {
                return 0;
            }

            let bmr;
            if (this.profile.gender === 'male') {
                bmr = 88.362 + (13.397 * this.profile.weight_kg) + (4.799 * this.profile.height_cm) - (5.677 * this.age);
            } else {
                bmr = 447.593 + (9.247 * this.profile.weight_kg) + (3.098 * this.profile.height_cm) - (4.330 * this.age);
            }

            return Math.round(bmr);
        }
    },
    async mounted() {
        await this.fetchProfile();
        this.updateTime();
        this.timeTimer = setInterval(this.updateTime, 1000);
    },
    beforeUnmount() {
        if (this.timeTimer) {
            clearInterval(this.timeTimer);
        }
    },
    methods: {
        async fetchProfile() {
            try {
                const response = await axios.get('/api/profile/my_profile/');
                this.profile = { ...this.profile, ...response.data };
            } catch (error) {
                console.error('获取个人信息失败：', error);
                this.errorMessage = '获取个人信息失败，请重试';
            }
        },

        async updateProfile() {
            this.loading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                const profileData = {
                    date_of_birth: this.profile.date_of_birth,
                    height_cm: this.profile.height_cm,
                    weight_kg: this.profile.weight_kg,
                    gender: this.profile.gender,
                    share_data: this.profile.share_data,
                    share_sleep: this.profile.share_sleep,
                    share_exercise: this.profile.share_exercise,
                    share_diet: this.profile.share_diet,
                    share_range: this.profile.share_range
                };

                await axios.put('/api/profile/update_profile/', profileData);
                this.successMessage = '个人信息更新成功！';

                // 3秒后清除成功提示
                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('更新个人信息失败：', error);
                if (error.response?.data) {
                    this.errorMessage = error.response.data.detail || '更新失败，请检查输入信息';
                } else {
                    this.errorMessage = '更新失败，请重试';
                }
            } finally {
                this.loading = false;
            }
        },

        formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        },

        getCurrentDate() {
            return new Date().toISOString().split('T')[0];
        },

        updateTime() {
            const now = new Date();
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                weekday: 'long'
            };
            this.currentTime = now.toLocaleDateString('zh-CN', options);
        },

        // 密码修改相关方法
        closePasswordModal() {
            this.showPasswordModal = false;
            this.passwordError = '';
            this.passwordForm = {
                oldPassword: '',
                newPassword: '',
                confirmPassword: ''
            };
        },

        async changePassword() {
            this.passwordError = '';

            // 验证新密码和确认密码是否一致
            if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
                this.passwordError = '新密码和确认密码不一致';
                return;
            }

            // 验证密码长度
            if (this.passwordForm.newPassword.length < 6) {
                this.passwordError = '新密码长度至少6位';
                return;
            }

            this.passwordLoading = true;

            try {
                await axios.post('/api/profile/change_password/', {
                    old_password: this.passwordForm.oldPassword,
                    new_password: this.passwordForm.newPassword
                });

                this.successMessage = '密码修改成功！';
                this.closePasswordModal();

                // 3秒后清除成功提示
                setTimeout(() => {
                    this.successMessage = '';
                }, 3000);

            } catch (error) {
                console.error('修改密码失败：', error);
                if (error.response?.data?.error) {
                    this.passwordError = error.response.data.error;
                } else {
                    this.passwordError = '修改密码失败，请重试';
                }
            } finally {
                this.passwordLoading = false;
            }
        },

        // 注销账号相关方法
        closeDeleteAccountModal() {
            this.showDeleteAccountModal = false;
            this.deleteAccountError = '';
            this.deleteAccountForm = {
                password: '',
                confirmed: false
            };
        },

        async deleteAccount() {
            this.deleteAccountError = '';

            if (!this.deleteAccountForm.confirmed) {
                this.deleteAccountError = '请确认您要注销账号';
                return;
            }

            if (!this.deleteAccountForm.password) {
                this.deleteAccountError = '请输入密码';
                return;
            }

            // 最后确认
            if (!confirm('这是最后的确认：您真的要永久注销您的账号吗？此操作无法撤销！')) {
                return;
            }

            this.deleteAccountLoading = true;

            try {
                await axios.post('/api/profile/delete_account/', {
                    password: this.deleteAccountForm.password
                });

                // 注销成功，清除本地数据并跳转到登录页
                localStorage.clear();
                sessionStorage.clear();

                // 显示成功消息
                alert('账号已成功注销。感谢您的使用，再见！');

                // 跳转到登录页
                this.$router.push('/login');

            } catch (error) {
                console.error('注销账号失败：', error);
                if (error.response?.data?.error) {
                    this.deleteAccountError = error.response.data.error;
                } else {
                    this.deleteAccountError = '注销失败，请重试';
                }
            } finally {
                this.deleteAccountLoading = false;
            }
        }
    }
}
</script>

<style scoped>
.profile-container {
    min-height: 100vh;
    background: #f5f7fa;
}

.header {
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
}

.back-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    background: none;
    border: none;
    color: #666;
    cursor: pointer;
    font-size: 14px;
    padding: 8px;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.back-btn:hover {
    background: #f5f7fa;
}

.back-btn svg {
    width: 20px;
    height: 20px;
}

.header h1 {
    color: #2c3e50;
    margin: 0;
    font-size: 20px;
}

.main-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px 20px;
}

.profile-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.profile-header {
    position: relative;
    text-align: center;
    padding: 0;
    border-bottom: 1px solid #e9ecef;
    overflow: hidden;
}

.profile-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    opacity: 1;
}

.profile-content {
    position: relative;
    padding: 40px 20px;
    color: white;
    z-index: 2;
}

.avatar {
    width: 80px;
    height: 80px;
    background: rgba(255, 255, 255, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    backdrop-filter: blur(10px);
}

.avatar svg {
    width: 40px;
    height: 40px;
    color: white;
}

.profile-header h2 {
    margin: 0 0 8px 0;
    font-size: 24px;
    font-weight: 600;
    color: white;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.join-date {
    margin: 8px 0;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

.current-time {
    margin-top: 12px;
    padding: 8px 16px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    color: white;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.profile-form {
    padding: 30px;
}

.form-section {
    margin-bottom: 30px;
}

.form-section h3 {
    color: #2c3e50;
    margin: 0 0 20px 0;
    font-size: 18px;
    border-bottom: 2px solid #e1e8ed;
    padding-bottom: 8px;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group label {
    color: #555;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 14px;
}

.form-group input,
.form-group select {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #409eff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.readonly-input {
    background: #f8f9fa !important;
    color: #6c757d !important;
    cursor: not-allowed !important;
}

.checkbox-group {
    flex-direction: row;
    align-items: center;
}

.checkbox-label {
    display: flex;
    align-items: center;
    cursor: pointer;
    margin: 0;
}

.checkbox-label input[type="checkbox"] {
    display: none;
}

.checkmark {
    width: 20px;
    height: 20px;
    border: 2px solid #ddd;
    border-radius: 4px;
    margin-right: 12px;
    position: relative;
    transition: all 0.3s;
}

.checkbox-label input[type="checkbox"]:checked+.checkmark {
    background: #409eff;
    border-color: #409eff;
}

.checkbox-label input[type="checkbox"]:checked+.checkmark::after {
    content: '✓';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 12px;
    font-weight: bold;
}

.form-actions {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid #e1e8ed;
}

.save-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 12px 40px;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.save-btn:hover:not(:disabled) {
    background: #367ddd;
}

.save-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.health-metrics {
    padding: 30px;
    border-top: 1px solid #e1e8ed;
    background: #f8f9fa;
}

.health-metrics h3 {
    color: #2c3e50;
    margin: 0 0 20px 0;
    font-size: 18px;
}

.metrics-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-card h4 {
    margin: 0 0 12px 0;
    color: #666;
    font-size: 14px;
    font-weight: normal;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    margin: 0 0 8px 0;
    color: #2c3e50;
}

.metric-status {
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}

.metric-status.normal {
    background: #e8f5e8;
    color: #388e3c;
}

.metric-status.underweight {
    background: #e3f2fd;
    color: #1976d2;
}

.metric-status.overweight {
    background: #fff3e0;
    color: #f57c00;
}

.metric-status.obese {
    background: #ffebee;
    color: #d32f2f;
}

.metric-unit {
    color: #999;
    font-size: 12px;
}

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
    color: #666;
    cursor: pointer;
    padding: 0;
    line-height: 1;
}

.close-btn svg {
    width: 16px;
    height: 16px;
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

@media (max-width: 768px) {
    .form-row {
        grid-template-columns: 1fr;
    }

    .metrics-grid {
        grid-template-columns: 1fr;
    }

    .main-content {
        padding: 20px 15px;
    }

    .profile-form {
        padding: 20px 15px;
    }
}

/* 安全设置样式 */
.security-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.change-password-btn {
    background: #409eff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.change-password-btn:hover {
    background: #337ecc;
}

.delete-account-btn {
    background: #f56c6c;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.3s;
}

.delete-account-btn:hover {
    background: #e25555;
}

/* 模态框样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-container {
    background: white;
    border-radius: 12px;
    width: 90%;
    max-width: 400px;
    padding: 0;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
    margin: 0;
    color: #2c3e50;
}

.modal-close-btn {
    background: none;
    border: none;
    padding: 8px;
    border-radius: 50%;
    cursor: pointer;
    color: #999;
    transition: all 0.2s;
}

.modal-close-btn:hover {
    background: #f5f5f5;
    color: #666;
}

.modal-close-btn svg {
    width: 20px;
    height: 20px;
}

.password-form {
    padding: 24px;
}

.password-error {
    color: #f56c6c;
    font-size: 14px;
    margin-bottom: 16px;
    padding: 8px 12px;
    background: #fef2f2;
    border-radius: 4px;
    border: 1px solid #fecaca;
}

.modal-actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
}

.cancel-btn {
    flex: 1;
    padding: 10px 16px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    color: #666;
    cursor: pointer;
    transition: all 0.2s;
}

.cancel-btn:hover {
    background: #f5f5f5;
}

.confirm-btn {
    flex: 1;
    padding: 10px 16px;
    border: none;
    border-radius: 6px;
    background: #409eff;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s;
}

.confirm-btn:hover:not(:disabled) {
    background: #337ecc;
}

.confirm-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* 注销账号模态框样式 */
.delete-modal .modal-content {
    max-width: 500px;
}

.warning-message {
    background: #fef0f0;
    border: 1px solid #fbc4c4;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.warning-icon {
    width: 24px;
    height: 24px;
    color: #f56c6c;
    flex-shrink: 0;
    margin-top: 2px;
}

.warning-message div h4 {
    color: #f56c6c;
    margin: 0 0 8px 0;
    font-size: 16px;
    font-weight: 600;
}

.warning-message div p {
    color: #606266;
    margin: 0 0 12px 0;
    line-height: 1.5;
}

.warning-message div ul {
    margin: 0;
    padding-left: 20px;
    color: #606266;
}

.warning-message div ul li {
    margin-bottom: 6px;
    line-height: 1.4;
}

.delete-account-content {
    padding: 0;
}

.delete-account-form {
    margin-top: 8px;
}

.delete-account-form .form-group {
    margin-bottom: 20px;
}

.delete-account-form .form-group label {
    display: block;
    margin-bottom: 8px;
    color: #303133;
    font-weight: 500;
}

.delete-account-form .checkbox-label {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    cursor: pointer;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 6px;
    border: 1px solid #e9ecef;
    transition: all 0.2s;
}

.delete-account-form .checkbox-label:hover {
    background: #e9ecef;
}

.delete-account-form .checkbox-label input[type="checkbox"] {
    display: none;
}

.delete-account-form .checkmark {
    width: 18px;
    height: 18px;
    border: 2px solid #ddd;
    border-radius: 4px;
    position: relative;
    flex-shrink: 0;
    margin-top: 2px;
    transition: all 0.3s;
}

.delete-account-form .checkbox-label input[type="checkbox"]:checked + .checkmark {
    background: #f56c6c;
    border-color: #f56c6c;
}

.delete-account-form .checkbox-label input[type="checkbox"]:checked + .checkmark::after {
    content: '✓';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 12px;
    font-weight: bold;
}

.delete-account-error {
    background: #fef0f0;
    border: 1px solid #fbc4c4;
    color: #f56c6c;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 14px;
}

.delete-confirm-btn {
    flex: 1;
    padding: 12px 16px;
    border: none;
    border-radius: 6px;
    background: #f56c6c;
    color: white;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.delete-confirm-btn:hover:not(:disabled) {
    background: #e25555;
}

.delete-confirm-btn:disabled {
    background: #f5f5f5;
    color: #c0c4cc;
    cursor: not-allowed;
}

.confirmation-checks {
    margin: 20px 0;
}

.checkbox-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 12px;
    gap: 8px;
}

.checkbox-item input[type="checkbox"] {
    margin-top: 2px;
    flex-shrink: 0;
}

.checkbox-item label {
    color: #606266;
    font-size: 14px;
    line-height: 1.4;
    cursor: pointer;
}

.delete-modal .form-group input {
    border: 1px solid #dcdfe6;
}

.delete-modal .btn-danger {
    background: #f56c6c;
}

.delete-modal .btn-danger:hover:not(:disabled) {
    background: #e25555;
}

.delete-modal .btn-danger:disabled {
    background: #f5f5f5;
    color: #c0c4cc;
    cursor: not-allowed;
}
</style>