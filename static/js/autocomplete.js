/**
A jQuery plugin for search hints

Author: Lorenzo Cioni - https://github.com/lorecioni
*/

(function($) {
	$.fn.autocomplete = function(params) {

		//Selections
		var currentSelection = -1;
		var currentProposals = [];
		//Default parameters
		params = $.extend({
			hints: [],
			placeholder: 'Search',
			width: 200,
			height: 16,
			showButton: false,
			buttonText: 'Search',
			onClick: function(){},
			onBlur: function(){}
		}, params);
		//Build messagess
		this.each(function() {
			//Container
			var searchContainer = $('.autocomplete-container');

			//Text input
			var input = $('.autocomplete-input');

			//推荐词
			var proposals = $('<div></div>').addClass('proposal-box');

			var proposalList = $('<ul></ul>').addClass('proposal-list');

			proposals.append(proposalList);

			//键盘按下事件
			input.keydown(function(e) {
				switch(e.which) {
					case 38: // 上箭头
					e.preventDefault();
					$('ul.proposal-list li').removeClass('selected');
					if((currentSelection - 1) >= 0){
						currentSelection--;
						$( "ul.proposal-list li:eq(" + currentSelection + ")" ).addClass('selected');
					} else {
						currentSelection = -1;
					}
					break;
					case 40: // 下箭头
					e.preventDefault();
					if((currentSelection + 1) < currentProposals.length){
						$('ul.proposal-list li').removeClass('selected');
						currentSelection++;
						$( "ul.proposal-list li:eq(" + currentSelection + ")" ).addClass('selected');
					}
					break;
					case 13: // Enter
						if(currentSelection > -1){
							var text = $( "ul.proposal-list li:eq(" + currentSelection + ")" ).html();
							var text_classname=$( "ul.proposal-list li:eq(" + currentSelection + ")" ).attr('class')
							input.val(text);
						}
						if(text_classname == undefined){
							text_classname = ''
						}
						currentSelection = -1;
						proposalList.empty();
						// var data_dict={'id':text_classname.split(' ')[1],'text':input.val()};
						params.onClick();
						break;
					case 27: // Esc button
						currentSelection = -1;
						proposalList.empty();
						input.val('');
						break;
				}
			});
			//	绑定按键松开事件
			input.bind("keyup", function(e){
				if(e.which != 13 && e.which != 27 && e.which != 38 && e.which != 40){
					currentProposals = [];
					currentSelection = -1;
					proposalList.empty();
					// 填充提示词
					if(input.val() != ''){
						var word = input.val();
						proposalList.empty();
						for(var test in params.hints){
							if(params.hints[test].split(';')[0].indexOf(word)!=-1){
								currentProposals.push(params.hints[test]);
								var element = $('<li></li>')
									.html(params.hints[test])
									.addClass('proposal')
									.addClass(params.hints[test])
									.click(function(){
										input.val($(this).html());
										proposalList.empty();
										// input 提交时的参数
										// var data_dict={'id':$(this).attr('class').split(' '),'text':input.val()}
										params.onClick();
									})
									.mouseenter(function() {
										$(this).addClass('selected');
									})
									.mouseleave(function() {
										$(this).removeClass('selected');
									});
								proposalList.append(element);
							}
						}
					}
				}
			});
			//失去焦点
			input.blur(function(e){
				currentSelection = -1;
				//proposalList.empty();
				params.onBlur();
			});

			//searchContainer.append(input);
			searchContainer.append(proposals);
			//$(this).append(searchContainer);
		});

		return this;
	};

})(jQuery);