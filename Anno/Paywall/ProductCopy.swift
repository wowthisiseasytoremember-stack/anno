import Foundation

struct ProductCopy {
    let language: LanguageMode

    var title: String {
        language == .vietnamese ? "Mở khóa kho lưu trữ Công giáo" : "Unlock the Catholic archive"
    }

    var subtitle: String {
        if language == .vietnamese {
            return "Các thánh, nghệ thuật thánh, nguồn và địa điểm hành hương cho từng ngày trong năm."
        }

        return "Saints, sacred art, sources, and pilgrimage places for every day of the year."
    }

    var benefits: [String] {
        if language == .vietnamese {
            return [
                "Tìm kiếm toàn bộ kho lưu trữ",
                "Mọi điểm hành hương trên bản đồ",
                "Phòng trưng bày nghệ thuật thánh",
                "Bài đọc hằng ngày bằng âm thanh",
                "Bộ sưu tập đã lưu",
                "Bảng nguồn mở rộng"
            ]
        }

        return [
            "Full archive search",
            "Every pilgrimage pin",
            "Sacred art gallery",
            "Audio daily entries",
            "Saved collections",
            "Expanded source sheets"
        ]
    }

    var primaryPlan: String {
        language == .vietnamese ? "Hằng năm - $49.99/năm" : "Annual - $49.99/year"
    }

    var secondaryPlan: String {
        language == .vietnamese ? "Hằng tháng - $5.99/tháng" : "Monthly - $5.99/month"
    }
}
