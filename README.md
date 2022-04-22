# EndNote-HistCite-Paper-Analysis

## 功能

使用Web of Science对感兴趣topic的检索结果，导入HistCite分析文献引用关系，基于EndNote对关键文章的标注，通过本脚本输出高清引用关系。

**功能：**

1. 分析高引文章的研究方向
1. 分析研究方向的发展
1. 相比HistCite的图更加高清，方便查看

**原理：**

* 基于HistCite提供的LCS数据，利用graphviz工具，将dot文件中的label值修改为文章缩写，绘制高引文章关系图，输出SVG高清格式。

**绘制效果：**

* HisCite输出效果：

  <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422165132991.png" alt="image-20220422165132991"  />

* 本脚本效果：

  <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422165224096.png" alt="image-20220422165224096" style="zoom:80%;" />
  
* 动画效果

  <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/2022-04-23%2007-20-44%2000_00_00-00_00_30.gif" alt="2022-04-23 07-20-44 00_00_00-00_00_30" style="zoom:150%;" />

## 步骤

### Step1. Web of Science检索文献

* 进入[WOS](https://www.webofscience.com/wos/woscc/basic-search)网站，输入检索关键词，如sonar imaging，选中感兴趣文章，选择导出

<img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422165447401.png" alt="image-20220422165447401" style="zoom:67%;" />

<img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422165619956.png" alt="image-20220422165619956" style="zoom: 67%;" />

* 导出时选择”**纯文本文件**“格式，记录内容选择”**全记录与引用的参考文献**“

  ![image-20220422165719037](https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422165719037.png)

### Step2. HistCite和EnNote分析文献

1. 将下载的文献txt用HistCitePro进行分析，[参考教程](https://twlig.github.io/2020/09/22/HistCite-Pro-2-1%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/)

2. Mark选中LCS最高的前N篇文章，并输出，导出为hci文件，重命名为txt文件

2. 使用Endnote导入该N篇文章，阅读，在research note中记录标注，如AUV导航

2. 使用Endnote导出该N篇，具体格式为 **标题\t年份\t作者\t标注\t摘要\t第二作者**

   这里具体的格式可以自己定义

   <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422170322955.png" alt="image-20220422170322955" style="zoom:67%;" />

   输出文件示例：**endnote.txt**

   ```
   A Comprehensive Bottom-Tracking Method for Sidescan Sonar Image Influenced by Complicated Measuring Environment	2017	J. H. Zhao, X. Wang, H. M. Zhang and A. X. Wang	SSS海底追踪	The estimations of water column depth and the towfish altitude and the measurements of the target's location and shape all depend on the accuracy and reliability of bottom tracking of a sidescan sonar (SSS) waterfall image. Traditionally, the threshold method has often been adopted,
   ```

   

### Step3. 获取文献信息

1. 使用HistCite重新导入该N篇文章，并在Graph Marker中，绘制该N篇文献关系。

   保存窗口中的文章信息到txt文件，注意不要复制起始三行。

   <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422163015691.png" alt="image-20220422163015691" style="zoom:50%;" />

   输出文件示例：**legend_full.txt**

   ```
   1. 1 Kirubarajan T, BarShalom Y
   Low observable target motion analysis using amplitude information
   IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS. 1996 OCT; 32 (4): 1367-1384
   LCR: 0   CR: 15   LCS: 13   GCS: 133   OCS:  
   
   2. 2 Rago C, Willett P, Bar-Shalom Y
   Detection-tracking performance with combined waveforms
   IEEE TRANSACTIONS ON AEROSPACE AND ELECTRONIC SYSTEMS. 1998 APR; 34 (2): 612-624
   LCR: 0   CR: 8   LCS: 0   GCS: 59   OCS:  
   ```

1. 在HistCite的Graph Marker中，保存窗口中的文章信息到txt文件，注意不要复制起始三行。

   <img src="https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422163358570.png" alt="image-20220422163358570" style="zoom:50%;" />

   输出文件示例：**legend_brief.txt**

   ```
   1.  1 Kirubarajan T, 1996, IEEE T AERO ELEC SYS, V32, P1367 13 133  
   2.  2 Rago C, 1998, IEEE T AERO ELEC SYS, V34, P612 0 59  
   ```



### Step4. 保存文献图信息

在HistCite的Graph Marker中，保存图节点信息，格式选择DOT。

![image-20220422163853310](https://cdn.jsdelivr.net/gh/ShaofengZou/doc_images//img/image-20220422163853310.png)

输出文件示例：**graph.dot**

```
digraph test {
	ratio="fill";
	node [fixedsize="true", fontsize="9", shape="circle"];
	edge [arrowhead="none", arrowsize="0.6", arrowtail="normal"];
	y1996 [fontsize="10", height="0.1668", label="1996", margin="0", rank="1996", shape="plaintext", width="0.398147893333333"];
	y1998 [fontsize="10", height="0.1668", label="1998", margin="0", rank="1998", shape="plaintext", width="0.398147893333333"];
	y2001 [fontsize="10", height="0.1668", label="2001", margin="0", rank="2001", shape="plaintext", width="0.398147893333333"];
```

### Step5. 生成高清引用关系图

> python demo.py