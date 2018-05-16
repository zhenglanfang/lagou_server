var citys = [];

$(function () {

    // 初始化
    // $('.first').each(function () {
    //     if (!$(this).is(':checked')) {
    //         $(this).click()
    //     }
    // });

    //异步获取city数据
    $.get('/search/city/', function (data) {
        citys = JSON.parse(data);
        var simple_city = '';
        var more_city = '';
        for (var city in citys) {
            var string_obj = '<input type="checkbox" name="city" value="' + citys[city] + '" form="search_form"><label>' + citys[city] + '</label>'
            if (city > 8) {
                if (city % 8 == 0) {
                    more_city += '<br/>'
                }
                more_city += string_obj
            }
            else {
                simple_city += string_obj
            }
        }
        $('.city').html(simple_city);
        $('.more_city').html(more_city);
        // 加载完城市后，加载搜索条件
        reload_filter();
    });
    //显示更多城市
    $('.get_more_type').click(function () {
        if ($('.more_city').is(':hidden')) {
            $('.more_city').show()
        }
        else {
            $('.more_city').hide()
        }
    });
    //首个选项选择时，其他不选
    $('.search_filter span + input').click(function () {
        if ($(this).is(':checked')) {
            $(this).parent().find('input').prop('checked', false);
            $(this).prop('checked', true);
        }
        $('#search_form').submit();
    });

    //其他选项选中时，首选项不选
    $('.search_filter').on('click', 'input:not(.first)', function () {
        if ($(this).is(':checked')) {
            // console.log($(this).parents('li'));
            $(this).parents('li').children('.first').prop('checked', false)
        }
        $('#search_form').submit();
    });

    $("input[name='salary']").click(function () {
        if ($(this).is(':checked')) {
            $(this).siblings('input').prop('checked', false)
        }
        $('#search_form').submit();
    });

    $('.sort_bar a').click(function () {
        $('.sort_bar .active').removeClass('active');
        $(this).addClass('active');
    });

    // positions = positions.data;
    // str_position = '';
    // for (var index in positions) {
    //     if (index == 5) {
    //         break
    //     }
    //     position = positions[index]
    //     str_position += '<li class="position_li"><div class="position"><div class="p_top">'
    //     str_position += '<h3 style="max-width: 180px;">'
    //     str_position += position.position_name
    //     str_position += '</h3><span class="add">[<em>'
    //     str_position += position.city + '▪'
    //     str_position += '</em>]' + '</span></a><span class="format-time">'
    //     str_position += position.publish_date
    //     str_position += '发布</span></div><div class="p_bot">'
    //     str_position += '<div class="li_b_l"><span class="money">'
    //     str_position += position.salary
    //     str_position += '</span>'
    //     str_position += position.work_year + '/' + position.education
    //     str_position += '</div></div></div>'
    //     str_position += '<div class="company"><div class="company_name"><a href="" target="_blank">'
    //     str_position += position.company_name
    //     str_position += '</a><i class="company_mark"></i></div><div class="industry">'
    //     str_position += '</div></div></li>'
    // }
    // $('.positions_list ul').html(str_position)
});