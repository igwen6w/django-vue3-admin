from django.contrib.auth.models import AbstractUser
from django.db import models

from backend import settings
from utils.models import CoreModel
from utils.utils import validate_mobile


# 定义状态枚举（可根据实际业务扩展）
class DepartmentStatus(models.IntegerChoices):
    DISABLED = 0, "禁用"  # 对应数据中的 status: 0
    ENABLED = 1, "启用"   # 对应数据中的 status: 1

class Dept(CoreModel):
    pid = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="父部门 ID"
    )
    name = models.CharField(max_length=100, verbose_name="部门名称")
    status = models.SmallIntegerField(
        choices=DepartmentStatus.choices,
        default=DepartmentStatus.DISABLED,
        verbose_name="部门状态"
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        # 若数据中时间需自动解析，可在保存时处理：
        # default=timezone.now  # 或通过数据导入时赋值
    )
    sort = models.IntegerField(
        default=0,
        verbose_name="显示排序",
        help_text="数值越小越靠前"
    )
    leader = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name="负责人"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="联系电话"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="邮箱"
    )
    remark = models.TextField(blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按创建时间倒序排列

# 菜单类型枚举
class MenuType(models.TextChoices):
    CATALOG = 'catalog', '目录'
    MENU = 'menu', '菜单'
    BUTTON = 'button', '按钮'
    EMBEDDED = 'embedded', '内嵌页面'
    LINK = 'link', '外部链接'

# 菜单状态枚举
class MenuStatus(models.IntegerChoices):
    ENABLED = 1, '启用'
    DISABLED = 0, '禁用'

# 菜单元数据模型（单独存储元数据，避免 JSONField）
class MenuMeta(CoreModel):
    title = models.CharField(max_length=200, verbose_name='标题')
    icon = models.CharField(max_length=100, blank=True, verbose_name='图标')
    order = models.IntegerField(default=0, verbose_name='排序')
    affix_tab = models.BooleanField(default=False, verbose_name='固定标签页')
    badge = models.CharField(max_length=50, blank=True, verbose_name='徽章文本')
    badge_type = models.CharField(max_length=20, blank=True, verbose_name='徽章类型')
    badge_variants = models.CharField(max_length=20, blank=True, verbose_name='徽章样式')
    iframe_src = models.URLField(blank=True, verbose_name='内嵌页面URL')
    link = models.URLField(blank=True, verbose_name='外部链接')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'system_menu_meta'
        verbose_name = '菜单元数据'
        verbose_name_plural = '菜单元数据'

# 主菜单模型
class Menu(CoreModel):
    pid = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='父菜单'
    )
    name = models.CharField(max_length=100, verbose_name='菜单名称')
    status = models.IntegerField(choices=MenuStatus.choices, default=MenuStatus.ENABLED, verbose_name='状态')
    type = models.CharField(choices=MenuType.choices, max_length=20, verbose_name='菜单类型')
    path = models.CharField(max_length=200, blank=True, verbose_name='路由路径')
    component = models.CharField(max_length=200, blank=True, verbose_name='组件路径')
    auth_code = models.CharField(max_length=100, blank=True, verbose_name='权限编码')
    meta = models.OneToOneField(MenuMeta, on_delete=models.CASCADE, verbose_name='元数据')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单管理'
        ordering = ['meta__order', 'id']

# 角色状态枚举
class RoleStatus(models.IntegerChoices):
    ENABLED = 1, '启用'
    DISABLED = 0, '禁用'

class Role(CoreModel):
    name = models.CharField(
        max_length=100,
        verbose_name='角色名称'
    )
    status = models.IntegerField(
        choices=RoleStatus.choices,
        default=RoleStatus.ENABLED,
        verbose_name='角色状态'
    )
    sort = models.IntegerField(
        default=0,
        verbose_name="显示排序",
        help_text="数值越小越靠前"
    )
    remark = models.TextField(
        blank=True,
        verbose_name='备注'
    )
    # 与菜单权限的多对多关联（假设菜单模型为 Menu，权限字段为 auth_code）
    permissions = models.ManyToManyField(
        'Menu',  # 引用之前设计的 Menu 模型
        through='RolePermission',
        verbose_name='关联权限'
    )

    class Meta:
        verbose_name = '角色管理'
        verbose_name_plural = verbose_name
        ordering = ["-create_time"]  # 按创建时间倒序排列

    def __str__(self):
        return self.name

# 中间表：角色与权限的关联（可扩展字段如权限生效时间）
class RolePermission(CoreModel):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='角色'
    )
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        verbose_name='菜单/权限'
    )
    # 可选：记录权限关联时间
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='权限关联时间'
    )

    class Meta:
        db_table = 'system_role_permission'
        verbose_name = '角色权限关联'
        verbose_name_plural = verbose_name

class DictType(CoreModel):
    """字典类型表"""
    name = models.CharField(max_length=100, default='', verbose_name='字典名称')
    type = models.CharField(max_length=100, default='', verbose_name='字典类型', db_index=True)
    status = models.BooleanField(default=True)
    deleted_time = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')

    class Meta:
        verbose_name = '字典类型'
        verbose_name_plural = '字典类型'
        db_table = 'system_dict_type'
        ordering = ['-id']

    def __str__(self):
        return self.name


class DictData(CoreModel):
    """字典数据表"""
    sort = models.IntegerField(default=0, verbose_name='字典排序')
    label = models.CharField(max_length=100, default='', verbose_name='字典标签')
    value = models.CharField(max_length=100, default='', verbose_name='字典键值')
    dict_type = models.ForeignKey(
        DictType,
        on_delete=models.CASCADE,
        related_name='dict_data',
        verbose_name='字典类型'
    )
    status = models.BooleanField(default=True)
    color_type = models.CharField(max_length=100, blank=True, default='', verbose_name='颜色类型')
    css_class = models.CharField(max_length=100, blank=True, default='', verbose_name='css 样式')

    class Meta:
        verbose_name = '字典数据'
        verbose_name_plural = '字典数据'
        db_table = 'system_dict_data'
        ordering = ['sort', 'id']

    def __str__(self):
        return self.label


class User(AbstractUser, CoreModel):
    mobile = models.CharField(max_length=11, null=True, validators=[validate_mobile], db_comment="手机号")
    nickname = models.CharField(max_length=50, blank=True, null=True, db_comment="昵称")
    gender = models.SmallIntegerField(blank=True, null=True, default=0, db_comment='性别')
    language = models.CharField('语言', max_length=20, blank=True, null=True, db_comment="语言")
    city = models.CharField('城市', max_length=20, blank=True, null=True, db_comment="城市")
    province = models.CharField('省份', max_length=50, blank=True, null=True, db_comment="省份")
    country = models.CharField('国家', max_length=50, blank=True, null=True, db_comment="国家")
    avatarUrl = models.URLField('头像', blank=True, null=True, db_comment="头像")

    dept = models.ManyToManyField(
        'Dept', blank=True, verbose_name='部门', db_constraint=False,
        related_name='users'
    )
    status = models.BooleanField(default=False, verbose_name='<帐号状态>（1正常 0停用）', db_comment="帐号状态")
    login_date = models.DateTimeField("<最后登录时间>", blank=True, null=True, db_comment="最后登录时间")
    login_ip = models.GenericIPAddressField(blank=True, null=True, db_comment="最后登录IP")

    class Meta:
        verbose_name = '用户数据'
        verbose_name_plural = verbose_name
        db_table = 'system_users'
