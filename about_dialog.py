from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from config import Config
from i18n import I18n
from widgets import ClickableLabel, AnimatedButton, BUTTON_STYLES


class AboutDialog(QDialog):
    """关于对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(I18n.tr("about_title"))
        self.setFixedSize(400, 220)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(20, 15, 20, 15)

        # 标题
        title_label = QLabel(Config.APP_NAME)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #339af0;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # 版本
        version_label = QLabel(f"{I18n.tr('about_version')} {Config.APP_VERSION}")
        version_label.setStyleSheet("font-size: 12px; color: #495057;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # 描述
        desc_label = QLabel(I18n.tr('about_description'))
        desc_label.setStyleSheet("font-size: 11px; color: #868e96;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # 作者（不可点击）
        author_label = QLabel(f"{I18n.tr('about_author')}: {Config.APP_AUTHOR}")
        author_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #495057;
            }
            QLabel:hover {
                color: #339af0;
            }
        """)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)

        # GitHub链接
        github_label = QLabel(f"GitHub: {Config.GITHUB_REPO}")
        github_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #495057;
            }
            QLabel:hover {
                color: #339af0;
            }
        """)
        github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_label.setCursor(Qt.CursorShape.PointingHandCursor)
        github_label.mousePressEvent = lambda e: self._open_github()
        layout.addWidget(github_label)

        # 问题反馈和查看详情
        link_layout = QHBoxLayout()
        link_layout.addStretch()

        feedback_label = ClickableLabel(
            I18n.tr('about_feedback'),
            normal_color="#339af0",
            hover_color="#228be6",
            underline_on_hover=True
        )
        feedback_label.set_click_callback(lambda e: self._open_issues())
        link_layout.addWidget(feedback_label)

        link_layout.addSpacing(20)

        details_label = ClickableLabel(
            I18n.tr('about_details'),
            normal_color="#339af0",
            hover_color="#228be6",
            underline_on_hover=True
        )
        details_label.set_click_callback(lambda e: self._open_details())
        link_layout.addWidget(details_label)

        link_layout.addStretch()
        layout.addLayout(link_layout)

        # 关闭按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        close_btn = AnimatedButton(I18n.tr('close'))
        close_btn.setFixedSize(120, 36)
        close_btn.setStyleSheet(BUTTON_STYLES['primary'])
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def _open_github(self):
        """打开 GitHub 链接"""
        QDesktopServices.openUrl(QUrl(f"https://github.com/{Config.GITHUB_REPO}"))

    def _open_issues(self):
        """打开 GitHub Issues 页面"""
        QDesktopServices.openUrl(QUrl(f"https://github.com/{Config.GITHUB_REPO}/issues"))

    def _open_details(self):
        """打开作者主页"""
        QDesktopServices.openUrl(QUrl(Config.APP_AUTHOR_LINK))