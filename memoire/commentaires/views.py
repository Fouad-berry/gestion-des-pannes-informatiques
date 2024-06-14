from django.shortcuts import render
from django.views.generic import DetailView
# Create your views here.
# class BlogDetail(DetailView):
#     template_name= 'commentaires/detail.html'
#     model= Blog

#     def get_context_data(self , **kwargs):
#         data = super().get_context_data(**kwargs)
#         connected_comments = Comment.objects.filter(CommentPost=self.get_object())
#         number_of_comments = connected_comments.count()
#         data['comments'] = connected_comments
#         data['no_of_comments'] = number_of_comments
#         data['comment_form'] = CommentForm()
#         return data

#     def post(self , request , *args , **kwargs):
#         if self.request.method == 'POST':
#             print('-------------------------------------------------------------------------------Reached here')
#             comment_form = CommentForm(self.request.POST)
#             if comment_form.is_valid():
#                 content = comment_form.cleaned_data['content']
#                 try:
#                     parent = comment_form.cleaned_data['parent']
#                 except:
#                     parent=None

            

#             new_comment = Comment(content=content , author = self.request.user , CommentPost=self.get_object() , parent=parent)
#             new_comment.save()
#             return redirect(self.request.path_info)