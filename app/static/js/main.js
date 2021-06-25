var socket = io('http://127.0.0.1:5050')
var soc_flask = io('http://127.0.0.1:5000')

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
    document.getElementById("notices").innerHTML = parsed_user_info.notices;
    const img_notice = document.getElementById('notice_img');
    img_notice.src = "/static/img/" + parsed_user_info.notices[0] + ".jpg";
})
