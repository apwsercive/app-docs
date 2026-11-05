---
version: "1.0"
updated: 2026-11-05
status: draft
---

# YiSense Nguồn nội dung và phương pháp lập quẻ

## Nguồn và suy ngẫm {#1}

Classics.json đóng gói dựa trên [dữ liệu cổ văn meihua](https://github.com/toastedqu/meihua/blob/main/app/data/classics.json), ngày lấy2026-09-19, giữ liên kết Wikisource và mã sửa đổi từng quẻ (Càn:2404991). Chỉ lấy cổ văn thuộc phạm vi công cộng, không lấy chú giải hiện đại của bên thứ ba. Quyền biên tập, dịch và ảnh hiện đại cần xét riêng. Gợi ý để suy ngẫm, không phải chú giải đầy đủ hay AI. Chủ đề ngày dùng thứ tự ngày trong lịch thiết bị: (thứ tự−1) mod 64, không phải dự đoán cá nhân.

## Đồng xu và số {#2}

Mỗi hào mô phỏng 3 đồng xu độc lập, có xác suất ngửa và sấp bằng nhau. Ngửa tính 3, sấp tính 2. Tổng 6 là lão âm, 7 là thiếu dương, 8 là thiếu âm, 9 là lão dương; xác suất lý thuyết lần lượt là 1/8, 3/8, 3/8 và 1/8. Lập 6 hào từ dưới lên; hào 6 và 9 đổi âm dương khi tạo quẻ biến. Phương pháp dùng số nhận 3 số nguyên dương từ 1 đến 1.000.000. Lấy số thứ nhất chia 8 để tìm thượng quái, số thứ hai chia 8 để tìm hạ quái, số thứ ba chia 6 để tìm hào động. Dùng số dư; dư 0 tính là 8 hoặc 6. Thứ tự là Càn, Đoài, Ly, Chấn, Tốn, Khảm, Cấn, Khôn. Hào được đánh số 1–6 từ dưới lên. Nếu cả ba ô đều trống, ứng dụng tự tạo ba số ngẫu nhiên từ 1 đến 999.

## Thời gian và giới hạn {#3}

Gọi S là tổng số thứ tự địa chi năm âm lịch (Tý = 1 đến Hợi = 12), số tháng âm lịch và ngày âm lịch; tháng nhuận dùng cùng số tháng. S chia 8 lấy dư để tìm thượng quái. Cộng số thứ tự chi giờ (Tý = 1 đến Hợi = 12) vào S để được T. T chia 8 lấy dư để tìm hạ quái, chia 6 lấy dư để tìm hào động. Dư 0 được xử lý như trên. Giờ Tý kéo dài từ 23:00 đến 01:00 nhưng ngày đổi lúc 00:00. Dùng giờ và múi giờ của thiết bị, gồm quy tắc giờ mùa hè của hệ thống; không hiệu chỉnh giờ mặt trời thực. Năm âm lịch đổi vào mùng một Tết, không phải Lập xuân; tháng âm lịch không được coi là trụ tháng theo tiết khí. Bản ghi lưu dữ liệu đầu vào, ngày giờ, múi giờ, giá trị 6 hào và phiên bản thuật toán (hiện là 1). Các trường phái có thể có quy tắc khác nhau; đây không phải dự đoán chắc chắn. Liên hệ [apw_service@163.com](mailto:apw_service@163.com).
