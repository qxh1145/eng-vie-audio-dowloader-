import sys
import Parser
import os, time
import playsound
import combine
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')


def clear_screen():
	"""Xóa màn hình terminal, hỗ trợ đa nền tảng (Windows/macOS/Linux)."""
	os.system('cls' if os.name == 'nt' else 'clear')


native = "vietnamese" 
SAVE_FOLDER = os.getenv('FOLDER_PATH') or "" #để trống thì mặc định lưu tại folder hiện tại
# Khai báo các hằng số mã màu để dễ quản lý và tái sử dụng
C_CYAN = "\033[96m"   # Xanh dương nhạt
C_GREEN = "\033[92m"  # Xanh lá
C_RED = "\033[91m"    # Đỏ
C_YELLOW = "\033[93m" # Vàng
C_RESET = "\033[0m"   # Reset về màu mặc định của terminal


clear_screen()
playing = 1
folder_path = SAVE_FOLDER if SAVE_FOLDER else os.getcwd()

if SAVE_FOLDER and not os.path.exists(SAVE_FOLDER):
	os.makedirs(SAVE_FOLDER)

def commands(word):
	global playing, folder_path
	if word == '/m':
		playing = 1 - playing


		if playing:
			print("\033[92mTự đông phát âm thanh: \033[96mBật")
		else:
			print("\033[92mTự đông phát âm thanh: \033[96mTắt")
	elif word == '/r':
		mp3_files = [f for f in os.listdir(folder_path) if f.endswith('.mp3')]
		for mp3_file in mp3_files:
			print(f'\033[96m{mp3_file}\033[96m\033[92m đã được bay vào thùng rác')
			os.remove(os.path.join(folder_path, mp3_file))

		print("\033[93mĐã xóa tất cả file audio\033[93m\n")
	elif word == '/cp':
		print(f"{C_CYAN}Đường dẫn hiện tại: {C_YELLOW}{folder_path}{C_RESET}")
		new_path = input(f'{C_GREEN}Nhập đường dẫn mới (để trống để giữ nguyên): {C_YELLOW}').strip()
		print(C_RESET, end='')
		if new_path:
			# Loại bỏ dấu ngoặc kép bao quanh nếu người dùng dán từ Explorer
			new_path = new_path.strip('"').strip("'")
			if not os.path.exists(new_path):
				try:
					os.makedirs(new_path)
					print(f"{C_GREEN}Đã tạo thư mục mới: {C_YELLOW}{new_path}{C_RESET}")
				except Exception as e:
					print(f"{C_RED}Lỗi: Không thể tạo thư mục '{new_path}': {e}{C_RESET}")
					Start()
					return 0
			if not os.path.isdir(new_path):
				print(f"{C_RED}Lỗi: '{new_path}' không phải là một thư mục hợp lệ.{C_RESET}")
				Start()
				return 0
			folder_path = os.path.abspath(new_path)
			print(f"{C_GREEN}✔ Đã đổi thư mục lưu thành: {C_YELLOW}{folder_path}{C_RESET}")
		else:
			print(f"{C_CYAN}Giữ nguyên đường dẫn: {C_YELLOW}{folder_path}{C_RESET}")
	else:
		print("\033[91mLệnh không hợp lệ\033[91m")

	Start()
	return 0


def Start():
	global playing, folder_path

	# Xác định màu sắc và text cho trạng thái linh hoạt
	status_color = C_GREEN if playing else C_RED
	status_text = "BẬT" if playing else "TẮT"

	# In khối menu điều khiển
	print(f"{C_CYAN}================ MENU ĐIỀU KHIỂN ================={C_RESET}")
	print(f"{C_CYAN}▶ Trạng thái Auto-play: {status_color}[ {status_text} ]{C_RESET}")
	print(f"{C_CYAN}▶ Lưu tại: {C_YELLOW}{folder_path}{C_RESET}")
	print(f"{C_CYAN}▶ Nhập {C_YELLOW}[/m]{C_CYAN}      : Bật / Tắt âm thanh{C_RESET}")
	print(f"{C_CYAN}▶ Nhập {C_YELLOW}[/r]{C_CYAN}      : Xóa toàn bộ file audio{C_RESET}")
	print(f"{C_CYAN}▶ Nhập {C_YELLOW}[/cp]{C_CYAN}     : Đổi thư mục lưu audio{C_RESET}")
	print(f"{C_CYAN}▶ Nhấn {C_YELLOW}[Ctrl+C]{C_CYAN}  : Thoát chương trình{C_RESET}")
	print(f"{C_CYAN}=================================================={C_RESET}\n")

	word = input('\033[95mNhập từ cần tải audio: \033[91m').strip()

	start = time.time()

	for ele in '''!()[]{};:'",<>.?@#$%^&*_~''':
		word = word.replace(ele, "")

	if(len(word) == 0):
		clear_screen()
		Start()

	if word[0] == '/':
		commands(word)

	clear_screen()
	print(word)
	
	save_path = os.path.join(folder_path, f"{word}.mp3")
	
	print("\033[92mĐang tải..\033[92m")
	
	

	Parser.define(word, save_path, 0, 1, 'english')

	if os.path.exists(save_path):
		if playing:
			playsound.playsound(save_path, True)
	else:
		print("\033[91mKhông tìm thấy từ này\033[91m")
		
		if (combine.comb(word, folder_path) and playing):
			
			playsound.playsound(save_path, True)


	# Hiển thị bản dịch tiếng Việt
	try:
		translations = Parser.get_translation(word, f"english-{native}")
		if translations:
			print(f"\n{C_CYAN}{'─' * 50}")
			print(f"BẢN DỊCH TIẾNG VIỆT CHO: {word.upper()}{C_RESET}")
			print(f"{C_CYAN}{'─' * 50}{C_RESET}")
			for group in translations:
				if group["pos"]:
					print(f"\n  {C_YELLOW}[{group['pos']}]{C_RESET}")
				for i, entry in enumerate(group["entries"], 1):
					if entry["en_def"]:
						print(f"  {C_CYAN}{i}. {entry['en_def']}{C_RESET}")
					if entry["vi_trans"]:
						print(f"     {C_GREEN}→ {entry['vi_trans']}{C_RESET}")
			print(f"{C_CYAN}{'─' * 50}{C_RESET}")
	except:
		pass

	print("\n\033[93m{:.2f}".format(time.time() - start) + " sec")
	print('\n')

	Start()

if __name__ == "__main__":
	Start()