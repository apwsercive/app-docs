---
version: "1.0"
updated: 2026-11-03
status: draft
---

# YiSense Nguồn nội dung và phương pháp lập quẻ

## Nguồn và suy ngẫm {#1}

Classics.json đóng gói dựa trên [dữ liệu cổ văn meihua](https://github.com/toastedqu/meihua/blob/main/app/data/classics.json), ngày lấy2026-09-19, giữ liên kết Wikisource và mã sửa đổi từng quẻ (Càn:2404991). Chỉ lấy cổ văn thuộc phạm vi công cộng, không lấy chú giải hiện đại của bên thứ ba. Quyền biên tập, dịch và ảnh hiện đại cần xét riêng. Gợi ý để suy ngẫm, không phải chú giải đầy đủ hay AI. Chủ đề ngày dùng thứ tự ngày trong lịch thiết bị: (thứ tự−1) mod 64, không phải dự đoán cá nhân.

## Đồng xu và số {#2}

Mỗi hào mô phỏng3 đồng xu độc lập công bằng: mặt ngửa3, sấp2. Tổng6 lão âm,7 thiếu dương,8 thiếu âm,9 lão dương có xác suất lý thuyết1/8,3/8,3/8,1/8. Lập6 hào từ dưới lên;6 và9 đổi âm dương. Ba số nguyên1–1.000.000: số thứ nhất mod 8 chọn thượng quái, thứ hai mod 8 hạ quái, thứ ba mod 6 hào động. Dư0 tính8 hoặc6. Thứ tự Càn, Đoài, Ly, Chấn, Tốn, Khảm, Cấn, Khôn; hào1–6 từ dưới lên. Trống cả ba thì tự sinh số1–999.

## Thời gian và giới hạn {#3}

S=thứ tự địa chi năm âm lịch (Tý1–Hợi12)+tháng âm+ngày âm; tháng nhuận giữ số tháng. S mod 8 chọn thượng quái. T=S+thứ tự giờ chi (Tý1–Hợi12); T mod 8 chọn hạ quái, T mod 6 hào động. Dư0 như trên. Giờ Tý23:00–01:00 nhưng đổi ngày00:00. Dùng giờ và múi giờ thiết bị, kể cả quy tắc giờ mùa hè hệ thống; không chỉnh giờ mặt trời thật. Đổi năm vào Tết âm lịch, không theo Lập Xuân; không dùng trụ tháng tiết khí. Lưu đầu vào, ngày giờ, múi giờ,6 hào và thuật toán phiên bản1. Các trường phái có thể khác; đây không phải dự đoán chắc chắn. Liên hệ [apw_service@163.com](mailto:apw_service@163.com).
