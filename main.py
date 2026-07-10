import os
import subprocess

def full_check():
    print("=== BỘ CÔNG CỤ KIỂM TRA ROOT TOÀN DIỆN ===")
    
    # 1. Quét Kernel (Tiến trình UID 0)
    print("\n[1/3] Đang quét tầng Kernel...")
    found_root_kernel = False
    try:
        procs = [d for d in os.listdir('/proc') if d.isdigit()]
        for pid in procs:
            with open(f'/proc/{pid}/status', 'r') as f:
                if any('Uid:	0' in line for line in f):
                    if int(pid) > 100: found_root_kernel = True
    except: pass
    print(f"-> Kết quả: {'PHÁT HIỆN DẤU VẾT ROOT' if found_root_kernel else 'Sạch'}")

    # 2. Quét Cấu hình Hệ thống (Properties)
    print("\n[2/3] Đang quét tầng Hệ thống...")
    found_root_prop = False
    props = ['ro.build.tags', 'ro.debuggable', 'ro.secure']
    for prop in props:
        try:
            val = subprocess.check_output(['getprop', prop]).decode().strip()
            if 'test-keys' in val or val == '1' and prop == 'ro.debuggable':
                found_root_prop = True
        except: pass
    print(f"-> Kết quả: {'PHÁT HIỆN DẤU VẾT ROOT' if found_root_prop else 'Sạch'}")

    # 3. Quét File thực thi (Binaries)
    print("\n[3/3] Đang quét tầng Binaries...")
    found_root_bin = False
    bin_paths = ['/sbin/su', '/system/bin/su', '/system/xbin/su', '/data/local/xbin/su']
    for path in bin_paths:
        if os.path.exists(path):
            found_root_bin = True
            print(f"-> Tìm thấy file đáng ngờ: {path}")
    print(f"-> Kết quả: {'PHÁT HIỆN DẤU VẾT ROOT' if found_root_bin else 'Sạch'}")

    # Tổng kết
    print("\n" + "="*40)
    if found_root_kernel or found_root_prop or found_root_bin:
        print("KẾT LUẬN CUỐI CÙNG: HỆ THỐNG CÓ DẤU HIỆU ĐÃ ROOT!")
    else:
        print("KẾT LUẬN CUỐI CÙNG: MÁY SẠCH (CHƯA PHÁT HIỆN ROOT).")

full_check()
```[span_0](start_span)[span_0](end_span)

