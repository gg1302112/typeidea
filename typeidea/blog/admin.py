from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import Post, Category, Tag


class CategoryOwnerFilter(admin.SimpleListFilter):
    """  自定义过滤器只展示当前用户分类  """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        print(self.value())
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'create_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        print(obj)
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def post_count(self, obj):
        counter = obj.post_set.count()
        print(counter)
        return counter

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'create_time', 'owner', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_bottom = True
    actions_on_top = True

    # 编辑页面
    save_on_top = True
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        print(request.user.username)
        print(type(request.user.username))
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.username == "admin":
            return qs
        else:
            return qs.filter(owner=request.user)