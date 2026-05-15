# Cambridge Dictionary Audio - Agent Overview

Tài liệu này cung cấp cái nhìn tổng quan về cấu trúc dự án và các thay đổi gần đây để các AI agent có thể nhanh chóng nắm bắt ngữ cảnh.

## 1. Mục đích dự án
Đây là một công cụ CLI (Command Line Interface) bằng Python cho phép tải file audio phát âm (giọng UK) và tra cứu nghĩa (Anh-Việt) của từ vựng từ trang [dictionary.cambridge.org](https://dictionary.cambridge.org). 

## 2. Cấu trúc Codebase

*   **`main.py`**: Entry point của chương trình.
    *   Chạy vòng lặp CLI tương tác với người dùng.
    *   Xử lý lệnh điều khiển: `/m` (bật/tắt tự động phát âm thanh), `/r` (xóa tất cả file `.mp3` trong thư mục lưu trữ), `/cp` (đổi thư mục lưu audio trong phiên làm việc).
    *   Gọi `Parser.py` để tải audio và lấy bản dịch.
    *   Sử dụng thư viện `playsound` để phát audio ngay sau khi tải.
    *   Cấu hình thư mục lưu trữ qua biến `SAVE_FOLDER` (mặc định `""`, fallback về `os.getcwd()`).
    *   Sử dụng `sys.stdout.reconfigure(encoding='utf-8')` để đảm bảo terminal Windows hiển thị đúng tiếng Việt.
    *   Sử dụng hàm `clear_screen()` hỗ trợ đa nền tảng thay cho `os.system('cls')`.
    *   Mọi xử lý đường dẫn đều dùng `os.path.join()` để tương thích cross-platform.

*   **`Parser.py`**: Module đảm nhiệm việc scraping dữ liệu từ Cambridge Dictionary.
    *   Dùng `requests` và `bs4` (BeautifulSoup) để parse HTML.
    *   `define(word, save_path, ...)`: Tìm link audio UK (`span` class `daud`), tải file mp3, in phiên âm IPA.
    *   `get_translation(word, mode, ...)`: Scrape khối định nghĩa (`def-block`), trích xuất định nghĩa tiếng Anh và bản dịch tiếng Việt, gom nhóm theo từ loại (part of speech). Hàm sử dụng `.get_text(" ", strip=True)` để đảm bảo các text node bên trong có khoảng trắng hợp lý.

*   **`combine.py`**: Xử lý trường hợp người dùng nhập một cụm từ (nhiều từ).
    *   Tải audio của từng từ riêng lẻ thông qua `Parser.define`.
    *   Sử dụng `pydub` (yêu cầu FFmpeg) để nối các file audio lại với nhau (`merge_and_normalize_audio`) và đồng bộ hóa âm lượng.
    *   Sử dụng `alive_progress` để hiển thị thanh tiến trình khi xử lý.
    *   Hàm `comb()` nhận thêm tham số `folder_path` tùy chọn, mọi đường dẫn đều dùng `os.path.join()`.

*   **Các file hỗ trợ**:
    *   `requirements.txt`: Các thư viện phụ thuộc (`alive_progress`, `beautifulsoup4`, `playsound`, `pydub`, `Requests`).
    *   `start.bat`: Script tiện ích để chạy chương trình nhanh (`python main.py`).
    *   `compile.bat`: Dùng `pyinstaller` để đóng gói script thành file `.exe`.
    *   `Design/`: Thư mục chứa tài nguyên UI như logo và ảnh/video demo.
    *   `.gitignore`: Cấu hình các file và thư mục không nên đưa lên GitHub (build, dist, cache, venv, mp3).

## 3. Lịch sử Thay đổi Gần đây (Changelog)
1.  **Chuyển đổi ngôn ngữ dịch**: Đổi ngôn ngữ đích mặc định sang Tiếng Việt (`english-vietnamese`).
2.  **Cấu hình thư mục lưu**: Thêm biến `SAVE_FOLDER` trong `main.py` để tùy chỉnh nơi lưu file `.mp3`.
3.  **Fix lỗi Indentation & Scope**: Sửa lỗi thụt lề ở khối in Menu và đưa các biến `status_color`, `status_text` vào trong scope của hàm `Start()` để cập nhật đúng trạng thái `/m`.
4.  **Cải tiến hiển thị bản dịch**: 
    *   Viết lại logic parse HTML trong `Parser.py` (`get_translation()`) để xử lý đúng cấu trúc trang `english-vietnamese` (tìm trực tiếp `def-block` và xử lý spacing với `get_text(" ", strip=True)`).
    *   Cập nhật `main.py` để hiển thị bản dịch rõ ràng, có cấu trúc (gom theo từ loại, đánh số định nghĩa Anh-Việt) kèm theo màu sắc terminal.
5.  **Fix lỗi Encoding**: Thêm `sys.stdout.reconfigure(encoding='utf-8')` để tránh lỗi `UnicodeEncodeError` trên môi trường terminal Windows khi in ký tự tiếng Việt.
6.  **Thêm lệnh `/cp` (Change Path)**: Cho phép người dùng đổi thư mục lưu file audio ngay trong phiên làm việc mà không cần sửa code. Hệ thống hiển thị đường dẫn hiện tại, nhận input đường dẫn mới, tự tạo thư mục nếu chưa tồn tại, và validate đầu vào.
7.  **Cấu hình `.gitignore`**: Thiết lập danh sách các file/thư mục không nên up lên GitHub, bao gồm các thư mục build của PyInstaller (`build/`, `dist/`), file spec, cache của Python (`__pycache__/`), môi trường ảo (`venv/`) và các file audio `.mp3` được tải về.
8.  **Refactor Cross-platform**:
    *   Thay thế toàn bộ nối chuỗi đường dẫn cứng bằng `\\` thành `os.path.join()` trong `main.py` và `combine.py`.
    *   Thay thế `os.system('cls')` bằng hàm `clear_screen()` kiểm tra `os.name` để hỗ trợ cả Windows, macOS và Linux.
    *   Đổi giá trị mặc định `SAVE_FOLDER` thành `""` (chuỗi rỗng), fallback về `os.getcwd()` để tránh lỗi đường dẫn không tồn tại trên máy khác.
    *   Hàm `combine.comb()` nhận thêm tham số `folder_path` để sử dụng cùng thư mục lưu với `main.py`.
    *   Bổ sung hướng dẫn cài FFmpeg trên macOS (`brew install ffmpeg`) và Linux (`sudo apt install ffmpeg`) vào `README.md`.
