#最最最重要的readme

##[博客](http://www.cnblogs.com/lixiaoliuer/p/7156546.html)

##有感
一开始的全选 反选什么还是很好写的，逻辑性也没有那么强。
到后面的编辑框的内容 有点麻烦，判断进入编辑模式后，再判断是否打钩，打了勾就找到上级标签的同级标签循环创建input标签。  
在进入编辑模式的时候会给每个tr标签加上一个自定义的属性相当于flag，退出时用text替换掉input。

##功能介绍
后台管理平台 ，编辑表格：
1. 非编辑模式：
可对每行进行选择； 反选； 取消选择
2. 编辑模式:
进入编辑模式时如果行被选中，则被选中的行万变为可编辑状态，未选中的不改变
退出编辑模式时，所有的行进入非编辑状态
处于编辑模式时，行被选中则进入编辑状态，取消选择则进入非编辑状态


##测试环境
OS:Windows 7 旗舰版  
编译器：HBuilder