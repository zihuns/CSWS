from django.shortcuts import render
from django.http import JsonResponse
from .models import Post
import os





def create_post(request):
    dir_path = os.getcwd() +'/webcompiler/'
    print(dir_path)
    # posts = Post.objects.all()
    response_data = {}

    if request.POST.get('action') == 'post':
        lang = request.POST.get('lang')
        code = request.POST.get('code')

        def run_code(file_name) : 
            text_file = open(dir_path+file_name, "wt")
            text_file.write(code) #Providing successful values ??in dictionary type
            text_file.close()
            extension = file_name.split('.')[-1]
            print(extension)
             
            if(extension =='c') :
                print(dir_path+file_name)
                os.system('gcc -o' + dir_path + 'output_c ' + dir_path+file_name + ' && ' + dir_path + 'output_c > ' + dir_path +'output_c.txt' ) # gcc -o ouputfilename, sourcefilename
                return(dir_path+'output_c.txt')

            elif(extension =='py') :
                os.system('python ' + dir_path +file_name+' > '+dir_path + '/output_py.txt') # > write or overwrite , >> append
                return(dir_path+'output_py.txt')
                

        outputfile = ''
        if(lang =="C"):
            file_name = "test.c"
            outputfile = run_code(file_name)
        elif(lang == "PYTHON") :
            file_name = "test.py"
            outputfile = run_code(file_name)

        print(dir_path + "output.txt")
        f = open(outputfile, "r")
        file_content = f.read()
        f.close()
        print(file_content)

        response_data['lang'] = lang
        response_data['code'] = code
        response_data['result'] = file_content

        return JsonResponse(response_data)

    # return render(request, 'create_post.html', {'posts':posts})    
    return render(request, 'webcompiler/create_post.html')   