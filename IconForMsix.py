import sys
import os
import ctypes
from pathlib import Path
from PIL import Image
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon

from config import Config
from i18n import I18n
from widgets import ToastNotification, AnimatedButton, BUTTON_STYLES
from about_dialog import AboutDialog


def get_resource_path(relative_path):
    """获取资源文件路径，兼容打包和未打包"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 图标尺寸规格配置
ICON_SPECS = [
    # StoreLogo系列
    ("StoreLogo.scale-100", 50, 50, 37, 37, True),
    ("StoreLogo.scale-125", 63, 63, 47, 47, True),
    ("StoreLogo.scale-150", 75, 75, 56, 56, True),
    ("StoreLogo.scale-200", 100, 100, 75, 75, True),
    ("StoreLogo.scale-400", 200, 200, 150, 150, True),
    # Square44x44Logo scale系列
    ("{name}-Square44x44Logo.scale-100", 44, 44, 33, 33, True),
    ("{name}-Square44x44Logo.scale-125", 55, 55, 41, 41, True),
    ("{name}-Square44x44Logo.scale-150", 66, 66, 49, 49, True),
    ("{name}-Square44x44Logo.scale-200", 88, 88, 66, 66, True),
    ("{name}-Square44x44Logo.scale-400", 176, 176, 132, 132, True),
    # Square44x44Logo targetsize系列
    ("{name}-Square44x44Logo.targetsize-16", 16, 16, 16, 16, False),
    ("{name}-Square44x44Logo.targetsize-16_altform-unplated", 16, 16, 16, 16, False),
    ("{name}-Square44x44Logo.targetsize-24", 24, 24, 24, 24, False),
    ("{name}-Square44x44Logo.targetsize-24_altform-unplated", 24, 24, 24, 24, False),
    ("{name}-Square44x44Logo.targetsize-32", 32, 32, 32, 32, False),
    ("{name}-Square44x44Logo.targetsize-32_altform-unplated", 32, 32, 32, 32, False),
    ("{name}-Square44x44Logo.targetsize-48", 48, 48, 48, 48, False),
    ("{name}-Square44x44Logo.targetsize-48_altform-unplated", 48, 48, 48, 48, False),
    ("{name}-Square44x44Logo.targetsize-256", 256, 256, 256, 256, False),
    ("{name}-Square44x44Logo.targetsize-256_altform-unplated", 256, 256, 256, 256, False),
    # Square71x71Logo系列
    ("{name}-Square71x71Logo.scale-100", 71, 71, 35, 35, True),
    ("{name}-Square71x71Logo.scale-125", 89, 89, 44, 44, True),
    ("{name}-Square71x71Logo.scale-150", 107, 107, 53, 53, True),
    ("{name}-Square71x71Logo.scale-200", 142, 142, 71, 71, True),
    ("{name}-Square71x71Logo.scale-400", 284, 284, 142, 142, True),
    # Square150x150Logo系列
    ("{name}-Square150x150Logo.scale-100", 150, 150, 75, 75, True),
    ("{name}-Square150x150Logo.scale-125", 188, 188, 94, 94, True),
    ("{name}-Square150x150Logo.scale-150", 225, 225, 112, 112, True),
    ("{name}-Square150x150Logo.scale-200", 300, 300, 150, 150, True),
    ("{name}-Square150x150Logo.scale-400", 600, 600, 300, 300, True),
    # Square310x310Logo系列
    ("{name}-Square310x310Logo.scale-100", 310, 310, 155, 155, True),
    ("{name}-Square310x310Logo.scale-125", 388, 388, 194, 194, True),
    ("{name}-Square310x310Logo.scale-150", 465, 465, 232, 232, True),
    ("{name}-Square310x310Logo.scale-200", 620, 620, 310, 310, True),
    ("{name}-Square310x310Logo.scale-400", 1240, 1240, 620, 620, True),
    # Wide310x150Logo系列
    ("{name}-Wide310x150Logo.scale-100", 310, 150, 75, 75, True),
    ("{name}-Wide310x150Logo.scale-125", 388, 188, 94, 94, True),
    ("{name}-Wide310x150Logo.scale-150", 465, 225, 112, 112, True),
    ("{name}-Wide310x150Logo.scale-200", 620, 300, 150, 150, True),
    ("{name}-Wide310x150Logo.scale-400", 1240, 600, 300, 300, True),
]


def generate_icon(source_img, total_w, total_h, icon_w, icon_h, has_border):
    canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    supersample = 4

    if has_border:
        super_icon_w = icon_w * supersample
        super_icon_h = icon_h * supersample
        super_total_w = total_w * supersample
        super_total_h = total_h * supersample
        super_canvas = Image.new("RGBA", (super_total_w, super_total_h), (0, 0, 0, 0))
        resized = source_img.resize((super_icon_w, super_icon_h), Image.Resampling.LANCZOS)
        x = (super_total_w - super_icon_w) // 2
        y = (super_total_h - super_icon_h) // 2
        super_canvas.paste(resized, (x, y), resized if resized.mode == "RGBA" else None)
        canvas = super_canvas.resize((total_w, total_h), Image.Resampling.LANCZOS)
    else:
        super_w = total_w * supersample
        super_h = total_h * supersample
        temp = source_img.resize((super_w, super_h), Image.Resampling.LANCZOS)
        canvas = temp.resize((total_w, total_h), Image.Resampling.LANCZOS)

    return canvas


def generate_all_icons(source_path, name_prefix, output_dir):
    source_img = Image.open(source_path).convert("RGBA")
    assets_dir = Path(output_dir) / "Assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for spec in ICON_SPECS:
        filename_template, total_w, total_h, icon_w, icon_h, has_border = spec
        filename = filename_template.replace("{name}", name_prefix) + ".png"
        output_path = assets_dir / filename
        icon = generate_icon(source_img, total_w, total_h, icon_w, icon_h, has_border)
        icon.save(output_path, "PNG", dpi=(96, 96))
        count += 1

    return count


class IconGeneratorThread(QThread):
    """图标生成线程"""
    finished = Signal(int, str)  # count, output_path
    error = Signal(str)

    def __init__(self, source_path, name_prefix, output_dir):
        super().__init__()
        self.source_path = source_path
        self.name_prefix = name_prefix
        self.output_dir = output_dir

    def run(self):
        try:
            count = generate_all_icons(self.source_path, self.name_prefix, self.output_dir)
            assets_path = str(Path(self.output_dir) / "Assets")
            self.finished.emit(count, assets_path)
        except Exception as e:
            self.error.emit(str(e))


class DropArea(QLabel):
    """拖拽接收区域"""

    image_selected = None

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_style("normal")
        self.setMinimumHeight(100)
        self.image_path = None

    def _update_style(self, state):
        if state == "hover":
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #4a9eff;
                    border-radius: 8px;
                    padding: 30px;
                    color: #4a9eff;
                    font-size: 13px;
                    background-color: rgba(74, 158, 255, 0.1);
                }
            """)
        elif state == "selected":
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #339af0;
                    border-radius: 8px;
                    padding: 30px;
                    color: #339af0;
                    font-size: 13px;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #888;
                    border-radius: 8px;
                    padding: 30px;
                    color: #888;
                    font-size: 13px;
                }
            """)

    def reset(self):
        self.image_path = None
        self.setText(I18n.tr("drop_hint"))
        self._update_style("normal")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._update_style("hover")

    def dragLeaveEvent(self, event):
        if self.image_path:
            self.setText(I18n.tr("drop_selected", name=Path(self.image_path).name))
        else:
            self.setText(I18n.tr("drop_hint"))
        self._update_style("normal")

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(".png"):
                self.image_path = file_path
                self.setText(I18n.tr("drop_selected", name=Path(file_path).name))
                self._update_style("selected")
                if self.image_selected:
                    self.image_selected(file_path)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(Config.APP_NAME)
        self.setFixedSize(420, 320)
        self._setup_ui()
        self._load_icon()

    def _load_icon(self):
        """加载程序图标并设置任务栏图标"""
        icon_path = get_resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

            # Windows任务栏图标设置
            if sys.platform == 'win32':
                try:
                    hwnd = int(self.winId())
                    hicon = ctypes.windll.user32.LoadImageW(
                        None, icon_path, 1,  # IMAGE_ICON
                        0, 0, 0x10  # LR_LOADFROMFILE
                    )
                    if hicon:
                        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 0, hicon)  # ICON_SMALL
                        ctypes.windll.user32.SendMessageW(hwnd, 0x80, 1, hicon)  # ICON_BIG
                except Exception:
                    pass

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 拖拽区域和清除按钮
        drop_layout = QHBoxLayout()
        self.drop_area = DropArea()
        self.drop_area.setText(I18n.tr("drop_hint"))
        self.drop_area.image_selected = self._on_image_selected
        drop_layout.addWidget(self.drop_area, 1)

        self.clear_btn = AnimatedButton(I18n.tr("btn_clear"))
        self.clear_btn.setFixedSize(50, 32)
        self.clear_btn.setStyleSheet(BUTTON_STYLES['clear'])
        self.clear_btn.clicked.connect(self._on_clear)
        drop_layout.addWidget(self.clear_btn)
        layout.addLayout(drop_layout)

        # 提示文字（固定高度，防止通知挤压）
        self.tip_label = QLabel(I18n.tr("tip_source_image"))
        self.tip_label.setStyleSheet("color: #868e96; font-size: 11px;")
        self.tip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tip_label.setFixedHeight(20)
        layout.addWidget(self.tip_label)

        # 通知区域（固定高度，始终占位）
        self._toast = ToastNotification(self)
        self._toast.set_waiting_text(I18n.tr("msg_waiting"))
        layout.addWidget(self._toast)

        # 文件名输入
        name_layout = QHBoxLayout()
        self.name_label = QLabel(I18n.tr("label_name_prefix"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(I18n.tr("placeholder_name"))
        self.name_input.textChanged.connect(self._on_name_changed)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # 底部按钮行：保存（左）、语言切换和关于（右）
        bottom_layout = QHBoxLayout()

        self.save_btn = AnimatedButton(I18n.tr("btn_save"))
        self.save_btn.setFixedSize(240, 32)
        self.save_btn.setStyleSheet(BUTTON_STYLES['primary'])
        self.save_btn.clicked.connect(self._on_save_clicked)
        bottom_layout.addWidget(self.save_btn)

        bottom_layout.addStretch()

        self.lang_btn = AnimatedButton("中/EN")
        self.lang_btn.setFixedSize(60, 32)
        self.lang_btn.setStyleSheet(BUTTON_STYLES['clear'])
        self.lang_btn.clicked.connect(self._toggle_language)
        bottom_layout.addWidget(self.lang_btn)

        self.about_btn = AnimatedButton(I18n.tr("btn_about"))
        self.about_btn.setFixedSize(60, 32)
        self.about_btn.setStyleSheet(BUTTON_STYLES['clear'])
        self.about_btn.clicked.connect(self._on_about)
        bottom_layout.addWidget(self.about_btn)

        layout.addLayout(bottom_layout)

        # 初始化按钮状态
        self._update_save_btn()

    def _toggle_language(self):
        """切换语言"""
        current = I18n.get_language()
        new_lang = "en" if current == "zh_CN" else "zh_CN"
        I18n.set_language(new_lang)
        self._refresh_ui()

    def _refresh_ui(self):
        """刷新界面文字"""
        self.drop_area.reset()
        self.tip_label.setText(I18n.tr("tip_source_image"))
        self.name_label.setText(I18n.tr("label_name_prefix"))
        self.name_input.setPlaceholderText(I18n.tr("placeholder_name"))
        self.clear_btn.setText(I18n.tr("btn_clear"))
        self.save_btn.setText(I18n.tr("btn_save"))
        self.about_btn.setText(I18n.tr("btn_about"))
        self._toast.set_waiting_text(I18n.tr("msg_waiting"))
        self._update_save_btn()

    def _on_image_selected(self, path):
        self._update_save_btn()

    def _on_name_changed(self, text):
        """名称输入变化时自动转换：英文转大写，中文不变"""
        # 阻止信号循环
        self.name_input.blockSignals(True)

        # 转换：英文字母转大写，中文和其他字符不变
        converted = ""
        for char in text:
            if char.isalpha() and ord(char) < 128:  # ASCII字母
                converted += char.upper()
            else:
                converted += char

        # 只在内容不同时更新
        if converted != text:
            self.name_input.setText(converted)

        self.name_input.blockSignals(False)
        self._update_save_btn()

    def _update_save_btn(self):
        """更新保存按钮状态：图片和名称都存在才启用"""
        has_image = self.drop_area.image_path is not None
        has_name = bool(self.name_input.text().strip())
        self.save_btn.setEnabled(has_image and has_name)

    def _on_clear(self):
        self.drop_area.reset()
        self._update_save_btn()

    def _on_save_clicked(self):
        name_prefix = self.name_input.text().strip()
        if not name_prefix:
            self._show_toast(I18n.tr("msg_name_required"), "error")
            return

        if not self.drop_area.image_path:
            self._show_toast(I18n.tr("msg_image_required"), "error")
            return

        output_dir = QFileDialog.getExistingDirectory(self, I18n.tr("btn_save"))
        if not output_dir:
            return

        # 禁用按钮，显示转换中
        self.save_btn.setEnabled(False)
        self.save_btn.setText("...")
        self._toast.show_converting()

        # 启动生成线程
        self._generator_thread = IconGeneratorThread(
            self.drop_area.image_path, name_prefix, output_dir
        )
        self._generator_thread.finished.connect(self._on_generate_finished)
        self._generator_thread.error.connect(self._on_generate_error)
        self._generator_thread.start()

    def _on_generate_finished(self, count, assets_path):
        """生成完成"""
        self.save_btn.setText(I18n.tr("btn_save"))
        self._update_save_btn()
        self._toast.show_result(
            f"{I18n.tr('msg_success', count=count)} {I18n.tr('msg_saved_to', path=assets_path)}",
            "success"
        )

    def _on_generate_error(self, error_msg):
        """生成出错"""
        self.save_btn.setText(I18n.tr("btn_save"))
        self._update_save_btn()
        self._toast.show_result(I18n.tr("msg_failed", error=error_msg), "error")

    def _on_about(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def _show_toast(self, message, msg_type="info"):
        self._toast.show_message(message, msg_type)


def main():
    # 设置AppUserModelID（必须在QApplication创建之前）
    if sys.platform == 'win32':
        app_id = f"LisseldeE.{Config.APP_NAME}.{Config.APP_VERSION}"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QApplication(sys.argv)

    # 设置应用程序信息
    app.setApplicationName(Config.APP_NAME)
    app.setApplicationVersion(Config.APP_VERSION)
    app.setOrganizationName("LisseldeE")

    # 设置应用图标
    icon_path = get_resource_path("icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()