import graphene
from graphene_django import DjangoObjectType
from main.models import Category, Post


class CategoryModelType(DjangoObjectType):
    class Meta:
        model = Category

# Работает как serializers
class PostModelType(DjangoObjectType):
    class Meta:
        model = Post

# Работает как viewset
class Query(graphene.ObjectType):
    category_model = graphene.List(CategoryModelType)
    post_model = graphene.List(PostModelType)

    def resolve_category_model(self, info):
        return Category.objects.all()

    def resolve_post_model(self, info):
        return Post.objects.all()


class CreateCategory(graphene.Mutation):#GET
    class Arguments:
        newname = graphene.String()
    category = graphene.Field(CategoryModelType)

    def mutate(self, info, newname):
        category = Category.objects.create(name=newname)
        category.save()
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):#PUT
    class Arguments:
        id = graphene.ID(required=True)
        newname = graphene.String()

    category = graphene.Field(CategoryModelType)

    def mutate(self, info, newid, newname):
        category = Category.objects.get(id=id)
        if newname:
            category.name = newname
        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation): #DELETE
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean() #False

    def mutate(self, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return DeleteCategory(success=True)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()

# Работает как routers
#schema = graphene.Schema(query=Query, mutation=Mutation)


class Query(graphene.ObjectType):
    category_model = graphene.List(CategoryModelType)
    post_model = graphene.List(PostModelType)

    def resolve_category_model(self, info):
        return Category.objects.all()

    def resolve_post_model(self, info):
        return Post.objects.all()


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.ID(required=True)

    post = graphene.Field(PostModelType)

    def mutate(self, info, title, content, category_id):
        category = Category.objects.get(id=category_id)
        post = Post.objects.create(title=title, content=content, category=category)
        post.save()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.ID()

    post = graphene.Field(PostModelType)

    def mutate(self, info, id, title=None, content=None, category_id=None):
        post = Post.objects.get(id=id)
        if title:
            post.title = title
        if content:
            post.content = content
        if category_id:
            category = Category.objects.get(id=category_id)
            post.category = category
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        post = Post.objects.get(id=id)
        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
