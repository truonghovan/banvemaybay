
function pay() {
    if (confirm("Ban chac chan thanh toan khong?") == true)
        fetch("/api/pay", {
            method: 'post'
        }).then(function(res) {
            return res.json()
        }).then(function(data) {
            if (data.error_code == 200){
                location.reload()
                confirm("Thanh toan thanh cong")==true
                window.location.href = "/payed";
                }
            else
                alert("THANH TOAN DANG CO LOI!!! VUI LONG THUC HIEN SAU!")
        })
}

function addToCart(Thoigianbay) {
    fetch("/api/chuyenbay", {
        method: 'post',
        body: JSON.stringify({
            "Thoigianbatdau": Thoigianbay
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function(res) {
        console.info(res)
        return res.json()
    }).then(function(data) {
        console.info(data)

    })
}
