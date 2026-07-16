import locale


class I18n:
    """国际化模块"""
    _language = None

    # 翻译文本
    _translations = {
        "zh_CN": {
            # 主界面
            "drop_hint": "拖拽PNG图片到此处",
            "drop_selected": "已选择: {name}",
            "tip_source_image": "提示：选择较大尺寸的源图片效果最佳",
            "label_name_prefix": "文件名前缀:",
            "placeholder_name": "如: myapp",
            "btn_save": "选择保存位置并生成图标",
            "btn_clear": "清除",
            "btn_about": "关于",
            "msg_name_required": "请输入文件名前缀",
            "msg_image_required": "请先拖入PNG图片",
            "msg_success": "成功生成 {count} 张图标",
            "msg_saved_to": "保存至: {path}",
            "msg_failed": "生成失败: {error}",
            "msg_waiting": "等待中...",
            "msg_converting": "转换中...",

            # 关于界面
            "about_title": "关于",
            "about_version": "版本",
            "about_description": "用于生成MSIX包图标的小工具",
            "about_author": "作者",
            "about_feedback": "问题反馈",
            "about_details": "查看详情",
            "about_check_update": "检查更新",
            "close": "关闭",
            "about_latest": "已是最新版本",
            "about_new_version": "发现新版本: {version}",
            "about_network_error": "网络错误: {error}",
            "about_check_failed": "检查失败: {error}",
        },
        "en": {
            # Main interface
            "drop_hint": "Drop PNG image here",
            "drop_selected": "Selected: {name}",
            "tip_source_image": "Tip: Larger source images yield better results",
            "label_name_prefix": "Name prefix:",
            "placeholder_name": "e.g. myapp",
            "btn_save": "Choose location and generate icons",
            "btn_clear": "Clear",
            "btn_about": "About",
            "msg_name_required": "Please enter name prefix",
            "msg_image_required": "Please drop a PNG image first",
            "msg_success": "Successfully generated {count} icons",
            "msg_saved_to": "Saved to: {path}",
            "msg_failed": "Generation failed: {error}",
            "msg_waiting": "Waiting...",
            "msg_converting": "Converting...",

            # About dialog
            "about_title": "About",
            "about_version": "Version",
            "about_description": "A small tool for generating MSIX package icons",
            "about_author": "Author",
            "about_feedback": "Feedback",
            "about_details": "Details",
            "about_check_update": "Check for Updates",
            "close": "Close",
            "about_latest": "You have the latest version",
            "about_new_version": "New version available: {version}",
            "about_network_error": "Network error: {error}",
            "about_check_failed": "Check failed: {error}",
        }
    }

    @classmethod
    def get_language(cls) -> str:
        """获取当前语言"""
        if cls._language is None:
            # 自动检测系统语言
            sys_lang = locale.getdefaultlocale()[0] or "en"
            if sys_lang.startswith("zh"):
                cls._language = "zh_CN"
            else:
                cls._language = "en"
        return cls._language

    @classmethod
    def set_language(cls, lang: str):
        """设置语言"""
        cls._language = lang

    @classmethod
    def tr(cls, key: str, **kwargs) -> str:
        """获取翻译文本"""
        lang = cls.get_language()
        translations = cls._translations.get(lang, cls._translations["en"])
        text = translations.get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text