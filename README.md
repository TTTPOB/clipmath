# Clipmath

clipmath是一个Python程序，用于从剪贴板中获取数学公式的图像，并使用OCR技术将其转换为LaTeX格式的数学表达式。它依赖于OCR Math API进行图像识别和转换。(仅在windows上测试)

## 安装

1. 使用pipx从GitHub安装`clipmath`程序：

```shell
pipx install git+https://github.com/TTTPOB/clipmath
```

## 配置

在使用`clipmath`之前，需要进行一次性的配置。请按照以下步骤生成配置文件：

1. 运行以下命令生成配置文件：

```shell
clipmath gen_config
```

2. 根据提示输入应用程序的密钥（App Key）和密钥（App Secret）。这些信息将用于访问OCR Math API。您可以在[OCR Math API平台](https://open.ocrmath.com/console)中获取自己的API密钥。

## 使用方法

运行以下命令来执行数学公式图像的OCR转换：

```shell
clipmath ocr
```

将数学公式图像复制到剪贴板中，然后运行上述命令。程序将从剪贴板中获取图像，并使用OCR技术将其转换为LaTeX格式的数学表达式。转换后的数学表达式将自动复制到剪贴板中，您可以将其粘贴到其他应用程序中使用。

**免责声明：** 请注意，`clipmath`程序依赖于OCR Math API进行图像转换，因此需要有效的API密钥。请确保按照OCR Math API的使用条款和条件使用API密钥，并了解可能产生的任何相关费用。

// 我很懒，这个readme由ChatGPT生成
