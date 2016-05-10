var setting = {	};
var zNodes =[
	{ name:"父节点1 - 展开", 
		children: [
			{ name:"父节点11 - 折叠",
				children: [
					{ name:"叶子节点111"},
					{ name:"叶子节点112"},
					{ name:"叶子节点113"},
					{ name:"叶子节点114"}
				]},
		]},
];
$(document).ready(function(){
	$.fn.zTree.init($("#treeDemo"), setting, zNodes);
});
