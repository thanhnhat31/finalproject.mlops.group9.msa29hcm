# GRADUATION INTERNSHIP - CAPSTONE PROJECT PROPOSAL

## 1. High-Level Architecture Overview
Hệ thống được chia thành 4 tầng logic, độc lập với nhau, hoạt động bất đồng bộ giữa luồng xử lý giao dịch lõi và luồng phục vụ trí tuệ nhân tạo nhằm tối ưu hóa hiệu năng.
- Tầng Thu thập & Xử lý luồng dữ liệu (Data Ingestion & Streaming Layer)
- Tầng Quản lý Đặc trưng & Lưu trữ (Feature Store & Storage Layer)
- Tầng Phục vụ Mô hình & Điều phối (Model Serving & Orchestration Layer)
- Tầng Tự động hóa MLOps & Giám sát (MLOps & Observability Layer)

---

## 2. Architecture Tier Details

### 2.1. Tầng Thu thập & Xử lý luồng dữ liệu (Data Ingestion & Streaming Layer)
- **Vai trò & Chức năng**: Tiếp nhận, phân loại và xử lý liên tục toàn bộ luồng sự kiện hành vi (Clickstream) cùng trạng thái giao dịch phát sinh từ phía người dùng theo thời gian thực (Real-time stream aggregation).
- **Bài toán & Vấn đề giải quyết**: * Triệt tiêu hoàn toàn Độ trễ dữ liệu quá lớn (Batch Processing Lag) của hệ thống cũ.
  - Thay vì chạy các tiến trình ngầm (Cron-jobs) quét database vào ban đêm gây trễ thông tin từ 1 đến 30 ngày, tầng này bóc tách dữ liệu và phát hiện dấu hiệu bất thường ngay tại thời điểm người dùng gặp sự cố hoặc có hành vi tiêu cực trên ứng dụng.
- **Các thành phần bên trong:**
  - **AWS Application Load Balancer / API Gateway**: Tiếp nhận traffic và điều hướng các gói dữ liệu JSON gửi từ Mobile App lên.
  - **Amazon MSK (Managed Streaming for Apache Kafka)**: Hàng đợi tin nhắn phân tán đóng vai trò tiếp nhận luồng sự kiện thô khổng lồ. Cấu hình Cluster chạy trên nhiều vùng khả dụng (Multi-AZ) với Replication Factor = 2 và Partitioning (phân vùng) dựa trên khóa user_id để đảm bảo tính tuần tự của dữ liệu.
  - **Amazon Managed Service for Apache Flink**: Công cụ tính toán luồng có trạng thái (Stateful Stream Processing). Flink sẽ "lắng nghe" Kafka để tính toán trực tiếp các đặc trưng động theo cửa sổ thời gian trượt (Sliding Windows như 1 giờ, 24 giờ, 7 ngày).

### 2.2. Tầng Quản lý Đặc trưng & Lưu trữ (Feature Store & Storage Layer)
- **Vai trò & Chức năng**: Quản lý, lưu trữ tập trung và nhất quán định nghĩa của các đặc trưng dữ liệu (Features). Tầng này có nhiệm vụ đồng bộ và phân phối các đặc trưng này ra hai kho lưu trữ riêng biệt phục vụ cho hai mục đích khác nhau (Huấn luyện và Dự đoán).
- **Bài toán & Vấn đề giải quyết**: * Giải quyết triệt để bài toán Xung đột tài nguyên hệ thống (Resource Contention) bằng cách cô lập hoàn toàn cơ sở dữ liệu Core Banking khỏi các truy vấn AI.
  - Khắc phục lỗi Mất đồng bộ dữ liệu (Online-Offline Feature Drift) – nguyên nhân chính khiến hệ thống cũ dự đoán sai lệch tới 35% do cấu trúc dữ liệu khi huấn luyện mô hình và khi chạy thực tế không trùng khớp.
- **Các thành phần bên trong**:
  - **Feast Feature Store**: Nền tảng quản lý mã nguồn đặc trưng tập trung, đảm bảo một định nghĩa dữ liệu duy nhất được áp dụng chung cho cả môi trường phát triển và môi trường production.
  - **Amazon ElastiCache for Redis (Online Store)**: Kho lưu trữ bộ nhớ đệm (RAM) dạng Key-Value theo user_id. Nhận dữ liệu tính toán trực tiếp từ Flink và đảm bảo tốc độ truy xuất đặc trưng (Lookup Latency) siêu nhanh dưới 5ms phục vụ cho việc chấm điểm churn thời gian thực.
  - **Amazon S3 / Amazon RDS for PostgreSQL Partitioned (Offline Store)**: Kho lưu trữ dữ liệu lịch sử nén dung lượng lớn, phục vụ riêng cho đội ngũ Data Science trích xuất dữ liệu huấn luyện lại mô hình mà không làm ảnh hưởng đến tiến trình vận hành thực tế.

### 2.3. Tầng Phục vụ Mô hình & Điều phối (Model Serving & Orchestration Layer)
- **Vai trò & Chức năng**: Tiếp nhận các yêu cầu truy vấn từ hệ thống CRM hoặc từ ứng dụng, tự động lấy đặc trưng từ Feature Store, đưa vào mô hình Machine Learning để chấm điểm rủi ro rời bỏ (Churn Score) và trả về kết quả nhằm kích hoạt các kịch bản giữ chân khách hàng phù hợp.
- **Bài toán & Vấn đề giải quyết**: * Khắc phục tình trạng Nghẽn tải, sập API và phản hồi chậm (> 300ms) của hệ thống cũ khi gặp đỉnh tải cao điểm (Peak load vọt lên từ 2,800 TPS đến 3,200 TPS).
  - Giữ vững cam kết dịch vụ khắt khe của hệ thống tài chính: SLA P95 Response Latency < 80ms dưới mức áp lực giả lập 2,000 requests/giây.
- **Các thành phần bên trong**:
  - **FastAPI Stateless Microservice**: Dịch vụ API được viết bằng mã nguồn bất đồng bộ (async/await) để tối ưu hóa năng lực xử lý non-blocking I/O.
  - **Mô hình LightGBM (ONNX Runtime)**: Mô hình AI phân loại dạng Tree-based siêu nhẹ (< 20MB) được biên dịch sang định dạng ONNX giúp tăng tốc độ chạy Inference xuống dưới 15ms, tiêu thụ cực ít RAM/CPU so với các kiến trúc Deep Learning phức tạp.
  - **Amazon EKS (Elastic Kubernetes Service)**: Hệ thống điều phối container quản lý các Pod chứa FastAPI. Cấu hình Horizontal Pod Autoscaler (HPA) phối hợp với Cluster Autoscaler để tự động nhân bản số lượng Pods (từ 3 lên tối đa 30 Pods) và tự động mua thêm tài nguyên phần cứng từ AWS khi traffic tăng đột biến.

### 2.4. Tầng Tự động hóa MLOps & Giám sát (MLOps & Observability Layer)
- **Vai trò & Chức năng**: Giám sát liên tục hiệu năng và độ ổn định kỹ thuật của toàn hệ thống; đồng thời quản lý vòng đời của mô hình AI, tự động hóa quy trình đóng gói, kiểm thử và tái huấn luyện mô hình khi có sự cố suy giảm chất lượng dữ liệu.
- **Bài toán & Vấn đề giải quyết**: * Giải quyết hiện tượng Suy giảm chất lượng mô hình theo thời gian (Model Drift / Data Drift) do hành vi của người dùng thay đổi hoặc do tính mùa vụ, điều mà hệ thống cũ hoàn toàn "mù" do triển khai thủ công và không có cơ chế giám sát.
- **Các thành phần bên trong**:
  - **Evidently AI**: Công cụ chuyên dụng liên tục đo lường khoảng cách phân phối giữa dữ liệu thực tế (Online) và dữ liệu huấn luyện quá khứ (Offline) để tự động phát hiện độ lệch (Drift).
  - **GitHub Actions Workflow & ArgoCD**: Hệ thống CI/CD tự động kích hoạt vòng lặp Continuous Training (CT) khi nhận cảnh báo từ Evidently AI. Quy trình này tự động bốc dữ liệu từ S3, tự động train lại mô hình, đóng gói thành Docker Image mới và triển khai lên Kubernetes theo chiến lược Canary Deployment (chuyển trước 10% tải để thử nghiệm an toàn).
  - **Prometheus & Grafana**: Hệ thống thu thập chỉ số và hiển thị Dashboard trực quan (theo dõi CPU, RAM, Error Rate, Tải RPS, và đặc biệt là chỉ số thời gian phản hồi P95).
---

## 3. Architecture Diagram
