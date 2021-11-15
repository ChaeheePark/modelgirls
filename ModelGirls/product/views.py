import os

from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect

from user.models import Profile
from .cloth_segmentation import cloth_segmetation
from .models import Product
import os

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/index.html', {'products': products})

def virtual_try_on(request, pk):
    product = Product.objects.get(pk=pk)
    product_image = str(product.image)
    user_image = str(request.user.profile.image)
    product_image = product_image.replace("cloth/", "")
    user_image = user_image.replace("image/", "")
    write_filename(user_image, product_image)

    cloth_segmetation(product_image, 'VITON-HD/datasets/test/cloth/', 'VITON-HD/datasets/test/cloth-mask/')
    os.system('python VITON-HD/test.py  --name 결과')
    result = '/static/results/결과/{}_{}'.format(user_image.split('_')[0], product_image)
    return render(request, 'product/try_on.html', {'product': product, 'result': result})

def write_filename(filename1, filename2):
    # 폴더
    data_path = 'VITON-HD/datasets'
    # 파일
    file_path = os.path.join(data_path, "test_pairs.txt")
    pairs = filename1 + " " + filename2
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(pairs)
    f.close()

    return print(pairs)