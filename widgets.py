from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QPoint, QEvent
from PySide6.QtGui import QFont, QEnterEvent


class AnimatedButton(QPushButton):
    """带点击动画的按钮 - 按下时下沉1px"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._original_pos = None
        self._is_pressed = False

    def event(self, event):
        if event.type() == QEvent.Type.LayoutRequest:
            if not self._is_pressed:
                self._original_pos = None
        return super().event(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._original_pos = self.pos()
            self._is_pressed = True
            super().mousePressEvent(event)
            if self._original_pos:
                self.move(QPoint(self._original_pos.x(), self._original_pos.y() + 1))
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_pressed = False
            if self._original_pos is not None:
                self.move(self._original_pos)
            super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)


# 按钮样式常量
BUTTON_STYLES = {
    'primary': """
        QPushButton {
            padding: 10px;
            font-size: 12px;
            background-color: #339af0;
            color: white;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #228be6;
        }
        QPushButton:pressed {
            background-color: #1c7ed6;
        }
        QPushButton:disabled {
            background-color: #dee2e6;
            color: #868e96;
        }
    """,
    'secondary': """
        QPushButton {
            padding: 10px;
            font-size: 12px;
            background-color: #e9ecef;
            color: #495057;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #dee2e6;
        }
        QPushButton:pressed {
            background-color: #ced4da;
        }
    """,
    'clear': """
        QPushButton {
            background-color: transparent;
            color: #868e96;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-size: 11px;
        }
        QPushButton:hover {
            color: #495057;
            border-color: #adb5bd;
        }
    """
}


class ToastNotification(QWidget):
    """底部通知组件"""

    def __init__(self, parent=None, duration=3000):
        super().__init__(parent)
        self._duration = duration
        self._parent = parent
        self._opacity_effect = None
        self._fade_animation = None

        self.setFixedHeight(32)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 保持固定大小策略
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 45, 45, 230);
                border-radius: 6px;
            }
        """)

        # 布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)

        self._label = QLabel()
        self._label.setStyleSheet("color: #868e96; font-size: 12px;")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._label)

        # 透明度效果
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)

    def show_message(self, message: str, msg_type: str = "info"):
        """显示消息"""
        self._label.setText(message)

        # 设置颜色
        if msg_type == "success":
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(46, 125, 50, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")
        elif msg_type == "error":
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(198, 40, 40, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(45, 45, 45, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")

        # 淡入动画
        self._fade_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_animation.setDuration(200)
        self._fade_animation.setStartValue(0)
        self._fade_animation.setEndValue(1)
        self._fade_animation.start()

        # 定时隐藏
        QTimer.singleShot(self._duration, self._fade_out)

    def show_converting(self):
        """显示转换中状态"""
        from i18n import I18n
        converting_text = I18n.tr("msg_converting")
        self._label.setText(converting_text)
        self._label.setStyleSheet("color: #339af0; font-size: 12px;")
        self.setStyleSheet("background-color: transparent;")

    def show_result(self, message: str, msg_type: str = "info"):
        """显示结果消息（成功/错误），完成后恢复等待状态"""
        # 先设置恢复文本
        from i18n import I18n
        self._waiting_text = I18n.tr("msg_waiting")

        self._label.setText(message)

        # 设置颜色
        if msg_type == "success":
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(46, 125, 50, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")
        elif msg_type == "error":
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(198, 40, 40, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: rgba(45, 45, 45, 230);
                    border-radius: 6px;
                }
            """)
            self._label.setStyleSheet("color: white; font-size: 12px;")

        # 淡入动画
        self._opacity_effect.setOpacity(0)
        self._fade_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_animation.setDuration(150)
        self._fade_animation.setStartValue(0)
        self._fade_animation.setEndValue(1)
        self._fade_animation.start()

        # 定时恢复等待状态
        QTimer.singleShot(3000, self._fade_out)

    def _fade_out(self):
        """淡出动画"""
        self._fade_animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        self._fade_animation.setDuration(200)
        self._fade_animation.setStartValue(1)
        self._fade_animation.setEndValue(0)
        self._fade_animation.finished.connect(self._clear)
        self._fade_animation.start()

    def _clear(self):
        """清除消息，恢复默认状态"""
        from i18n import I18n
        waiting_text = self._waiting_text if hasattr(self, '_waiting_text') else I18n.tr("msg_waiting")
        self._label.setText(waiting_text)
        self._label.setStyleSheet("color: #868e96; font-size: 12px;")
        self.setStyleSheet("background-color: transparent;")
        # 重置透明度
        self._opacity_effect.setOpacity(1)

    def set_waiting_text(self, text: str):
        """设置等待状态文本"""
        self._waiting_text = text
        self._label.setText(text)
        self._label.setStyleSheet("color: #868e96; font-size: 12px;")
        self.setStyleSheet("background-color: transparent;")


class ClickableLabel(QLabel):
    """可点击标签类 - 支持悬浮效果和下划线"""

    def __init__(self, text="", parent=None,
                 normal_color="#339af0", hover_color="#228be6",
                 underline_on_hover=True):
        super().__init__(text, parent)

        self._normal_color = normal_color
        self._hover_color = hover_color
        self._underline_on_hover = underline_on_hover
        self._is_hovering = False
        self._click_callback = None

        # 设置默认样式
        self.setStyleSheet(f"QLabel {{ font-size: 11px; color: {self._normal_color}; }}")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 保存原始字体
        self._original_font = self.font()

    def enterEvent(self, event):
        """鼠标进入 - 应用 hover 样式"""
        if isinstance(event, QEnterEvent):
            self._is_hovering = True
            self._apply_hover_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开 - 恢复正常样式"""
        self._is_hovering = False
        self._apply_normal_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """鼠标点击 - 执行回调"""
        if event.button() == Qt.MouseButton.LeftButton and self._click_callback:
            self._click_callback(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放 - 保持 hover 状态"""
        if self._is_hovering:
            self._apply_hover_style()

    def set_click_callback(self, callback):
        """设置点击回调函数"""
        self._click_callback = callback
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _apply_hover_style(self):
        """应用 hover 样式"""
        self.setStyleSheet(f"QLabel {{ font-size: 11px; color: {self._hover_color}; }}")

        if self._underline_on_hover:
            font = QFont(self._original_font)
            font.setUnderline(True)
            self.setFont(font)

    def _apply_normal_style(self):
        """应用正常样式"""
        self.setStyleSheet(f"QLabel {{ font-size: 11px; color: {self._normal_color}; }}")

        if self._underline_on_hover:
            font = QFont(self._original_font)
            font.setUnderline(False)
            self.setFont(font)