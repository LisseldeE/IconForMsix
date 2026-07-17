# IconForMsix - MSIX图标生成工具

## 项目简介

IconForMsix 是一款简洁高效的MSIX包图标生成工具。只需拖拽一张PNG图片，即可自动生成40种不同尺寸的图标文件，完美适配微软商店应用打包需求。采用超采样技术处理，确保图标边缘平滑无锯齿。

## 项目截图

![主界面](https://lisseldee.github.io/images/webp/5-1.webp)

## 项目信息

- **项目名称**: IconForMsix
- **项目作者**: Lisselde_E
- **项目主页**: https://lisseldee.github.io/#5
- **项目仓库**: https://github.com/LisseldeE/IconForMsix

## 功能特性

### 图标生成
- 拖拽PNG图片一键生成40种尺寸图标
- 支持StoreLogo、Square44x44Logo、Square71x71Logo、Square150x150Logo、Square310x310Logo、Wide310x150Logo等全系规格
- 超采样技术处理，减少边缘锯齿
- 96dpi标准输出，符合微软商店要求

### 界面交互
- 简洁直观的拖拽操作
- 支持中/英文界面切换
- 自动识别系统语言
- 输入名称自动转换英文为大写
- 子线程处理，避免界面卡死

### 用户体验
- 底部通知提示，不干扰操作
- 固定窗口高度，避免界面跳动
- Windows任务栏图标正确显示

## 使用方法

1. 拖拽PNG图片到拖拽区域
2. 输入应用名称（英文自动转大写）
3. 点击保存按钮选择保存位置
4. 自动生成Assets文件夹及40张图标

## 生成规格

| 类型 | 数量 | 说明 |
|------|------|------|
| StoreLogo | 5 | 商店Logo系列 |
| Square44x44Logo | 15 | 44x44图标系列（含targetsize） |
| Square71x71Logo | 5 | 71x71图标系列 |
| Square150x150Logo | 5 | 150x150图标系列 |
| Square310x310Logo | 5 | 310x310图标系列 |
| Wide310x150Logo | 5 | 宽幅图标系列 |

## 更新日志

### 2026.7.16 R1

**#02**
- 优化了部分细节

详见 [更新日志](https://github.com/LisseldeE/IconForMsix/blob/main/CHANGELOG.md)

## 技术栈

- Python 3.x
- PySide6
- Pillow

## 安装与运行

### 系统要求
- Python 3.8 或更高版本
- Windows 10 或更高版本

### 安装依赖
```bash
pip install PySide6 Pillow
```

### 运行程序
```bash
python IconForMsix.py
```

## 开源声明

本项目采用 MIT 开源协议，详见 [LICENSE](https://github.com/LisseldeE/IconForMsix/blob/main/LICENSE) 文件。

## 反馈

如有问题或建议，欢迎提交 Issue！