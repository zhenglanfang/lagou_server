$(function () {
    // // 初始化日期
    // $('#api_form input[name="end_date"]').val(new Date().toLocaleDateString());

    // 判断当前页面是公司职位还是所以职位
    var company = $('#api_form input[name="company_name"]');

    //数据预览 异步请求
    $('#api_form input[name="query"]').on("click", function () {
        var url = '';
        if (company.length > 0) {
            var company_name = company.val();
            if (!company_name) {
                return false
            }
            url = '/api/company/' + company_name
        }
        else {
            url = '/api/job/';
            if (!check_date()) {
                return false
            }
        }
        $.ajax({
            type: 'get',
            data: $('#api_form').serialize(),
            url: url,
            cache: false,
            dataType: 'html',
            success: function (data) {
                $('.view_list').html(data)
            }
        })
    });

    //下载
    $('#api_form').submit(function () {
        if (company.length > 0) {
            var company_name = company.val();
            if (!company_name) {
                alert('请输入公司名称！');
                return false
            }
            return company.val();
        }
        else {
            return check_date()
        }
    });

    // 下载
    // $('#api_form input[name="download"]').on("click", function () {
    //     $('#openfile').click();
    //     console.log('12')
    // });

    search_hint()
});

// 判断开始时间是否小于结束时间
function check_date() {
    var start_date = $('#api_form input[name="start_date"]').val();
    var end_date = $('#api_form input[name="end_date"]').val();
    if (start_date && end_date) {
        var start_date_arr = start_date.split('-');
        var end_date_arr = end_date.split('-');
        start_date = new Date(start_date_arr[0], start_date_arr[1], start_date_arr[2]);
        end_date = new Date(end_date_arr[0], end_date_arr[1], end_date_arr[2]);
        if ((end_date.getTime() - start_date.getTime()) >= 0) {
            return true;
        }
        else {
            alert('结束时间必须大于开始时间');
            return false;
        }
    }
    alert('请选择开始时间和结束时间！');
    return false;
}


function search_hint() {
    var proposals;
    $.ajax({
        type: 'get',
        async: false,
        url: '/api/get_companies/',
        success: function (data) {
            proposals = data;
        }
    });
    $('.autocomplete-container').autocomplete({
        hints: proposals,
        width: 300,
        height: 30,
        onClick: function () {
            $('#api_form input[name="query"]').click()
        }
    });
}
