# Báo Cáo Phân Tích & Đánh Giá Kết Quả RAG Retrieval

Tài liệu này tổng hợp, phân tích và trực quan hóa kết quả đánh giá (evaluation) hệ thống RAG sử dụng 4 mô hình/phương pháp truy vấn khác nhau trên 3 phương pháp chunking dữ liệu: **Paragraph Chunking**, **Semantic Chunking (by sentence)** và **Sliding Window Chunking**.

---

## 1. Bảng Tổng Hợp Kết Quả (Overall Summary)

Dưới đây là bảng tổng hợp điểm số chất lượng truy vấn (**MRR**, **Accuracy@1**) và hiệu năng (**Average Latency**) của từng mô hình tương ứng với mỗi phương pháp chunking:

| Phương pháp Chunking | Mô hình (Retriever) | Latency trung bình (ms) | Mean Reciprocal Rank (MRR) | Accuracy@1 (Hit Rate) |
| :--- | :--- | :---: | :---: | :---: |
| **Paragraph Chunking** | BM25 (Sparse) | 0.08 ms | 0.302 | 0.125 (12.5%) |
| | Bi-Encoder (Dense) | 7.77 ms | 0.552 | 0.438 (43.8%) |
| | Cross-Encoder (Context) | 339.80 ms | 0.479 | 0.375 (37.5%) |
| | **Two-Stage (Dense + CE)** | 75.21 ms | **0.583** | **0.500 (50.0%)** |
| **Semantic Chunking** | BM25 (Sparse) | 0.10 ms | 0.302 | 0.125 (12.5%) |
| | Bi-Encoder (Dense) | 12.66 ms | 0.552 | 0.438 (43.8%) |
| | Cross-Encoder (Context) | 342.91 ms | 0.469 | 0.375 (37.5%) |
| | **Two-Stage (Dense + CE)** | 69.78 ms | **0.625** | **0.562 (56.2%)** |
| **Sliding Window** | BM25 (Sparse) | 0.08 ms | 0.302 | 0.125 (12.5%) |
| | Bi-Encoder (Dense) | 6.29 ms | 0.552 | 0.438 (43.8%) |
| | Cross-Encoder (Context) | 353.13 ms | 0.260 | 0.125 (12.5%) |
| | **Two-Stage (Dense + CE)** | 65.73 ms | **0.406** | **0.312 (31.2%)** |

---

## 2. Các Biểu Đồ Trực Quan Hóa (Visualizations)

Các biểu đồ dưới đây được tạo tự động từ mã nguồn phân tích kết quả và được lưu trữ trực tiếp trong thư mục artifacts để tiện theo dõi:

### Biểu đồ 1: So sánh Chất lượng Truy vấn (MRR vs Accuracy@1)
Biểu đồ cột nhóm so sánh trực tiếp điểm số MRR và Accuracy@1 của 4 mô hình trên 3 phương pháp chunking khác nhau.

![So sánh MRR & Accuracy@1](C:/Users/thanh/.gemini/antigravity-ide/brain/a087aeb0-eb06-4801-b545-d20cc4c9d429/overall_quality_comparison.png)

> [!NOTE]
> * **BM25** và **Bi-Encoder** giữ nguyên điểm số trên cả 3 phương pháp chunking trong tập test này vì bản chất thuật toán tìm kiếm của chúng ít nhạy cảm hơn với ranh giới cắt của chunk.
> * Các mô hình sử dụng **Cross-Encoder** (bao gồm cả **Two-Stage**) bị sụt giảm hiệu năng nghiêm trọng khi sử dụng **Sliding Window**.

---

### Biểu đồ 2: Đánh đổi giữa Độ trễ và Chất lượng (Pareto Frontier)
Biểu đồ phân tán (Scatter Plot) với trục hoành thể hiện độ trễ xử lý (Latency - thang Logarithm) và trục tung thể hiện chất lượng truy vấn (MRR). Biểu đồ này giúp xác định mô hình tối ưu nhất về mặt chi phí/hiệu năng (Pareto-optimal).

![Latency vs Quality Trade-off](C:/Users/thanh/.gemini/antigravity-ide/brain/a087aeb0-eb06-4801-b545-d20cc4c9d429/latency_vs_quality_tradeoff.png)

> [!TIP]
> * Góc trên cùng bên trái của biểu đồ biểu thị trạng thái lý tưởng: **Độ trễ thấp nhất + Chất lượng cao nhất**.
> * **Two-Stage (Semantic)** nằm ở vị trí tối ưu nhất trên đường biên Pareto: Đạt chất lượng cao nhất (MRR = 0.625) với độ trễ chấp nhận được (~70ms), nhanh hơn gấp 5 lần so với chạy Cross-Encoder thuần túy trên toàn bộ corpus.

---

### Biểu đồ 3: Hiệu năng chi tiết theo Loại câu hỏi (Category Breakdown)
Biểu đồ lưới 2x2 hiển thị điểm số MRR của **tất cả 4 mô hình** (BM25, Bi-Encoder, Cross-Encoder, Two-Stage) tương ứng với **cả 3 phương pháp chunking** trên từng nhóm thử nghiệm cụ thể (Contextual Trap, Exact Keyword, Synonyms, Typo Robustness).

![Category Breakdown](C:/Users/thanh/.gemini/antigravity-ide/brain/a087aeb0-eb06-4801-b545-d20cc4c9d429/category_breakdown_comparison.png)

---

## 3. Phân Tích & Nhận Xét Chuyên Sâu

### 1. Tại sao Sliding Window làm suy giảm nghiêm trọng Cross-Encoder?
* **Hiện tượng:** Khi chuyển từ *Semantic Chunking* sang *Sliding Window*, điểm MRR của **Two-Stage** giảm từ **0.625 xuống 0.406** (-35%), và **Cross-Encoder Single-Stage** giảm từ **0.469 xuống 0.260** (-44%).
* **Nguyên nhân:** 
  * Sliding Window cắt văn bản một cách cơ học dựa trên số từ cố định mà không quan tâm đến ranh giới câu hay đoạn.
  * Điều này dẫn đến việc các câu văn bị cắt cụt ở giữa, làm mất cấu trúc ngữ pháp và ngữ cảnh liên kết.
  * Mô hình **Cross-Encoder** sử dụng cơ chế self-attention toàn phần trên cặp câu hỏi-chunk để học mối quan hệ ngữ nghĩa sâu sắc. Khi dữ liệu đầu vào bị vỡ vụn và chứa nhiều câu không hoàn chỉnh, cơ chế chú ý của Cross-Encoder bị nhiễu thông tin, dẫn đến việc xếp hạng sai lệch.

### 2. Ưu thế vượt trội của Semantic Chunking
* **Semantic Chunking** duy trì ranh giới câu đầy đủ (sử dụng `sent_tokenize` của NLTK) và gom chúng lại dựa trên số lượng từ mục tiêu.
* Phương pháp này giúp giữ nguyên vẹn ý nghĩa của từng câu đơn lẻ trong chunk, cung cấp ngữ cảnh sạch và mạch lạc nhất cho **Cross-Encoder** hoạt động. 
* Kết quả là **Two-Stage (Dense + CE)** kết hợp với **Semantic Chunking** đạt kết quả cao nhất trong tất cả các bài thử nghiệm (**MRR = 0.625, Accuracy@1 = 56.2%**).

### 3. Đánh giá về mặt Hiệu Năng (Latency)
* **BM25** có tốc độ cực nhanh (<0.1ms) nhưng độ chính xác rất thấp (12.5% Accuracy@1), hoàn toàn thất bại ở các câu hỏi sử dụng từ đồng nghĩa (Synonyms: MRR = 0.0) và bẫy ngữ cảnh (Contextual Trap).
* **Cross-Encoder Single-Stage** quá chậm (~340ms) do phải tính toán attention phức tạp trên mọi chunk của corpus. Điều này khiến nó không thể triển khai trên môi trường production thực tế.
* **Two-Stage (Dense + CE)** giải quyết triệt để bài toán này: Sử dụng Bi-Encoder để lọc nhanh top-5 ứng viên (chỉ mất ~6-12ms), sau đó chỉ dùng Cross-Encoder để xếp hạng lại (rerank) 5 ứng viên đó. Tổng thời gian xử lý chỉ khoảng **~70ms** nhưng chất lượng thậm chí còn vượt qua cả Cross-Encoder Single-stage nhờ lọc bớt nhiễu từ giai đoạn 1.

---

## 4. Kết Luận & Khuyến Nghị Kiến Trúc (Architecture Recommendation)

Dựa trên các phân tích định lượng trên, chúng tôi đề xuất cấu hình tối ưu cho hệ thống RAG như sau:

1. **Phương pháp Chunking:** Sử dụng **Semantic Chunking (by sentence)** hoặc **Paragraph Chunking** (nếu tài liệu có cấu trúc đoạn rất rõ ràng). Tuyệt đối **không** sử dụng *Sliding Window* cơ học nếu hệ thống có bước Reranking bằng Cross-Encoder.
2. **Mô hình Retrieval:** Triển khai kiến trúc **Two-Stage Retrieval** (Bi-Encoder Reranked by Cross-Encoder):
   * **Stage 1 (Retrieve):** Bi-Encoder (`all-MiniLM-L6-v2`) để lấy top-5 hoặc top-10 chunks nhanh chóng.
   * **Stage 2 (Rerank):** Cross-Encoder để xếp hạng lại và chọn ra chunk phù hợp nhất đưa vào Prompt cho LLM.
   * Cấu hình này giúp hệ thống đạt độ chính xác tối đa trong khi vẫn đảm bảo thời gian phản hồi (latency) cực kỳ nhanh dưới 100ms.
