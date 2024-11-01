# Floodlight-SDN-StaticEntryPusherAPI
0. Bài toán: XÂY DỰNG MỘT TOPO THỬ NGHIỆM CÓ ÍT NHẤT 10 SWITCHES TRÊN MININET. XÂY DỰNG ỨNG DỤNG (SDN APP) CHO PHÉP ĐỊNH TUYẾN DỮ LIỆU GIỮA 2 ĐIỂM NGUỒN ĐÍCH BẤT KỲ THEO MỘT ĐƯỜNG ĐI THEO MỘT TUYẾN ĐƯỜNG DO NGƯỜI DÙNG NHẬP VÀO.
1. Môi trường thử nghiệm
- 01 Server (192.168.58.154) chạy mininet để giả lập (bao gồm mininet cli và miniedit, sử dụng ovsk, protocols OpenFlow13)
- 01 Server (192.168.58.155:6653) chạy Floodlight SDN Controller
- Mô tả:
  ![image](https://github.com/user-attachments/assets/be912257-bf0e-490d-8e39-78e1b640875f)
2. Về ứng dụng: Sử dụng các thư viện Python (Python 3.11.9) để sử dụng các API do Floodlight cung cấp để thực hiện định tuyến 
3. Về Static Entry Pusher API: https://floodlight.atlassian.net/wiki/spaces/floodlightcontroller/pages/1343518/Static+Entry+Pusher+API
4. Hình ảnh mô tả đầu vào, đầu ra:
![example](https://github.com/user-attachments/assets/1b84233a-7a0d-41d5-bc1e-06c830a9a71f)
5. File chính chạy chương trình: entrypusher.py
6. Video hướng dẫn cài đặt Mininet để mô phỏng mạng topology: https://www.youtube.com/watch?v=QgGuqJ4bxHw&feature=youtu.be
