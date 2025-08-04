帮助我编写一个项目用于抓取一个图书网站的数据，并对其进行分析。

## 业务需求描述

抓取网站可以用到两个接口。第一个接口用于获取图书的列表信息：

- URL: https://api.ituring.com.cn/api/Search/Advanced
- HTTP Method: POST
- Payload: `{"categoryId":0,"sort":"new","page":2,"name":"","edition":1}`

返回的JSON结构如下大致如下：

```
{
    "bookItems": [
        {
            "authors": [],
            "translators": [],
            "authorNameString": "傅莘莘",
            "translatorNameString": "",
            "bookStatus": "上市销售",
            "id": 3365,
            "coverKey": "250172bebc60ce7c98e3",
            "name": "自制深度学习推理框架",
            "isbn": "978-7-115-66258-3",
            "abstract": "本书手把手带领读者实现深度学习推理框架，并支持大语言模型的推理。 全书共9章，以实现开源深度学习推理框架KuiperInfer为例，从基础的张量设计入手，逐步深入讲解计算图、核心算子等关键模块的设计与实现。此外，书中还介绍了如何支持深度学习模型，如ResNet、YOLOv5，以及大语言模型Llama 2的推理。书中代码基于C++，贴近业界实践。 \r\n\r\n本书面向深度学习初学者、希望进一步了解深度学习推理框架的开发者，以及其他对相关内容感兴趣的AI从业者。跟着本书，你不仅能够掌握深度学习推理框架的核心知识，还能在本项目基础上进行二次开发。",
            "bookEditionPrices": [
                {
                    "id": 3365,
                    "name": "79.80",
                    "key": "Paper"
                }
            ]
        }
    ],
    "pagination": {
        "pageCount": 140,
        "totalItemCount": 2100,
        "pageNumber": 2,
        "hasPreviousPage": true,
        "hasNextPage": true,
        "isFirstPage": false,
        "isLastPage": false
    }
}
```
第二个接口用于获取单本书的信息

- URL:https://api.ituring.com.cn/api/Book/3365
- HTTP Method: GET

返回的JSON结构字段非常多，我在意的重要字段如下：

```
{
    "voteCount": 1,
    "favCount": 21,
    "commentCount": 2,
    "viewCount": 1565,
    "authorNameString": "傅莘莘",
    "publishDate": "2025-03-12T00:00:00",
    "categories": [
        [
            {
                "id": 1,
                "name": "计算机",
                "key": null
            },
            {
                "id": 49,
                "name": "人工智能",
                "key": null
            }
        ]
    ]
    "bookCollectionName": "图灵原创",
    "briefIntro": {
        "highlight": "【简单学】8000 多行代码即可从零实现深度学习推理框架\r\n【透彻学】透明解析推理框架内部机制，不再是黑盒工具\r\n【轻松学】附赠 B 站免费配套视频，附赠本书配套源代码\r\n【一起学】 基于 GitHub 2.7k 星标开源项目 KuiperInfer\r\n【多模型】支持 ResNet、YOLOv5，支持 Llama 等大模型推理\r\n",
        "authorInfo": "傅莘莘\r\n\r\nAI 系统工程师，专注于深度学习推理框架与 AI 编译器的研发。曾主导多款深度学习推理框架从 0 到 1 的设计与实现，在推理效率与精度优化方面取得了实际成果。\r\n\r\n在 B 站开设了“自制推理框架”“自制大模型推理框架”等系列视频公开课（累计播放数超过 10 万），以通俗易懂的方式讲解技术，深受学生及其他技术爱好者的喜爱。\r\n\r\nB 站 ID: 我是傅傅猪，GitHub 账号：zjhellofss。",
        "specialNotes": "",
        "abstract": "本书手把手带领读者实现深度学习推理框架，并支持大语言模型的推理。 全书共9章，以实现开源深度学习推理框架KuiperInfer为例，从基础的张量设计入手，逐步深入讲解计算图、核心算子等关键模块的设计与实现。此外，书中还介绍了如何支持深度学习模型，如ResNet、YOLOv5，以及大语言模型Llama 2的推理。书中代码基于C++，贴近业界实践。 \r\n\r\n本书面向深度学习初学者、希望进一步了解深度学习推理框架的开发者，以及其他对相关内容感兴趣的AI从业者。跟着本书，你不仅能够掌握深度学习推理框架的核心知识，还能在本项目基础上进行二次开发。",
        "bookContact": ""
    },
    "tags": [
        {
            "id": 36,
            "name": "c++",
            "key": null
        },
    ],
    "pressName": "图灵教育",
    "id": 3365,
    "name": "自制深度学习推理框架",
    "isbn": "978-7-115-66258-3",
    "abstract": "本书手把手带领读者实现深度学习推理框架，并支持大语言模型的推理。 全书共9章，以实现开源深度学习推理框架KuiperInfer为例，从基础的张量设计入手，逐步深入讲解计算图、核心算子等关键模块的设计与实现。此外，书中还介绍了如何支持深度学习模型，如ResNet、YOLOv5，以及大语言模型Llama 2的推理。书中代码基于C++，贴近业界实践。 \r\n\r\n本书面向深度学习初学者、希望进一步了解深度学习推理框架的开发者，以及其他对相关内容感兴趣的AI从业者。跟着本书，你不仅能够掌握深度学习推理框架的核心知识，还能在本项目基础上进行二次开发。",
}
```

你需要将能够抓取到的所有数据全部保存到本地, 然后根据图书的信息赋予该图书一个技术标签，例如JavaScript，AI、大模型、数据库等等。一本书只能有一个标签，你可以调用大语言模型来完成对书技术标签的判断，例如OpenAI，我的OpenAI API Key为:xxxx

但你不一定要选择使用OpenAI，因为OpenAI需要额外花钱，优先保证准确性，其次保证金钱上的花费要少。

在给每个图书打上标签之后,统计每个标签每年出版图书的数量，并按照年将一个标签每年的出版数量绘制成图表


## 技术要求

- 整个项目必须使用Python语言编写
- 你可以安装所有你需要的Python类库，但必须安装在python-venv生成的虚拟开发环境中
- 考虑到这是一个数据抓取程序，为了保证访问不过于频繁而被网站的防火墙察觉，每个请求和上一个请求保持5秒的间隔
- 抓取到的所有数据必须以JSON格式按分类保存在本地以供离线分析

---

你可以看到在book_classifier文件中我们使用的是OpenAI对图书进行分类，请修改该文件，确保它也可以使用Gemini对图书进行分类。我的Gemini的API_KEY为xxxx。默认是用OpenAI但可以通过参数控制其使用Gemini。并且还要修改引用该classifier的文件 @config.py @data_analyzer.py 