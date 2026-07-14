# GRADUATION INTERNSHIP - CAPSTONE PROJECT PROPOSAL

## 1. Tổng quan về Doanh nghiệp và Quy mô Vận hành (Enterprise Profile & Scale)
- Tên tổ chức giả lập: Công ty Cổ phần Công nghệ Tài chính X – đơn vị sở hữu và vận hành nền tảng ví điện tử X, nằm trong Top thị trường thanh toán số tại Việt Nam.
- Số lượng người dùng đăng ký (Registered Users): 5.5 triệu tài khoản.
- Lượng người dùng hoạt động hàng tháng (MAU): 2.2 triệu người dùng.
- Lượng người dùng hoạt động hàng ngày (DAU): 850,000 người dùng.
- Tải lượng hệ thống trung bình (Average Load): 600 TPS (Transactions Per Second).
- Tải lượng đỉnh (Peak Load): Hệ thống đạt mức từ 2,800 TPS đến 3,200 TPS vào các khung giờ cao điểm (11h30–13h00 thanh toán ăn trưa và 18h30–20h30 mua sắm, thanh toán hóa đơn gia đình) hoặc trong các ngày hội mua sắm trùng ngày (05/05, 06/06) khi triển khai các chiến dịch hoàn tiền toàn sàn.
---

## 2. Định nghĩa Kỹ thuật về Khách hàng Rời bỏ (Customer Churn Definition)
Để xây dựng một hệ thống dự đoán chính xác, mô hình kinh doanh của X phân loại một tài khoản người dùng thuộc nhóm Rời bỏ (Churned) khi tài khoản đó thỏa mãn ít nhất một trong các điều kiện kỹ thuật sau trong vòng 30 ngày liên tiếp:
- Không phát sinh bất kỳ giao dịch tài chính chủ động nào từ phía người dùng (bao gồm: Chuyển tiền, thanh toán hóa đơn điện/nước/internet, nạp tiền điện thoại, quét mã QR Code thanh toán tại quầy).
- Gặp lỗi giao dịch liên quan đến liên kết ngân hàng và ngay sau đó thực hiện hành vi hủy liên kết (Unlink) toàn bộ các thẻ tài khoản Napas/Visa/Mastercard ra khỏi hệ thống ví.
- Thực hiện lệnh rút toàn bộ số dư khả dụng (Available Balance) về tài khoản ngân hàng gốc và duy trì số dư ví ở mức bằng 0 VND, đồng thời không phát sinh lượt mở ứng dụng (App Open).
---

## 3. Thực trạng Kinh doanh và Thiệt hại Tài chính (Business Impact)
- Tỷ lệ rời bỏ hiện tại (Monthly Churn Rate): Trung bình 4.2% mỗi tháng trên tổng lượng người dùng hoạt động (MAU), tương đương với việc doanh nghiệp mất đi khoảng 92,400 người dùng hoạt động sau mỗi chu kỳ 30 ngày.
- Chi phí thu hút một khách hàng mới (CAC - Customer Acquisition Cost): Ước tính khoảng 180,000 VND cho mỗi người dùng đăng ký và định danh (KYC) thành công (bao gồm chi phí quảng cáo, tặng voucher chào mừng).
- Chi phí giữ chân một khách hàng cũ có dấu hiệu rời bỏ (Retention Cost): Chỉ tiêu tốn khoảng 35,000 VND dưới dạng phân phối mã giảm giá trúng đích hoặc ưu đãi hoàn tiền dịch vụ thiết yếu.
- Hệ quả tài chính: Việc không chủ động phát hiện sớm khiến doanh nghiệp liên tục phải dùng ngân sách CAC lớn để bù đắp lượng người dùng sụt giảm. Tổn thất trực tiếp từ việc giảm doanh thu phí chiết khấu giao dịch (Take Rate) kết hợp với việc lãng phí ngân sách Marketing đại trà lên tới 16.6 tỷ VND mỗi tháng.
---

## 4. Hạ tầng Kỹ thuật Hiện tại và Lỗ hổng Hệ thống (Legacy Technical Gaps)
- Hệ thống hiện tại của X đang vận hành trên kiến trúc phân nhánh nhưng cơ sở dữ liệu lưu trữ lịch sử giao dịch và log hành vi người dùng vẫn tập trung tại một cụm Database quan hệ (PostgreSQL) cốt lõi. Các lỗ hổng kỹ thuật bao gồm:
- Độ trễ dữ liệu quá lớn (Batch Processing Lag): Quy trình phân tích churn hiện tại sử dụng các tiến trình chạy ngầm định kỳ (Cron-jobs) quét dữ liệu vào lúc 1h30 sáng mỗi ngày. Hệ thống thực hiện các câu lệnh SQL Query phức tạp để lọc ra những User không có hoạt động trong 30 ngày qua. Kết quả là danh sách gửi sang bộ phận Marketing bị trễ từ 1 đến 30 ngày, thời điểm người dùng thực tế đã gỡ ứng dụng khỏi thiết bị.
- Xung đột tài nguyên hệ thống (Resource Contention): Khi lượng giao dịch tăng trưởng, việc chạy các câu lệnh SQL Query quét hàng triệu dòng lịch sử để phân tích hành vi gây ra hiện tượng khóa bảng (Table Locking). Điều này làm nghẽn và tăng thời gian phản hồi (Latency) của luồng thanh toán cốt lõi, trực tiếp gây ra lỗi sập giao dịch (Transaction Timeout) cho các khách hàng đang mua sắm thực tế vào giờ cao điểm.
- Mất đồng bộ dữ liệu (Online-Offline Feature Drift): Đội ngũ dữ liệu xây dựng mô hình AI trên môi trường thử nghiệm (Offline) với dữ liệu lịch sử đã qua làm sạch, nhưng khi triển khai thực tế dưới dạng một API phục vụ (Online Serving), cấu trúc dữ liệu thô (raw JSON) gửi từ Mobile App lên không đồng nhất về định dạng và thời gian tính toán, dẫn đến tỷ lệ dự đoán sai (False Positive) vượt mức 35%, gây phân phối nhầm Voucher cho các user đang hoạt động bình thường.
---