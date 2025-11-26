# 启动音乐系统后端和前端服务的PowerShell脚本
Write-Host "开始启动音乐系统服务..."

# 启动后端服务（Django）
Write-Host "正在启动后端服务..."
Start-Process powershell.exe -ArgumentList "cd backend; python manage.py runserver"

# 等待2秒让后端服务开始启动
Start-Sleep -Seconds 2

# 启动前端服务
Write-Host "正在启动前端服务..."
Start-Process powershell.exe -ArgumentList "cd frontend; npm run dev"

Write-Host "\n服务启动完成！"
Write-Host "- 后端服务通常运行在 http://localhost:8000"
Write-Host "- 前端服务通常运行在 http://localhost:3000"
Write-Host "\n请在浏览器中访问前端服务地址以使用音乐系统。"
