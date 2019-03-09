# 将官方 python3 运行作为父镜像
FROM python:3.7

# 设置工作目录
WORKDIR /Users/wuljchange/dockerApp/easyBlog

# 复制项目到工作目录中的容器
ADD . /Users/wuljchange/dockerApp/easyBlog

# 安装项目依赖软件包
RUN pip3 install -r requirements.txt

# 暴露端口 80 供容器外使用
EXPOSE 80

# 运行项目
CMD python3 manage.py runserver 0.0.0.0:80
