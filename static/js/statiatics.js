var first_type = ['Java', 'PHP', 'Python', 'Go', 'C#', 'C++', 'Node.js', 'MySQL', 'Ruby', 'Android', 'web前端', '测试工程师',
    '机器学习', '区块链', '数据挖掘'];


$(function () {
    var chart = echarts.init(document.getElementById('container'));

    $('.left_menu li a').click(function () {
        $('.left_menu .active').removeClass('active');
        $(this).addClass('active');
    });

    $('#positions_rank').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/positions_rank/',
            success: function (data) {
                console.log('positions_rank');
                console.log(data);
                chart.hideLoading();
                position_rank(chart, data, '年需求量排名')
            }
        });
    });

    $('#position_type_distribute').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/position_type_distribute/',
            success: function (data) {
                console.log('position_type_distribute');
                console.log(data);
                chart.hideLoading();
                position_rank(chart, data, '年不同类别职位需求量');
            }
        });
    });

    $('#city_distribute').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/city_distribute/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                city_position(chart, data, '年城市职位需求')
            }
        });
    });

    $('#position_city_distribute').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/position_city_distribute/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_salary(chart, data, '职位城市需求', true);
            }
        });
    });

    $('#education_distribute').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/education_distribute/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_salary(chart, data, '年不同学历需求量', true)
            }
        });
    });

    $('#second_type_salary').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/second_type_salary/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_rank(chart, data, '年职位平均薪资', true)
            }
        });
    });

    $('#first_type_salary').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/first_type_salary/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_rank(chart, filter_first_type(data), '年热门职位平均薪资', true)
            }
        });
    });

    $('#city_salary').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/city_salary/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_salary(chart, data, '年城市平均薪资')
            }
        });
    });

    $('#education_salary').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/education_salary/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_salary(chart, data, '年不同学历要求的平均薪资');
            }
        });
    });

    $('#work_year_salary').click(function () {
        chart.showLoading();
        $.ajax({
            type: 'get',
            url: '/statistics/work_year_salary/',
            success: function (data) {
                console.log(data);
                chart.hideLoading();
                position_salary(chart, data, '年不同工作经验要求的平均薪资');
            }
        });
    });

    $('#positions_rank').click()
});

function position_rank(chart, data, text, flag=false) {
    var series = [];
    var selected = {};
    var title_text = text;
    for (var x in data) {
        series.push({
            name: x,
            type: 'bar',
            data: data[x]['value']
        });
        selected[x] = false;
    }
    selected[x] = true;
    var option = {
        title: {
            text: x + title_text,
            left: '6%',
            textStyle: {
                fontSize: 15
            }
        },
        tooltip: {
            formatter: function (bar_data) {
                // console.log(bar_data);
                var res = bar_data.seriesName + '<br/>';
                res += bar_data.name + ': ';
                if (flag) {
                    res += bar_data.value.toFixed(2) + 'k'
                }
                else {
                    var index = bar_data.dataIndex;
                    res += bar_data.value + ' (' + data[bar_data.seriesName]['score'][index].toFixed(2) + '%)';
                }
                return res
            }
        },
        legend: {
            selected: selected
        },
        xAxis: {
            axisLabel: {
                interval: 0
                // rotate: 40
            },
            data: data[x]['type']
        },
        yAxis: {},
        series: series
    };
    chart.setOption(option, true);
    chart.off('legendselectchanged');
    // 自定义点击图例事件
    chart.on('legendselectchanged', function (params) {
        // console.log(params);
        var change_text;
        if (params['selected'][params['name']]) {
            change_text = params['name'] + title_text;
            set_select_false(params['selected'], params['name'])
        }
        chart.setOption({
            title: {
                text: change_text
            },
            legend: {
                selected: params['selected']
            },
            xAxis: {
                data: data[params['name']]['type']
            }
        });
    });
}

function position_salary(chart, data, text, flag=false) {
    var series = [];
    var selected = {};
    var xAxis_dict = {};
    var title_text = text;
    for (var x in data) {
        series.push({
            name: x,
            type: 'bar',
            data: data[x]
        });
        selected[x] = false;
        xAxis_dict[x] = get_type(data[x])
    }
    selected[x] = true;
    var option = {
        title: {
            text: x + title_text,
            left: '6%',
            textStyle: {
                fontSize: 15
            }
        },
        tooltip: {
            enterable: true, // 设置鼠标停留时，可以显示提示内容
            confine: true,
            formatter: function (params) {
                // console.log(params);
                var tip_data = params['data'];
                var text_title = '平均薪资';
                var title_value = tip_data["value"].toFixed(2) + 'k';
                if (flag) {
                    text_title = '需求量';
                    title_value = tip_data.value + ' (' + tip_data['score'].toFixed(2) + '%)'
                }
                var tipHtml = '';
                tipHtml = '<div style="height:360px;width:400px;color:black;cborder-radius:5px;background:#fff;box-shadow:0 0 10px 5px #aaa">' +
                    '    <div style="height:30px;width:100%;border-radius:5px;background:#F8F9F9;border-bottom:1px solid #F0F0F0">' +
                    '        <span style="line-height:30px;margin-left:18px">' + params.name + '</span>' +
                    '    </div>' +
                    '    <div style="height:50px;width:100%;background:#fff">' +
                    '        <div style="padding-left:18px;padding-top:22px">' +
                    '            <span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#49AA36"></span> ' +
                    '            <span>' + text_title + '</span>' +
                    '            <span style="float:right;margin-right:18px">' + title_value + '</span>' +
                    '        </div>' +
                    '    </div>' +
                    '    <div id="tooltipBarId" style="height:260px;width:100%;border-radius:0 0 5px 0;background:#fff"></div>' +
                    '</div>';
                setTimeout(function () {
                    if (flag) {
                        tooltip_charts_pie(tip_data)
                    }
                    else {
                        tooltip_charts_bar(tip_data.type_positions);
                    }
                }, 10);
                return tipHtml;
            }
        },
        legend: {
            selected: selected
        },
        xAxis: {
            axisLabel: {
                interval: 0
                // rotate: 40
            },
            type: 'category',
            data: xAxis_dict[x]
        },
        yAxis: {},
        series: series
    };
    chart.setOption(option, true);
    chart.off('legendselectchanged');
    // 自定义点击图例事件
    chart.on('legendselectchanged', function (params) {
        // console.log(params);
        var change_text;
        if (params['selected'][params['name']]) {
            change_text = params['name'] + title_text;
            set_select_false(params['selected'], params['name'])
        }
        chart.setOption({
            title: {
                text: change_text
            },
            legend: {
                selected: params['selected']
            },
            xAxis: {
                data: xAxis_dict[params['name']]
            }
        });
    });
}

function city_position(chart, data, text) {
    var legend_data = [];
    var selected = {};
    var title_text = text;
    var series = [];
    for (var x in data) {
        series.push(
            {
                name: x,
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: data[x].splice(0, 20)
            }
        );
        selected[x] = false;
        legend_data.push(x);
    }
    selected[x] = true;
    var option = {
        title: {
            text: x + title_text,
            left: '6%',
            textStyle: {
                fontSize: 15
            }
        },
        tooltip: {
            enterable: true, // 鼠标是否可进入提示框浮层
            confine: true, // 是否将 tooltip 框限制在图表的区域内
            formatter: function (params) {
                console.log(params);
                var tip_data = params['data'];
                flag = 'false';
                if (flag) {
                    text_title = '需求量';
                    title_value = tip_data.value + ' (' + tip_data['score'].toFixed(2) + '%)'
                }
                var tipHtml = '';
                tipHtml = '<div style="height:360px;width:400px;color:black;cborder-radius:5px;background:#fff;box-shadow:0 0 10px 5px #aaa">' +
                    '    <div style="height:30px;width:100%;border-radius:5px;background:#F8F9F9;border-bottom:1px solid #F0F0F0">' +
                    '        <span style="line-height:30px;margin-left:18px">' + params.name + '</span>' +
                    '    </div>' +
                    '    <div style="height:50px;width:100%;background:#fff">' +
                    '        <div style="padding-left:18px;padding-top:22px">' +
                    '            <span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#49AA36"></span> ' +
                    '            <span>' + text_title + '</span>' +
                    '            <span style="float:right;margin-right:18px">' + title_value + '</span>' +
                    '        </div>' +
                    '    </div>' +
                    '    <div id="tooltipBarId" style="height:260px;width:100%;border-radius:0 0 5px 0;background:#fff"></div>' +
                    '</div>';
                setTimeout(function () {
                    if (flag) {
                        tooltip_charts_pie(tip_data)
                    }
                    else {
                        tooltip_charts_bar(tip_data.type_positions);
                    }
                }, 10);
                return tipHtml;
            }
        },
        legend: {
            data: legend_data,
            selected: selected
        },
        series: series
    };
    chart.setOption(option, true);
    // 解绑事件处理函数
    chart.off('legendselectchanged');
    // 自定义点击图例事件
    chart.on('legendselectchanged', function (params) {
        console.log(params);
        var change_text;
        if (params['selected'][params['name']]) {
            change_text = params['name'] + title_text;
            set_select_false(params['selected'], params['name'])
        }
        chart.setOption({
            title: {
                text: change_text
            },
            legend: {
                selected: params['selected']
            }
        });
    });
}

// 设置selected 只有一个被选中
function set_select_false(selected_dict, select) {
    for (var i in selected_dict) {
        if (i != select) {
            selected_dict[i] = false;
        }
    }
    return selected_dict
}

// 提取xAxis的数据
function get_type(data) {
    var items = [];
    for (var i = 0; i < data.length; i++) {
        items.push(data[i]['name'])
    }
    return items
}

function tooltip_charts_bar(data) {
    console.log(data);
    var myChart = echarts.init(document.getElementById('tooltipBarId'));
    var option = {
        tooltip: {},
        xAxis: {
            type: 'category',
            interval: true,
            axisLabel: {rotate: 45},
            axisTick: {show: false},
            data: data['first_type']
        },
        yAxis: {}, color: ['#49AA36'],
        grid: {show: true, backgroundColor: '#FAFAFA', left: 30, right: 20, top: 20},
        series: [
            {type: 'bar', smooth: true, seriesLayoutBy: 'row', barWidth: 10, data: data['values']}
        ]
    };
    myChart.setOption(option);
}

function tooltip_charts_pie(data) {
    // console.log('pie');
    // console.log(data);
    var myChart = echarts.init(document.getElementById('tooltipBarId'));
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{c} &nbsp;({d}%)"
        },
        dataset: {
            source: {
                'product': data['type_positions']['type'],
                'count': data['type_positions']['count']
            }
        },
        series: [
            {
                name: data['name'],
                type: 'pie',
                radius: '55%',
                center: ['50%', '55%']
            }
        ]
    };
    myChart.setOption(option);
}

function filter_first_type(data) {
    var new_data = {};
    for (var year in data) {
        new_data[year] = {};
        new_data[year]['type'] = [];
        new_data[year]['value'] = [];
        for (var i = 0; i < data[year]['type'].length; i++) {
            if (jQuery.inArray(data[year]['type'][i], first_type) > -1) {
                new_data[year]['type'].push(data[year]['type'][i]);
                new_data[year]['value'].push(data[year]['value'][i]);
            }
        }
    }
    return new_data
}

