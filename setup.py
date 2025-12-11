# -*- coding: utf-8 -*-

import distutils.cmd
import os
import subprocess
from io import open

from setuptools import setup, find_packages


class WebpackBuildCommand(distutils.cmd.Command):

    description = "Generate static assets"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not 'CI' in os.environ and not 'TOX_ENV_NAME' in os.environ:
            subprocess.run(['npm', 'install'], check=True)
            subprocess.run(['node_modules/.bin/webpack', '--config', 'webpack.prod.js'], check=True)


class WebpackDevelopCommand(distutils.cmd.Command):

    description = "Run Webpack dev server"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(
            ["node_modules/.bin/webpack-dev-server", "--open", "--config", "webpack.dev.js"],
            check=True
        )


class UpdateTranslationsCommand(distutils.cmd.Command):

    description = "Run all localization commands"

    user_options = []
    sub_commands = [
        ('extract_messages', None),
        ('update_catalog', None),
        ('transifex', None),
        ('compile_catalog', None),
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class TransifexCommand(distutils.cmd.Command):

    description = "Update translation files through Transifex"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.run(['tx', 'push', '--source'], check=True)
        subprocess.run(['tx', 'pull', '--mode', 'onlyreviewed', '-f', '-a'], check=True)


# -*- coding: utf-8 -*-
import distutils.cmd
import os
import subprocess
from io import open
from setuptools import setup, find_packages

# ... (保留你之前的 Webpack 等 Class 定义，这里省略) ...

setup(
    name='matrixhawk_sphinx_rtd_theme',
    version='0.0.2',
    
    # 1. 扫描包：自动找到当前目录下的 matrixhawk_sphinx_rtd_theme 文件夹
    packages=find_packages(),
    
    # 2. 包含资源：确保 theme.conf, .html, .css 被打包
    include_package_data=True,

    # 3. 依赖声明
    install_requires=[
        'sphinx',
        'docutils',
    ],

    # 【新增核心配置】注册入口点
    # 这就是告诉 Sphinx：“嘿，我是一个主题，名字叫 matrixhawk_sphinx_rtd_theme”
    # 格式为：'主题名 = 包名'
    entry_points={
        'sphinx.html_themes': [
            'matrixhawk_sphinx_rtd_theme = matrixhawk_sphinx_rtd_theme',
        ],
    },

    cmdclass={
        'update_translations': UpdateTranslationsCommand,
        'transifex': TransifexCommand,
        'build_assets': WebpackBuildCommand,
        'watch': WebpackDevelopCommand,
    },
)
