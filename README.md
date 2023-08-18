## README

这是通过自然语言生成3D会议室场景的自然语言处理以及坐标生成两大模块的集成代码。

演示视频: https://youtu.be/-KQIO2Bjcgo

项目PPT: https://docs.google.com/presentation/d/1duKLEwBsL5Ag4DLseSTtiLTeXsv35CDm0btZYLu-8oU/edit?usp=sharing

### 运行效果

<img src="https://courselearning.oss-cn-beijing.aliyuncs.com/analyzeEmotion/Picture1.png" style="zoom:50%;" />

![](https://courselearning.oss-cn-beijing.aliyuncs.com/analyzeEmotion/Screenshot%202023-08-17%20at%2021.27.36.png)

![](https://courselearning.oss-cn-beijing.aliyuncs.com/analyzeEmotion/Screenshot%202023-08-17%20at%2021.27.47.png)

### 坐标生成模块

位于`generate_position`文件夹下

### 自然语言模块

其余均是自然语言模块

### 运行项目说明

此项目运行起来具体步骤如下：

1. 下载OpenAI的whisper的small模型，并重命名为`small.pt`，放于`./models/small.pt`。（或者从此链接下载相应模型）

2. 根据此链接（https://drive.google.com/file/d/1xvPerX0FhjlGllYc-dkjT7xEzlIhvL85/view?usp=share_link）下载`export.pkl`模型，并放入`./category_predict/models/export.pkl`。

3. 安装CUDA、torch（测试版本为1.9.1+cu111）、torchaudio（测试版本为0.9.1）、torchvision（测试版本为0.10.1+cu111） （没有CUDA应该可以安装CPU版的，但是速度较慢）

4. https://manyili12345.github.io/Publication/2018/T2S/index.html

   下载网站中的NLP_Code，并按照代码中的README跑起来`JavaScene`项目（只需要跑代码中的这一个项目即可！！），如果成功运行，会出现`nlp server is running`。（注意，应该要把`StanfordCoreNLP`相应jar包导入idea才能运行。）

5. 整个代码包搜索`D:`，将所有绝对路径替换成当前运行机器的新的绝对路径。值得注意的是，此项目对应的目录前缀是`D:/four2/Graduating Design/nlp/`

6. 将代码包下的msedgedriver更改成符合运行机器的edge相应版本的edgedriver。（如果没有edge浏览器，可以下载相应的chromedriver，再将`translateUtil.py`的23行更改成相应文件路径即可）

7. 将`CoreNLP.py`文件第四、五行左右路径换成`2`中`JavaScene`的`StanfordCoreNLP`路径，并且在`StanfordCoreNLP`官网中下载相应的中文Jar包（可能要重命名，如果出错的话），放入`JavaScene`的`StanfordCoreNLP`文件夹中。

8. 将`SEL_params.txt`第一行绝对路径改成`2`中下载的`NLP_release`文件夹的绝对路径

9. 输入`pip install -r requirements.txt`，安装python所需包

10. 运行`2`中java项目、素材选择模块项目、当前的`main.py`，即可成功运行项目