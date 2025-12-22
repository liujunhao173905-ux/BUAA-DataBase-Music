// 用于辅助前端判断用户名是否存在的API调用
import axios from 'axios';

export async function checkUserExists(username) {
  return axios.get(`/api/user_exists/?username=${encodeURIComponent(username)}`);
}
