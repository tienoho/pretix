# Hướng Dẫn Sử Dụng và Vận Hành Hệ Thống Pretix Mở Rộng

Tài liệu này hướng dẫn chi tiết cách cấu hình và sử dụng các tính năng mới được tích hợp vào hệ thống Pretix, bao gồm cổng thanh toán OnePay, thông báo Zalo ZNS, và xuất hóa đơn điện tử MISA.

## 1. Triển Khai Hệ Thống (Deployment)

Hệ thống đã được cấu hình để chạy trên môi trường Docker.

### Yêu cầu
*   Docker và Docker Compose đã được cài đặt trên server.

### Cách chạy
Tại thư mục gốc của dự án, chạy lệnh:

```bash
docker-compose up -d
```

Lệnh này sẽ khởi động 4 dịch vụ:
1.  `pretix`: Web server chính (cổng 8000).
2.  `pretix-worker`: Xử lý các tác vụ ngầm (gửi tin Zalo, gửi hóa đơn MISA).
3.  `db`: Cơ sở dữ liệu PostgreSQL.
4.  `redis`: Bộ nhớ đệm và hàng đợi tin nhắn.

Truy cập website tại: `http://localhost:8000` (hoặc IP server của bạn).
Tài khoản admin mặc định (nếu chưa có): Chạy `docker-compose exec pretix python3 -m pretix createsuperuser` để tạo.

---

## 2. Cổng Thanh Toán OnePay

Cho phép khách hàng thanh toán vé qua cổng OnePay (ATM nội địa / Visa / Master).

### Cấu hình
1.  Đăng nhập trang quản trị sự kiện (`Control Panel`).
2.  Vào menu **Cài đặt (Settings)** -> **Thanh toán (Payments)**.
3.  Tìm **OnePay** và bật nó lên.
4.  Nhập các thông tin từ OnePay cung cấp:
    *   **Merchant ID**: Mã đơn vị chấp nhận thẻ.
    *   **Access Code**: Mã truy cập.
    *   **Hash Key**: Khóa bảo mật (Secure Hash).
    *   **Endpoint**: Chọn môi trường "Test Environment" để kiểm thử hoặc "Live" để chạy thật.
5.  Lưu lại.

### Lưu ý quan trọng
*   Hệ thống tự động phát hiện IP khách hàng để gửi sang OnePay (fix lỗi "Invalid Client IP").
*   Số tiền thanh toán sẽ được tự động chuyển đổi (VND không có số thập phân).

---

## 3. Tích Hợp Zalo ZNS (Zalo Notification Service)

Gửi tin nhắn thông báo vé, xác nhận đơn hàng qua Zalo OA.

### Cấu hình
1.  Vào menu **Cài đặt (Settings)** -> **Zalo ZNS Settings** (ở menu bên trái).
2.  Nhập thông tin:
    *   **Access Token**: Token truy cập OA (Lưu ý: Token này thường hết hạn sau 25h, cần cơ chế làm mới nếu dùng lâu dài).
    *   **Template ID**: ID mẫu tin ZNS đã đăng ký với Zalo.
    *   **Template Data Mapping**: Cấu hình ánh xạ dữ liệu JSON. Ví dụ:
        ```json
        {
          "customer_name": "name",
          "order_code": "code",
          "amount": "total"
        }
        ```
        *(Cột trái là biến trong Template Zalo, cột phải là trường dữ liệu của Pretix: `name`, `code`, `total`, `email`)*.

### Sử dụng
*   **Tự động:** Tin nhắn sẽ được gửi tự động khi đơn hàng chuyển sang trạng thái "Đã thanh toán" (Paid).
*   **Thủ công:**
    1.  Vào chi tiết một đơn hàng.
    2.  Ở tab **Zalo ZNS History**, bạn có thể xem trạng thái gửi.
    3.  Nhấn nút **Resend ZNS** để gửi lại tin nhắn thủ công nếu cần.

---

## 4. Tích Hợp Hóa Đơn Điện Tử MISA

Tự động xuất và gửi hóa đơn điện tử khi khách hàng thanh toán thành công.

### Cấu hình
1.  Vào menu **Cài đặt (Settings)** -> **MISA E-Invoice Settings**.
2.  Bật **Enable MISA Integration**.
3.  Nhập thông tin kết nối MISA:
    *   **API URL**: Đường dẫn API (ví dụ: `https://test-api.misa.vn`).
    *   **App ID**, **Tax Code** (Mã số thuế), **Username**, **Password**: Tài khoản kết nối MISA.
    *   **Series (Ký hiệu)**, **Template Code (Mẫu số)**: Thông tin mẫu hóa đơn.

### Vận hành
*   Khi đơn hàng được thanh toán (`Paid`), hệ thống sẽ tự động đăng nhập vào MISA (có cache token) và phát hành hóa đơn.
*   Thông tin xuất hóa đơn lấy từ mục "Invoice Address" mà khách hàng nhập khi mua vé.
*   Xem lịch sử xuất hóa đơn tại menu **MISA History** trong trang quản lý sự kiện.

---

## 5. Nâng Cấp Hệ Thống (Core Fixes)

*   **Xử lý Đụng độ (Race Condition):** Đã nâng cấp thuật toán khóa đơn hàng (Pessimistic Locking). Giờ đây, khi nhiều khách cùng tranh mua 1 vé cuối cùng, hệ thống đảm bảo không bao giờ bán quá số lượng (overselling).
*   **Giao diện Mobile:** Nút "Thêm vào giỏ" (Add to cart) đã được ghim (sticky) ở dưới cùng màn hình điện thoại, giúp khách hàng mua vé dễ dàng hơn mà không cần cuộn trang.
