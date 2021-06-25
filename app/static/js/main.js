var socket = io('http://127.0.0.1:5050');
var soc_flask = io('http://127.0.0.1:5000');
var max_page = 0;
var current_page = 0;
var category = "";
socket.on("connect", function () {
    console.log("Connected...!", socket.connected);
});

socket.on('user', function (user_id) {
    console.log(user_id);
    soc_flask.emit('user', user_id)
})

socket.on('response_back', function (image) {
    const image_id = document.getElementById('image');
    image_id.src = image;
});

soc_flask.on('user_info', function (user_info) {
    console.log(user_info)
    var parsed_user_info = JSON.parse(user_info)
    document.getElementById("id").innerHTML = parsed_user_info.current_user;
    document.getElementById("notice_group").innerHTML = parsed_user_info.category;
    category = parsed_user_info.category;
    document.getElementById("notices").innerHTML = parsed_user_info.notices.notice;
    const img_notice = document.getElementById('notice_img');
    max_page = parseInt(parsed_user_info.notices.pages);
    current_page = 0;
    img_notice.src = "/static/img/" + parsed_user_info.category.toLowerCase() + "/" + current_page + ".jpg";
})

document.addEventListener('keydown', function (e) {
    const img_notice = document.getElementById('notice_img');
    if (e.key == "ArrowLeft") {
        console.log("LEFT");
        if (current_page > 0) {
            current_page = current_page - 1;
        }
        img_notice.src = "/static/img/" + category.toLowerCase() + "/" + current_page + ".jpg";
    }
    if (e.key == "ArrowRight") {
        console.log("RIGHT")
        if (current_page < max_page - 1) {
            current_page = current_page + 1;
        }
        img_notice.src = "/static/img/" + category.toLowerCase() + "/" + current_page + ".jpg";
    }
})
