# Backend Instructions

Đây là project backend của Pocket Ledger.

Trước khi sửa các task liên quan đến frontend:
- Luôn đọc tài liệu task trong `../docs`.
- Nếu task liên quan màn hình thống kê giao dịch, đọc file:
  `../docs/TASK_TRANSACTION_SUMMARY.md`

Nguyên tắc:
- Ưu tiên filter/tổng hợp dữ liệu ở backend thay vì bắt frontend tải toàn bộ dữ liệu.
- Giữ response cũ nếu có thể.
- Nếu thêm endpoint mới, cần ghi rõ request params và response mẫu.
- Nếu sửa endpoint cũ, cần đảm bảo không phá các màn hình khác.