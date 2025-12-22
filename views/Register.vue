<template>
  <div class="auth-wrapper">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-shape shape-4"></div>
    </div>

    <div class="register-container">
      <!-- 品牌区域 -->
      <div class="brand-section">
        <div class="logo-container">
          <div class="health-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,21.35L10.55,20.03C5.4,15.36 2,12.27 2,8.5C2,5.41 4.42,3 7.5,3C9.24,3 10.91,3.81 12,5.08C13.09,3.81 14.76,3 16.5,3C19.58,3 22,5.41 22,8.5C22,12.27 18.6,15.36 13.45,20.03L12,21.35Z"/>
            </svg>
          </div>
          <h1 class="brand-title">加入健康管理</h1>
          <p class="brand-subtitle">开启您的健康生活之旅</p>
        </div>
      </div>

      <!-- 注册表单区域 -->
      <div class="form-section">
        <div class="form-header">
          <h2>创建新账户</h2>
          <p>只需几步即可开始您的健康管理</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <div class="input-wrapper">
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z"/>
                </svg>
              </div>
              <input
                v-model="username"
                type="text"
                required
                placeholder="请输入用户名"
                class="form-input"
                :class="{ 'input-error': usernameError }"
                @blur="validateUsername"
              />
              <div v-if="usernameValid" class="input-status success">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M10,17L5,12L6.41,10.58L10,14.17L17.59,6.58L19,8M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2Z"/>
                </svg>
              </div>
            </div>
            <div v-if="usernameError" class="field-error">{{ usernameError }}</div>
            <div v-else-if="username.length > 0" class="field-hint">用户名长度: {{ username.length }} 字符</div>
          </div>

          <div class="form-group">
            <div class="input-wrapper">
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z"/>
                </svg>
              </div>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="请输入密码"
                class="form-input"
                :class="{ 'input-error': passwordError }"
                @input="validatePassword"
              />
              <button 
                type="button" 
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.09L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.76,7.13 11.37,7 12,7Z"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"/>
                </svg>
              </button>
            </div>
            <div v-if="passwordError" class="field-error">{{ passwordError }}</div>
            <div v-else-if="password.length > 0" class="password-strength">
              <div class="strength-bar">
                <div class="strength-fill" :style="{ width: passwordStrength + '%' }" :class="passwordStrengthClass"></div>
              </div>
              <span class="strength-text" :class="passwordStrengthClass">{{ passwordStrengthText }}</span>
            </div>
          </div>

          <div class="form-group">
            <div class="input-wrapper">
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z"/>
                </svg>
              </div>
              <input
                v-model="confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                placeholder="请再次输入密码"
                class="form-input"
                :class="{ 'input-error': confirmPasswordError, 'input-success': confirmPasswordValid }"
                @input="validateConfirmPassword"
              />
              <button 
                type="button" 
                class="password-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.09L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.76,7.13 11.37,7 12,7Z"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"/>
                </svg>
              </button>
              <div v-if="confirmPasswordValid" class="input-status success">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M10,17L5,12L6.41,10.58L10,14.17L17.59,6.58L19,8M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2Z"/>
                </svg>
              </div>
            </div>
            <div v-if="confirmPasswordError" class="field-error">{{ confirmPasswordError }}</div>
            <div v-else-if="confirmPasswordValid" class="field-success">密码确认无误</div>
          </div>

          <button type="submit" :disabled="loading || !formValid" class="register-btn">
            <span v-if="loading" class="loading-spinner"></span>
            <span v-else class="btn-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
              </svg>
            </span>
            {{ loading ? '注册中...' : '创建账户' }}
          </button>

          <div class="form-footer">
            <div class="terms-notice">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
              </svg>
              <span>注册即表示您同意我们的服务条款和隐私政策</span>
            </div>

            <div class="divider">
              <span>或</span>
            </div>
            
            <div class="switch-auth">
              <span>已经有账号了？</span>
              <router-link to="/login" class="auth-link">
                立即登录
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z"/>
                </svg>
              </router-link>
            </div>
          </div>
        </form>

        <!-- 错误提示 -->
        <div v-if="errorMessage" class="error-toast">
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M13,13H11V7H13M11,15H13V17H11M15.73,3H8.27L3,8.27V15.73L8.27,21H15.73L21,15.73V8.27L15.73,3Z"/>
            </svg>
          </div>
          <span class="error-text">{{ errorMessage }}</span>
          <button @click="errorMessage = ''" class="error-close">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"/>
            </svg>
          </button>
        </div>

        <!-- 成功提示 -->
        <div v-if="successMessage" class="success-toast">
          <div class="success-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M10,17L5,12L6.41,10.58L10,14.17L17.59,6.58L19,8M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2Z"/>
            </svg>
          </div>
          <span class="success-text">{{ successMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      loading: false,
      errorMessage: '',
      successMessage: '',
      showPassword: false,
      showConfirmPassword: false,
      usernameError: '',
      passwordError: '',
      confirmPasswordError: ''
    };
  },
  // 清除可能存在的无效token
  created() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    // 清除axios header
    delete axios.defaults.headers.common['Authorization'];
  },
  computed: {
    usernameValid() {
      return this.username.length >= 3 && !this.usernameError;
    },
    passwordStrength() {
      if (this.password.length < 6) return 20;
      if (this.password.length < 8) return 40;
      
      let score = 40;
      if (/[a-z]/.test(this.password)) score += 15;
      if (/[A-Z]/.test(this.password)) score += 15;
      if (/[0-9]/.test(this.password)) score += 15;
      if (/[^A-Za-z0-9]/.test(this.password)) score += 15;
      
      return Math.min(score, 100);
    },
    passwordStrengthClass() {
      if (this.passwordStrength < 40) return 'weak';
      if (this.passwordStrength < 70) return 'medium';
      return 'strong';
    },
    passwordStrengthText() {
      if (this.passwordStrength < 40) return '弱';
      if (this.passwordStrength < 70) return '中等';
      return '强';
    },
    confirmPasswordValid() {
      return this.confirmPassword.length > 0 && this.password === this.confirmPassword && !this.confirmPasswordError;
    },
    formValid() {
      return this.usernameValid && this.password.length >= 6 && this.confirmPasswordValid && !this.passwordError;
    }
  },
  methods: {
    validateUsername() {
      if (this.username.length < 3) {
        this.usernameError = '用户名至少需要3个字符';
      } else if (this.username.length > 20) {
        this.usernameError = '用户名不能超过20个字符';
      } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(this.username)) {
        this.usernameError = '用户名只能包含字母、数字、下划线和中文';
      } else {
        this.usernameError = '';
      }
    },
    validatePassword() {
      if (this.password.length < 6) {
        this.passwordError = '密码至少需要6个字符';
      } else if (this.password.length > 50) {
        this.passwordError = '密码不能超过50个字符';
      } else {
        this.passwordError = '';
      }
      this.validateConfirmPassword();
    },
    validateConfirmPassword() {
      if (this.confirmPassword.length > 0 && this.password !== this.confirmPassword) {
        this.confirmPasswordError = '两次输入的密码不一致';
      } else {
        this.confirmPasswordError = '';
      }
    },
    async handleRegister() {
      // 最后一次验证
      this.validateUsername();
      this.validatePassword();
      this.validateConfirmPassword();

      if (!this.formValid) {
        this.errorMessage = '请检查并修正表单中的错误';
        return;
      }

      this.loading = true;
      this.errorMessage = '';
      this.successMessage = '';

      try {
        console.log('准备发送注册请求...'); // 调试信息

        const response = await axios({
          method: 'POST',
          url: '/api/register/post/',
          data: {
            username: this.username,
            password: this.password
          },
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 10000 // 10秒超时
        });

        console.log('注册响应：', response); // 完整响应信息

        this.successMessage = '注册成功！正在跳转到登录页面...';
        
        setTimeout(() => {
          this.$router.push('/login');
        }, 2000);

      } catch (error) {
        console.error('注册完整错误信息：', error);

        if (error.code === 'ECONNABORTED') {
          this.errorMessage = '请求超时，请检查网络连接';
        } else if (error.message === 'Network Error') {
          this.errorMessage = '网络错误，请检查后端服务是否正常运行';
        } else if (error.response) {
          console.error('服务器错误响应：', error.response.data);
          const status = error.response.status;
          const data = error.response.data;

          if (status === 400) {
            if (data.username) {
              this.errorMessage = data.username[0] || '用户名已存在';
            } else {
              this.errorMessage = data.detail || data.non_field_errors?.[0] || '注册信息有误';
            }
          } else if (status === 500) {
            this.errorMessage = '服务器内部错误，请稍后重试';
          } else {
            this.errorMessage = data.detail || `请求失败 (${status})`;
          }
        } else if (error.request) {
          console.error('没有收到响应：', error.request);
          this.errorMessage = '无法连接到服务器，请检查网络或后端服务';
        } else {
          console.error('请求配置错误：', error.message);
          this.errorMessage = '请求配置错误：' + error.message;
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.floating-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: 5%;
  left: 5%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 15%;
  right: 10%;
  animation-delay: 2s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  bottom: 15%;
  left: 15%;
  animation-delay: 4s;
}

.shape-4 {
  width: 80px;
  height: 80px;
  bottom: 25%;
  right: 20%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(120deg); }
  66% { transform: translateY(10px) rotate(240deg); }
}

.register-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 900px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 650px;
  overflow: hidden;
  animation: slideUp 0.8s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 品牌区域 */
.brand-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  position: relative;
}

.brand-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1" fill="white" opacity="0.1"/><circle cx="80" cy="40" r="1" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.logo-container {
  text-align: center;
  position: relative;
  z-index: 1;
}

.health-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 2s ease-in-out infinite;
}

.health-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 12px 0;
  background: linear-gradient(45deg, #fff, #e8f2ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin: 0;
  font-weight: 300;
}

/* 表单区域 */
.form-section {
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow-y: auto;
}

.form-header {
  margin-bottom: 32px;
  text-align: center;
}

.form-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.form-header p {
  color: #7f8c8d;
  margin: 0;
  font-size: 16px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  position: relative;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  z-index: 2;
  color: #7f8c8d;
  transition: color 0.3s;
}

.input-icon svg {
  width: 20px;
  height: 20px;
}

.form-input {
  width: 100%;
  padding: 16px 16px 16px 52px;
  border: 2px solid #e8ecf0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s;
  background: #fafbfc;
  color: #2c3e50;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.form-input:focus + .input-icon,
.form-input:not(:placeholder-shown) + .input-icon {
  color: #667eea;
}

.form-input.input-error {
  border-color: #e74c3c;
  background: #fdf2f2;
}

.form-input.input-success {
  border-color: #27ae60;
  background: #f8fff8;
}

.input-status {
  position: absolute;
  right: 52px;
  z-index: 2;
}

.input-status.success svg {
  width: 20px;
  height: 20px;
  color: #27ae60;
}

.password-toggle {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  color: #7f8c8d;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.3s;
  z-index: 2;
}

.password-toggle:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.password-toggle svg {
  width: 20px;
  height: 20px;
}

.field-error {
  color: #e74c3c;
  font-size: 12px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.field-success {
  color: #27ae60;
  font-size: 12px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.field-hint {
  color: #7f8c8d;
  font-size: 12px;
  margin-top: 6px;
}

.password-strength {
  margin-top: 8px;
}

.strength-bar {
  height: 4px;
  background: #e8ecf0;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 4px;
}

.strength-fill {
  height: 100%;
  transition: all 0.3s;
  border-radius: 2px;
}

.strength-fill.weak {
  background: #e74c3c;
}

.strength-fill.medium {
  background: #f39c12;
}

.strength-fill.strong {
  background: #27ae60;
}

.strength-text {
  font-size: 12px;
  font-weight: 500;
}

.strength-text.weak {
  color: #e74c3c;
}

.strength-text.medium {
  color: #f39c12;
}

.strength-text.strong {
  color: #27ae60;
}

.register-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px 24px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
  margin-top: 8px;
}

.register-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.register-btn:hover::before {
  left: 100%;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.register-btn:active {
  transform: translateY(0);
}

.register-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-icon svg {
  width: 20px;
  height: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.form-footer {
  margin-top: 24px;
}

.terms-notice {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #7f8c8d;
  font-size: 12px;
  margin-bottom: 20px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.terms-notice svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #667eea;
}

.divider {
  position: relative;
  text-align: center;
  margin: 20px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e8ecf0;
}

.divider span {
  background: white;
  color: #7f8c8d;
  padding: 0 16px;
  font-size: 14px;
  position: relative;
}

.switch-auth {
  text-align: center;
  color: #7f8c8d;
  font-size: 14px;
}

.auth-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.3s;
}

.auth-link:hover {
  color: #5a67d8;
  transform: translateX(2px);
}

.auth-link svg {
  width: 16px;
  height: 16px;
}

/* 错误提示 */
.error-toast {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #c53030;
  box-shadow: 0 4px 12px rgba(197, 48, 48, 0.15);
  animation: slideIn 0.3s ease-out;
}

/* 成功提示 */
.success-toast {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: #f0fff4;
  border: 1px solid #9ae6b4;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #2f855a;
  box-shadow: 0 4px 12px rgba(47, 133, 90, 0.15);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-icon svg,
.success-icon svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.error-text,
.success-text {
  flex: 1;
  font-size: 14px;
}

.error-close {
  background: none;
  border: none;
  color: #c53030;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.error-close:hover {
  background: rgba(197, 48, 48, 0.1);
}

.error-close svg {
  width: 16px;
  height: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-wrapper {
    padding: 10px;
  }

  .register-container {
    grid-template-columns: 1fr;
    max-width: 400px;
    min-height: auto;
  }

  .brand-section {
    padding: 40px 20px;
  }

  .health-icon {
    width: 60px;
    height: 60px;
  }

  .health-icon svg {
    width: 30px;
    height: 30px;
  }

  .brand-title {
    font-size: 24px;
  }

  .brand-subtitle {
    font-size: 14px;
  }

  .form-section {
    padding: 40px 20px;
  }

  .form-header h2 {
    font-size: 24px;
  }

  .form-header p {
    font-size: 14px;
  }

  .floating-shape {
    display: none;
  }

  .register-form {
    gap: 16px;
  }

  .form-footer {
    margin-top: 20px;
  }
}
</style>