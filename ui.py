import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QSpinBox, QProgressBar, QMessageBox, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from model_loader import ModelLoader
from gallery import ImageGallery
from generator import generate_images
from utils import ensure_output_dir, get_seed

class ImageGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stable Diffusion 이미지 생성기")
        self.setStyleSheet("background-color: #121212; color: #f0f0f0;")
        self.output_dir = ensure_output_dir("generated_images")
        self.image_paths = []
        self.pipe_txt2img = None
        self.pipe_img2img = None
        self.setup_ui()
        self.load_models()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("프롬프트 입력")
        layout.addWidget(self.prompt_input)

        size_layout = QHBoxLayout()
        self.width_input = QSpinBox()
        self.width_input.setRange(8, 2048)
        self.width_input.setValue(512)
        self.width_input.setSingleStep(8)
        size_layout.addWidget(QLabel("너비:"))
        size_layout.addWidget(self.width_input)

        self.height_input = QSpinBox()
        self.height_input.setRange(8, 2048)
        self.height_input.setValue(512)
        self.height_input.setSingleStep(8)
        size_layout.addWidget(QLabel("높이:"))
        size_layout.addWidget(self.height_input)
        layout.addLayout(size_layout)

        count_seed_layout = QHBoxLayout()
        self.num_images_input = QSpinBox()
        self.num_images_input.setRange(1, 10)
        self.num_images_input.setValue(1)
        count_seed_layout.addWidget(QLabel("개수:"))
        count_seed_layout.addWidget(self.num_images_input)

        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("랜덤 시드 (선택)")
        count_seed_layout.addWidget(QLabel("시드:"))
        count_seed_layout.addWidget(self.seed_input)
        layout.addLayout(count_seed_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.generate_button = QPushButton("이미지 생성")
        self.generate_button.clicked.connect(self.generate_images)
        layout.addWidget(self.generate_button)

        self.save_button = QPushButton("이미지 저장 위치 선택")
        self.save_button.clicked.connect(self.choose_save_location)
        layout.addWidget(self.save_button)

        self.gallery_button = QPushButton("갤러리 보기")
        self.gallery_button.clicked.connect(self.open_gallery)
        layout.addWidget(self.gallery_button)

        self.scroll_area = QScrollArea()
        self.image_container = QVBoxLayout()
        frame = QFrame()
        frame.setLayout(self.image_container)
        self.scroll_area.setWidget(frame)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area, stretch=1)

        self.setLayout(layout)

    def load_models(self):
        self.model_loader = ModelLoader()
        self.model_loader.finished.connect(self.models_loaded)
        self.model_loader.start()

    def models_loaded(self, pipe_txt2img, pipe_img2img):
        self.pipe_txt2img = pipe_txt2img
        self.pipe_img2img = pipe_img2img
        QMessageBox.information(self, "모델 로딩 완료", "모델이 성공적으로 로딩되었습니다.")

    def choose_save_location(self):
        directory = QFileDialog.getExistingDirectory(self, "저장할 폴더 선택", self.output_dir)
        if directory:
            self.output_dir = directory

    def open_gallery(self):
        if self.image_paths:
            gallery = ImageGallery(self.image_paths)
            gallery.exec_()
        else:
            QMessageBox.information(self, "갤러리", "생성된 이미지가 없습니다.")

    def generate_images(self):
        if not self.pipe_txt2img:
            QMessageBox.warning(self, "모델 로딩 중", "모델이 아직 로딩되지 않았습니다.")
            return

        prompt = self.prompt_input.text().strip()
        width, height = self.width_input.value(), self.height_input.value()
        num_images = self.num_images_input.value()
        seed = get_seed(self.seed_input.text().strip())

        if not prompt:
            QMessageBox.warning(self, "입력 오류", "프롬프트를 입력하세요.")
            return

        self.image_paths = generate_images(
            self.pipe_txt2img, prompt, width, height, num_images, seed, self.output_dir
        )

        for path in self.image_paths:
            pixmap = QPixmap(path).scaled(256, 256, Qt.KeepAspectRatio)
            label = QLabel()
            label.setPixmap(pixmap)
            self.image_container.addWidget(label)

        self.progress_bar.setValue(100)
        QMessageBox.information(self, "완료", f"{num_images}개의 이미지가 생성되었습니다.")