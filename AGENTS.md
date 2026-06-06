# Backend Instructions

Day la project backend cua Pocket Ledger.

Truoc khi sua cac task lien quan den frontend hoac data contract:
- Luon doc tai lieu task trong `../docs`.
- Neu task lien quan man hinh thong ke giao dich, doc `../docs/TASK_TRANSACTION_SUMMARY.md`.
- Neu task lien quan tab thong ke/phan tich tieu dung hoac app shell, doc `../docs/TASK_ANALYTICS_APP_SHELL.md`.

Nguyen tac:
- Uu tien filter/tong hop du lieu o backend thay vi bat frontend tai toan bo du lieu.
- Giu response cu neu co the.
- Neu them endpoint moi, can ghi ro request params va response mau.
- Neu sua endpoint cu, can dam bao khong pha cac man hinh khac.

Analytics:
- Cac endpoint analytics nam duoi `/transactions/analytics`.
- Tat ca endpoint analytics can Bearer auth.
- User thuong chi tong hop du lieu cua chinh minh; admin giu behavior rong hon hien co.
- Filter analytics optional gom `transaction_type` va `category_key` khi endpoint co ho tro.
- `category_key` trong analytics la filter optional; neu bo trong thi lay tat ca danh muc.
