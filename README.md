# Cambridge Dictionary Audio <img align="center" width="38px" src="Design/logo.png" />

> **⚠️ DÀNH CHO CÁC AI AGENT:**
> **Luôn luôn đọc hướng dẫn trong file `AGENT.md` đầu tiên trước khi thực hiện bất kỳ chỉnh sửa nào trong codebase này.**

Đây là một chương trình bằng Python chạy trên Terminal (Command Line), giúp bạn:
1. Tải **file audio phát âm (giọng UK)** chuẩn từ [dictionary.cambridge.org](https://dictionary.cambridge.org) và tự động phát âm thanh.
2. Hiển thị **bản dịch Tiếng Việt** có cấu trúc rõ ràng (định nghĩa, phân loại từ) ngay trên màn hình terminal.
3. Hỗ trợ tra từ đơn lẻ hoặc cả cụm từ (tự động nối file audio).

<img src="Design/Presen.gif" width="800"/>

---

## 🛠 Yêu cầu hệ thống (Prerequisites)

Để chạy chương trình này bằng mã nguồn, máy tính của bạn cần cài đặt:
- **Python 3.7+** (đã check "Add Python to PATH" khi cài đặt).
- *(Tùy chọn)* **FFmpeg**: Cần thiết nếu bạn muốn sử dụng tính năng tra **cụm từ** (ghép nhiều file audio lại với nhau). Tải FFmpeg và thêm vào biến môi trường PATH của hệ điều hành.

## 🚀 Hướng dẫn Cài đặt & Chạy

**Bước 1:** Tải dự án này về máy (Download ZIP hoặc dùng `git clone`).

**Bước 2:** Mở Terminal (hoặc Command Prompt / PowerShell) tại thư mục chứa dự án, cài đặt các thư viện bắt buộc:

**Dành cho Windows:**
```sh
pip install -r requirements.txt
```

**Dành cho macOS / Linux:**
```sh
pip3 install -r requirements.txt
```

**Bước 3:** Khởi chạy chương trình

**Dành cho Windows:**
Bạn có thể click đúp vào file `start.bat` để khởi chạy nhanh, hoặc gõ lệnh:
```sh
python main.py
```

**Dành cho macOS / Linux:**
Mở Terminal và gõ lệnh:
```sh
python3 main.py
```

## 📖 Hướng dẫn Sử dụng

Sau khi khởi chạy, chương trình sẽ hiển thị Menu điều khiển. Bạn chỉ cần **nhập từ tiếng Anh hoặc cụm từ** cần tra vào và nhấn Enter. 
Chờ 1-2 giây, file `.mp3` sẽ được tải về, âm thanh sẽ tự động phát và bản dịch tiếng Việt sẽ hiển thị.

**Các lệnh điều khiển đặc biệt (nhập vào ô tìm kiếm):**

- `/m` : Bật hoặc Tắt tính năng tự động phát âm thanh ngay sau khi tải.
- `/r` : Xóa toàn bộ các file `.mp3` đã được tải về trong thư mục lưu trữ để giải phóng dung lượng.
- Nhấn `Ctrl + C` để thoát chương trình.

## ⚙️ Cấu hình Thư mục Lưu Audio
Mặc định, các file `.mp3` tải về sẽ nằm chung thư mục với code. Nếu bạn muốn lưu sang chỗ khác (ví dụ: `D:\Audio`), hãy mở file `main.py` và sửa dòng sau ở đầu file:
```python
SAVE_FOLDER = r"D:\Audio"
```
