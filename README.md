# candy_crawler
基于python开发的图片爬虫，它具备以下特点：

* 通过Chrome headless模拟真实网页的加载和操作，可以使爬虫程序像真实用户一样浏览页面，从而可以做更多的事情
* 利用python的并发特性，高效地搜索和下载图片资源

参考资料：

* [Python 爬虫杂记 - Chrome Headless](https://www.jianshu.com/p/779b8b23e08f)
* [selenim官网](https://selenium-python.readthedocs.io/) 
* [Beautiful Soup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)

## 开发思录

### 为什么从花瓣网开始？

* 容易确定边界，根据画板划定区域；
* 参考价值高，众多用户采集更新；
* 体量大，难以手动保存大量素材；
* 良好归类，避免了从海量图片中筛选；

### 一个简单的爬虫包括哪些部分？

* 搜索资源：获得高清图片下载地址
* 采集资源：用多线程并行下载

### 简析花瓣网画板

以这个“棋牌品类”画板为例，分析出实现爬虫的思路：

画板示例：http://huaban.com/boards/24199444/

图片url示例：http://hbimg.b0.upaiyun.com/1d86ca6b1fdaca2775227b4c8400405720398938d6880-4cOLVt

#### 难点解析：

* 图片url是不连续的，不能通过某个自增量去延伸出**画板**中的其他图片，需要通过画板>图片预览>原图展示，这两个步骤，才能获取到想要的大图素材；
* 画板中的图片不是一次性全部展示出来的，需要不断去加载下一页，直到全部加载出来为止；
* 下载图片时，发现url中没法确认图片的类型，需要从返回头里面获取MIME类型；


我们的爬虫搜索资源执行的步骤是：

* 第一步：打开画板链接，如http://huaban.com/boards/24199444/；
* 第二步：搜索html中的元素`.pin a.layer-view`，采集其中的`href`属性；
* 第三步：加载下一页时，首先从页面中获取`.pin[data-seq]:last-child`元素，获得其中的`data-seq`属性，然后构造分页请求的url：http://huaban.com/boards/24199444/?jpibwab0&max=1582731010&limit=20&wfl=1 ，其中`max`参数就是`data-seq`的值；
* 第四步：重复第二步到第三步，直到没有记录返回为止；
* 第五步：循环采集到的url，请求素材预览的页面，从页面中查询`.zoom-layer img`元素，元素中的`src`属性就是原图的路径，将其采集到新的列表中；
* 第六步：循环这个列表下载图片；

### 源码分析

* 单进程的实现

* 多进程实现并发搜索和下载

* 打包发布

### 运行效果

