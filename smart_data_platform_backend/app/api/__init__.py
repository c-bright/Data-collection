"""
API接口模块，提供系统对外服务接口
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Union

from flask import Blueprint, Flask

import app.api as default_api_package

# 创建各个API蓝图
# 注意：BlueprintAutoRegistrar 会自动发现并注册蓝图，无需显式导入

class BlueprintAutoRegistrar:
    """
    自动发现并注册 `app.api` 包下所有 Blueprint 实例。

    用法示例（在 `main.py` 中）::

        from flask import Flask
        from app.api import BlueprintAutoRegistrar

        app = Flask(__name__)
        BlueprintAutoRegistrar().register(app)
    """

    def __init__(self, package: Union[str, object] = default_api_package) -> None:
        """
        :param package: 可以是包对象（默认 app.api）或包名字符串，如 "app.api"
        """
        if isinstance(package, str):
            self.package = importlib.import_module(package)
        else:
            self.package = package

    def register(self, app: Flask) -> None:
        """
        遍历包下所有模块，查找其中的 Blueprint 实例并注册到 Flask 应用。
        """
        package = self.package
        package_name = package.__name__

        # 遍历包下所有子模块（不递归子包，如果需要递归，可去掉 is_pkg 判断）
        for _, module_name, is_pkg in pkgutil.iter_modules(
            package.__path__, package_name + "."
        ):
            if is_pkg:
                #递归，子包
                continue

            module = importlib.import_module(module_name)

            # 在模块中查找所有 Blueprint 实例并注册
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)


"""

方案B：优化「商品详情页」
增强 ProductDetail.vue 功能
添加"一键分析"按钮，调用 /analysis/run 接口
实现分析进度条和差评预览
打通前后端流程闭环
方案C：重构「可视化分析页」
整合 Analysis1.vue 和 Analysis2.vue 逻辑
实现图表联动交互（点击散点→显示对应标签）
优化ECharts配色和加载体验
提升数据分析深度
方案D：技术架构升级
引入 Pinia 状态管理
统一封装API调用层
添加全局loading和toast通知
优化代码质量和可维护性"""


__all__ = ['BlueprintAutoRegistrar',  ]