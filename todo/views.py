from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from django.http import Http404


from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
        #1.	Task: これは「タスク」という名前のリストやカードを保存する場所（箱のようなもの）。この箱には、みんなの宿題リストややることリストのように、いろんなタスクが入っている。
        #2.	objects: これは「箱の管理者」です。この人（プログラムの部分）は、箱の中にあるものを探したり、取り出したり、追加したりするお手伝いをしてくれる。
        #3.	all(): これは「全部見せて！」と言っている命令。管理者に「箱の中にあるすべてのもの（タスク）を見せてください」とお願いしているようなもの。
        tasks = Task.objects.filter(user=request.user)  # ここを修正
        templates = Template.objects.filter(user=request.user)

        form = TaskForm()
        template_form = TaskTemplateForm

        if 'task_submit' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)  # taskという変数は作成するがフォームのデータは一旦保存しない
                task.user = request.user  # 現在のログイン中のユーザーを設定
                #taskオブジェクト自体が生成されていないから先に記述してもエラーになる
                task.save()

        elif 'template_submit' in request.POST:  # テンプレート作成フォームのsubmitボタンの名前で識別
            template_form = TaskTemplateForm(request.POST)
            if template_form.is_valid():
                template = template_form.save(commit=False)
                template.user = request.user  # ログインしているユーザーを設定
                template.save()

        #contextは「コンテキスト」と言って、ウェブページに渡す「情報」をまとめたものです
        context = {'tasks' :tasks, 'templates' :templates} #{'tasks': tasks}は「辞書」という形で、「名前」と「その中身」をセットにしています。ここでは、tasksという名前の中に、「全部のタスク（やること）」のリストが入っている。
        return render(request, 'todo/list.html', context)






def toggle_task_completion(request, pk):
    task = get_object_or_404(Task, id=pk)  # タスクを取得
    task.is_completed = not task.is_completed  # 完了状態を切り替え
    task.save()  # 変更を保存
    return redirect('list')





@login_required
def category_tasks_view(request, category):
    # 指定されたカテゴリのタスクをフィルタリング
    tasks = Task.objects.filter(category=category, user=request.user)
    # 現在のユーザーのテンプレートを取得
    templates = Template.objects.filter(user=request.user)
    context = {'tasks': tasks, 'category': category, 'templates': templates}
    return render(request, 'todo/category_tasks.html', context)




@login_required
def create_task_from_template(request, template_id):
    template = get_object_or_404(Template, id=template_id, user=request.user)
    templates = Template.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('list')
    else:
        # テンプレートからフォームを初期化
        form = TaskForm(initial={
            'title': template.title,
            'subtitle1': template.subtitle1,
            'subtitle2': template.subtitle2,
            'subtitle3': template.subtitle3,
            'subtitle4': template.subtitle4,
            'subtitle5': template.subtitle5,
            'category': template.category,
            'priority': template.priority,
        })

    return render(request, 'todo/create_task_from_template.html', {'form': form, 'template': template, 'templates': templates, 'template_pk': template.pk})








@login_required
def updateTask(request, pk):
    templates = Template.objects.filter(user=request.user)

    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:  # タスクが見つからない場合
        raise Http404("タスクが見つかりません。")

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form=TaskForm(request.POST, instance=task)  #instance=task を使うことで、既存の入力内容を編集するためのフォームが上書き作成される
        if form.is_valid():
            form.save()

            # サブタスクの完了状態を確認し、親タスクの完了状態も確認
            task.check_if_completed()

            return redirect('list')


    else:
        form = TaskForm(instance=task)  # フォームに既存のタスクデータを表示

    context = {'form': form, 'task': task, 'templates': templates}

    return render(request, 'todo/update_task.html', context)







@login_required
def deleteTask(request, pk):

    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {'item': item}

    return render(request, 'todo/delete_task.html', context)





@method_decorator(login_required, name='dispatch')
class DeleteTemplateView(DeleteView):
    template_name = 'todo/delete_template.html'
    model = Template
    success_url = reverse_lazy('list')









def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        print("User logged out successfully.")  # デバッグメッセージ
    else:
        print("User is not logged in.")
    return redirect('list')




#form = TaskForm(request.POST, instance=task)
#TaskFormというフォームを使って、「送られてきた情報」を使って「どのタスクを更新するか」を指定しています。
#request.POSTは、ユーザーがフォームに入力して送ったデータです。
#instance=taskは、「どのタスクを更新するか」を指定するために使います。ここでは、すでにあるtaskというタスクを編集します。
#つまり、「このフォームには、ユーザーが入力した情報を使って、特定のタスクを更新するよ！」という意味です。


#if form.is_valid():

#これは、「ユーザーが入力した情報が正しいかどうか」をチェックします。
#is_valid()は、「このフォームに入力されたデータがちゃんとしているか」を調べてくれます。
#もし、すべての情報が正しく入力されていたら、次の処理に進みます。

#form.save()
#この部分は、「タスクを保存する」という処理です。
#つまり、「ユーザーが入力した情報を使って、既存のタスクを新しい情報で上書きするよ！」ということです。

#return redirect('list')
#redirectは、「どこか別のページに移動する」という意味です。
#ここでは、タスクを保存した後に「タスクリストのページ（listページ）に戻るよ！」ということです。
#listというのは、タスク一覧ページの名前です。

#else:
#もし、ユーザーがまだ何も送っていない場合（つまり、ページに初めてアクセスした場合）にどうするかを決めます。
#これは「もしPOSTじゃなかったら」という意味です。

#form = TaskForm(instance=task)
#ここでは、「タスクを編集するフォーム」を作っています。
#instance=taskは、既存のタスクの情報をフォームに入れて表示するために使います。
#これにより、ユーザーはタスクの現在の情報を見て、それを変更できるようになります。

